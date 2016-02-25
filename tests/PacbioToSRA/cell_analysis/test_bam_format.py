import unittest

from PacbioToSRA.cell_analysis.bam_format import BamFormat
from tests import *


class TestBamFormat(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.TestBamFormat
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.TestBamFormat.test_instrument_model.test_instrument_model

    To run all test:
    $ python -m unittest discover -v
    """

    def test_instrument_model(self):
        self.assertIsNotNone(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).instrument_model)

    def test_required_file_extensions(self):
        self.assertIsNotNone(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).required_file_extensions)

    def test_file_type(self):
        self.assertIsNotNone(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).file_type)

    def test_analysis_metadata_file_extension(self):
        self.assertIsNotNone(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).analysis_metadata_file_extension)

    def test_root_dir(self):
        self.assertEqual(
            SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH,
            BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).root_dir
        )

    def test_software_platform(self):
        self.assertIsNotNone(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).software_platform)

    def test_files(self):
        # not perfect but enough
        self.assertEqual(
            2,     # number of files
            len(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).files)
        )

    def test_file_info_map(self):
        # not perfect but enough
        self.assertEqual(
            2,     # number of files
            len(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).file_info_map)
        )

    def test_software_platform(self):
        self.assertIsNotNone(BamFormat(SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH).analysis_metadata_file)


if __name__ == '__main__':
    unittest.main()
