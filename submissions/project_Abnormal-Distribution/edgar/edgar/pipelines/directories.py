import os
import shutil

DOWNLOADED_ARCHIVES_DIRECTORY = 'downloaded_archives'
UNZIPPED_ARCHIVES_DIRECTORY = 'unzipped_archives'


def create_output_and_temporary_directories(output_directory: str, temporary_directory: str) -> None:
    """
    Create the output and temporary directories (clear existing directories)
    :param output_directory: (relative or absolute) path to where the extracted contracts should be saved
    :param temporary_directory: (relative or absolute) path to where the SEC daily feed archives are downloaded and
    unzipped
    """

    # If the output directory already exists, clear it
    if os.path.isdir(output_directory):
        shutil.rmtree(output_directory)

    # If the temporary directory already exists, clear it
    if os.path.isdir(temporary_directory):
        shutil.rmtree(temporary_directory)

    # Create the output directory
    os.mkdir(output_directory)

    # Create the temporary directory and its sub-directories
    os.mkdir(temporary_directory)
    os.mkdir(os.path.join(temporary_directory, DOWNLOADED_ARCHIVES_DIRECTORY))
    os.mkdir(os.path.join(temporary_directory, UNZIPPED_ARCHIVES_DIRECTORY))


def delete_temporary_directories(temporary_directory: str) -> None:
    """
    Delete temporary directories used by the pipelines
    :param temporary_directory: (relative or absolute) path to where the SEC daily archives are downloaded and unzipped
    """

    # If the temporary directory already exists, clear it
    if os.path.isdir(temporary_directory):
        shutil.rmtree(temporary_directory)
