from tests import *


@skip_base_class
class BaseTestForCellAnalysisTranslator(unittest.TestCase):
    """This class is used so the format classes can reuse the same tests."""

    cell_analysis = None
    inst = None

    def test_cell_analysis_format_class(self):
        self.assertIsNotNone(self.inst.cell_analysis_format_class)

    def test_translate_sample_name(self):
        self.assertIsNotNone(self.inst.translate_sample_name(self.cell_analysis))

    def test_translate_library_id(self):
        self.assertIsNotNone(self.inst.translate_library_id(self.cell_analysis))

    def test_translate_design_description(self):
        self.assertIsNotNone(self.inst.translate_design_description(self.cell_analysis))

    def test_translate_platform(self):
        self.assertIsNotNone(self.inst.translate_platform(self.cell_analysis))

    def test_translate_instrument_model(self):
        self.assertIsNotNone(self.inst.translate_instrument_model(self.cell_analysis))

    def test_translate_file_type(self):
        self.assertIsNotNone(self.inst.translate_file_type(self.cell_analysis))

    def test_translate_run_id(self):
        self.assertIsNotNone(self.inst.translate_run_id(self.cell_analysis))


if __name__ == '__main__':
    unittest.main()
