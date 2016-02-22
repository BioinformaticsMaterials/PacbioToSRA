import logging

# TODO: @register
from PacbioToSRA.cell_analysis.bam_format import BamFormat
from PacbioToSRA.cell_analysis.hd5_format import HD5Format


logger = logging.getLogger(__name__)


class FormatFactory(object):
    @staticmethod
    def newCellAnalysis(dir):
        clazzes = set([HD5Format, BamFormat])
        for clz in clazzes:
            try:
                return clz(dir)
            except:
                pass

        raise Exception("Cell Analysis Format object could not be created.")


if __name__ == '__main__':
    dirs = set([
        '/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/bam2/r54016_20160209_005307/1_A01',
        '/Users/clongboy/projects/PacbioToSRA/src/PacbioToSRA/temp/2015-04-16_42141_1139__Hummingbird_17kb_plate_7/H01_1',
    ])

    for d in dirs:
        print d
        o = FormatFactory.newCellAnalysis(d)
        print o.instrument_model
