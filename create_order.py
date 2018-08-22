# -*- coding: utf-8 -*-
from flask import Flask, request, abort, jsonify
from conf import booker_config
from conf import refreshConfig
import time
from engine import bookerEngineInstance
from req.booker_req import BookerReq
import logging
import json

app = Flask(__name__)

logger = logging.getLogger("lcc_booker")


@app.route('/lcc/booker/refresh', methods=['POST', 'GET'])
def refresh():
    logger.info('refresh configure!')
    refreshConfig()


@app.route('/lcc/booker', methods=['POST'])
def create_order():
    req = BookerReq()

    logger.info('request: {0}'.format(request.json))

    if not req.constructor(request.json):
        return json.dumps({"status": "5", "message": "Invalid request parameters!"})

    startTime = time.time()
    result = bookerEngineInstance.run(req)
    endTime = time.time()

    jsonResult = json.dumps(result)

    logger.info('response:{0:.0f}, {1}'.format(endTime - startTime, jsonResult))

    return jsonResult


if __name__ == '__main__':
    port = booker_config.getint('server', 'port')
    logger.info('get port: {0}'.format(port))

    app.run(host="0.0.0.0", port=port, debug=True)
