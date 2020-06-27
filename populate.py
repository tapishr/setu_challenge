from app import db
from models import Users
from models import Customers
from models import Transactions


user = Users()
user.user = "Setu"
user.key = "f2550385427e404421b22c3c388f3a57"
db.session.add(user)
db.session.commit()


cust = Customers()
cust.name = "Tapish"
cust.amount = 1323.0
cust.duedate = "12-12-19"
cust.mobileno = "9000090000"
db.session.add(cust)
db.session.commit()


cust2 = Customers()
cust2.name = "Adam"
cust2.amount = 2035.0
cust2.duedate = "1-2-20"
cust2.mobileno = "9008070060"
db.session.add(cust2)
db.session.commit()