from flask import Flask, render_template, request, render_template_string
from werkzeug.utils import secure_filename
from subprocess import getoutput as shell
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'upload/'
shell('echo $FLAG > /flag')

@app.route('/')
def upload_file():
    return render_template('index.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader():
    if request.method == 'POST':
        abs_path = os.path.dirname(__file__)
        f = request.files['file']
        filename = f.filename
        if '.' in filename:
            prefix, suffix = filename.split('.')
            white_list = ['py3', 'jpg', 'png']
            if suffix in white_list:
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
                try:
                    content = str(shell('python3 %s/upload/%s' % (abs_path, filename)))
                    if "%" in content:
                        content.replace('%', '')
                except Exception as e:
                    content = str(e)
                html = 'file uploaded successfully!<!-- %s -->' % str(content)
                return render_template_string(html)
            else:
                return "The file is not allowed to upload!"
        else:
            return "The file is not allowed to upload!"

    else:
        return "Method Not Allowed"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)