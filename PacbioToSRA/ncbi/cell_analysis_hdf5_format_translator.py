import logging

from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format
from PacbioToSRA.ncbi.abstract_cell_analysis_translator import AbstractCellAnalysisTranslator


logger = logging.getLogger(__name__)


class CellAnalysisHDF5FormatTranslator(AbstractCellAnalysisTranslator):
    @property
    def cell_analysis_format_class(self):
        return HDF5Format

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

