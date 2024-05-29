from flask_wtf import FlaskForm
from flask_wtf.file import MultipleFileField, FileAllowed, FileRequired, FileSize
from wtforms import SelectField, SubmitField, ValidationError


def file_count_limit(max_count: int, message: str) -> any:
    def _file_count_limit(form, field):
        if len(field.data) > max_count:
            raise ValidationError(message=message)
    return _file_count_limit


class ScannerForm(FlaskForm):
    images = MultipleFileField('Images', validators=[
        FileRequired(message='Please select at least one image.'),
        FileAllowed(['jpg', 'png', 'jpeg', 'heic'],
                    message='Only PNG, JPG, HEIC, or JPEG files allowed.'),
        FileSize(max_size=7 * 1024 * 1024,
                 message='File size should not exceed 7 MB.'),
        file_count_limit(
            max_count=15,  message="You cannot upload more than 15 images")
    ])
    document_effect = SelectField('Document Effect Type', choices=[
                                  ('grayscale', 'Grayscale'), ('colored', 'Colored')])
    out_file_type = SelectField('Output File Type', choices=[
                                ('pdf', 'Pdf'), ('image', 'Image')])
    submit = SubmitField('Submit')
