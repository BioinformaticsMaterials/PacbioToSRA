import logging
import os
import subprocess
import sys
import time

from PacbioToSRA.FaspManagerPython import pyfaspmgmt


logger = logging.getLogger(__name__)


class SraSubmission(object):
    NCBI_SUBMISSION_SERVER = 'upload.ncbi.nlm.nih.gov'
    NCBI_DEFAULT_DEST_FOLDER_NAME = 'incoming'

    def __init__(self, username, ssh_key_file, dest_path=NCBI_DEFAULT_DEST_FOLDER_NAME):
        self.username = username

        if not os.path.exists(ssh_key_file):
            raise Exception("File for ssh key does not exists!")
        self.ssh_key_file = os.path.abspath(ssh_key_file)           # Aspera's ascp command requires an absolute path

        self.dest_path = dest_path

        self.ascp_cmd = self._get_ascp_cmd()

    def _get_ascp_cmd(self):
        """Locates the Aspera ascp command.

        :return:    Location of the ascp command
        :rtype      string
        """
        try:
            return subprocess.check_output(['which', 'ascp']).strip()
        except:
            return None

    def ascp_cmd_exist(self):
        """Checks if the ascp command exists.
        """
        return True if self.ascp_cmd else False

    def submit_files(self, files):
        """Submits a list of files to NCBI.

        :param      files:  List of files to send.
        :type       files:  list
        """
        session = pyfaspmgmt.FaspSend(
            user=self.username,
            remote_host=self.NCBI_SUBMISSION_SERVER,
            src_files=files,
            key_file=self.ssh_key_file,
            dest_dir=self.dest_path,
            args=[              # TODO: make these configurable
                '-QT',
                '-l200m',       # TODO: why limit max transfer rate
                '-k1'
            ]
        )

        while session.status() not in ("DONE", "ERROR"):
            time.sleep(.5)
            sys.stdout.write("\r%02d%% Complete" % session.pctComplete())
            sys.stdout.flush()

        print ""

        if session.status() == "DONE":
            logging.info("File Transfer Successful")
        else:
            logging.error("Transfer Failed! Message: {}".format(session.errs))

