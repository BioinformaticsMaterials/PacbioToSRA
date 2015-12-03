import unittest

from PacbioToSRA.ncbi.sra_submission import *
from tests import *


class TestSraSubmission(unittest.TestCase):
    """To run these tests:
    $ python -m unittest -v tests.PacbioToSRA.ncbi.test_sra_submission
    $ python -m unittest -v tests.PacbioToSRA.ncbi.test_sra_submission.TestSraSubmission
    $ python -m unittest -v tests.PacbioToSRA.ncbi.test_sra_submission.TestSraSubmission.test_ssh_key_does_not_exist
    """

    def test_ssh_key_does_not_exist(self):
        with self.assertRaises(Exception):
            SraSubmission('username', 'ssh/key/file/does/not/exist')


if __name__ == '__main__':
    unittest.main()
