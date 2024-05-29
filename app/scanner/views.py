import zipfile
import cv2
import os
import numpy as np

from fpdf import FPDF
from io import BytesIO
from flask import Blueprint, flash, render_template, request, redirect, send_file

from app.scanner.forms import ScannerForm
from app.core.utils import scan_doc

scanner_bp = Blueprint('scanner', __name__)


@scanner_bp.route('/', methods=['GET', 'POST'])
def scanner_view():
    form = ScannerForm()
    if form.validate_on_submit():
        images = form.images.data
        if not images:
            flash('No images part!', 'error')
            return redirect(request.url)
        try:
            out_imgs = []
            output_file_type = form.out_file_type.data
            pdf = FPDF()
            SCALE = 0.5
            for index, image in enumerate(images):
                image_data = image.read()
                np_image = np.frombuffer(image_data, np.uint8)
                img = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

                doc_effect_type = form.document_effect.data

                image = scan_doc(img, doc_effect_type, SCALE)

                UPLOAD_PATH = f"temp_{index}.jpg"
                cv2.imwrite(UPLOAD_PATH, image)
                out_imgs.append(UPLOAD_PATH)

                if output_file_type == "pdf":
                    pdf.add_page()
                    pdf.image(UPLOAD_PATH, x=10, y=10,
                              w=image.shape[1] * SCALE / 3, h=image.shape[0] * SCALE / 3)
                    os.remove(UPLOAD_PATH)

            if output_file_type == "pdf":
                pdf_io = BytesIO()
                p = pdf.output(pdf_io, dest='S').encode('latin-1')
                pdf_out = BytesIO(p)
                pdf_out.seek(0)

                return send_file(pdf_out, as_attachment=True, mimetype='application/pdf', download_name='scanned_document.pdf')

            elif output_file_type == "image":
                zip_io = BytesIO()
                with zipfile.ZipFile(zip_io, 'w') as zip_file:
                    for image_path in out_imgs:
                        zip_file.write(
                            image_path, os.path.basename(image_path))
                        os.remove(image_path)
                zip_io.seek(0)
                return send_file(zip_io, as_attachment=True, mimetype='application/zip', download_name='scanned_images.zip')

        except Exception as e:
            flash(f"An error occurred: {e}", 'error')

    return render_template('scanner/scanner.html', form=form)
