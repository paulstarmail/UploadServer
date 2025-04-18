#!/usr/bin/python3

from flask import Flask, request, render_template_string, jsonify
from subprocess import check_output
import requests
import sys
import os

# Create the Flask application
app = Flask(__name__)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# HTML template with JavaScript progress bar
UPLOAD_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Upload Files with Accurate Progress</title>
  <style>
    #progressContainer {
      width: 100%;
      background-color: #eee;
      margin-top: 10px;
    }
    #progressBar {
      width: 0%;
      height: 20px;
      background-color: green;
      text-align: center;
      color: white;
    }
    #statusText {
      margin-top: 10px;
    }
  </style>
</head>
<body>
  <h1>Upload Files</h1>
  <form id="uploadForm">
    <label for="file">Choose file(s):</label>
    <input type="file" name="file" id="file" multiple><br><br>
    <button type="submit">Upload</button>
  </form>

  <div id="progressContainer">
    <div id="progressBar">0%</div>
  </div>
  <div id="statusText"></div>

  <script>
    document.getElementById('uploadForm').addEventListener('submit', function(e) {
      e.preventDefault();

      const files = document.getElementById('file').files;
      if (files.length === 0) {
        alert("Please select a file to upload.");
        return;
      }

      const formData = new FormData();
      for (let i = 0; i < files.length; i++) {
        formData.append('file', files[i]);
      }

      const xhr = new XMLHttpRequest();
      xhr.open('POST', '/upload', true);

      const progressBar = document.getElementById('progressBar');
      const statusText = document.getElementById('statusText');
      let lastProgress = 0;

      xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
          const percentComplete = Math.round((e.loaded / e.total) * 85); // Cap at 85%
          lastProgress = percentComplete;
          progressBar.style.width = percentComplete + '%';
          progressBar.textContent = percentComplete + '%';
          statusText.textContent = "Uploading files...";
        }
      };

      xhr.onload = function() {
        if (xhr.status === 200) {
          // Simulate final progress to 100%
          let fakeProgress = lastProgress;
          const interval = setInterval(() => {
            fakeProgress += 1;
            progressBar.style.width = fakeProgress + '%';
            progressBar.textContent = fakeProgress + '%';
            if (fakeProgress >= 100) {
              clearInterval(interval);
              statusText.textContent = "Upload complete. Files saved successfully!";
              document.getElementById('uploadForm').reset();
            }
          }, 20); // Adjust speed as needed
        } else {
          statusText.textContent = "Upload failed.";
        }
      };

      xhr.onerror = function() {
        statusText.textContent = "Upload error occurred.";
      };

      xhr.send(formData);
    });
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(UPLOAD_FORM)

@app.route('/upload', methods=['POST'])
def upload_file():
    files = request.files.getlist('file')
    if not files:
        return jsonify({"error": "No selected file"}), 400
    
    for file in files:
        if file and file.filename:
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
    
    return jsonify({"success": True})

def get_public_ip():
    try:
        response = requests.get("https://api.ipify.org?format=json")
        ip = response.json()["ip"].strip()
        return ip
    except requests.RequestException as e:
        print("Error fetching IP:", e)
        return None

FIREWALL_PORT = "30003"

if __name__ == '__main__':
    try:
        port = str(sys.argv[1])
    except:
        port = "6003"
    print("Public URL: http://" + str(get_public_ip()) + ":" + FIREWALL_PORT)
    ip = check_output(['hostname', '--all-ip-addresses'])
    ip = ip.decode("utf-8").strip()
    print("Local URL: http://" + ip + ":" + port)
    try:
        app.run(debug=True, host='0.0.0.0', port=port)
    except:
        print("\nERROR: The port " + port + " is in use by some other program.")
