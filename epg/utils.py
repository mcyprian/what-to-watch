import csv
import gzip
import os
import shutil
import logging
import tempfile
import zipfile
from urllib.request import urlretrieve
from urllib.parse import urljoin
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


class IMDBFetcher(object):

    def __init__(self):
        self.base_url = "https://datasets.imdbws.com/"
        self.tempdir = tempfile.mkdtemp()
        self.titles = {}
        self.ratings = {}
        self.titles_tar = self.get_archive("title.akas.tsv.gz")
        self.ratings_tar = self.get_archive("title.ratings.tsv.gz")

    def __enter__(self):
        self.fetch_data()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        shutil.rmtree(self.tempdir)

    def get_archive(self, tsv_name):
        file_path = os.path.join(self.tempdir, tsv_name)
        urlretrieve(urljoin(self.base_url, tsv_name), file_path)
        return file_path

    def fetch_data(self):
        with gzip.open(self.titles_tar, 'rt') as csvfile:
            spamreader = csv.reader(
                csvfile, delimiter='\t', quotechar='|')
            for row in spamreader:
                self.titles[row[2]] = row[0]

        with gzip.open(self.ratings_tar, 'rt') as csvfile:
            spamreader = csv.reader(
                csvfile, delimiter='\t', quotechar='|')
            for row in spamreader:
                self.ratings[row[0]] = row[1]

    def get_rating(self, original_name):
        try:
            return self.ratings[self.titles[original_name]]
        except KeyError:
            return None
