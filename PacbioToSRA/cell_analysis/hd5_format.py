import logging

from PacbioToSRA.cell_analysis.abstract_format import AbstractFormat, PACB_SMART_ANALYSIS


logger = logging.getLogger(__name__)


# constants
RS2 = 'PacBio RS II'


class HD5Format(AbstractFormat):
    @property
    def instrument_model(self):
        return RS2

    @property
    def required_file_extensions(self):
        return set(['.metadata.xml', '.1.bax.h5', '.2.bax.h5', '.3.bax.h5', '.bas.h5'])

    @property
    def analysis_metadata_file(self):
        return self._find_analysis_metadata_file(".*\.metadata\.xml$")


if __name__ == '__main__':
    ca_with_hd5 = HD5Format('/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/2015-04-16_42141_1139__Hummingbird_17kb_plate_7/H01_1')
    print 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'
    print ca_with_hd5.root_dir
    print 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT'
    print ca_with_hd5.software_platform
    print 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
    print ca_with_hd5.instrument_model
    print 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
    print ca_with_hd5.files
    print '5555555555555555555555555555555555555555'
    print ca_with_hd5.analysis_metadata_file
    print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
    from pprint import pprint
    # pprint(ca_with_hd5.file_info_map)
    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    print ca_with_hd5.get_value_from_analysis_metadata_file('Run/Name')

