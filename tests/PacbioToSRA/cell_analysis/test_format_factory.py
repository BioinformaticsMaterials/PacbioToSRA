import os

from PacbioToSRA.cell_analysis.bam_format import BamFormat
from PacbioToSRA.cell_analysis.format_factory import FormatFactory
from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format
from tests import *


class TestFormatFactory(unittest.TestCase):

    def test_newCellAnalysis(self):
        test_cases = [
            {
                'input': SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH,
                'expected_result': BamFormat,
            },
            {
                'input': SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH,
                'expected_result': HDF5Format,
            },

        ]

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                type(FormatFactory.newCellAnalysis(test['input']))
            )

    def test_newCellAnalysis_throws_exception(self):
        with self.assertRaises(Exception):
            FormatFactory.newCellAnalysis(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':
    unittest.main()
