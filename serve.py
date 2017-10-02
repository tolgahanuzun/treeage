from __future__ import unicode_literals
from bottle import Bottle, request, response
from bottle import route
from bottle import static_file
from app import treeage

app = Bottle()

template = """<html>
<head><title>Home</title></head>
<body>
<h1>Upload a file</h1>
<form method="POST" enctype="multipart/form-data" action="/">
<input type="file" name="uploadfile" /><br>
<input type="submit" value="Submit" />
</form>
</body>
</html>"""


@app.get('/')
def home():
    return template

@app.post('/')
def upload():
    upload_file = request.POST['uploadfile']
    upload_file.save('./')

    try:
        count, link = treeage(upload_file.filename)
    except:
        return '''<h1><a href='/'>Return Upload Page</a></h1><p>Make sure you upload images</p>'''

    return """<html>
            <head><title>Home</title></head>
            <body>
            <h1><a href='/'>Return Upload Page</a></h1>
            <h3>Circle : {0} (+- 5)</h1>
            <img src='{1}'>
            </body>
            </html>
            """.format(count, link)

if __name__ == "__main__":
    app.run(debug=True)