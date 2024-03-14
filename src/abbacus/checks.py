from docx.text.paragraph import Paragraph


def is_heading(para: Paragraph) -> bool:
    return para.style.name.startswith("Heading")


def is_title(para: Paragraph) -> bool:
    return para.style.name.startswith("Title")


def is_subtitle(para: Paragraph) -> bool:
    return para.style.name.startswith("Subtitle")


def is_caption(para: Paragraph) -> bool:
    return para.style.name.startswith("Caption")
