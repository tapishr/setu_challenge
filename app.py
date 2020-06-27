#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" app.py: Module for running server and handling requests
    
    Author: Tapish Rathore
"""
import os
import secrets
import datetime
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
from exceptions import SetuError, ErrorCodes


app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


from models import Users
from models import Customers
from models import Transactions


@app.errorhandler(SetuError)
def handle_error_codes(error):
    '''
    error handling function for setting status codes and error body
    '''
    response = jsonify(error.to_dict())
    response.status_code = error.httpcode
    return response


def auth_key(view_function):
    '''
    Decorator function for api key authorization
    '''
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        apikey = None
        if 'X-API-KEY' in request.headers:
            apikey = request.headers['X-API-KEY']
            user = None
            try:
                user = Users.query.filter_by(key=apikey).first()
            except Exception as e:
                print(e)
                raise SetuError(ErrorCodes.Unhandled_error)
            if not user:
                raise SetuError(ErrorCodes.Auth_error)
        else:
            raise SetuError(ErrorCodes.Auth_error)
        return view_function(*args, **kwargs)
    return decorated_function


@app.route("/api/v1/fetch-bill", methods=["POST"])
@auth_key
def fetch_bill():
    '''
    Function for fetching bill of particular customer
    '''
    expected = {
        "mobileNumber": ""
    }
    body = request.get_json()
    verify_request_body(body, expected)
    # Get data from db
    cust = None
    try:
        cust = Customers.query.filter_by(mobileno=body["mobileNumber"]).first()
    except Exception as e:
        print(e)
        raise SetuError(ErrorCodes.Customer_not_found)
    if not cust:
        raise SetuError(ErrorCodes.Customer_not_found)
    # Generate refID
    # Not a scalable/secure way to generate refID, only for demo
    refID = ""
    if cust.amount > 0:
        refID = 'r' + secrets.token_hex(16)
    # Store refID
    tr = Transactions(refID)
    tr.custID = cust.custID
    try:
        db.session.add(tr)
        db.session.commit()
    except Exception as e:
        print(e)
        # Keep trying to insert in Transactions table
    # Jsonify and send with proper code in case of error
    r = {
        "status": "SUCCESS",
        "data": {
            "customerName": cust.name,
            "dueAmount": str(cust.amount),
            "dueDate": cust.duedate,
            "refID": refID
        }
    }
    return jsonify(r)


@app.route("/api/v1/payment-update", methods=["POST"])
@auth_key
def payment_update():
    '''
    Function for updating payment of a customer
    '''
    expected = {
        "refID": "",
        "transaction": {
            "amountPaid": "",
            "date": "",
            "id": ""
        }
    }
    body = request.get_json()
    verify_request_body(body, expected)
    try:
        datetime.datetime.strptime(body["date"], '%Y-%m-%d')
    except ValueError:
        raise SetuError(ErrorCodes.Invalid_api_parameters)
    # Check if this refid and transactionID is seen before, return result if already present
    tr = None
    try:
        tr = Transactions.query.filter_by(refID=body["refID"]).first()
    except Exception as e:
        print(e)
        raise SetuError(ErrorCodes.Unhandled_error)
    if tr:
        new_amount = float(body["transaction"]["amountPaid"])
        if tr.transactionID:
            # Transaction already present
            if tr.transactionID != body["transaction"]["id"]:
                raise SetuError(ErrorCodes.Invalid_ref_id)
            if tr.amount != new_amount:
                raise SetuError(ErrorCodes.Amount_mismatch)
        else:
            # Update Customers table
            cust = Customers.query.filter_by(custID=tr.custID).first()
            if not cust:
                raise SetuError(ErrorCodes.Customer_not_found)
            if new_amount != cust.amount:
                raise SetuError(ErrorCodes.Amount_mismatch)
            cust.amount = 0
            cust.duedate = ""
            try:
                # Update cust
                db.session.commit()
                tr.transactionID = body["transaction"]["id"]
                tr.amount = new_amount
                tr.date = body["transaction"]["date"]
                # Update tr
                db.session.commit()
            except Exception as e:
                print(e)
                raise SetuError(ErrorCodes.Unhandled_error)
        r = {
                "status": "SUCCESS",
                "data": {       
                    "ackID": tr.refID
                }
            }
        return jsonify(r)
    else:
        raise SetuError(ErrorCodes.Invalid_ref_id)


def verify_request_body(body, expected):
    '''
    Function for verifying if request body is correct.
    Will not check for spurious fields in body that are not required
    '''
    if not body:
        raise SetuError(ErrorCodes.Invalid_api_parameters)
    for k,v in expected.items():
        if k not in body:
            raise SetuError(ErrorCodes.Invalid_api_parameters)
        if type(v) != type(body[k]):
            raise SetuError(ErrorCodes.Invalid_api_parameters)
        if isinstance(v, dict):
            verify_request_body(body[k], v)


if __name__ == '__main__':
    app.run()