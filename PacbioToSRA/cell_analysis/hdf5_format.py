import logging

from PacbioToSRA.cell_analysis.abstract_format import AbstractFormat


logger = logging.getLogger(__name__)


# constants
RS2 = 'PacBio RS II'
HDF5_FILE_TYPE = 'PacBio_HDF5'


class HDF5Format(AbstractFormat):
    @property
    def instrument_model(self):
        return RS2

    @property
    def required_file_extensions(self):
        return set(['metadata.xml', '1.bax.h5', '2.bax.h5', '3.bax.h5', 'bas.h5'])

    @property
    def file_type(self):
        return HDF5_FILE_TYPE

    @property
    def analysis_metadata_file_extension(self):
        return 'metadata.xml'


if __name__ == '__main__':
    ca_with_hdf5 = HDF5Format('/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/2015-04-16_42141_1139__Hummingbird_17kb_plate_7/H01_1')
    print 'RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR'
    print ca_with_hdf5.root_dir
    print 'TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT'
    print ca_with_hdf5.software_platform
    print 'YYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY'
    print ca_with_hdf5.instrument_model
    print 'EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
    print ca_with_hdf5.files
    print '5555555555555555555555555555555555555555'
    print ca_with_hdf5.analysis_metadata_file
    print 'WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'
    from pprint import pprint
    # pprint(ca_with_hdf5.file_info_map)
    print '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^'
    print ca_with_hdf5.get_value_from_analysis_metadata_file('Run/Name')

