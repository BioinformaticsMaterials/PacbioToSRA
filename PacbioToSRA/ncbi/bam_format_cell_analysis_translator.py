import logging

from PacbioToSRA.ncbi.abstract_cell_analysis_translator import AbstractCellAnalysisTranslator


logger = logging.getLogger(__name__)


class BamFormatCellAnalysisTranslator(AbstractCellAnalysisTranslator):
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


if __name__ == '__main__':
    from PacbioToSRA.cell_analysis.bam_format import BamFormat

    ca_in_bam = BamFormat('/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/bam2/r54016_20160209_005307/1_A01')
    bfcat = BamFormatCellAnalysisTranslator()
    print bfcat.translate_sample_name(ca_in_bam)
    print bfcat.translate_library_id(ca_in_bam)
    print bfcat.translate_platform(ca_in_bam)
    print bfcat.translate_instrument_model(ca_in_bam)
    print bfcat.translate_design_description(ca_in_bam)
    print bfcat.translate_file_type(ca_in_bam)
    print bfcat.translate_run_id(ca_in_bam)

