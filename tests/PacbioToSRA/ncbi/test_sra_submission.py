from PacbioToSRA.ncbi.sra_submission import *
from tests import *


class TestSraSubmission(unittest.TestCase):

    def test_ssh_key_does_not_exist(self):
        with self.assertRaises(Exception):
            SraSubmission('username', 'ssh/key/file/does/not/exist')


if __name__ == '__main__':
    unittest.main()
