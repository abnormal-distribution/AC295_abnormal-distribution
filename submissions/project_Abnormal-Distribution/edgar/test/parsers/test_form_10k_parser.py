from unittest import TestCase

from edgar.parsers.form_10k_parser import Form10KParser

UNPARSED_DOCUMENT = """
<html>
  [head data that should not be parsed]
  <body>
    <div class='title'>Form 10-K</div>
    <br>
    <hr>
    <div>Content</div>
    <div>1</div>
    <hr>
    <div>More Content</div>
    <div>2</div>
  </body>
</html>
"""


class TestForm10KParser(TestCase):

    def test_form_10_k_parser(self):
        """Test the Form 10-K parser correctly parses documents"""

        # Initialise the Form 10-K parser
        parser = Form10KParser()

        # Parse the document
        parsed_document = parser(UNPARSED_DOCUMENT)

        # Compare the parsed document with the expected output
        expected_document = [
            {'page_num': None, 'page': 'Form 10-K'},
            {'page_num': 1, 'page': 'Content 1'},
            {'page_num': 2, 'page': 'More Content 2'},
        ]
        for expected, actual in zip(parsed_document, expected_document):
            self.assertDictEqual(expected, actual)
