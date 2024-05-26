from flask import Blueprint, render_template, request, redirect, url_for

ocr_bp = Blueprint('ocr', __name__)

@ocr_bp.route('/', methods=['GET', 'POST'])
def ocr():
    if request.method == 'POST':
        files = request.files.getlist('images')
        # Process OCR on the files here
        return redirect(url_for('ocr.ocr'))
    return render_template('ocr/ocr.html')