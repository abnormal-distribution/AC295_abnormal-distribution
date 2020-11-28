import re
from typing import List

from edgar.extractors.abstract_extractor import Extractor

# Document match constants
CHARACTER_SEARCH_LIMIT = 10000
FORM_10K = 'FORM 10-K'


class Form10KExtractor(Extractor):
    """Extract Form 10-K documents from a raw eXtensible Business Reporting Language submission"""

    name = 'Form 10-K Extractor'

    def extract(self, raw_submission: str) -> List[str]:
        """
        Extract Form 10-K documents from a raw eXtensible Business Reporting Language submission
        :param raw_submission: raw XBRL submission
        :return: list of extracted documents
        """

        # Extract HTML documents from the submission
        html_documents = self._extract_html_documents(raw_submission)

        # Match Form 10-K documents
        documents = self._match_form_10k_documents(html_documents)

        return documents

    @staticmethod
    def _extract_html_documents(raw_submission: str) -> List[str]:
        """
        Extract HTML documents embedded in an XBRL submission
        :param raw_submission: raw XBRL submission
        :return: HTML documents embedded within the XBRL submission (i.e. content between <html> tags)
        """

        # Match all content between <html> and </html> tags
        regex_html = re.compile('<html>(.*?)</html>', re.DOTALL)

        return regex_html.findall(raw_submission)

    @staticmethod
    def _match_form_10k_documents(html_documents: List[str]) -> List[str]:
        """
        Match Form 10-K documents
        :param html_documents: HTML documents
        :return: matched Form 10-K documents
        """

        documents = []

        # Match documents which contain the phrase 'Form 10K'
        for idx, document in enumerate(html_documents):
            if FORM_10K in document[0: CHARACTER_SEARCH_LIMIT]:
                documents.append(document)

        return documents
