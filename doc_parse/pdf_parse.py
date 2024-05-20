"""
Author：wangzhe
Create date:2024/4/20
Description:
"""
from typing import Optional, Container, Tuple, Union

from pdfminer.layout import LAParams, LTTextBox, LTTextLine
from pdfminer.high_level import extract_pages

from doc2image.pdf2img import pdf_image
from utils.util import FileOrName


def extract_pdf(
    pdf_file: FileOrName,
    output_folder: str = "",
    password: str = "",
    page_numbers: Optional[Container[int]] = None,
    maxpages: int = 0,
    caching: bool = True,
    laparams: Optional[LAParams] = None,
    size: Union[Tuple, int] = None,
    need_image: bool = False,
):
    """
    Extract PDF文件的layout格式
    :param pdf_file: Either a file path or a file-like object for the PDF file to be worked on.
    :param password: For encrypted PDFs, the password to decrypt.
    :param page_numbers: List of zero-indexed page numbers to extract.
    :param maxpages: The maximum number of pages to parse
    :param caching: If resources should be cached
    :param laparams: An LAParams object from pdfminer.layout. If None, uses some default settings that often work well.
    :param size: Size of the resulting image(s), uses the Pillow (width, height) standard, defaults to None
    :param need_image:
    :return: LTPage objects
    """
    page_index = 0
    pdf_layout, page2image_path, page2image = {}, {}, {}
    if laparams is None:
        laparams = LAParams(detect_vertical=True)
    if need_image:
        page2image_path, page2image = pdf_image(pdf_file, output_folder, size=size)
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
        text_list = []
        row = 0
        height = layout.height
        width = layout.width
        for element in layout:
            row += 1
            if isinstance(element, (LTTextBox, LTTextLine)):
                text = element.get_text()
                x0, y0 = element.x0, element.y0
                x1, y1 = element.x1, element.y1
                text_list.append(
                    {
                        "text": text,
                        "position": {"llx": x0, "lly": height-y0, "urx": x1, "ury": height-y1},
                    }
                )
        pdf_layout[page_index] = {
            "text_list": text_list,
            "height": height,
            "width": width,
            "page": page_index,
            "image": page2image.get(page_index, None)
        }
    return pdf_layout
