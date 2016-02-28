from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format
from PacbioToSRA.ncbi.cell_analysis_hdf5_format_translator import CellAnalysisHDF5FormatTranslator
from tests import *
from tests.PacbioToSRA.ncbi.base_test_for_cell_analysis_translator import BaseTestForCellAnalysisTranslator


class TestCellAnalysisBamFormatTranslator(BaseTestForCellAnalysisTranslator):

    cell_analysis = HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH)
    inst = CellAnalysisHDF5FormatTranslator


if __name__ == '__main__':
    unittest.main()
