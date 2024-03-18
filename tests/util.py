from docx.document import Document


def word_count(doc: Document) -> int:
    count = 0
    for para in doc.paragraphs:
        txt = para.text
        if txt == "":
            continue

        words = txt.split()
        for word in words:
            if word not in (".", "-", "_"):
                count += 1
    return count
