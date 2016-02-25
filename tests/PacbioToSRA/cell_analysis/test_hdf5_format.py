from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format
from tests import *
from tests.PacbioToSRA.cell_analysis.base_format_tests import BaseFormatTests


class TestHDF5Format(BaseFormatTests):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.TestHDF5Format
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.TestHDF5Format.test_instrument_model.test_instrument_model

    To run all test:
    $ python -m unittest discover -v
    """


    data_dir_for_tests = SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH
    inst = HDF5Format(data_dir_for_tests)
    num_valid_files = 5

    def test_get_value_from_analysis_metadata_file(self):
        test_cases = [
            {
                'input': 'Run/RunId',
                'expected_result': 'H01_1_Run_RunID',
            },
            {
                'input': 'Sample/Name',
                'expected_result': 'H01_1_Sample_Name',
            },
            {
                'input': 'Primary/ConfigFileName',
                'expected_result': 'H01_1_Primary_ConfigFileName.xml',
            },
        ]

        analysis = self.inst

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                analysis.get_value_from_analysis_metadata_file(test['input'])
            )


if __name__ == '__main__':
    unittest.main()
