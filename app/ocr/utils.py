from io import BytesIO
from fpdf import FPDF
from docx import Document


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
