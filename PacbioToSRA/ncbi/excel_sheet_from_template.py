import os
import shutil

from openpyxl import load_workbook


# TODO: logging


class ExcelSheetFromTemplate(object):

    NCBI_SRA_SUBMISSION_FILE = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'templates',
        'SRA_submission.xlsx'
    )
    FILES_WORKSHEET_NAME = 'Sheet1'
    SR_DATA_WORKSHEET_NAME = 'SRA_data'

    def __init__(self, filename):
        if os.path.exists(filename):
            raise Exception("File already exists: {}".format(filename))

        self._output_file = filename
        self._copy_template(self._output_file)

        self._output_wb = load_workbook(filename=self._output_file)
        self._files_ws = self._output_wb.get_sheet_by_name(self.FILES_WORKSHEET_NAME)
        self._sr_data_ws = self._output_wb.get_sheet_by_name(self.SR_DATA_WORKSHEET_NAME)

    def _copy_template(self, output_file):
        """

        :param output_file:
        :return:
        """
        shutil.copy(self.NCBI_SRA_SUBMISSION_FILE, output_file)

    def _save_output_workbook(self):
        self._output_wb.save(self._output_file)

    def write_to_files_worksheet(self, rows):
        '''
        ws_for_files = wb.active
        ws_for_files.title = 'Sheet1'
        ws_for_files.append(['Library_ID', 'Run_ID', 'Filename', 'md5sum'])
        '''

        self._do_write_to_worksheet(self._files_ws, rows)

    def write_to_sr_data_worksheet(self, rows):
        '''
        # Create excel sheet for sample runs
        ws_for_sr_data = wb.create_sheet(index=0, title='SRA_data')
        ws_for_sr_data.append([
            'bioproject_accession',
            'biosample_accession',
            'sample_name',
            'library_ID',
            'title/short description',
            'library_strategy (click for details)',
            'library_source (click for details)',
            'library_selection (click for details)',
            'library_layout',
            'platform (click for details)',
            'instrument_model',
            'design_description',
            'reference_genome_assembly (or accession)',
            'alignment_software',
            'forward_read_length',
            'reverse_read_length',
            'filetype',
            'filename',
            'MD5_checksum',
            'filetype',
            'filename',
            'MD5_checksum',
        ])
        '''
        self._do_write_to_worksheet(self._sr_data_ws, rows)

    def _do_write_to_worksheet(self, ws, rows):
        # assumes that each worksheet has a header

        row_index = 2           # excel worksheets start at 1. skip header

        for row in rows:
            col_index = 1

            for entry in row:
                ws.cell(row=row_index, column=col_index).value = entry
                col_index += 1

            row_index += 1

        self._save_output_workbook()

