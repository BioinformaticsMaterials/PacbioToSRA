#!/usr/bin/env python
""" This script will upload the data sets specified in your input.fofn to NCBI.

Usage:
    send_to_ncbi.py --help
    send_to_ncbi.py --bioproject_accession=BIOPROJECT_ACCESSION --biosample_accession=BIOSAMPLE_ACCESSION --input_fofn=INPUT_FOFN_FILE --ncbi_username=NCBI_USERNAME --ncbi_ssh_key_file=SSH_KEY_FILE [--excel_output_file=EXCEL_OUTPUT_FILE]

Example:
    send_to_ncbi.py --bioproject_accession=project1 --biosample_accession=sample1 --input_fofn=/path/to/input.fofn --ncbi_username=myusername --ncbi_ssh_key_file=/path/to/ssh/file
    send_to_ncbi.py --bioproject_accession=project1 --biosample_accession=sample1 --input_fofn=/path/to/input.fofn --ncbi_username=myusername --ncbi_ssh_key_file=/path/to/ssh/file --excel_output_file=my_sra_submission.xlsx

Options:
    -h --help                                       Show this screen.
    --version                                       Show version.
    --bioproject_accession=BIOPROJECT_ACCESSION     NCBI bioproject ID created on the NCBI website.
    --biosample_accession=BIOSAMPLE_ACCESSION       NCBI biosample ID created on the NCBI website.
    --input_fofn=INPUT_FOFN_FILE                    The input.fofn file.
    --ncbi_username=NCBI_USERNAME                   Username to use to upload data sets to NCBI.
    --ncbi_ssh_key_file=SSH_KEY_FILE                SSH key  to use to upload data sets to NCBI.
    --excel_output_file=EXCEL_OUTPUT_FILE           Name of the output file. Format of output is .xslx.
                                                    Default will SRA_submission_<date>.xlsx
"""
import sys
from os.path import realpath, dirname
APP_ROOT_FULLPATH = dirname(dirname(realpath(__file__)))
sys.path.insert(1, APP_ROOT_FULLPATH)

import concurrent
import errno
import logging
import os

from datetime import datetime
from docopt import docopt
from PacbioToSRA.cell_analysis_result import CellAnalysisResult
from PacbioToSRA.ncbi.excel_sheet_from_template import ExcelSheetFromTemplate
from PacbioToSRA.ncbi.sra_submission import SraSubmission


# TODO: This should eventually go into a config file
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger(__name__)


def __parse_args(args):
    """This parses all the command line arguments. Also checks the input parameters

    :param  args:   Input arguments
    :type   args:   list
    :return:        Parsed input arguments
    :rtype          tuple
    """
    input_fofn_file = args['--input_fofn']
    bioproject_accession = args['--bioproject_accession']
    biosample_accession = args['--biosample_accession']
    username = args['--ncbi_username']
    ssh_key = args['--ncbi_ssh_key_file']

    excel_output_filename = args['--excel_output_file'] \
        if args['--excel_output_file'] is not None \
        else generate_excel_file_name()

    # check if input file exists
    if not os.path.exists(input_fofn_file):
        print ("[ERROR] File does not exist: {}".format(input_fofn_file))
        sys.exit(errno.ENOENT)      # file/dir does not exist status code

    # check if output file already exists
    if os.path.exists(excel_output_filename):
        print ("[ERROR] File already exist: {}".format(excel_output_filename))
        sys.exit(errno.ENOENT)      # file/dir does not exist status code

    # check if ssh key exists
    if not os.path.exists(ssh_key):
        print ("[ERROR] File does not exist: {}".format(ssh_key))
        sys.exit(errno.ENOENT)      # file/dir does not exist status code

    return bioproject_accession, biosample_accession, input_fofn_file, username, ssh_key, excel_output_filename


def extract_cell_analysis_result_dirs_from_input_fofn_file(input_fofn_file):
    """Extracts all the root directories from the input.fofn file.

    :param  input_fofn_file:    The file that contains the cell analysis result files.
    :type   input_fofn_file:    string
    :return:                    Root directories of the cell analysis results.
    :rtype                      list
    """
    logger.info("Extracting root directory from: {} ....".format(input_fofn_file))
    dirs = set()
    with open(input_fofn_file, 'r') as fp:
        for f in fp:
            # ex: /mnt/data3/vol60/2420308/0001/Analysis_Results/m150325_061829_42142_c100811842550000001823178610081510_s1_p0.1.subreads.fasta
            # want everything before "Analysis_Results"
            d = dirname(dirname(f.strip()))

            if d == '':
                continue

            if not os.path.exists(d):
                print ("[ERROR] Reading input.fofn file... Directory does not exist: {}".format(d))
                sys.exit(errno.ENOENT)      # file/dir does not exist status code

            dirs.add(d)

    if not dirs:
        print ('[ERROR] No directories found in input.fofn file.')
        sys.exit(errno.ENODATA)

    return dirs


def get_cell_analysis_result_data(dirs):
    """Get cell analys result information from all the directories

    :param  dirs:   Directories
    :type   dirs:   list
    :return:        Objects that hold information for all the cell result directories
    :rtype          list
    """
    results = []
    for d in dirs:
        logger.info("Retrieving cell analysis result data from: {}".format(d))
        results.append(CellAnalysisResult(d))

    return results


def generate_rows_for_files_worksheet(cell_analysis_results):
    """Generates all the rows for the worksheet that contains information on all the files.

    :param  cell_analysis_results:  List of all cell analysis result info
    :type   cell_analysis_results:  list
    :return:                        List of rows to insert into an excel worksheet
    :rtype                          list
    """
    logger.info('Creating Excel data for all file information...')

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = dict((executor.submit(analysis.get_info_for_files), analysis) for analysis in cell_analysis_results)

    rows = []
    for future in concurrent.futures.as_completed(futures):
        analysis = futures[future]

        sample_name = analysis.get_value_from_xml_path('Sample/Name')
        sample_plateid = analysis.get_value_from_xml_path('Sample/PlateId')

        for f, info in future.result().iteritems():
            rows.append([sample_name, sample_plateid, info['filename'], info['md5sum']])

    return rows


def generate_rows_for_sr_data_worksheet(cell_analysis_results):
    """Generates all the rows for the worksheet that contains sr data.

    :param  cell_analysis_results:  All cell analysis result info
    :type   cell_analysis_results:  list
    :return:                        Rows to insert into an excel worksheet
    :rtype                          list
    """
    logger.info('Creating Excel data for cell analysis...')
    rows = []
    unique_sample_names = set()
    for r in cell_analysis_results:
        sample_name = r.get_value_from_xml_path('Sample/Name')
        design_desc = r.get_value_from_xml_path('Primary/ConfigFileName').rstrip('.xml')
        if sample_name not in unique_sample_names:
            rows.append([
                bioproject_accession,           # bioproject_accession
                biosample_accession,            # biosample_accession
                sample_name,                    # sample_name
                sample_name,                    # library_ID
                None,                           # title/short description
                None,                           # library_strategy (click for details)
                None,                           # library_source (click for details)
                None,                           # library_selection (click for details)
                None,                           # library_layout
                r.get_platform(),               # platform (click for details)
                r.get_instrument_model(),       # instrument_model
                design_desc,                    # design_description
                None,                           # reference_genome_assembly (or accession)
                None,                           # alignment_software
                None,                           # forward_read_length
                None,                           # reverse_read_length
                r.get_file_type(),              # filetype
                None,                           # filename
                None,                           # MD5_checksum
                None,                           # filetype
                None,                           # filename
                None,                           # MD5_checksum
            ])

        unique_sample_names.add(sample_name)

    return rows


def creat_excel_workbook(output_filename, files_ws_rows, sr_data_ws_rows):
    """Creates the Excel workbook

    :param  output_filename:    Output file name
    :type   output_filename:    string
    :param  files_ws_rows:      Rows of file data
    :type   files_ws_rows:      list
    :param  sr_data_ws_rows:    Rows of SR Data
    :type   sr_data_ws_rows:    list
    """
    logger.info("Creating {}...".format(output_filename))
    wb = ExcelSheetFromTemplate(output_filename)
    logger.info('    Writing to files worksheet...')
    wb.write_to_files_worksheet(files_ws_rows)
    logger.info('    Writing to sra data worksheet...')
    wb.write_to_sr_data_worksheet(sr_data_ws_rows)


def generate_excel_file_name():
    """ Create an Excel workbook output file name with the current date.

    :return:    Name of Excel file
    :rtype      string
    """
    return "SRA_submission_{}.xlsx".format(datetime.now().strftime("%Y%m%d%H%M"))


def submit_files_to_ncbi(files, username, ssh_key):
    """Sends a list of files to NCBI

    :param      files:      Files to send.
    :type       files:      list
    :param      username:   Username for NCBI
    :type       username    string
    :param      ssh_key:    ssh key file
    :rtype      ssh_key:    string
    """
    logger.info("Submitting files to NCBI...")

    sra = SraSubmission(username, ssh_key)
    sra.submit_files(files)


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Send to NCBI .5')

    bioproject_accession, biosample_accession, input_fofn_file, username, ssh_key, excel_output_filename = \
        __parse_args(arguments)

    # return if ascp command does not exist
    if not SraSubmission(username, ssh_key).ascp_cmd_exist():
        logging.error("Could not find Aspera's ascp command!")
        sys.exit(errno.ENOENT)      # file/dir does not exist status code

    input_fofn_dirs = extract_cell_analysis_result_dirs_from_input_fofn_file(input_fofn_file)

    cell_analysis_results = get_cell_analysis_result_data(input_fofn_dirs)

    files_ws_rows = generate_rows_for_files_worksheet(cell_analysis_results)
    sr_data_ws_rows = generate_rows_for_sr_data_worksheet(cell_analysis_results)

    creat_excel_workbook(excel_output_filename, files_ws_rows, sr_data_ws_rows)

    # Get all files to upload
    files_only = []
    for result in cell_analysis_results:
        files_only.extend(result.get_files())

    submit_files_to_ncbi(files_only, username, ssh_key)

    logger.info("Complete!")

