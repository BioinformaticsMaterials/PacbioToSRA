import logging

# TODO: @register
from PacbioToSRA.ncbi.cell_analysis_bam_format_translator import CellAnalysisBamFormatTranslator
from PacbioToSRA.ncbi.cell_analysis_hdf5_format_translator import CellAnalysisHDF5FormatTranslator


logger = logging.getLogger(__name__)


class CellAnalysisTranslatorFactory(object):
    @staticmethod
    def newCellAnalysisTranslator(cell_analysis):
        for clz in set([CellAnalysisBamFormatTranslator, CellAnalysisHDF5FormatTranslator]):
            if clz().cell_analysis_format_class == type(cell_analysis):
                return clz()

        raise Exception("Can't understand cell analysis format.")

