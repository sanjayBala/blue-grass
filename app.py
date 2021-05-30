import os
from flask import Flask, render_template, flash, request, redirect, send_from_directory
from flask_wtf import file
from forms.main_form import UploadForm, MarkForm
from flask.helpers import url_for
from werkzeug.utils import secure_filename
import pandas as pd
from main import *

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = '57916238bbsdasda13ce0c676dsde280ba245'
app.config['UPLOAD_FOLDER'] = './'
app.logger.setLevel('INFO')

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadForm()
    message = ''
    if request.method == 'POST':
        file = request.files['file']
        if form.validate_on_submit() and file.filename != '':
            filepath = secure_filename(file.filename)
            file.save(filepath)
            return redirect(url_for('choose_mark', filepath=filepath, broker=str(form.broker.data)))
    return render_template('index.html', form=form, message=message)

@app.route('/choose_mark/<string:filepath>/<string:broker>', methods=['GET', 'POST'])
def choose_mark(filepath, broker):
    form = MarkForm()
    MARK_LIST = build_mark_list(filepath, broker)
    if request.method == 'POST':
        output_filepath = main_process(filepath, broker, request.form.getlist('mark_list'))
        download_url = get_download_url(output_filepath)
        return download_url
    return render_template('choose_mark.html', form=form, marks=MARK_LIST)


def get_download_url(filename):
    uploads = os.path.join(app.config['UPLOAD_FOLDER'])
    return send_from_directory(uploads, filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)