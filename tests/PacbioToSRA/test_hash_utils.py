from PacbioToSRA.hash_utils import *
from tests import *


class TestHashUtils(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.test_hash_utils
    $ python -m unittest -v tests.PacbioToSRA.test_hash_utils.TestHashUtils
    $ python -m unittest -v tests.PacbioToSRA.test_hash_utils.TestHashUtils.test_md5

    To run all test:
    $ python -m unittest discover -v
    """

    def test_md5(self):
        self.assertEqual(
            '8300a100d55f896080e0c4f18895414e',     # calculated on the command line
            md5(MD5SUM_TEST_FILE)
        )

