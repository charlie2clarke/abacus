import datetime
import logging
import os
from shutil import copyfile
from tempfile import gettempdir
from typing import Iterator, Tuple, Union

import click
import docx
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import Table, _Cell
from docx.text.paragraph import Paragraph

from abacus.checks import is_caption, is_heading, is_subtitle, is_title
from abacus.config import DEFAULT_CFG_PATH, Cfg, InvalidIgnoredSections


class InputNotFoundException(Exception):
    def __init__(self, input: str) -> None:
        self.input = input
        super().__init__(f"File {self.input} not found")


class InvalidInput(ValueError):
    pass


class FileCopyException(Exception):
    pass


class DocLoadException(Exception):
    def __init__(self) -> None:
        super().__init__(
            "Couldn't load the document, this could be due to a permissions error"
        )


class InvalidDocObject(ValueError):
    def __init__(
        self,
        element: Document,
    ) -> None:
        self.element = element
        super().__init__(f"Invalid object in document: {self.element}")


def parse_input(input: str) -> Tuple[str, str]:
    if os.path.splitext(input)[-1] != ".docx":
        raise InvalidInput(f"{input} is not a .docx file")
    return os.path.dirname(input), os.path.basename(input)


def copy_doc(input: str) -> str:
    if not os.path.isfile(input):
        raise InputNotFoundException(input)
    filename = os.path.join(gettempdir(), os.path.basename(input))
    try:
        copyfile(input, filename)
        return filename
    except Exception as e:
        raise FileCopyException(f"An error occurred whilst copying the input file: {e}")


def load_doc(filepath: str) -> Document:
    try:
        doc = docx.Document(filepath)
    except:
        raise
    if doc is None:
        raise Exception(f"Document is null at path: {filepath}")
    return doc


def rm_tmp_doc(filepath: str) -> None:
    try:
        os.remove(filepath)
    except:
        logging.error(f"Error removing temp {filepath} file during cleanup")


def iter_block_items(parent: Document) -> Iterator[Union[Table, Paragraph]]:
    """
    Yield each paragraph and table child within *parent*, in document
    order. Each returned value is an instance of either Table or
    Paragraph. *parent* would most commonly be a reference to a main
    Document object, but also works for a _Cell object, which itself can
    contain paragraphs and tables.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise InvalidDocObject(parent)

    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def should_clear_body_elem(para: Paragraph) -> bool:
    checks = {
        "headings": is_heading,
        "titles": is_title,
        "subtitles": is_subtitle,
        "captions": is_caption,
    }

    for opt, cfg in Cfg().opts.items():
        if opt in ("bibliography", "ignored_sections"):
            continue

        if opt not in checks:
            raise Exception(f"{opt} is not an implemented check")
        if cfg.value:
            is_prop = checks[opt](para)
            if is_prop:
                return True
    return False


def should_clear_other() -> bool:
    return Cfg().opts["bibliography"].value


def should_clear_nested() -> bool:
    return Cfg().opts["bibliography"].value


def heading_lvl(para: Paragraph) -> int:
    return int(para.style.name.lstrip("Heading "))


def is_ignore_end(para: Paragraph, lvl: int) -> bool:
    return is_heading(para) and heading_lvl(para) == lvl


def is_ignore_sect(para: Paragraph) -> bool:
    ignored_sects = Cfg().opts["ignored_sections"]
    if not ignored_sects:
        return False
    return is_heading(para) and para.text.lower() in [
        sect.lower() for sect in ignored_sects.value
    ]


def rm_element(elem: CT_P) -> None:
    elem.getparent().remove(elem)
    elem._p = elem._element = None


# Might need renaming depending on how things like citations and things are handled
def rm_nested(elem: CT_P) -> None:
    sdts = elem.xpath("w:sdt")
    if sdts:
        for sdt in sdts:
            sdt.getparent().remove(sdt)


# Could just re-use above, but shall see how citations, etc. are handled
def rm_other(doc: Document) -> None:
    body = doc._body._element
    sdts = body.xpath("w:sdt")
    if sdts:
        for sdt in sdts:
            sdt.getparent().remove(sdt)


def process_doc(doc: Document) -> Document:
    ignored_sect, ignored_sect_lvl = None, None
    try:
        for block_item in iter_block_items(doc):
            if isinstance(block_item, Paragraph):
                if block_item.text == "":
                    continue

                if is_ignore_end(block_item, ignored_sect_lvl):
                    ignored_sect, ignored_sect_lvl = None, None
                if is_ignore_sect(block_item):
                    ignored_sect = block_item.text.lower()
                    ignored_sect_lvl = heading_lvl(block_item)

                if ignored_sect:
                    rm_element(block_item._element)
                elif should_clear_body_elem(block_item):
                    rm_element(block_item._element)
                elif should_clear_nested():
                    rm_nested(block_item._element)
            elif isinstance(block_item, Table):
                pass
        if should_clear_other():
            rm_other(doc)
    except InvalidDocObject:
        raise

    return doc


def filename(basename: str, overwrite: bool) -> str:
    return (
        f"ABACUS_{datetime.now().strftime('%d-%m-%Y_%H%M%S')}_{basename}"
        if not overwrite
        else f"ABACUS_{basename}"
    )


@click.command()
@click.option(
    "--input", "-i", help="The file path to the document", required=True, type=str
)
@click.option(
    "--config",
    "-c",
    help="The config file to be read which details the abbacus' exclusion rules",
    default=DEFAULT_CFG_PATH,
    type=str,
)
@click.option(
    "--overwrite",
    "-o",
    help="Whether the output word doc (which is a copy of the original) should be overwritten. If set to False, then the file name will include the timestamp of when it was written",
    default=True,
    type=bool,
)
def main(input: str, config: str, overwrite: bool) -> None:
    filepath = ""
    try:
        Cfg(config)
        dir, basename = parse_input(input)
        filepath = copy_doc(input)
        doc = load_doc(filepath)
        doc = process_doc(doc)
        output = os.path.join(dir, filename(basename, overwrite))
        doc.save(output)
        logging.info(f"Output file: {output}")
    except (
        InvalidIgnoredSections,
        InputNotFoundException,
        InvalidInput,
        DocLoadException,
    ) as e:
        logging.error(f"An error occured relating to a bad input: {e}")
    except (FileCopyException, InvalidDocObject) as e:
        logging.error(f"Internal error: {e}")
        raise
    except PermissionError as e:
        logging.error(f"You need to close the file {output} before trying again")
    except Exception as e:
        logging.error(f"An unknown error occured: {e}")
    finally:
        if filepath:
            rm_tmp_doc(filepath)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(levelname)s] %(asctime)s %(pathname)s:%(lineno)d - %(message)s",
        datefmt="%H:%M:%S",
    )
    main()
