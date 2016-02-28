from PacbioToSRA.ncbi.abstract_cell_analysis_translator import AbstractCellAnalysisTranslator
from tests import *


class TestAbstractFormat(unittest.TestCase):

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
