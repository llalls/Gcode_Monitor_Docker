import io
import os, sys
import threading
import numpy as np
import base64, string
from PIL import Image
from threading import Lock
from flask import url_for, Flask, request, redirect, render_template, send_from_directory, jsonify
import gcodeCompare

app = Flask(__name__, template_folder='templates')
lock = Lock()

@app.route('/')
def web_form():
    return render_template('web_form.html')

@app.route('/GcodeViewer_server_version.html')
def gcodeViewer():
    return render_template('GcodeViewer_server_version.html')

@app.route('/camera1_server_version.html')
def camera1():
    return render_template('camera1_server_version.html')

@app.route('/camera2_server_version.html')
def camera2():
    return render_template('camera2_server_version.html')


@app.route('/upload', methods=['POST'])
def upload():
    imageURL = request.form.get('dataURL', '')
    rotate_frequency = request.form.get('rotate_frequency', '')
    image_position_data_x = request.form.get('camera_position_x', '')
    image_position_data_y = request.form.get('camera_position_y', '')
    image_position_data_z = request.form.get('camera_position_z', '')
    
    
    pil_img = Image.open(io.BytesIO(base64.b64decode(imageURL)))

    
    lock.acquire()
    gcodeCompare.image_compare(pil_img, rotate_frequency, image_position_data_x, image_position_data_y, image_position_data_z)
    lock.release()

    return('upload success!')


@app.route('/rotate', methods=['GET'])
def rotate():
    camera_position_list = gcodeCompare.get_image_compare_list()

    print('rotate flask: ' + str(camera_position_list))


    rotate_data_flask = {
        'rotate_time': camera_position_list[0][0],
        'position_x' : camera_position_list[0][1],
        'position_y' : camera_position_list[0][2],
        'position_z' : camera_position_list[0][3]
    }
    return jsonify(rotate_data_flask)


def gcodeImage_filename(upload_Time):
    filename = 'gcodeImage_' + str(upload_Time) + '.jpg' 
    return filename


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8888)

    lock = threading.Lock()