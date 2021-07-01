import os

from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kkkdsfksdmfkiosfksfalreaoadlasdalaell'
Bootstrap(app)


class UploadForm(FlaskForm):
    file = FileField()


@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    try:
        shutil.rmtree('./static/runs/detect/exp')
    except FileNotFoundError:
        pass
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        os.system(
                'python E:/pyton/Aerial-polar-bears/yolov5/models/detect.py --weights ./yolov5/weights/best.pt --conf 0.4 '
                '--img 416 --source ./uploads --project ./static/runs/detect')
        os.remove(f'./uploads/{filename}')

        return redirect(url_for('image', filename=filename))

    return render_template('index.html', form=form)


@app.route('/image/<filename>', methods=['GET', 'POST'])
def image(filename):
    return render_template('label_image.html', filename=filename)


if __name__ == '__main__':
    app.run(debug=True)
