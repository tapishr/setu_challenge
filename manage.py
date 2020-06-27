#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" manage.py: Module for managing the app and db servers
    
    Author: Tapish Rathore
"""
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from app import app, db

migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()
