from os.path import realpath, dirname, join


TEST_ROOT_FULLPATH = dirname(realpath(__file__))
CELL_ANALYSIS_WITH_BAM_FILES_TEST_DATA_PATH = join(TEST_ROOT_FULLPATH, 'data', 'cell_analysis_in_bam')
SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH = join(CELL_ANALYSIS_WITH_BAM_FILES_TEST_DATA_PATH, '1_A01')
CELL_ANALYSIS_WITH_HDF5_FILES_TEST_DATA_PATH = join(TEST_ROOT_FULLPATH, 'data', 'cell_analysis_in_hdf5')
SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH = join(CELL_ANALYSIS_WITH_HDF5_FILES_TEST_DATA_PATH, 'H01_1')
MD5SUM_TEST_FILE = join(TEST_ROOT_FULLPATH, 'data', 'md5sum.txt')


# https://gist.github.com/jonashaag/834a5f6051094dbed3bc
#   Fixes issue of running the tests in the base class. Ugh!
import unittest
def skip_base_class(base_cls):
    class BaseClassSkipper(base_cls):
        @classmethod
        def setUpClass(cls):
            if cls is BaseClassSkipper:
                raise unittest.SkipTest("Base class")
            super(BaseClassSkipper, cls).setUpClass()
    return BaseClassSkipper


