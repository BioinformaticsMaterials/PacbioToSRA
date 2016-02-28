from PacbioToSRA.ncbi.excel_sheet_from_template import *
from tests import *


class TestExcelSheetFromTemplate(unittest.TestCase):

    def test_that_excel_file_already_exists(self):
        with self.assertRaises(Exception):
            ExcelSheetFromTemplate(__file__)


if __name__ == '__main__':
    unittest.main()
