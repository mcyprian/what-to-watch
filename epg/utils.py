import os
import logging
import tempfile
import zipfile
from urllib.request import urlretrieve
from xml.parsers.expat import ExpatError

import xmltodict

logger = logging.getLogger(__name__)


def parse_xml(filename):
    with open(filename, 'r') as fi:
        return xmltodict.parse(fi.read())


def unpack_archive(archive_url):
    data_dicts = []

    try:
        zip_filename, _ = urlretrieve(archive_url)
    except ValueError:
        logger.warning("Failed to fetch data from URL {0}".format(archive_url))
        return {}
    with tempfile.TemporaryDirectory() as tmpdir:
        try:
            with zipfile.ZipFile(zip_filename, 'r') as archive:
                archive.extractall(path=tmpdir)
                for filename in os.listdir(tmpdir):
                    try:
                        data_dicts.append(
                            parse_xml(os.path.join(tmpdir, filename))
                        )
                    except ExpatError:
                        logger.warning("Invalid XML data in file {0}.".format(
                            filename))
                        continue
                return data_dicts
        except zipfile.BadZipFile:
            logger.warning("Failed to open zip file from location {0}".format(
                archive_url))
            return {}
