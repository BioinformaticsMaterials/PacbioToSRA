import unittest

from PacbioToSRA.hash_utils import md5
from tests import *


# https://gist.github.com/jonashaag/834a5f6051094dbed3bc
#   Fixes issue of running the tests in the base class. Ugh!
def test_base(base_cls):
    class BaseClassSkipper(base_cls):
        @classmethod
        def setUpClass(cls):
            if cls is BaseClassSkipper:
                raise unittest.SkipTest("Base class")
            super(BaseClassSkipper, cls).setUpClass()
    return BaseClassSkipper


@test_base
class BaseFormatTests(unittest.TestCase):
    """This class is used so the format classes can reuse the same tests."""

    inst = None
    data_dir_for_tests = None
    num_valid_files = None

    def test_instrument_model(self):
        self.assertIsNotNone(self.inst.instrument_model)

    def test_required_file_extensions(self):
        self.assertIsNotNone(self.inst.required_file_extensions)

    def test_file_type(self):
        self.assertIsNotNone(self.inst.file_type)

    def test_analysis_metadata_file_extension(self):
        self.assertIsNotNone(self.inst.analysis_metadata_file_extension)

    def test_root_dir(self):
        self.assertEqual(
            self.data_dir_for_tests,
            self.inst.root_dir
        )

    def test_software_platform(self):
        self.assertIsNotNone(self.inst.software_platform)

    def test_files(self):
        # not perfect but enough
        self.assertEqual(
            self.num_valid_files,
            len(self.inst.files)
        )

    def test_file_info_map(self):
        # not perfect but enough
        self.assertEqual(
            self.num_valid_files,
            len(self.inst.file_info_map)
        )

    def test_software_platform(self):
        self.assertIsNotNone(self.inst.analysis_metadata_file)

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
            self.inst._find_analysis_metadata_file(files, search_ext)
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
                self.inst._find_analysis_metadata_file(files, search_ext)
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
                self.inst._find_analysis_metadata_file(files, search_ext)
            )

    def test_generate_file_info_map_check_md5sum(self):
        analysis = self.inst
        file_info_map = analysis.file_info_map
        files = analysis.files

        self.assertEqual(len(files), len(file_info_map))

        for f in files:
            self.assertEqual(md5(f), file_info_map[f]['md5sum'])

    def test_get_value_from_analysis_metadata_file_with_invalid_path(self):
        with self.assertRaises(Exception):
            self.inst.get_value_from_analysis_metadata_file('does/not/exist')

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

        analysis = self.inst

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                analysis.required_files_exist(test['input']['files'], test['input']['extensions'])
            )


if __name__ == '__main__':
    unittest.main()
