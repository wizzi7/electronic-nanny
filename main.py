import requests
from flask import Flask, render_template, request
from flask_restful import Api
import os
from turbo_flask import Turbo
import threading


from werkzeug.utils import redirect

app = Flask(__name__)
turbo = Turbo(app)
api = Api(app)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

image  = ''
image2 = ''
image3 = ''
image4 = ''
image5 = ''
image6 = ''
video  = ''
audio  = ''


# POST methods
@app.route('/sendimage', methods=['POST', 'GET'])
def upload_image():
    if request.method == 'POST':
        profile = request.files['file']
        filename = profile.filename
        profile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global image, image2, image3, image4, image5, image6
        image6 = image5
        image5 = image4
        image4 = image3
        image3 = image2
        image2 = image
        image = filename
        inject_load()
    return '', 200


@app.route('/sendvideo', methods=['POST'])
def upload_video():
    if request.method == 'POST':
        # save the single "profile" file
        profile = request.files['file']
        filename = profile.filename
        profile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global video
        video = filename
        return '', 200


@app.route('/sendvoice', methods=['POST'])
def upload_voice():
    if request.method == 'POST':
        # save the single "profile" file
        profile = request.files['file']
        filename = profile.filename
        profile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        global audio
        audio = filename
        return '', 200


@app.context_processor
def inject_load():
    global image
    return {'load': 'static/uploads/' + image, 'load2': 'static/uploads/' + image2, 'load3': 'static/uploads/' + image3
            , 'load4': 'static/uploads/' + image4, 'load5': 'static/uploads/' + image5,
            'load6': 'static/uploads/' + image6, 'loadvideo': 'static/uploads/' + video,
            'loadaudio': 'static/uploads/' + audio}


@app.before_first_request
def before_first_request():
    threading.Thread(target=update_load).start()


def update_load():
    with app.app_context():
        while True:
            turbo.push(turbo.replace(render_template('index.html'), 'load'))


# Get methods
@app.route('/getimage', methods=['GET'])
def get_image():
    BASE = 'http://192.168.0.192:5000/getimage'
    requests.get(BASE)
    return redirect("/")


@app.route('/getvideo', methods=['GET'])
def get_video():
    BASE = 'http://192.168.0.192:5000/getvideo'
    requests.get(BASE)
    return render_template("video.html", loadvideo='static/uploads/' + video)


@app.route('/getvoice', methods=['GET'])
def get_voice():
    BASE = 'http://192.168.0.192:5000/getvoice'
    requests.get(BASE)
    return render_template("voice.html", loadaudio='static/uploads/' + audio)


# ustawienie automatu na robienie zdj co 5 min - wlaczenie
@app.route('/setroboton', methods=['GET'])
def turn_on_robot():
    BASE = 'http://192.168.0.192:5000/setroboton'
    requests.get(BASE)
    return redirect("/")


# ustawienie automatu na robienie zdj co 5 min - wylaczenie
@app.route('/setrobotoff', methods=['GET'])
def turn_off_robot():
    BASE = 'http://192.168.0.192:5000/setrobotoff'
    requests.get(BASE)
    return redirect("/")


@app.route('/')
def show_index():
    return render_template("index.html")


@app.route('/video')
def show_video():
    return render_template("video.html")


@app.route('/photo')
def back_to_main():
    return render_template("index.html")


@app.route('/voice')
def show_voice():
    return render_template("voice.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
