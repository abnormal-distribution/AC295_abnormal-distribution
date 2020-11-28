from unittest import TestCase

from hypothesis import given
from hypothesis.strategies import text
from mock import patch

from edgar.extractors.form_10k_extractor import Form10KExtractor, FORM_10K


class TestForm10KExtractor(TestCase):

    def setUp(self):
        """Instantiate a Form 10-K extractor"""

        self.extractor = Form10KExtractor()

    @given(submission=text())
    def test_extractor_does_not_match_non_html(self, submission):
        """Test that non-HTML text is not matched"""

        contracts = self.extractor(submission)
        self.assertListEqual(contracts, [])

    @given(generated_text=text())
    def test_extractor_does_not_match_unsigned_documents(self, generated_text):
        """Test that unsigned HTML documents are not matched"""

        submission = f'<html>{generated_text}</html>'
        contracts = self.extractor(submission)
        self.assertListEqual(contracts, [])

    @given(generated_text=text())
    def test_extractor_does_not_match_non_form_10k_documents(self, generated_text):
        """Test that signed HTML documents which do not contain the Form 10-K identifier are not matched"""

        submission = f'<html>{generated_text}</html>'
        contracts = self.extractor(submission)
        self.assertListEqual(contracts, [])

    @patch('edgar.extractors.form_10k_extractor.CHARACTER_SEARCH_LIMIT', 10)
    @given(generated_text=text(min_size=10))
    def test_extractor_does_not_match_documents_if_the_form_10_k_identifier_is_not_near_the_top(self, generated_text):
        """
        Test that signed HTML documents where the Form 10-K identifier is not near the top are not matched. This is
        because these documents are usually not contracts, but directors reports, accounting statements, etc. which
        refer to Form 10-K documents elsewhere in the submission
        """

        # To make testing easier, CHARACTER_SEARCH_LIMIT - the maximum distance between the start of the document and
        # the end of the Form 10-K 10 identifier - is reduced to 10

        submission = f'<html>{generated_text} {FORM_10K}</html>'
        contracts = self.extractor(submission)
        self.assertListEqual(contracts, [])
