import logging
import os
import platform
import sys
import time


logger = logging.getLogger(__name__)


class SraSubmission(object):
    NCBI_SUBMISSION_SERVER = 'upload.ncbi.nlm.nih.gov'
    NCBI_DEFAULT_DEST_FOLDER_NAME = 'incoming'
    ASCP_CMD_ROOT_PATH = os.path.join(
            os.path.dirname(os.path.dirname(os.path.realpath(__file__))),
            'aspera',
            'aspera-redist-3.5.2',
            'bin'
    )

    def __init__(self, username, ssh_key_file, dest_path=NCBI_DEFAULT_DEST_FOLDER_NAME):
        self.username = username

        if not os.path.exists(ssh_key_file):
            raise Exception("File for ssh key does not exists!")
        self.ssh_key_file = os.path.abspath(ssh_key_file)           # Aspera's ascp command requires an absolute path

        self.dest_path = dest_path

        self.ascp_cmd = self._get_ascp_cmd()

    @classmethod
    def _get_ascp_cmd(cls):
        """Locates the Aspera ascp command.

        :return:    Location of the ascp command
        :rtype      string
        """
        p = sys.platform.lower()

        if p.startswith('linux'):
            return cls._get_ascp_cmd_for_linux()
        elif p.startswith('darwin'):
            return cls._get_ascp_cmd_for_mac()
        else:
            return None

    @classmethod
    def _get_ascp_cmd_for_linux(cls):
        # http://stackoverflow.com/questions/9964396/python-check-if-a-system-is-32-or-64-bit-to-determine-whether-to-run-the-funct
        return os.path.join(
            cls.ASCP_CMD_ROOT_PATH,
            'linux-64' if (sys.maxsize > 2**32) else 'linux-32',
            'ascp'
        )

    @classmethod
    def _get_ascp_cmd_for_mac(cls):
        mac_ver, _, __ = platform.mac_ver()
        return os.path.join(
            cls.ASCP_CMD_ROOT_PATH,
            'mac-intel-10.6' if mac_ver.startswith('10.6') else 'mac-intel-10.7',
            'ascp'
        )

    def ascp_cmd_exist(self):
        """Checks if the ascp command exists.
        """
        return True if os.path.isfile(os.path.join(self.ascp_cmd)) else False

    @classmethod
    def calc_sum(cls, files):
        s = 0

        for f in files:
            s += os.path.getsize(f)

        return s

    def submit_files(self, files):
        """Submits a list of files to NCBI.

        :param      files:  List of files to send.
        :type       files:  list
        """
        # import here because Aspera's module does undesirable things if you import it too soon (import at top of file)
        from PacbioToSRA.aspera.FaspManagerPython import pyfaspmgmt

        session = pyfaspmgmt.FaspSend(
            ascpPath=self.ascp_cmd,
            user=self.username,
            dest_host=self.NCBI_SUBMISSION_SERVER,
            src_files=files,
            key_file=self.ssh_key_file,
            dest_dir=self.dest_path,
            args=[              # TODO: make these configurable
                '-QT',
                '-l200m',       # TODO: why limit max transfer rate
                '-k1',
            ]
        )

        session.totalBytes = self.calc_sum(files)

        while session.status() not in ("DONE", "ERROR"):
            time.sleep(.5)
            sys.stdout.write("\r%02d%% Complete" % session.pctComplete())
            sys.stdout.flush()

        print ""

        if session.status() == "DONE":
            logging.info("File Transfer Successful")
        else:
            logging.error("Transfer Failed! Message: {}".format(session.errs))

        # Ugh! Aspera's module creates log files and config files. Let's delete them
        rm_files = ['faspmgmt.conf', 'faspmgmt.log']
        for f in rm_files:
            if os.path.isfile(f):
                os.remove(f)
