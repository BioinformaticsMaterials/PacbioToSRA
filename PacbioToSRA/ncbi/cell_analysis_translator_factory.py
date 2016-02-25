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


if __name__ == '__main__':
    from PacbioToSRA.cell_analysis.bam_format import BamFormat
    from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format

    ca_in_bam = BamFormat('/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/bam2/r54016_20160209_005307/1_A01')
    print type(CellAnalysisTranslatorFactory.newCellAnalysisTranslator(ca_in_bam))

    ca_in_hdf5 = HDF5Format('/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/2015-04-16_42141_1139__Hummingbird_17kb_plate_7/H01_1')
    print type(CellAnalysisTranslatorFactory.newCellAnalysisTranslator(ca_in_hdf5))

