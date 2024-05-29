import cv2
import numpy as np

from io import BytesIO
from fpdf import FPDF
from docx import Document
from imutils.perspective import four_point_transform


def create_pdf(texts: list[str]) -> BytesIO:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)

    for text in texts:
        pdf.multi_cell(0, 10, text)

    pdf_io = BytesIO()
    p = pdf.output(pdf_io, dest='S').encode('latin-1')
    pdf_io = BytesIO(p)
    pdf_io.seek(0)

    return pdf_io


def create_docx(texts: list[str]) -> BytesIO:
    doc = Document()
    for text in texts:
        doc.add_paragraph(text)

    doc_io = BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)

    return doc_io


def image_post_processing(image: np.ndarray) -> np.ndarray:
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, threshold = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    return threshold


def find_biggest_contours(contours: np.ndarray) -> np.ndarray:
    max_area = 0
    WIDTH, HEIGHT = 1920, 1080
    biggest_contours = np.array(
        [[0, 0], [WIDTH, 0], [WIDTH, HEIGHT], [0, HEIGHT]])

    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:
            peri = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.015 * peri, True)
            if area > max_area and len(approx) == 4:
                biggest_contours = approx
                max_area = area

    return biggest_contours


def detect_edges(image: np.ndarray) -> list:
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, threshold = cv2.threshold(
            blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(
            threshold, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        if not contours:
            # Handle the case where no contours are found
            raise ValueError("No contours found in the image.")

        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        return contours

    except cv2.error as e:
        raise RuntimeError(
            "An error occurred while processing the image with OpenCV.") from e
    except Exception as e:
        raise RuntimeError("An unexpected error occurred.") from e


def scan_doc(img, doc_effect_type, scale):
    edges = detect_edges(img)
    b_contours = find_biggest_contours(edges)
    warped_image = four_point_transform(img, b_contours.reshape(4, 2))

    resized_warp_image = cv2.resize(warped_image, (int(
        scale * warped_image.shape[1]), int(scale * warped_image.shape[0])))

    if doc_effect_type == "colored":
        return resized_warp_image

    elif doc_effect_type == "grayscale":

        p_image = image_post_processing(warped_image)

        p_image = p_image[10:p_image.shape[0] -
                          10, 10:p_image.shape[1] - 10]
        p_image_resized = cv2.resize(
            p_image, (int(scale * p_image.shape[1]), int(scale * p_image.shape[0])))

        return p_image_resized
