from os.path import realpath, dirname, join


TEST_ROOT_FULLPATH = dirname(realpath(__file__))
CELL_ANALYSIS_WITH_H5_FILES_TEST_DATA_PATH = join(TEST_ROOT_FULLPATH, 'data', 'cell_analysis_result_with_h5')
CELL_ANALYSIS_WITH_BAM_FILES_TEST_DATA_PATH = join(TEST_ROOT_FULLPATH, 'data', 'cell_analysis_result_with_bam')
MD5SUM_TEST_FILE = join(TEST_ROOT_FULLPATH, 'data', 'md5sum.txt')
