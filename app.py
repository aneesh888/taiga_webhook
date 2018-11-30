import os
import logging
from datetime import datetime, timedelta
from flask import Flask, request, abort, jsonify

WEBHOOK_VERIFY_TOKEN = '63c566b641a0172c54a7895c4e3976a539e14a630ff37a09'

app = Flask(__name__)

gunicorn_error_logger = logging.getLogger('gunicorn.error')
app.logger.handlers.extend(gunicorn_error_logger.handlers)
app.logger.setLevel(logging.INFO)
app.logger.debug('this will show in the log')

authorised_clients = {}


def verify_signature(key, data, signature):
    mac = hmac.new(key.encode("utf-8"), msg=data, digestmod=hashlib.sha1)
    return mac.hexdigest() == signature


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        verify_token = request.args.get('verify_token')
        if verify_token == WEBHOOK_VERIFY_TOKEN:
            authorised_clients[request.remote_addr] = datetime.now()
            return jsonify({'status': 'success'}), 200
        else:
            return jsonify({'status': 'bad token'}), 401

    elif request.method == 'POST':
        client = request.remote_addr
        return jsonify({'status': 'success'}), 200
    else:
        abort(400)


@app.route('/', methods=['GET'])
def index():
    return jsonify({'status': 'success'}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
