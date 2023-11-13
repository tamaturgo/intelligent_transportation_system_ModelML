import sqlite3
import os


enum_types = {
    'rule_type': ['speed', 'time', 'stop', 'parking', 'no_entry', 'no_turn'],
    'rule_enable': ['true', 'false']
}


def migrate():
    # Create a connection to the database
    conn = sqlite3.connect('its.db')
    c = conn.cursor()

    # Create the tables
    c.execute('''CREATE TABLE IF NOT EXISTS area
        (id INTEGER PRIMARY KEY, name TEXT, description TEXT, polygon TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS rule
        (id INTEGER PRIMARY KEY, name TEXT, type TEXT, enable BOOLEAN, class TEXT,
        value TEXT, area_id INTEGER, FOREIGN KEY(area_id) REFERENCES area(id))''')
