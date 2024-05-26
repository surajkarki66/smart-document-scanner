from flask import Blueprint, render_template, request, redirect, url_for

scanner_bp = Blueprint('scanner', __name__)

@scanner_bp.route('/', methods=['GET', 'POST'])
def scanner():
    if request.method == 'POST':
        files = request.files.getlist('images')
        # Process scanning on the files here
        return redirect(url_for('scanner.scanner'))
    return render_template('scanner/scanner.html')