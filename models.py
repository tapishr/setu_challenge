#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" models.py: Module for declaring Tables and columns of the database
    
    Author: Tapish Rathore
"""
from app import db


class Customers(db.Model):
    """
    Class encapsulating customers table, which contains information about customers
    """
    __tablename__ = 'customers'

    name = db.Column(db.String(), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    duedate = db.Column(db.String(), nullable=False)
    mobileno = db.Column(db.String(), index=True, unique=True, nullable=False)
    custID = db.Column(db.Integer, index=True, primary_key=True)


class Transactions(db.Model):
    """
    Class encapsulating transactions table, which records transaction details
    """
    __tablename__ = 'transactions'

    refID = db.Column(db.String(), index=True)
    transactionID = db.Column(db.String())
    custID = db.Column(db.Integer)
    amount = db.Column(db.Float)
    date = db.Column(db.String())
    ID = db.Column(db.Integer, primary_key=True)

    def __init__(self, refID):
        self.refID = refID


class Users(db.Model):
    """
    Class encapsulating users table, which contains information about users of the application
    """
    __tablename__ = 'users'

    user = db.Column(db.String(), nullable=False)
    key = db.Column(db.String(), index=True, unique=True, nullable=False)
    ID = db.Column(db.Integer, primary_key=True)
