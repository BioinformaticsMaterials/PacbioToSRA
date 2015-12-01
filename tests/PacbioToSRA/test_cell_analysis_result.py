import unittest

from PacbioToSRA.cell_analysis_result import *
from tests import *


class TestCellAnalysisResult(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis_result
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis_result.TestCellAnalysisResult
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis_result.TestCellAnalysisResult.test_directory_does_not_exist
    """

    def test_directory_does_not_exist(self):
        with self.assertRaises(OSError):
            CellAnalysisResult('path/does/not/exist')

    def test_get_instrument_model_for_h5_files(self):
        self.assertEqual(
            CellAnalysisResult.RS2,
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_H5_FILES_TEST_DATA_PATH).get_instrument_model()
        )

    def test_get_instrument_model_for_bam_files(self):
        self.assertEqual(
            CellAnalysisResult.SEQUEL,
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_BAM_FILES_TEST_DATA_PATH).get_instrument_model()
        )

    def test_get_file_type_for_h5_files(self):
        self.assertEqual(
            CellAnalysisResult.HDF5_FILE_TYPE,
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_H5_FILES_TEST_DATA_PATH).get_file_type()
        )

    def test_get_file_type_for_bam_files(self):
        self.assertEqual(
            CellAnalysisResult.BAM_FILE_TYPE,
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_BAM_FILES_TEST_DATA_PATH).get_file_type()
        )

    def test_get_sample_name_for_h5_files(self):
        self.assertEqual(
            'H5_Sample_Name',
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_H5_FILES_TEST_DATA_PATH).get_sample_name()
        )

    def test_get_sample_name_for_bam_files(self):
        self.assertEqual(
            'BAM_Sample_Name',
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_BAM_FILES_TEST_DATA_PATH).get_sample_name()
        )

    def test_get_sample_plateid_for_h5_files(self):
        self.assertEqual(
            'H5_Sample_PlateId',
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_H5_FILES_TEST_DATA_PATH).get_sample_plateid()
        )

    def test_get_sample_plateid_for_bam_files(self):
        self.assertEqual(
            'BAM_Sample_PlateId',
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_BAM_FILES_TEST_DATA_PATH).get_sample_plateid()
        )

    def test_get_run_name_for_h5_files(self):
        self.assertEqual(
            'H5_Run_Name',
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_H5_FILES_TEST_DATA_PATH).get_run_name()
        )

    def test_get_run_name_for_bam_files(self):
        self.assertEqual(
            'BAM_Run_Name',
            CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_BAM_FILES_TEST_DATA_PATH).get_run_name()
        )


if __name__ == '__main__':
    unittest.main()
