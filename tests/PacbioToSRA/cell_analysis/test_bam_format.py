from PacbioToSRA.cell_analysis.bam_format import BamFormat
from tests import *
from tests.PacbioToSRA.cell_analysis.base_format_tests import BaseFormatTests


class TestBamFormat(BaseFormatTests):

    data_dir_for_tests = SINGLE_BAM_CELL_ANALYSIS_TEST_DATA_PATH
    inst = BamFormat(data_dir_for_tests)
    num_valid_files = 2

    def test_get_value_from_analysis_metadata_file(self):
        test_cases = [
            {
                'input': {
                    'path': 'pbmeta:CollectionMetadata/pbmeta:WellSample',
                    'attribute': 'Name',
                },
                'expected_result': 'CollectionMetadata_WellSample_Name_11111',
            },
            {
                'input': {
                    'path': 'pbmeta:CollectionMetadata/pbmeta:Primary/pbmeta:ConfigFileName',
                    'attribute': None,
                },
                'expected_result': 'CollectionMetadata_Primary_ConfigFileName_11111.xml',
            },
        ]

        analysis = self.inst

        for test in test_cases:
            self.assertEqual(
                test['expected_result'],
                analysis.get_value_from_analysis_metadata_file(test['input']['path'], test['input']['attribute'])
            )


if __name__ == '__main__':
    unittest.main()
