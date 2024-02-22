''' query.py - sql query for chat.db '''
from __future__ import annotations
import sqlite3
from datetime import datetime, timezone


def find_guid_by_display_name(db, name):
    query = f'''
    SELECT guid
    FROM chat
    WHERE display_name = '{name}'
    '''

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None


def find_chat_identifier(db, name):
    query = f'''
    SELECT chat_identifier
    FROM chat
    WHERE display_name = '{name}'
    '''

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None


def pull_latest_text_message(db, chat):
    query = f'''
    SELECT
    message.text,
    message.date,
    CASE
        WHEN message.is_from_me = 1 THEN 'self'
        ELSE handle.id
    END AS sender_phone_or_email
    FROM message
    JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
    LEFT JOIN handle ON message.handle_id = handle.ROWID
    WHERE chat_message_join.chat_id = (SELECT ROWID FROM chat WHERE guid = '{chat}')
    AND message.text LIKE '@chad%'
    ORDER BY message.date DESC
    LIMIT 1;
    '''
    '''
    SELECT message.text, date, handle.id AS sender_phone_or_email
    FROM message
    JOIN chat_message_join ON message.ROWID = chat_message_join.message_id
    JOIN handle ON message.handle_id = handle.ROWID
    WHERE chat_message_join.chat_id = (SELECT ROWID FROM chat WHERE guid = '{guid}')
    AND message.text LIKE '@chad%'
    ORDER BY message.date DESC
    LIMIT 1;
    '''

    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()

    if result:
        time = convert_timestamp(result[1])
        output = {
            'text': result[0],
            'date': time,
            'sender': result[2]
        }
        return output
    else:
        return None


def convert_timestamp(ns_timestamp):
    # Convert from nanoseconds to seconds
    timestamp_in_sec = ns_timestamp / 1e9

    # Calculate offset from Unix epoch (1970) to macOS epoch (2001) in seconds
    epoch_offset = (datetime(2001, 1, 1, tzinfo=timezone.utc) - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

    # Adjust macOS timestamp to Unix timestamp
    unix_timestamp = timestamp_in_sec + epoch_offset

    # Convert to human-readable format, now using timezone-aware datetime object
    readable_date = datetime.fromtimestamp(unix_timestamp, timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    return readable_date


def wal_checkpoint(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute("PRAGMA wal_checkpoint(FULL);")
    conn.commit()
    conn.close()
