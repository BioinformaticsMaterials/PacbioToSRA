import unittest

from PacbioToSRA.cell_analysis_result import *
from tests import *


class TestCellAnalysisResult(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis_result
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis_result.TestCellAnalysisResult
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis_result.TestCellAnalysisResult.test_directory_does_not_exist

    To run all test:
    $ python -m unittest discover -v
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

    def test_get_value_from_xml_path_from_h5_files(self):
        test_cases = [
            {
                'input': 'Sample/Name',
                'expected_value': 'H5_Sample_Name',
            },
            {
                'input': 'Sample/PlateId',
                'expected_value': 'H5_Sample_PlateId',
            },
            {
                'input': 'Run/Name',
                'expected_value': 'H5_Run_Name',
            },
            {
                'input': 'TemplatePrep/Name',
                'expected_value': 'H5_TemplatePrep_Name',
            },
            {
                'input': 'BindingKit/Name',
                'expected_value': 'H5_BindingKit_Name',
            },
            {
                'input': 'Primary/ConfigFileName',
                'expected_value': 'H5_Primary_ConfigFileName.xml',
            },

        ]

        c = CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_H5_FILES_TEST_DATA_PATH)

        for test in test_cases:
            self.assertEqual(test['expected_value'], c.get_value_from_xml_path(test['input']))

    def test_get_value_from_xml_path_from_bam_files(self):
        test_cases = [
            {
                'input': 'Sample/Name',
                'expected_value': 'BAM_Sample_Name',
            },
            {
                'input': 'Sample/PlateId',
                'expected_value': 'BAM_Sample_PlateId',
            },
            {
                'input': 'Run/Name',
                'expected_value': 'BAM_Run_Name',
            },
            {
                'input': 'TemplatePrep/Name',
                'expected_value': 'BAM_TemplatePrep_Name',
            },
            {
                'input': 'BindingKit/Name',
                'expected_value': 'BAM_BindingKit_Name',
            },
            {
                'input': 'Primary/ConfigFileName',
                'expected_value': 'BAM_Primary_ConfigFileName.xml',
            },

        ]

        c = CellAnalysisResult(CELL_ANALYSIS_RESULT_WITH_BAM_FILES_TEST_DATA_PATH)

        for test in test_cases:
            self.assertEqual(test['expected_value'], c.get_value_from_xml_path(test['input']))


if __name__ == '__main__':
    unittest.main()
