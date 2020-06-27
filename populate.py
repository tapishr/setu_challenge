#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" populate.py: Script used to clear all tables and fill them with sample data from
    users.json and customers.json in the same directory. To run, use - 
    python populate.py
    
    Author: Tapish Rathore
"""
import json
from app import db
from models import Users
from models import Customers
from models import Transactions


with open('users.json') as f:
    users = json.load(f)
Users.query.delete()
for u in users["users"]:
    user = Users()
    user.user = u["user"]
    user.key = u["key"]
    db.session.add(user)
    db.session.commit()
with open('customers.json') as f:
    customers = json.load(f)
Customers.query.delete()
for c in customers["customers"]:
    cust = Customers()
    cust.name = c["customerName"]
    cust.amount = c["dueAmount"]
    cust.duedate = c["dueDate"]
    cust.mobileno = c["mobileNumber"]
    db.session.add(cust)
    db.session.commit()
Transactions.query.delete()