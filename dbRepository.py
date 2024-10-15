import logging
import sqlite3
from typing import List


class DbRepository:
    connection = None
    cursor = None  # mistaken use of a class variable

    ProcessedMessageIdTableName = 'ProcessedMessageId'

    def __init__(self, dbFileName: str):
        self.connection = sqlite3.connect(dbFileName)
        self.cursor = self.connection.cursor()

    def checkMessageIdExist(self, messageGroupId: str) -> bool:
        self.cursor.execute(f'SELECT * FROM ProcessedMessageId WHERE messageId = \'{messageGroupId}\'')
        results = self.cursor.fetchall()
        if (len(results) == 0): return False
        return True

    def getTargetChannelUsernames(self) -> List[str]:
        self.cursor.execute(f'SELECT * FROM TargetChannelUsernames')
        results = self.cursor.fetchall()
        usernames = list(map(lambda x: x[1], results))
        return usernames

    def addMessageId(self, messageGroupId: str):
        try:
            self.cursor.execute('BEGIN')
            self.cursor.execute(f'INSERT INTO {self.ProcessedMessageIdTableName} (messageId) VALUES (?)',
                                [messageGroupId])
            self.cursor.execute('COMMIT')
        except Exception as err:
            logging.error(err)
            self.cursor.execute('ROLLBACK')

    def initTables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS StopWords (
            id INTEGER PRIMARY KEY,
            word TEXT NOT NULL
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ProcessedMessageId (
            id INTEGER PRIMARY KEY,
            messageId TEXT NOT NULL
            )
            ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS TargetChannelUsernames (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            title TEXT NOT NULL
            )
            ''')
        self.connection.commit()

    def __del__(self):
        self.connection.close()
