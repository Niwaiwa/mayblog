from flask import make_response, jsonify
from myapp.common.ReturnCode import ReturnCode
import logging
from typing import Any

log = logging.getLogger('Response')

def response(status_code: int = 401, code: int = 0, msg: str = None, content: Any = None):
    # log.info('response')
    response_format = {"code": code, "msg": msg if msg is not None else ReturnCode.code.get(code)}
    if content:
        response_format.update({'content': content})
    if status_code:
        return make_response(jsonify(response_format)), status_code
    return make_response(jsonify(response_format))