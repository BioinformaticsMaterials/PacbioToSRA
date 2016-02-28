import os

from PacbioToSRA.cell_analysis.abstract_format import AbstractFormat, InvalidDirectoryException
from tests import *


class ChildOfAbstractFormat(AbstractFormat):

    @property
    def instrument_model(self):
        return 'instrument_model'

    @property
    def required_file_extensions(self):
        return set(['required_file_extensions'])

    @property
    def file_type(self):
        return 'file_type'

    @property
    def analysis_metadata_file_extension(self):
        return 'analysis_metadata_file_extension'


class TestAbstractFormat(unittest.TestCase):

    def test__init__directory_does_not_exist(self):
        with self.assertRaises(OSError):
            ChildOfAbstractFormat('path/does/not/exist')

    def test__init__directory_is_not_valid(self):
        with self.assertRaises(InvalidDirectoryException):
            ChildOfAbstractFormat(os.path.dirname(os.path.realpath(__file__)))

    def test_file_has_extension(self):
        test_cases = [
            {
                'input': {
                    'file': 'file.txt',
                    'extension': 'txt',
                },
                'expected_result': True,
            },
            {
                'input': {
                    'file': '/path/to/file/input.fofn',
                    'extension': 'fofn',
                },
                'expected_result': True,
            },
            {
                'input': {
                    'file': '/path/with.a.period/file.log',
                    'extension': 'log',
                },
                'expected_result': True,
            },
            {
                'input': {
                    'file': 'file.with.many..periods.csv',
                    'extension': 'csv',
                },
                'expected_result': True,
            },
            {
                'input': {
                    'file': 'sample.run.metadata.xml',
                    'extension': 'metadata.xml',
                },
                'expected_result': True,
            },
            {
                'input': {
                    'file': 'file.txt',
                    'extension': 'csv',
                },
                'expected_result': False,
            },
            {
                'input': {
                    'file': '/csv/csv/csv/file.log',
                    'extension': 'csv',
                },
                'expected_result': False,
            },
            {
                'input': {
                    'file': 'csv.csv.csv.txt',
                    'extension': 'csv',
                },
                'expected_result': False,
            },
        ]

        for t in test_cases:
            self.assertEqual(
                t['expected_result'],
                AbstractFormat.file_has_extension(t['input']['file'], t['input']['extension'])
            )


if __name__ == '__main__':
    unittest.main()
