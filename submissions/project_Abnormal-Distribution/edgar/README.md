# EDGAR

Obtain, download, extract and parse documents from the Security and Exchange Commission's EDGAR daily archives (https://www.sec.gov/Archives/edgar/Feed/).

## Installation

1. Set up a virtual environment

    ```virtualenv -p `which python3.8` venv```

    (To install the `virtualenvironment` package, run `python3 -m pip install --user virtualenv`)

2. Add the project root to `PYTHONPATH`

    Open `venv/bin/activate` and append

    ```export PYTHONPATH="${PYTHONPATH}:/path/to/project/root"```

3. Activate the virtual environment

    ```source venv/bin/activate```

4. Install module dependencies

    ```pip install -r requirements.txt```
    
## Usage

### Downloading and extracting documents

```python download.py year quarter output [--num_processes]```

Arguments:
* `year` year(s) to download. Data are available from 1995 to 2019

* `quarter` quarter(s) to download

* `output` output directory for extracted documents

* [Optional:] `--num_processes` or `-n` number of CPUs to run in parallel (default is every CPU)

Because the daily archives are large, each archive is deleted as soon as its documents have been extracted and saved to disk.

### Parsing documents

```python parse.py input output [--num_processes] [--parse_html_tags] [--html_tags_to_ignore]```

Arguments:
* `input` input directory containing Form 10-K documents

* `output` output path for parsed documents

* [Optional:] `--num_processes` or `-n` number of CPUs to run in parallel (default is every CPU)
