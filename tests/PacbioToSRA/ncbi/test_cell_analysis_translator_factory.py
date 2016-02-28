from PacbioToSRA.cell_analysis.bam_format import BamFormat
from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format
from PacbioToSRA.ncbi.cell_analysis_bam_format_translator import CellAnalysisBamFormatTranslator
from PacbioToSRA.ncbi.cell_analysis_hdf5_format_translator import CellAnalysisHDF5FormatTranslator
from PacbioToSRA.ncbi.cell_analysis_translator_factory import CellAnalysisTranslatorFactory
from tests import *


class TestCellAnalysisTranslatorFactory(unittest.TestCase):

    def test_newCellAnalysisTranslator(self):
        test_cases = [
            {
                'input': BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH),
                'expected_result': CellAnalysisBamFormatTranslator,
            },
            {
                'input': HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH),
                'expected_result': CellAnalysisHDF5FormatTranslator,
            },

        ]

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                type(CellAnalysisTranslatorFactory.newCellAnalysisTranslator(test['input']))
            )

    def test_newCellAnalysisTranslator_throws_exception(self):
        with self.assertRaises(Exception):
            CellAnalysisTranslatorFactory.newCellAnalysisTranslator(None)


if __name__ == '__main__':
    unittest.main()
