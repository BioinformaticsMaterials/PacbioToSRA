import unittest

from PacbioToSRA.cell_analysis.hdf5_format import HDF5Format
from PacbioToSRA.hash_utils import md5
from tests import *


class TestHDF5Format(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.TestHDF5Format
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.TestHDF5Format.test_instrument_model.test_instrument_model

    To run all test:
    $ python -m unittest discover -v
    """

    def test_instrument_model(self):
        self.assertIsNotNone(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).instrument_model)

    def test_required_file_extensions(self):
        self.assertIsNotNone(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).required_file_extensions)

    def test_file_type(self):
        self.assertIsNotNone(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).file_type)

    def test_analysis_metadata_file_extension(self):
        self.assertIsNotNone(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).analysis_metadata_file_extension)

    def test_root_dir(self):
        self.assertEqual(
            SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH,
            HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).root_dir
        )

    def test_software_platform(self):
        self.assertIsNotNone(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).software_platform)

    def test_files(self):
        # not perfect but enough
        self.assertEqual(
            5,     # number of files
            len(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).files)
        )

    def test_file_info_map(self):
        # not perfect but enough
        self.assertEqual(
            5,     # number of files
            len(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).file_info_map)
        )

    def test_software_platform(self):
        self.assertIsNotNone(HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).analysis_metadata_file)

    def test_find_analysis_metadata_file_finds_one_file(self):
        f = '/path/to/file.zip'
        search_ext = 'zip'

        files = set([
            '/path/to/file.csv',
            '/path/to/file.gif',
            '/path/to/file.jpg',
            '/path/to/file.doc',
            f,
        ])

        self.assertEqual(
            f,
            HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH)._find_analysis_metadata_file(files, search_ext)
        )

    def test_find_analysis_metadata_file_finds_too_many_files(self):
        f = '/path/to/file.zip'
        search_ext = 'zip'

        files = set([
            '/path/to/file.csv',
            '/path/to/file.gif',
            '/path/to/file.jpg',
            '/path/to/file.doc',
            f,
            '/path/to/file2.zip',
        ])

        with self.assertRaises(Exception):
            self.assertEqual(
                f,
                HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH)._find_analysis_metadata_file(files, search_ext)
            )

    def test_find_analysis_metadata_file_finds_no_files(self):
        f = '/path/to/file.zip'
        search_ext = 'zip'

        files = set([
            '/path/to/file.csv',
            '/path/to/file.gif',
            '/path/to/file.jpg',
            '/path/to/file.doc',
        ])

        with self.assertRaises(Exception):
            self.assertEqual(
                f,
                HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH)._find_analysis_metadata_file(files, search_ext)
            )

    def test_generate_file_info_map_check_md5sum(self):
        analysis = HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH)
        file_info_map = analysis.file_info_map
        files = analysis.files

        self.assertEqual(len(files), len(file_info_map))

        for f in files:
            self.assertEqual(md5(f), file_info_map[f]['md5sum'])

    def test_get_value_from_analysis_metadata_file(self):
        test_cases = [
            {
                'input': 'Run/RunId',
                'expected_result': 'H01_1_Run_RunID',
            },
            {
                'input': 'Sample/Name',
                'expected_result': 'H01_1_Sample_Name',
            },
            {
                'input': 'Primary/ConfigFileName',
                'expected_result': 'H01_1_Primary_ConfigFileName.xml',
            },
        ]

        analysis = HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH)

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                analysis.get_value_from_analysis_metadata_file(test['input'])
            )

    def test_get_value_from_analysis_metadata_file_with_invalid_path(self):
        with self.assertRaises(Exception):
            HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH).get_value_from_analysis_metadata_file('does/not/exist')

    def test_required_files_exist(self):
        test_cases = [
            {
                'input': {
                    'files': [
                        '/path/to/file.zip',
                        'report.csv',
                        '/path/to/file.xlsx',
                        'this/is/a/file.milk.does.a.body.good'
                    ],
                    'extensions': ['zip', 'csv', 'xlsx', 'milk.does.a.body.good'],
                },
                'expected_result': True,
            },
            {
                'input': {
                    'files': [
                        '/path/to/file.zip',
                        'report.csv',
                        '/path/to/file.xlsx',
                    ],
                    'extensions': ['zip', 'csv', 'xlsx', 'this.does.not.exist'],
                },
                'expected_result': False,
            },
            {
                'input': {
                    'files': [
                        '/path/to/file.zip',
                        'report.csv',
                        '/path/to/file.xlsx',
                        '/path/to/extra/extension.extra',
                    ],
                    'extensions': ['zip', 'csv', 'xlsx'],
                },
                'expected_result': True,
            },
        ]

        analysis = HDF5Format(SINGLE_HDF5_CELL_ANALYSIS_TEST_DATA_PATH)

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                analysis.required_files_exist(test['input']['files'], test['input']['extensions'])
            )


if __name__ == '__main__':
    unittest.main()
