from PacbioToSRA.ncbi.abstract_cell_analysis_translator import AbstractCellAnalysisTranslator
from tests import *


class TestAbstractFormat(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_format
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_formatTest.AbstractFormat
    $ python -m unittest -v tests.PacbioToSRA.cell_analysis.test_abstract_formatTest.AbstractFormat.test__init__directory_does_not_exist

    To run all test:
    $ python -m unittest discover -v
    """

    def test_generate_run_id_from_filename(self):
        test_cases = [
            {
                'input': 'this_is_the_run_id.txt',
                'expected_result': 'this_is_the_run_id',
            },
            {
                'input': 'this_is_the_run_id.1.2.3.txt',
                'expected_result': 'this_is_the_run_id',
            },
            {
                'input': '/the/full/path/to/this/file.log',
                'expected_result': 'file',
            },

        ]

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                AbstractCellAnalysisTranslator._generate_run_id_from_filename(test['input'])
            )


if __name__ == '__main__':
    unittest.main()
