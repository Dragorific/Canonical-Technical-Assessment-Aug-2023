import sqlite3
import json

def create_database():
    connection = sqlite3.connect('audit_log.db')
    cursor = connection.cursor()
    cursor.execute(
        'CREATE TABLE IF NOT EXISTS events ('
        'id INTEGER PRIMARY KEY, '
        'timestamp TEXT, '
        'event_type TEXT, '
        'user_id TEXT, '
        'variant_data TEXT'
        ');'
    )
    connection.commit()
    connection.close()

def add_event(event):
    connection = sqlite3.connect('audit_log.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO events (timestamp, event_type, user_id, variant_data)
    VALUES (?, ?, ?, ?);
    ''', (event.timestamp, event.event_type, event.user_id, json.dumps(event.variant_data)))
    connection.commit()
    connection.close()

def query_events(filter_dict):
    connection = sqlite3.connect('audit_log.db')
    cursor = connection.cursor()
    
    if filter_dict:
        query = 'SELECT * FROM events WHERE ' + ' AND '.join([f"{k} = ?" for k in filter_dict.keys()])
        cursor.execute(query, tuple(filter_dict.values()))
    else:
        cursor.execute('SELECT * FROM events')  # No filters, select all events
    
    results = cursor.fetchall()
    connection.close()
    return [dict(zip(['id', 'timestamp', 'event_type', 'user_id', 'variant_data'], row)) for row in results]
