import glob
import logging
import os
import shutil
import traceback
from typing import List, Optional
from urllib.parse import urlparse

import requests

from edgar.extractors.abstract_extractor import Extractor
from edgar.pipelines.directories import DOWNLOADED_ARCHIVES_DIRECTORY, UNZIPPED_ARCHIVES_DIRECTORY

RAW_SUBMISSION_FORMATS = ['corr01', 'nc']
HTML_EXTENSION = '.htm'


class EdgarPipeline:
    """
    Downloads an SEC daily feed archive and extracts contracts
    :param contract_extractor: module which matches contracts
    :param outputs_directory: target location of extracted contracts
    :param temporary_directory: temporary location of downloaded SEC daily feed archives and raw XBRL submissions
    """

    def __init__(self, contract_extractor: Extractor, outputs_directory: str, temporary_directory: str) -> None:
        self.contract_extractor = contract_extractor()
        self.outputs_directory = outputs_directory
        self.temporary_directory = temporary_directory
        self.downloaded_archives_directory = os.path.join(self.temporary_directory, DOWNLOADED_ARCHIVES_DIRECTORY)
        self.unzipped_archives_directory = os.path.join(self.temporary_directory, UNZIPPED_ARCHIVES_DIRECTORY)

    def __call__(self, *args, **kwargs):
        return self.run_pipeline(*args, **kwargs)

    def run_pipeline(self, archive_url: str) -> int:
        """
        1. Download and unzip an SEC daily feed archive
        2. Extract contracts and save them to disk
        3. Delete the downloaded archive and all temporary files
        :param archive_url: URL of SEC daily feed archive
        :return: the number of contracts extracted
        """

        downloaded_archive_target = None
        unzipped_data_directory = None
        contracts_extracted = 0

        try:
            # Download SEC daily feed archive to the downloads directory (use the same filename as the server)
            filename_on_server = os.path.split(urlparse(archive_url).path)[-1]
            downloaded_archive_target = os.path.join(self.downloaded_archives_directory, filename_on_server)
            self._download_feed_archive(archive_url, downloaded_archive_target)

            # Unzip SEC daily feed archive
            unzipped_data_directory = self._unzip_daily_feed_archive(downloaded_archive_target)

            # Obtain the filepaths of the raw XBRL files
            data_filepaths = self._find_raw_submissions_in_data_directory(unzipped_data_directory)

            for data_filepath in data_filepaths:
                # Load the raw submission into memory
                raw_submission = self._load_raw_submission(data_filepath)

                # Extract contract
                contracts = self.contract_extractor(raw_submission)

                # Increment the counter by the number of contracts found
                contracts_extracted += len(contracts)

                # Prefix each saved contract with the filename (no extension) of the raw XBRL file from which it was
                # extracted
                saved_contract_prefix = os.path.split(data_filepath)[-1]

                # Save each contract to disk (one HTML file per contract)
                self._save_contracts(contracts, saved_contract_prefix)

            logging.debug(f'Extracted {contracts_extracted} from {archive_url}')

        # TODO: write a narrower exception clause
        # Temporarily using a broad exception clause to discover the exceptions which are raised when the connection to
        # the SEC's server fails
        except Exception as exception:
            logging.error(traceback.format_exc())
            logging.info(f'Unable to process {archive_url}')

        # Whether or not the extraction was successful, delete the SEC daily feed archive and the unzipped XBRL files
        finally:
            self._clean_up_downloaded_files(downloaded_archive_target, unzipped_data_directory)

        return contracts_extracted

    @staticmethod
    def _download_feed_archive(archive_url: str, target_filepath: str, chunk_size: Optional[int] = None) -> None:
        """
        Download an SEC daily feed archive into the downloads directory
        :param archive_url: URL of SEC daily feed archive
        :param target_filepath: target filepath of downloaded SEC daily feed archive
        :param chunk_size: number of bytes to read into memory in each chunk. If None, use the downloaded chunk sizes
        """

        # Submit a GET request to the SEC data server. Stream the data, so it does not need to be read into memory at
        # once
        response = requests.get(archive_url, stream=True)

        # Track how much has been downloaded
        downloaded_length = 0

        with open(target_filepath, 'wb') as write_file:

            # Read the downloaded data into memory in chunks
            for chunk in response.iter_content(chunk_size):

                # Stop downloading if there is a keep-alive chunk
                if (not chunk) and (downloaded_length >= int(response.headers['Content-Length'])):
                    break

                # Update the tracker
                downloaded_length += len(chunk)

                # Write the downloaded chunk to disk
                write_file.write(chunk)

    def _unzip_daily_feed_archive(self, path_to_archive: str) -> str:
        """
        Unzip an SEC daily feed archive into the data directory
        :param path_to_archive: (relative or absolute) path to SEC daily feed archive
        feed archive should be unzipped
        :return: path to unzipped data directory
        """

        # Extract the filename (no extension) from the filepath
        archive_name = os.path.split(path_to_archive)[-1].split('.')[0]

        # Determine where to unzip the archive
        unzipped_data_directory = os.path.join(self.unzipped_archives_directory, archive_name)

        # Unzip the archive
        shutil.unpack_archive(path_to_archive, unzipped_data_directory)

        return unzipped_data_directory

    @staticmethod
    def _find_raw_submissions_in_data_directory(data_directory: str) -> List[str]:
        """
        Obtain the filepaths of raw XBRL files in a specified data directory
        :param data_directory: (relative or absolute) path to data directory containing raw SEC submissions
        :return: list of filepaths to raw SEC submissions, relative if data_directory is relative
        """

        data_filepaths = []

        # Match SEC submissions for each valid submission format
        for raw_submission_format in RAW_SUBMISSION_FORMATS:
            filepath_pattern_to_match = os.path.join(data_directory, f'*.{raw_submission_format}')
            matched_filepaths = glob.glob(filepath_pattern_to_match)
            data_filepaths += matched_filepaths

        return data_filepaths

    @staticmethod
    def _load_raw_submission(path_to_raw_submission: str) -> str:
        """
        Read a raw SEC submission into memory
        :param path_to_raw_submission: filepath to raw SEC submission
        :return: raw SEC submission
        """

        with open(path_to_raw_submission, 'r') as read_file:
            raw_submission = read_file.read()

        return raw_submission

    def _save_contracts(self, contracts: List[str], prefix: str) -> None:
        """
        Save extracted contracts to disk (one HTML file per contract)
        :param contracts: contracts extracted from SEC submission
        :param prefix: filename prefix for the extracted contract (usually the identifier of the SEC submission it was
        extracted from)
        :return: list of extracted contracts
        """

        for idx, contract in enumerate(contracts):
            # Determine the filename
            output_filename = prefix + str(idx) + '-' + HTML_EXTENSION
            output_filepath = os.path.join(self.outputs_directory, output_filename)

            # Write the contract to disk
            with open(output_filepath, 'w') as write_file:
                write_file.write(contract)

    @staticmethod
    def _clean_up_downloaded_files(path_to_downloaded_archive: Optional[str] = None,
                                   path_to_unzipped_data: Optional[str] = None) -> None:
        """
        Delete the SEC daily feed data (zipped and unzipped) from which the contracts were extracted
        :param path_to_downloaded_archive: (relative or absolute) path to SEC daily feed archive
        :param path_to_unzipped_data: (relative or absolute) path to data directory containing raw SEC submissions
        """

        # Delete the SEC daily feed archive
        if path_to_downloaded_archive:
            if os.path.exists(path_to_downloaded_archive):
                os.remove(path_to_downloaded_archive)

        # Delete the unzipped data directory
        if path_to_unzipped_data:
            if os.path.isdir(path_to_unzipped_data):
                shutil.rmtree(path_to_unzipped_data)
