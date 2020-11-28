import logging
import multiprocessing
import os
from typing import List, Optional

from tqdm import tqdm

from edgar.extractors.abstract_extractor import Extractor
from edgar.pipelines.edgar_pipeline import EdgarPipeline

logging.basicConfig(level=logging.INFO)


def extract_documents_in_parallel(archive_urls: List[str], document_extractor: Extractor, outputs_directory: str,
                                  temporary_directory: str, num_processes: Optional[int] = None) -> None:
    """
    Downloads SEC daily archives and extracts documents (in parallel)
    :param archive_urls: list of URLs of SEC daily feed archives
    :param document_extractor: module which matches documents
    :param outputs_directory: target location of extracted documents
    :param temporary_directory: temporary location of downloaded SEC daily feed archives and raw XBRL submissions
    :param num_processes: number of parallel pipelines (i.e. CPUs) to run at once
    """

    # If `num_processes` isn't set, use every CPU
    num_processes = num_processes or multiprocessing.cpu_count()

    pipeline = EdgarPipeline(document_extractor, outputs_directory, temporary_directory)

    # Set up the multiprocessing pool
    multiprocessing_pool = multiprocessing.Pool(num_processes)

    # Set up an iterator to execute one pipeline per archive
    pipeline_iterator = multiprocessing_pool.imap(pipeline, archive_urls)
    pipeline_iterator = tqdm(pipeline_iterator, total=len(archive_urls))

    documents_extracted = 0

    for pipeline in pipeline_iterator:
        documents_extracted += pipeline
        pipeline_iterator.set_description(f'Extracted {documents_extracted} documents')

    # Close the multiprocessing pool
    multiprocessing_pool.close()

    # Log results
    logging.info(
        f'Extracted {documents_extracted} documents to "{os.path.abspath(outputs_directory)}/"'
    )
