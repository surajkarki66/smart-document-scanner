import pytesseract

from PIL import Image
from flask import Blueprint, render_template, send_file, flash, redirect, request


from app.ocr.forms import OCRForm
from app.core.utils import create_pdf, create_docx

ocr_bp = Blueprint('ocr', __name__)


@ocr_bp.route('/', methods=['GET', 'POST'])
def ocr_view():
    form = OCRForm()
    if form.validate_on_submit():
        images = form.images.data
        if not images:
            flash('No image part!', 'error')
            return redirect(request.url)

        text_output = []
        for image in images:
            try:
                img = Image.open(image)
                text = pytesseract.image_to_string(img)
                text_output.append(text)

            except Exception as e:
                flash(f'Error processing file!', 'error')
                return redirect(request.url)

        doc_format = form.format.data

        if doc_format == 'pdf':
            pdf_io = create_pdf(text_output)
            return send_file(pdf_io, as_attachment=True, mimetype='application/pdf', download_name='output.pdf')

        else:
            docx_io = create_docx(text_output)
            return send_file(docx_io, as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document', download_name='output.docx')

    return render_template('ocr/ocr.html', form=form)
