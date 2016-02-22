import logging

from PacbioToSRA.cell_analysis.hd5_format import HD5Format
from PacbioToSRA.ncbi.abstract_cell_analysis_translator import AbstractCellAnalysisTranslator


logger = logging.getLogger(__name__)


class CellAnalysisHD5FormatTranslator(AbstractCellAnalysisTranslator):
    @property
    def cell_analysis_format_class(self):
        return HD5Format

    @staticmethod
    def translate_sample_name(cell_analysis):
        return cell_analysis.get_value_from_analysis_metadata_file(
            'Sample/Name'
        )

    @staticmethod
    def translate_library_id(cell_analysis):
        return cell_analysis.get_value_from_analysis_metadata_file(
            'Sample/Name'
        )

    @staticmethod
    def translate_design_description(cell_analysis):
        return cell_analysis\
            .get_value_from_analysis_metadata_file('Primary/ConfigFileName')\
            .rstrip('.xml')


if __name__ == '__main__':
    from PacbioToSRA.cell_analysis.hd5_format import HD5Format

    ca_in_hd5 = HD5Format('/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/2015-04-16_42141_1139__Hummingbird_17kb_plate_7/H01_1')
    hd5cat = CellAnalysisHD5FormatTranslator()
    print hd5cat.translate_sample_name(ca_in_hd5)
    print hd5cat.translate_library_id(ca_in_hd5)
    print hd5cat.translate_platform(ca_in_hd5)
    print hd5cat.translate_instrument_model(ca_in_hd5)
    print hd5cat.translate_design_description(ca_in_hd5)
    print hd5cat.translate_file_type(ca_in_hd5)
    print hd5cat.translate_run_id(ca_in_hd5)

