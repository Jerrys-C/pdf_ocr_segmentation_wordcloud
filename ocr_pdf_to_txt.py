import fitz  # PyMuPDF
from PIL import Image
import pytesseract
import io
from tqdm import tqdm


# 提取 PDF 中的图像
def extract_images_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    images = []

    for page_num in tqdm(range(len(doc)), desc="Extracting images from PDF", unit="page"):
        page = doc.load_page(page_num)
        images_in_page = page.get_images(full=True)

        for img in images_in_page:
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            images.append(image)

    return images


# 对图像进行 OCR 并提取文本
def ocr_images(images, output_path):
    with open(output_path, 'w', encoding='utf-8') as f:
        for i, image in tqdm(enumerate(images), total=len(images), desc="Processing OCR", unit="image"):
            text = pytesseract.image_to_string(image, lang="chi_sim")
            f.write(f"\n\n--- Page {i + 1} ---\n\n")  # 在每页之间添加分隔符
            f.write(text)


# 主函数：提取图像并执行 OCR
def main(pdf_path, output_path):
    # 提取 PDF 中的图像
    images = extract_images_from_pdf(pdf_path)

    # 对提取的图像进行 OCR 并保存到文本文件
    ocr_images(images, output_path)


# 使用示例
pdf_path = "data/sample.pdf"  # PDF 文件路径
output_path = "output_text.txt"  # 输出文本文件路径
main(pdf_path, output_path)