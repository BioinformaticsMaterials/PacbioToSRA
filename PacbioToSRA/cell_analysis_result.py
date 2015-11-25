import hash_utils

from glob import glob
from os.path import join, isdir, dirname, basename
from xml.dom import minidom

# TODO: logger


class CellAnalysisResult(object):

    def __init__(self, absolute_path):
        # check if directory exists
        if not isdir(absolute_path):
            raise OSError("Directory does not exist: {}".format(absolute_path))

        # defaults
        self.root_dir = absolute_path
        self.analysis_results_dir = join(self.root_dir, 'Analysis_Results')
        self.metadata_xml_file_contents = None
        self.file_info = None

        #TODO
        # self.design_description = 'P6C4'

    def get_platform(self):
        """For now, can only return PacBio_SMRT
        :return:    Platform
        :rtype      string
        """
        # TODO: Needs these constants
        return 'PACBIO_SMRT'

    def get_instrument_model(self):
        """Determines the instrument the analysis was ran on.

        :return:    Instrument
        :rtype      string
        """
        # TODO: Needs these constants
        if self.get_bam_files():
            return 'PacBio Sequel'
        else:
            return 'PacBio RS II'

    def get_file_type(self):
        """Determines the file type for the analysis.

        :return:    File type
        :rtype      string
        """
        # TODO: Needs these constants
        if self.get_bam_files():
            return 'bam'
        else:
            return 'PacBio_HDF5'

    def get_bas_h5_files(self):
        """Gets absolute path for files ending with *.bas.h5

        :return list
        """
        return glob(join(self.analysis_results_dir, '*.bas.h5'))

    def get_bax_h5_files(self):
        """Gets absolute path for files ending with *.bax.h5

        :return list
        """
        return glob(join(self.analysis_results_dir, '*.bax.h5'))

    def get_metadata_xml_file(self):
        """Gets absolute path for files ending with *.metadata.h5

        :return string  Return only one file
        """
        file_type = '*.metadata.xml'
        files = glob(join(self.root_dir, file_type))

        if len(files) < 1:
            # found more than one file which isn't expect
            raise Exception('Found more than one {} file: {}'.format(file_type, files))
        elif len(files) > 1:
            # found no file which isn't expect
            raise Exception('Found no {} file'.format(file_type))

        return files[0]

    def get_bam_files(self):
        """Gets absolute path for files ending with *.bam
        This is for Sequel

        :return list
        """
        return glob(join(self.analysis_results_dir, '*.bam'))

    def get_files(self):
        """Gets all the files that the NCBI needs.

        :return list
        """
        return self.get_bas_h5_files() + self.get_bax_h5_files() + [self.get_metadata_xml_file()] + self.get_bam_files()

    def __load_metadata_xml_contents(self):
        """Loads the contents of the metadata_xml file into the instance.
        """
        if self.metadata_xml_file_contents is None:
            self.metadata_xml_file_contents = minidom.parse(self.get_metadata_xml_file())

    def get_sample_name(self):
        """Gets the sample name.

        :return string
        """
        self.__load_metadata_xml_contents()

        try:
            return self.metadata_xml_file_contents \
                .getElementsByTagName('Sample')[0] \
                .getElementsByTagName('Name')[0] \
                .firstChild.data
        except:
            raise Exception("No path to Sample/Name")

    def get_sample_plateid(self):
        """Gets the sample plate id.

        :return string
        """
        self.__load_metadata_xml_contents()

        try:
            return self.metadata_xml_file_contents \
                .getElementsByTagName('Sample')[0] \
                .getElementsByTagName('PlateId')[0] \
                .firstChild.data
        except:
            raise Exception("No path to Sample/PlateId")

    def get_run_name(self):
        """Gets the run name.

        :return string
        """
        self.__load_metadata_xml_contents()

        try:
            #TODO: check if this path is correct. original script was using the directory name
            return self.metadata_xml_file_contents \
                .getElementsByTagName('Run')[0] \
                .getElementsByTagName('Name')[0] \
                .firstChild.data
        except:
            raise Exception("No path to Run/Name")

    def get_info_for_files(self):
        if self.file_info:
            return self.file_info

        file_infos = {
            # <file>: {
            #   filename: ...,
            #   md5sum: ...,
            # },
            # '/mnt/data/m15253.bax.h5': {
            #   filename: 'm15253.bax.h5',
            #   md5sum: '26d155cbf85691c937feea9fe4f762e2',
            # },
            # ...
        }

        files = self.get_files()

        # get all the info for each file
        # TODO: files are huge so it's slow. Do this asynchronously
        for f in files:
            file_infos[f] = {
                'filename': basename(f),
                'md5sum': hash_utils.md5(f),
            }

        return file_infos


if __name__ == '__main__':
    # TODO: Create a test infrastructure
    from pprint import pprint
    # print AnalysisResults('directory_does_NOT_exist')
    d = '/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/src/sample/2015-04-16_42141_1139__Hummingbird_17kb_plate_7/H01_1'
    o = CellAnalysisResult(d)
    print(o.get_bas_h5_files())
    print(o.get_bax_h5_files())
    print(o.get_metadata_xml_file())
    print(o.get_sample_name())
    print(o.get_cell_name())
    print(o.get_run_name())
    pprint(o.get_info_for_files())

