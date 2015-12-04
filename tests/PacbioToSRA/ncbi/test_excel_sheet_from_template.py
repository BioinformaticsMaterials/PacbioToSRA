import unittest

from PacbioToSRA.ncbi.excel_sheet_from_template import *
from tests import *


class TestExcelSheetFromTemplate(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.ncbi.test_excel_sheet_from_template
    $ python -m unittest -v tests.PacbioToSRA.ncbi.test_excel_sheet_from_template.TestExcelSheetFromTemplate
    $ python -m unittest -v tests.PacbioToSRA.ncbi.test_excel_sheet_from_template.TestExcelSheetFromTemplate.test_that_excel_file_already_exists

    To run all test:
    $ python -m unittest discover -v
    """

    def test_that_excel_file_already_exists(self):
        with self.assertRaises(Exception):
            ExcelSheetFromTemplate(__file__)


if __name__ == '__main__':
    unittest.main()
