#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" exceptions.py: Module containing definitions of errors
    
    Author: Tapish Rathore
"""
from enum import Enum


class SetuError(Exception):
    """
    Generic class for raising excpetions and returning error codes
    """
    response_body = {
        "status": "ERROR",
        "errorCode": ""}
  
    def __init__(self, enumval):
        Exception.__init__(self)
        self.enumval = enumval
        self.error_info = ErrorInfo.get(self.enumval, None)
        if self.error_info:
            hc = self.error_info.get("httpcode", None)
            if hc:
                self.httpcode = hc
            else:
                self.error_info = ErrorInfo[ErrorCodes.Unhandled_error]
                self.httpcode = self.error_info["httpcode"]
        else:
            self.error_info = ErrorInfo[ErrorCodes.Unhandled_error]
            self.httpcode = self.error_info["httpcode"]
    
    def to_dict(self):
        ec = self.error_info.get("errorcode", None)
        if ec:
            self.response_body["errorCode"] = ec
        else:
            self.error_info = ErrorInfo[ErrorCodes.Unhandled_error]
            self.httpcode = self.error_info["httpcode"]
            self.response_body["errorCode"] = self.error_info["errorcode"]
        return self.response_body

class ErrorCodes(Enum):
    Auth_error = 1
    Invalid_api_parameters = 2
    Customer_not_found = 3
    Invalid_ref_id = 4
    Amount_mismatch = 5
    Path_not_found = 6
    Unhandled_error = 7


ErrorInfo = {
    ErrorCodes.Auth_error : {
        "httpcode": 403,
        "errorcode": "auth-error"
    },
    ErrorCodes.Invalid_api_parameters : {
        "httpcode": 400,
        "errorcode": "invalid-api-parameters"
    },
    ErrorCodes.Customer_not_found : {
        "httpcode": 404,
        "errorcode": "customer-not-found"
    },
    ErrorCodes.Invalid_ref_id : {
        "httpcode": 404,
        "errorcode": "invalid-ref-id"
    },
    ErrorCodes.Amount_mismatch : {
        "httpcode": 400,
        "errorcode": "amount-mismatch"
    },
    ErrorCodes.Path_not_found : {
        "httpcode": 404,
        "errorcode": "path-not-found"
    },
    ErrorCodes.Unhandled_error : {
        "httpcode": 500,
        "errorcode": "unhandled-error"
    }
}