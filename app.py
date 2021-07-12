from datetime import datetime
import time

from flask import Flask, render_template, jsonify, request, url_for
from flask_socketio import SocketIO, emit


async_mode = None
app = Flask(__name__)
sio = SocketIO(app, async_mode=async_mode)


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html', time=datetime.now())


@app.route('/client_server', methods=['POST', 'GET'])
def client_server():
    return render_template('client_server.html', time=datetime.now())


@app.route('/server_client', methods=['POST', 'GET'])
def server_client():
    return render_template('server_client.html', time=datetime.now())


@app.route('/api', methods=['POST', 'GET'])
def api():
    if request.method == 'POST':
        try:
            param = request.form['param']
        except KeyError as ke:
            response = {'error': str(ke)}
            return jsonify(response)

        if param == 'time':
            response = {'time': str(datetime.now().time())}
        elif param == 'date':
            response = {'date': str(datetime.now().date())}
        else:
            response = {'error': 'param must be "time" or "date"'}

        return jsonify(response)
    else:
        response = {'time': datetime.now()}
        return jsonify(response)


@sio.on('from_client_event')
def from_client_to_server(message):
    emit('from_server_event', {'time': str(datetime.now())}, broadcast=False)


def from_server_to_client():
    while True:
        sio.emit('from_server_event2', {'time': str(datetime.now())})
        time.sleep(1)


if __name__ == "__main__":
    sio.start_background_task(target=from_server_to_client)
    sio.run(app, debug=True)
