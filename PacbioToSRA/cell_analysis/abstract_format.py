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
        # check if directory exists
        if not isdir(absolute_path):
            raise OSError("Directory does not exist: {}".format(absolute_path))

        # defaults
        self.__root_dir = absolute_path
        self.__software_platform = self.software_platform
        self.__instrument_model = self.instrument_model
        self.__files = set()
        self.__file_info_map = {}
        self.__analysis_metadata_file = self.analysis_metadata_file
        self.__analysis_metadata_contents = None
        self.__required_file_extensions = set()

        if not self._required_files_exist(self.files, self.required_file_extensions):
            raise Exception("Missing required files. Require: {}".format(list(self.required_file_extensions)))

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
        """There must be a file with all these following extensions.

        :return     File extensions
        :rtype      set
        """
        raise Exception("Missing implementation of abstract property.")

    @property
    def files(self):
        """Files in the cell analysis.

        :return     files
        :rtype      set
        """
        if not self.__files:
            for root, _, filenames in os.walk(self.root_dir):
                self.__files.update([os.path.join(root, f) for f in filenames])

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

    @property
    @abstractproperty
    def analysis_metadata_file(self):
        """Metadata file that provides info on the cell analysis."""
        raise Exception("Missing implementation of abstract property.")

    def _find_analysis_metadata_file(self, regex):
        """Finds cell analysis metadata file that provides information about the analysis.

        :param  regex:  Regular expresssion to search fo the file. Ex: ".*\.metadata\.xml$"
        :type   regex:  string
        :return:        Full path to file.
        :rtype          string
        """
        found = []
        pattern = re.compile(regex)
        for f in self.files:
            if pattern.match(f):
                found.append(f)

        if len(found) > 1:
            # found more than one file which isn't expect
            raise Exception('Found more than one file matching "{}". Files: {}'.format(regex, found))
        elif len(found) < 1:
            # found no file which isn't expect
            raise Exception('Found no files matching "{}"'.format(regex))

        return found[0]

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

    @classmethod
    def _required_files_exist(cls, files, extensions):
        """Checks that the file list contains each file extension.

        :param  files:      Files
        :type   files:      set
        :param  extensions: Extensions (ex: .bam, .metadata.xml)
        :type   extensions: set
        :return:            Result of whether a file exists for each extension.
        :rtype              boolean
        """
        for ext in extensions:
            match = False

            for f in files:
                if f.endswith(ext):
                    match = True
                    break

            if not match:
                return False

        return True

