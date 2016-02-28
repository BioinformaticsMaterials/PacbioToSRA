import logging

from PacbioToSRA.cell_analysis.bam_format import BamFormat
from PacbioToSRA.ncbi.abstract_cell_analysis_translator import AbstractCellAnalysisTranslator


logger = logging.getLogger(__name__)


class CellAnalysisBamFormatTranslator(AbstractCellAnalysisTranslator):
    @property
    def cell_analysis_format_class(self):
        return BamFormat

    @staticmethod
    def translate_sample_name(cell_analysis):
        return cell_analysis.get_value_from_analysis_metadata_file(
            'pbmeta:CollectionMetadata/pbmeta:WellSample',
            'Name'
        )

    @staticmethod
    def translate_library_id(cell_analysis):
        return cell_analysis.get_value_from_analysis_metadata_file(
            'pbmeta:CollectionMetadata/pbmeta:WellSample',
            'Name'
        )

    @staticmethod
    def translate_design_description(cell_analysis):
        return cell_analysis\
            .get_value_from_analysis_metadata_file('pbmeta:CollectionMetadata/pbmeta:Primary/pbmeta:ConfigFileName')\
            .rstrip('.xml')

