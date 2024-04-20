"""
Author：wangzhe
Create date:2024/4/20
Description:
"""
import os

from pdf2image import convert_from_bytes

"""
安装pdf2image包， 需要依赖poppler包
https://github.com/wang91zhe/pdf2image/blob/master/README.md
"""
def pdf_image(pdf_path: str = "", output_folder: str = ""):
    """
    PDF转Image
    :param pdf_path: pdf路径
    :param output_folder: 图片保存路径
    :return:
    """
    page2image_path, page2image = {}, {}
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    with open(pdf_path, "rb") as pdf:
        images = convert_from_bytes(pdf.read())
    # 遍历图片列表并保存每一页为PNG文件
    for i, image in enumerate(images):
        filename = os.path.join(output_folder, f"page_{i+1}.png")
        image.save(filename, "PNG")
        page2image_path[i+1] = filename
        page2image[i+1] = image
    return page2image_path, page2image
