from flask import Flask, request
from flask_restful import Api
import os

app = Flask(__name__)

api = Api(app)


@app.route('/getimage', methods=['GET'])
def send_image():
    if request.method == 'GET':
        os.system('python makeimg.py')
    return '', 200


@app.route('/getvideo', methods=['GET'])
def send_video():
    if request.method == 'GET':
        os.system('python makevideo.py')
    return '', 200


@app.route('/getvoice', methods=['GET'])
def send_voice():
    if request.method == 'GET':
        os.system('python mainraspi.py')
    return '', 200


@app.route('/setroboton', methods=['GET'])
def turn_on_robot():
    if request.method == 'GET':
        os.system('sudo /etc/init.d/cron start')
    return '', 200


@app.route('/setrobotoff', methods=['GET'])
def turn_off_robot():
    if request.method == 'GET':
        os.system('sudo /etc/init.d/cron stop')
    return '', 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
