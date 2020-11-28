import argparse
import logging
import multiprocessing
import os
import shutil
import tempfile
from glob import glob
from typing import Optional

from tqdm import tqdm

from edgar.parsers.form_10k_parser import Form10KParser
from edgar.pipelines.edgar_pipeline import HTML_EXTENSION

logging.basicConfig(level=logging.INFO)


def parse_documents(html_documents: str, parsed_documents: str, num_processes: Optional[int] = None) -> None:
    """
    Parses a directory of Form 10-K documents - one document per line
    :param html_documents: input directory containing HTML Form 10-K documents
    :param parsed_documents: output path for parsed documents
    :param num_processes: num_processes: number of parallel processes (i.e. CPUs)
    """

    # If `num_processes` is not specified, use every CPU
    num_processes = num_processes or multiprocessing.cpu_count()

    # Obtain the filepaths for the extracted documents
    document_filepaths = glob(f'{html_documents}/*{HTML_EXTENSION}')

    # Load the extracted documents into memory
    extracted_documents = []
    for filepath in document_filepaths:
        with open(filepath, 'r') as document:
            extracted_document = document.read()
        extracted_documents.append(extracted_document)

    # Log parameters
    logging.info(
        f'Parsing {len(extracted_documents)} documents from {os.path.abspath(html_documents)}/ using '
        f'{num_processes} CPUs in parallel'
    )

    # Initialise a Form 10-K parser
    parser = Form10KParser()

    # Set up the multiprocessing pool
    multiprocessing_pool = multiprocessing.Pool(num_processes)

    # Set up an iterator to run the pipelines in parallel
    pipeline_iterator = multiprocessing_pool.imap(parser, extracted_documents)
    pipeline_iterator = tqdm(pipeline_iterator, desc='Parser', total=len(extracted_documents))

    # Create a temporary file to write the parsed documents
    file_descriptor, temporary_file_path = tempfile.mkstemp(suffix='txt')

    # Parse the documents (in parallel) and write them to a temporary file (one document per line). When this is done,
    # move the temporary file to its permanent location: `{base_path}-{document_hash}.txt`
    try:
        documents_parsed = 0
        with open(temporary_file_path, 'w') as temporary_file:
            for parsed_document in pipeline_iterator:
                temporary_file.write(parsed_document + '\n')
                documents_parsed += 1
        shutil.move(temporary_file_path, parsed_documents)

    # Ensure that the temporary file is deleted
    finally:
        if os.path.isfile(temporary_file_path):
            os.remove(temporary_file_path)

    # Close the multiprocessing pool
    multiprocessing_pool.close()
    multiprocessing_pool.join()

    # Log results
    logging.info(
        f'Parsed {documents_parsed} documents, outputs saved to "{parsed_documents}"'
    )


if __name__ == '__main__':
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Parse extracted SEC documents')
    parser.add_argument('input', type=str,
                        help='input directory containing Form 10-K documents')
    parser.add_argument('output', type=str,
                        help='output path for parsed documents')
    parser.add_argument('-n', '--num_processes', type=int, default=None,
                        help='number of parallel processes (i.e. CPUs)')
    args = parser.parse_args()

    # Parse the extracted SEC documents in parallel
    parse_documents(
        html_documents=args.input,
        parsed_documents=args.output,
        num_processes=args.num_processes,
    )
