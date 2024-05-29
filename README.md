# UploadServer
A Flask based upload server for ubuntu. This application can be used to transfer any file from any device with a web-browser installed and connected to the same network where this application is running.


Pre-requisites
==============
Install all dependencies which are imported in the "main.py" file. This step is needed only if the software does not work out-of-the-box.

Procedure to start the server
=============================
1. Run the below command to start serving.\
   $ ./main.py <port>
2. Enter the URL displayed, inside the address bar of the web-browser of the client device.
3. The uploaded files will be in the folder "files" of this server application.
