from flask import make_response
import json


class ReturnError(Exception):
    def __init__(self, code, msg=None, **kwargs):
        self.code = code
        self.msg = msg if msg else ReturnCode.code.get(code)

    def __str__(self):
        return self.msg


class ReturnCode:
    code = {
        0: 'ok',
        1: 'Internal Error',
        10: 'Please log in.',
        11: 'Please log in again.',
        101: 'Register failed. Please try again.',
        102: 'User already exists. Please Log in.',
        103: 'Log in failed, Please try again.',
        901: 'Invalid request',
        902: 'Invalid request parm',
        903: 'Invalid request data',
        904: 'This page does not exist',
    }

    @staticmethod
    def response(status_code=401, code=0, msg=None, data=None):
        rData = ReturnCode.genReturnData(status_code, code, msg, data)
        r = make_response(rData)
        r.headers['Content-Type'] = 'application/json'
        return r

    @staticmethod
    def genReturnData(status_code=200, code=0, msg=None, data=None):
        rtn_format = {
            "code": code,
            "msg": msg if msg else ReturnCode.code.get(code, "")
        }
        if data:
            for (key, value) in data.items():
                rtn_format.update({key: value})
        return json.dumps(rtn_format, default=str), status_code

