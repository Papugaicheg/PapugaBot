import pyodbc
import aiogram
import datetime
from multipledispatch import dispatch

connectionString = ("DRIVER={ODBC Driver 17 for SQL Server};""Server=LAPTOP-EPU9MU39\EGORSQL;"
                    "Database = [Курсы иностранных языков];""Trusted_Connection=yes")
# PapugaBot
connection = pyodbc.connect(connectionString, autocommit=True)
db_cursor = connection.cursor()


@dispatch(str, tuple)
async def db_insert(req, par):
    db_cursor.execute(req, par)


@dispatch(str)
async def db_insert(req):
    db_cursor.execute(req)


@dispatch(str, tuple)
async def db_select(req, par):
    db_cursor.execute(req, par)
    req = db_cursor.fetchall()
    return req


@dispatch(str)
async def db_select(req):
    db_cursor.execute(req)
    req = db_cursor.fetchall()
    return req
