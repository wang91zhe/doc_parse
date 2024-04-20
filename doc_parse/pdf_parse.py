"""
Author：wangzhe
Create date:2024/4/20
Description:
"""
from typing import Optional, Container

from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.high_level import extract_pages

from utils.util import FileOrName


def extract_pdf(
    pdf_file: FileOrName,
    password: str = "",
    page_numbers: Optional[Container[int]] = None,
    maxpages: int = 0,
    caching: bool = True,
    laparams: Optional[LAParams] = None,
):
    """
    Extract PDF文件的layout格式
    :param pdf_file: Either a file path or a file-like object for the PDF file to be worked on.
    :param password: For encrypted PDFs, the password to decrypt.
    :param page_numbers: List of zero-indexed page numbers to extract.
    :param maxpages: The maximum number of pages to parse
    :param caching: If resources should be cached
    :param laparams: An LAParams object from pdfminer.layout. If None, uses some default settings that often work well.
    :return: LTPage objects
    """
    page_index = 0
    pdf_layout = {}
    if laparams is None:
        laparams = LAParams(detect_vertical=True)
    pages = extract_pages(
        pdf_file,
        password=password,
        page_numbers=page_numbers,
        maxpages=maxpages,
        caching=caching,
        laparams=laparams,
    )
    for layout in pages:
        page_index += 1
        node_list = []
        row = 0
        height = layout.height
        width = layout.width
        for element in layout:
            row += 1
            if isinstance(element, (LTTextBox, LTTextLine)):
                text = element.get_text()
                x0, y0 = element.x0, element.y0
                x1, y1 = element.x1, element.y1
                node_list.append(
                    {
                        "text": text,
                        "text_rectangle": {"llx": x0, "lly": height-y0, "urx": x1, "ury": height-y1},
                    }
                )
        pdf_layout[page_index] = {
            "text_list": node_list,
            "height": height,
            "width": width,
            "page": page_index,
        }
    return pdf_layout
