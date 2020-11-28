import argparse
import logging
import multiprocessing
import os
from typing import List, Union

from edgar.crawlers.edgar_crawler import edgar_crawler
from edgar.extractors.abstract_extractor import Extractor
from edgar.extractors.form_10k_extractor import Form10KExtractor
from edgar.pipelines.directories import create_output_and_temporary_directories, delete_temporary_directories
from edgar.pipelines.edgar_parallel import extract_documents_in_parallel

logging.basicConfig(level=logging.INFO)

EXTRACTORS = {'Form10K': Form10KExtractor}
OUTPUTS_DIRECTORY = 'documents'
TEMPORARY_DIRECTORY = '_tmp'


def download_and_extract_documents(year: Union[int, List[str], List[int], range],
                                   quarter: Union[int, List[str], List[int], range],
                                   document_extractor: Extractor, outputs_directory: str, num_processes: int) -> None:
    """
    Obtains, downloads and extracts documents from SEC EDGAR daily archives for each day in the year(s) and quarter(s)
    specified
    :param year: year(s) to retrieve
    :param quarter: quarter(s) to retrieve
    :param document_extractor: module which matches documents
    :param outputs_directory: (relative or absolute) path to where the extracted documents should be saved
    :param num_processes: number of parallel processes (i.e. CPUs)
    """

    # If `num_processes` is not specified, use every CPU
    num_processes = num_processes or multiprocessing.cpu_count()

    # Log parameters
    logging.info(
        f'Obtaining data for {year}, quarter {quarter} using {document_extractor.name}. Extracted documents '
        f'will be saved to "{os.path.abspath(outputs_directory)}/". Running {args.num_processes} CPUs in parallel'
    )

    # Create the output and temporary directories (clear existing directories)
    create_output_and_temporary_directories(outputs_directory, TEMPORARY_DIRECTORY)

    # Obtain the SEC EDGAR daily archive URLs for each day in the year(s) and quarter(s) specified
    daily_archive_urls = edgar_crawler(year, quarter, num_processes)

    # Downloads SEC daily archives and extracts documents (in parallel)
    extract_documents_in_parallel(
        daily_archive_urls,
        document_extractor,
        outputs_directory,
        TEMPORARY_DIRECTORY,
        num_processes
    )

    # Delete temporary directories
    delete_temporary_directories(TEMPORARY_DIRECTORY)


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Obtain, download and extract documents from SEC EDGAR daily archives')
    parser.add_argument('year', nargs='+', type=int, help='year(s) to retrieve')
    parser.add_argument('quarter', nargs='+', type=int, help='quarter(s) to retrieve')
    parser.add_argument('output', type=str,
                        help='output path to extracted documents')
    parser.add_argument('-n', '--num_processes', type=int, default=None,
                        help='number of parallel processes (i.e. CPUs)')
    parser.add_argument('-e', '--extractor', type=str, default='Form10K', choices=['Form10K'],
                        help='module which matches documents')
    args = parser.parse_args()

    # Choose an extractor
    extractor = EXTRACTORS[args.extractor]

    # Obtain, download and extract documents from SEC EDGAR daily archives
    download_and_extract_documents(
        year=args.year,
        quarter=args.quarter,
        document_extractor=extractor,
        num_processes=args.num_processes,
        outputs_directory=args.outputs_directory
    )
