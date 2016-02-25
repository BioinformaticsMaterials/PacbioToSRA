from PacbioToSRA.cell_analysis.bam_format import BamFormat
from PacbioToSRA.ncbi.cell_analysis_bam_format_translator import CellAnalysisBamFormatTranslator
from tests import *
from tests.PacbioToSRA.ncbi.base_test_for_cell_analysis_translator import BaseTestForCellAnalysisTranslator


class TestCellAnalysisBamFormatTranslator(BaseTestForCellAnalysisTranslator):
    cell_analysis = BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH)
    inst = CellAnalysisBamFormatTranslator


if __name__ == '__main__':
    unittest.main()
