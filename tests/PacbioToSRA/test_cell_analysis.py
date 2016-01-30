import unittest

from PacbioToSRA.cell_analysis import *
from tests import *


class TestCellAnalysis(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis.TestCellAnalysis
    $ python -m unittest -v tests.PacbioToSRA.test_cell_analysis.TestCellAnalysis.test_directory_does_not_exist

    To run all test:
    $ python -m unittest discover -v
    """

    def test_directory_does_not_exist(self):
        with self.assertRaises(OSError):
            CellAnalysis('path/does/not/exist')

    def test_get_instrument_model_for_h5_files(self):
        self.assertEqual(
            CellAnalysis.RS2,
            CellAnalysis(CELL_ANALYSIS_WITH_H5_FILES_TEST_DATA_PATH).get_instrument_model()
        )

    def test_get_instrument_model_for_bam_files(self):
        self.assertEqual(
            CellAnalysis.SEQUEL,
            CellAnalysis(CELL_ANALYSIS_WITH_BAM_FILES_TEST_DATA_PATH).get_instrument_model()
        )

    def test_get_file_type_for_h5_files(self):
        self.assertEqual(
            CellAnalysis.HDF5_FILE_TYPE,
            CellAnalysis(CELL_ANALYSIS_WITH_H5_FILES_TEST_DATA_PATH).get_file_type()
        )

    def test_get_file_type_for_bam_files(self):
        self.assertEqual(
            CellAnalysis.BAM_FILE_TYPE,
            CellAnalysis(CELL_ANALYSIS_WITH_BAM_FILES_TEST_DATA_PATH).get_file_type()
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

        c = CellAnalysis(CELL_ANALYSIS_WITH_H5_FILES_TEST_DATA_PATH)

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

        c = CellAnalysis(CELL_ANALYSIS_WITH_BAM_FILES_TEST_DATA_PATH)

        for test in test_cases:
            self.assertEqual(test['expected_value'], c.get_value_from_xml_path(test['input']))


if __name__ == '__main__':
    unittest.main()
