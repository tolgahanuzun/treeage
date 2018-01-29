import os
from flask import Flask, request, redirect, url_for, render_template
from werkzeug import secure_filename

from app import treeage

UPLOAD_FOLDER = './img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_url = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_url)
        else:
            return render_template('index.html', data={'error':'Are you sure this is a picture file?'})            
            
        try:
            count, link = treeage(file_url)
            return render_template('index.html', data={'result':link, 'count':count})
        except:
            return render_template('index.html', data={'error':'''Oh, no! Can you report the scenario and the file to me?
        https://github.com/tolgahanuzun/treeage'''})

    return redirect(url_for('index'))
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)