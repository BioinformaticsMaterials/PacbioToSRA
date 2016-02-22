import logging

from PacbioToSRA.cell_analysis.abstract_format import AbstractFormat, PACB_SMART_ANALYSIS


logger = logging.getLogger(__name__)


# constants
SEQUEL = 'PacBio Sequel'


class BamFormat(AbstractFormat):
    @property
    def instrument_model(self):
        return SEQUEL

    @property
    def required_file_extensions(self):
        return set(['.subreadset.xml', '.subreads.bam'])

    @property
    def analysis_metadata_file(self):
        return self._find_analysis_metadata_file('.*\.subreadset\.xml$')


if __name__ == '__main__':
    ca_in_bam = BamFormat('/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/bam2/r54016_20160209_005307/1_A01')
    print 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'
    print ca_in_bam.root_dir
    print 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT'
    print ca_in_bam.software_platform
    print 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
    print ca_in_bam.instrument_model
    print 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
    print ca_in_bam.files
    print '5555555555555555555555555555555555555555'
    print ca_in_bam.analysis_metadata_file
    print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
    from pprint import pprint
    # pprint(ca_in_bam.file_info_map)
    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    print ca_in_bam.get_value_from_analysis_metadata_file(
        'pbmeta:CollectionMetadata/pbmeta:WellSample',
        'Name'
    )


