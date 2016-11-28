from flask import Flask, request
import logging


app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('stub')


@app.route('/<string:msg_id>', methods=['POST'])
def index(msg_id):
    data = request.data
    logger.info(data)
    return "OK"


if __name__ == '__main__':
    app.debug=True
    app.run(host='0.0.0.0', port=8000)
