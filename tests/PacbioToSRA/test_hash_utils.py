from PacbioToSRA.hash_utils import *
from tests import *


class TestHashUtils(unittest.TestCase):

    def test_md5(self):
        self.assertEqual(
            '8300a100d55f896080e0c4f18895414e',     # calculated on the command line
            md5(MD5SUM_TEST_FILE)
        )

