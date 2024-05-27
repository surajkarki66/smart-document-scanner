from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileAllowed, FileRequired, FileSize
from wtforms import SelectField, SubmitField


class OCRForm(FlaskForm):
    files = MultipleFileField('Files', validators=[
        FileRequired(message='Please select at least one file.'),
        FileAllowed(['jpg', 'png', 'jpeg', 'heic'],
                    message='Only PNG, JPG, HEIC, or JPEG files allowed.'),
        FileSize(max_size=7 * 1024 * 1024,
                 message='File size should not exceed 7 MB.')
    ])
    format = SelectField('Format', choices=[('pdf', 'PDF'), ('docx', 'DOCX')])
    submit = SubmitField('Submit')
