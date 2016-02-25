import concurrent.futures
import logging
import os
import re

from PacbioToSRA import hash_utils
from abc import ABCMeta, abstractproperty
from os.path import isdir, basename
from xml.dom import minidom


logger = logging.getLogger(__name__)


# constants
PACB_SMART_ANALYSIS = 'PACBIO_SMRT'


class AbstractFormat:
    __metaclass__ = ABCMeta

    def __init__(self, absolute_path):
        """
        :param  absolute_path:          Path to cell analysis files
        :rtype  absolute_path:          string
        """
        logger.debug("Creating cell analysis instance for {}: {}".format(self.__class__.__name__, absolute_path))

        # check if directory exists
        if not isdir(absolute_path):
            raise OSError("Directory does not exist: {}".format(absolute_path))

        # defaults
        self.__root_dir = absolute_path
        self.__software_platform = self.software_platform
        self.__files = set()
        self.__file_info_map = {}
        self.__analysis_metadata_file = None
        self.__analysis_metadata_contents = None

        # abstract properties
        self.__instrument_model = self.instrument_model
        self.__required_file_extensions = self.required_file_extensions
        self.__file_type = self.file_type
        self.__analysis_metadata_file_extension = self.analysis_metadata_file_extension

        if not self.is_dir_valid():
            raise InvalidDirectoryException("Directory is not valid.")

        logger.debug('Instance created.')

    ######################
    # Abstract Properties
    ######################
    @property
    @abstractproperty
    def instrument_model(self):
        """The instrument model that the analysis was ran on. Ex: Sequel

        :return     Instrument model
        :rtype      string
        """
        raise Exception("Missing implementation of abstract property.")

    @property
    @abstractproperty
    def required_file_extensions(self):
        """There must be a file associated with all these following extensions.

        :return     File extensions
        :rtype      set
        """
        raise Exception("Missing implementation of abstract property.")

    @property
    @abstractproperty
    def file_type(self):
        """The type the files are in.

        :return     type
        :rtype      string
        """
        raise Exception("Missing implementation of abstract property.")

    @property
    @abstractproperty
    def analysis_metadata_file_extension(self):
        """File extension that contains provides info on the cell analysis."""
        raise Exception("Missing implementation of abstract property.")

    ######################
    # Properties
    ######################
    @property
    def root_dir(self):
        """Absolute path containing the analysis.

        :return:    Path
        :rtype      string
        """
        return self.__root_dir

    @property
    def software_platform(self):
        """Software platform that the analysis was ran on.

        :return     Software platform
        :rtype      string
        """
        return PACB_SMART_ANALYSIS

    @property
    def files(self):
        """Files in the cell analysis.

        :return     files
        :rtype      set
        """
        if self.__files:
            return self.__files

        for root, _, filenames in os.walk(self.root_dir):
            for f in filenames:
                ext = self.extract_file_extension(f)

                if ext in self.required_file_extensions:
                    self.__files.add(os.path.join(root, f))

        return self.__files

    @property
    def file_info_map(self):
        """Additional information on the files.

        :return:    Additional info on the files
        :rtype      dict
        """

        if not self.__file_info_map:
            self.__file_info_map = self.__generate_file_info_map(self.files)

        return self.__file_info_map

    @property
    def analysis_metadata_file(self):
        """Metadata file that provides info on the cell analysis."""
        if not self.__analysis_metadata_file:
            self.__analysis_metadata_file = self._find_analysis_metadata_file(
                self.files, self.analysis_metadata_file_extension
            )

        return self.__analysis_metadata_file

    @classmethod
    def _find_analysis_metadata_file(cls, files, extension):
        """From the list of files, finds the file for the metadata.

        :param  files:      Files
        :type   files:      set
        :param  extension:  Extension
        :param  extension:  string
        :return:            Metadata file.
        :rtype              string
        """
        found = []
        for f in files:
            if extension == cls.extract_file_extension(f):
                found.append(f)

        # expect that only 1 file is found
        if len(found) > 1:
            # found more than one file
            raise Exception('Found more than one file matching "{}". Files: {}'.format(extension, found))
        elif len(found) < 1:
            # found no files
            raise Exception('Found no files matching "{}"'.format(analysis_metadata_file_extension))

        return found[0]


    ######################
    # Methods
    ######################

    @classmethod
    def __generate_file_info_map(cls, files):
        """Returns additional info on all the files.

        :param  files:  Files
        :type   files:  set
        :return:        Additional files on the files.
                        Return format:
                            {
                                <file>: {
                                    filename: ...,
                                    md5sum: ...,
                                },
                                ...
                            }

                        Ex:
                            {
                                '/mnt/data/m15253.bax.h5': {
                                    filename: 'm15253.bax.h5',
                                    md5sum: '26d155cbf85691c937feea9fe4f762e2',
                                },
                                ...
                            }

        :rtype          dict
        """
        logger.debug("Getting file info for all files: {}".format(files))

        f_map = {}

        # files are huge so calculate md5sum for several files in parallel
        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = {}
            i = 0
            total_files = len(files)

            for f in files:
                i += 1
                logger.debug("   ({}/{}) Submitting md5sum job to process pool for file: {}".format(i, total_files, f))
                futures[executor.submit(hash_utils.md5, f)] = f

        for future in concurrent.futures.as_completed(futures):
            md5sum = future.result()

            logger.debug("md5sum results. file: {} md5sum: {}".format(f, md5sum))

            f = futures[future]
            f_map[f] = {
                'filename': basename(f),
                'md5sum': md5sum,
            }

        return f_map

    def get_value_from_analysis_metadata_file(self, path, attribute=None):
        """Extracts data from the xml file.

        :param  path:   Path to data. Input format: /path/to/field => <path><to><field>value</field></to></path>
        :type   path:   string
        :return:        Value in xml field
        :rtype          string
        """
        # Loads the contents of the metadata_xml file into the instance so it doesn't have to get regenerated on every call.
        if self.__analysis_metadata_contents is None:
            self.__analysis_metadata_contents = minidom.parse(self.analysis_metadata_file)

        path_in_parts = path.split('/')

        try:
            xml = self.__analysis_metadata_contents
            for path_part in path_in_parts:
                xml = xml.getElementsByTagName(path_part)[0]

            if attribute:
                return xml.getAttribute(attribute)
            else:
                return xml.firstChild.data

        except:
            raise Exception("No path to {}".format(path))

    def is_dir_valid(self):
        """Checks whether the directory is valid such as containing all the required files. This function exists so
        this can be overwritten to add more checks.
        """
        return self.required_files_exist(self.files, self.required_file_extensions)

    @classmethod
    def required_files_exist(cls, files, extensions):
        """Checks that the file list contains each file extension.

        :param  files:      Files
        :type   files:      set
        :param  extensions: Extensions (ex: bam, metadata.xml)
        :type   extensions: set
        :return:            Result of whether a file exists for each extension.
        :rtype              boolean
        """
        logger.debug("Checking that all required files exist.")
        extensions_exist = dict.fromkeys(extensions, False)

        for f in files:
            ext = cls.extract_file_extension(f)

            if ext not in extensions:
                continue

            extensions_exist[ext] = True

        logger.debug("Check directory results: {}".format(extensions_exist))
        return all(extensions_exist.itervalues())

    @staticmethod
    def extract_file_extension(f):
        """ Extracts everything after the first "." (ex: input.metatdata.xml => metadata.xml)

        :param  f:  File name
        :type   f:  string
        :return:    File extension
        :rtype      string
        """
        try:
            return f.split('.', 1)[1]
        except:
            raise


class InvalidDirectoryException(Exception):
    pass

