import logging
import os
import subprocess


logger = logging.getLogger(__name__)


class SraSubmission(object):
    NCBI_SUBMISSION_SERVER = 'upload.ncbi.nlm.nih.gov'
    NCBI_DEFAULT_DEST_FOLDER_NAME = 'incoming'

    def __init__(self, username, ssh_key_file, dest_path=NCBI_DEFAULT_DEST_FOLDER_NAME):
        self.username = username

        if not os.path.exists(ssh_key_file):
            raise Exception("File for ssh key does not exists!")
        self.ssh_key_file = ssh_key_file

        self.dest_path = dest_path

        self.ascp_cmd = self._get_ascp_cmd()

    def _get_ascp_cmd(self):
        """Locates the Aspera ascp command.

        :return:    Location of the ascp command
        :rtype      string
        """
        try:
            return subprocess.check_output(['which', 'ascp']).strip()
        except Exception as e:
            logger.error("Could not find Aspera's ascp command!")
            raise

    def submit_files(self, files):
        """Submits a list of files to NCBI.

        :param      files:  List of files to send.
        :type       files:  list
        """
        for f in files:
            self.submit_file(f)

    def submit_file(self, f):
        """Submits an individual file to NCBI.

        :param      f:  File to send
        :type       f:  string
        """
        try:
            pass    # TODO: Remove this and uncomment lines below

            # Example bash command: /path/to/aspera/ascp -i /path/to/ssh_key -QT -l200m -k1 /path/to/file ncbi_username@upload.ncbi.nlm.nih.gov:/path/to/destination/folder
            # TODO: Make this more configurable
            # subprocess.call([
            #     self.ascp_cmd,
            #     '-i', self.ssh_key_file,
            #     '-QT',
            #     '-l200m',           # TODO: why limit  max transfer rate
            #     '-k1',
            #     f,
            #     "{}@{}:{}".format(self.username, self.NCBI_SUBMISSION_SERVER, self.dest_path)
            # ])
        except Exception as e:
            logger.error("Submitting file failed: {}".format(f))
            raise


if __name__ == '__main__':
    files = ['a', 'b']
    username = 't'
    ssh = '../../../ssh/aspera.pacbio.openssh.open_permissions'

    o = SraSubmission(username, ssh)
    o.submit_files(files)

