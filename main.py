from flask import Flask, render_template, jsonify, request
import requests
import numpy
import base64
import cv2

app = Flask(__name__)

url = "http://34.72.141.162:5050/detect"
headers = {"content-type": "image/jpg"}


def get_base64(image):
    _, im_arr = cv2.imencode('.jpg', image)
    im_bytes = im_arr.tobytes()
    img_base64 = base64.encodebytes(im_bytes).decode('ascii')
    return img_base64


in_holder = get_base64(cv2.imread('static/orange_in.jpg'))
out_holder = get_base64(cv2.imread('static/orange_out.jpg'))


@app.route('/', methods=['GET', 'POST'])
def home():
    return jsonify({"Objects Detector": "/objects_detector"})


@app.route('/objects_detector', methods=['GET', 'POST'])
def objects_detector():
    if request.method == 'POST':
        img_file = request.files['my_uploaded_file']
        if img_file:
            [in_base64, out_base64] = detect_objects(img_file)
            return render_template('index.html', img_in_base64=in_base64, img_out_base64=out_base64)
        else:
            print("No Image selected")
    return render_template('index.html', img_in_base64=in_holder, img_out_base64=out_holder)


def detect_objects(img_file):
    image = cv2.imdecode(numpy.frombuffer(img_file.read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    _, img_encoded = cv2.imencode(".jpg", image)

    in_base64 = get_base64(image)

    # send HTTP request to the server
    response = requests.post(url, data=img_encoded.tobytes(), headers=headers)
    predictions = response.json()

    # annotate the image
    for pred in predictions:
        (x, y) = (pred["boxes"][0], pred["boxes"][1])
        (w, h) = (pred["boxes"][2], pred["boxes"][3])

        # draw a bounding box rectangle and label on the image
        cv2.rectangle(image, (x, y), (x + w, y + h), pred["color"], 1)
        text = "{}: {:.4f}".format(pred["label"], pred["confidence"])
        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, pred["color"], 2)

    out_base64 = get_base64(image)
    return [in_base64, out_base64]


if __name__ == '__main__':
    app.run(debug=True)
