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

