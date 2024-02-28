import traceback
from flask import abort, jsonify, make_response
from pymongo.errors import DuplicateKeyError
from werkzeug.exceptions import HTTPException, BadRequest, BadRequestKeyError
from bson.errors import InvalidId


def throw_error(field, **kwargs):
    traceback.print_exc()
    if field == None:
        return jsonify({'message': "{}".format(kwargs['message'])}), kwargs['code']
    if type(field) is KeyError:
        return jsonify({'message': "{}--name is undefined".format(field)}), 500
    elif type(field) is NameError:
        return jsonify({'message': "{}-field is undefined".format(field)}), 500
    elif type(field) is TypeError:
        return jsonify({'message': "{}".format(field)}), 500
    elif type(field) is DuplicateKeyError:
        return jsonify({'message': "{}-duplicate key error".format(field)}), 409
    elif type(field) is HTTPException:
        return abort(make_response(jsonify(message="something went wrong"), 500))
    elif type(field) is UnboundLocalError:
        return jsonify({'message': "{}".format(field)}), 500
    elif type(field) is BadRequest:
        return jsonify({'message': "{}".format(field)}), 400
    elif type(field) is AttributeError:
        return jsonify({'message': "{}".format(field)}), 500
    elif type(field) is InvalidId:
        return jsonify({'message': "{}".format(field)}), 500
    elif type(field) is BadRequestKeyError:
        return jsonify({'message': "{}".format(field)}), 400


def get_handled_errors(error):
    errors = [
        KeyError,
        NameError,
        TypeError,
        InvalidId,
        AttributeError,
        HTTPException,
        BadRequest,
        UnboundLocalError,
        DuplicateKeyError,
        BadRequestKeyError,
    ]
    return error in errors