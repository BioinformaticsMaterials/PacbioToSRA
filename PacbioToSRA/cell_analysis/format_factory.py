import logging

# TODO: @register
from PacbioToSRA.cell_analysis.abstract_format import InvalidDirectoryException
from PacbioToSRA.cell_analysis.bam_format import BamFormat
from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format


logger = logging.getLogger(__name__)


class FormatFactory(object):
    @staticmethod
    def newCellAnalysis(dir):
        clazzes = set([BamFormat, HDF5Format])
        for clz in clazzes:
            try:
                logger.debug("{} trying to create instance for: {}".format(__name__, clz.__name__))
                obj = clz(dir)
                logger.debug("Directory: {} => Type: {}".format(dir, clz.__name__))
                return obj
            except InvalidDirectoryException as e:
                logger.debug(e.message)
            except:
                raise

        raise Exception("Cell Analysis Format object could not be created.")

