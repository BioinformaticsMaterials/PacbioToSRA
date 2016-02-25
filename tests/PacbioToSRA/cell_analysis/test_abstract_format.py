import os
import unittest

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
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_format
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_formatTest.AbstractFormat
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_formatTest.AbstractFormat.test__init__directory_does_not_exist

    To run all test:
    $ python -m unittest discover -v
    """

    def test__init__directory_does_not_exist(self):
        with self.assertRaises(OSError):
            ChildOfAbstractFormat('path/does/not/exist')

    def test__init__directory_is_not_valid(self):
        with self.assertRaises(InvalidDirectoryException):
            ChildOfAbstractFormat(os.path.dirname(os.path.realpath(__file__)))

    def test_extract_file_extension(self):
        test_cases = [
            {
                'input': 'test.csv',
                'expected_result': 'csv',
            },
            {
                'input': 'this.has.multiple.periods.txt',
                'expected_result': 'has.multiple.periods.txt',
            },
            {
                'input': '/full/path/to/file.doc',
                'expected_result': 'doc',
            },
        ]

        for t in test_cases:
            self.assertEqual(
                t['expected_result'],
                AbstractFormat.extract_file_extension(t['input'])
            )

    def test_extract_file_extension_with_no_extension(self):
        with self.assertRaises(Exception):
            AbstractFormat.extract_file_extension('this_has_no_extension')


if __name__ == '__main__':
    unittest.main()
