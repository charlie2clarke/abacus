import os
from dataclasses import dataclass
from typing import List

import docx

from abacus.__main__ import process_doc
from abacus.config import Cfg
from tests.util import word_count


@dataclass
class TestCase:
    name: str
    input: str


def test_e2e() -> None:
    TEST_DATA = os.path.join("tests", "data")
    TEST_CFG = os.path.join(TEST_DATA, "test-config.ini")
    # Each test docx file contains only the relevant attribute which will be stripped meaning the
    # resulting word count should be 0.
    tests: List[TestCase] = [
        TestCase(name="strips headings", input="headings.docx"),
        TestCase(name="strips titles", input="titles.docx"),
        TestCase(name="strips subtitles", input="subtitles.docx"),
        TestCase(name="strips captions", input="captions.docx"),
        TestCase(name="strips ignored sections", input="ignored_sections.docx"),
        TestCase(name="strips bibliography", input="bibliography.docx"),
    ]

    for test in tests:
        input = os.path.join(TEST_DATA, test.input)
        try:
            Cfg(TEST_CFG)
            doc = docx.Document(input)
        except Exception as e:
            raise Exception(f"Couldn't setup '{test.name}' test: {e}")

        assert doc is not None

        doc = process_doc(doc)

        assert word_count(doc) == 0
