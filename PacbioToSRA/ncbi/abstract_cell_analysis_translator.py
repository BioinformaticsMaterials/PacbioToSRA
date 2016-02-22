import logging

from abc import ABCMeta, abstractmethod, abstractproperty
from os.path import basename


logger = logging.getLogger(__name__)


class AbstractCellAnalysisTranslator:
    __metaclass__ = ABCMeta

    @property
    @abstractproperty
    def cell_analysis_format_class(self):
        """Returns the cell analysis format class that this translator class will be used for.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                Cell analysis format class (ex: BamFormat)
        :rtype                  class
        """
        raise Exception("Missing implementation of abstract property.")

    @staticmethod
    @abstractmethod
    def translate_sample_name(cell_analysis):
        """Returns the sample name from a cell analysis.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                Sample name
        :rtype                  string
        """
        raise Exception("Missing implementation of abstract property.")

    @staticmethod
    @abstractmethod
    def translate_library_id(cell_analysis):
        """Returns the library id from a cell analysis.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                Library id
        :rtype                  string
        """
        raise Exception("Missing implementation of abstract property.")

    @staticmethod
    @abstractmethod
    def translate_design_description(cell_analysis):
        """Returns the design descriptionfrom a cell analysis.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                Design description
        :rtype                  string
        """
        raise Exception("Missing implementation of abstract property.")

    @staticmethod
    def translate_platform(cell_analysis):
        """Returns the platform from a cell analysis.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                platform
        :rtype                  string
        """
        return cell_analysis.software_platform

    @staticmethod
    def translate_instrument_model(cell_analysis):
        """Returns the instrument_model from a cell analysis.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                Instrument model
        :rtype                  string
        """
        return cell_analysis.instrument_model

    @staticmethod
    def translate_file_type(cell_analysis):
        """Returns the file type from a cell analysis.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                file type
        :rtype                  string
        """
        return cell_analysis.file_type

    @classmethod
    def translate_run_id(cls, cell_analysis):
        """Returns the run id from a cell analysis.

        :param  cell_analysis:  Cell analysis such as cell_analysis.bam_format
        :rtype  cell_analysis:  Child of cell_analysis.abstract_format.AbstractFormat
        :return:                Run id
        :rtype                  string
        """
        get_any_file = next(iter(cell_analysis.files))
        return cls._generate_run_id_from_filename(get_any_file)

    @staticmethod
    def _generate_run_id_from_filename(filename):
        f = basename(filename)
        parts = f.split('.')
        return parts[0]

