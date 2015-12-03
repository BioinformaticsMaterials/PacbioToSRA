import hashlib


# http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file
def md5(fname):
    """Calculate the md5sum of a file.

    :param  fname:  Absolute path to file
    :type   fname:  string
    :return:        md5sum
    :rtype          string
    """
    hash = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
    return hash.hexdigest()