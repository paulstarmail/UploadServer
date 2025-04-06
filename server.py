#!/usr/bin/python3

from flask import Flask, request, render_template_string
import os

# Create the Flask application
app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template for the upload form
UPLOAD_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Upload Files</title>
  <script>
    function showUploadSuccess() {
      alert("File(s) successfully uploaded!");
    }
  </script>
</head>
<body>
  <h1>Upload Files</h1>
  <form action="/upload" method="POST" enctype="multipart/form-data">
    <label for="file">Choose a file:</label>
    <input type="file" name="file" id="file" multiple><br><br>
    <button type="submit">Upload</button>
  </form>
  {% if success %}
    <script>
      window.onload = showUploadSuccess;
    </script>
  {% endif %}
</body>
</html>
'''

# Route to display the upload form
@app.route('/')
def index():
    return render_template_string(UPLOAD_FORM, success=False)

# Route to handle file upload
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    
    files = request.files.getlist('file')
    if not files:
        return "No selected file", 400
    
    for file in files:
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    
    return render_template_string(UPLOAD_FORM, success=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

