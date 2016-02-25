import logging

from PacbioToSRA.cell_analysis.abstract_format import AbstractFormat


logger = logging.getLogger(__name__)


# constants
SEQUEL = 'PacBio Sequel'
BAM_FILE_TYPE = 'bam'


class BamFormat(AbstractFormat):
    @property
    def instrument_model(self):
        return SEQUEL

    @property
    def required_file_extensions(self):
        return set(['subreadset.xml', 'subreads.bam'])

    @property
    def file_type(self):
        return BAM_FILE_TYPE

    @property
    def analysis_metadata_file_extension(self):
        return 'subreadset.xml'

