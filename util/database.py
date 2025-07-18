# -*- coding: UTF-8 -*-
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlQueryModel
from util.logger import logger
import datetime

db_path = ''


def get_db_path(path):
    global db_path
    db_path = path


def init_database():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(db_path)
    if not db.open():
        logger.error('database - init_database - Database not open!')
        return False

    query = QSqlQuery()
    query.exec('PRAGMA encoding = "UTF-8"')
    tableStructure = '''CREATE TABLE IF NOT EXISTS pregnant
    (reportId  INTEGER  PRIMARY KEY  AUTOINCREMENT, name  TEXT  NOT NULL, age  INTEGER, pregweek  INTEGER,
     doctor  TEXT  NOT NULL, date  TEXT  NOT NULL, result  TEXT  NOT NULL, report  TEXT  NOT NULL, operation  TEXT)'''
    query.exec(tableStructure)
    tableStructure = '''CREATE TABLE IF NOT EXISTS doctor
    (userId  INTEGER  PRIMARY KEY  AUTOINCREMENT, loginName  TEXT  NOT NULL, password  TEXT  NOT NULL,
     identity TEXT  NOT NULL, cardId  TEXT  NOT NULL, gender  TEXT, department  TEXT,
     loginNumber  INTEGER  NOT NULL, lastTime  TEXT  NOT NULL, operation  TEXT)'''
    query.exec(tableStructure)
    # query.exec(f"insert into pregnant (name, age, pregweek, doctor, date, result, report) values('zhangsan', 23, 23, 'zhaodan', '2024-03-19', 'normal', 'pdf')")
    query.exec("SELECT * FROM doctor WHERE userId = 1")
    if not query.first():
        now = datetime.date.today().strftime('%Y-%m-%d')
        query.exec(
            f"INSERT INTO doctor VALUES(1, 'admin', '123456', 'A', '500000200202240000', 'F', 'Computer', 0, '{now}', 'A')")
        query.exec(
            f"INSERT INTO doctor VALUES(2, 'jzpei', '123456', 'D', '500000200202240001', 'F', 'Computer', 0, '{now}', 'D')")
    logger.info('database - init_database - Database opened!')


def add(table: str, keys: list, values: list):
    try:
        if len(keys) != len(values):
            logger.error('database - add - The length of key and value do not match!')
            return False
        if len(values) == 0:
            logger.error('database - add - No data!')
            return False
        if table not in ['pregnant', 'doctor']:
            logger.error('database - add - Tabel name error!')
            return False

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_path)
        if not db.open():
            logger.error('database - add - Database not open!')
            return False

        query = QSqlQuery()
        sql1 = f"insert into {table} ("
        sql2 = ") values("
        for i in range(len(values)):
            sql1 = sql1 + str(keys[i])
            if isinstance(values[i], str):
                sql2 = sql2 + f"'{values[i]}'"
            else:
                sql2 = sql2 + str(values[i])
            if i < len(values) - 1:
                sql1 = sql1 + ", "
                sql2 = sql2 + ", "
        sql = sql1 + sql2 + ')'
        logger.info(f'database - add -  {sql}')
        query.exec(sql)
        return True
    except Exception as e:
        logger.error(f'database - add - {e}')
        return False


def find(table: str, keys: list, values: list, curPage=-1, pageCount=-1, queryKey=None):
    try:
        if len(keys) != len(values):
            logger.error('database - find - The length of key and value do not match!')
            return [], QSqlQueryModel()
        if table not in ['pregnant', 'doctor']:
            logger.error('database - find - Tabel name error!')
            return [], QSqlQueryModel()

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_path)
        if not db.open():
            logger.error('database - find - Database not open!')
            return [], QSqlQueryModel()

        queryModel = QSqlQueryModel()
        sql = 'SELECT '
        if queryKey is not None:
            if not isinstance(queryKey, list):
                logger.error('database - find - The query key error!')
                return [], QSqlQueryModel()
            for i in range(len(queryKey)):
                sql = sql + queryKey[i]
                if i < len(queryKey) - 1:
                    sql = sql + ', '
        else:
            sql = sql + '*'

        sql = sql + f" FROM {table}"
        results = []
        if len(keys) != 0:
            sql = sql + f" WHERE"
            for i in range(len(keys)):
                if values[i] == '':
                    sql = sql + f" {keys[i]} = NULL"
                elif isinstance(values[i], str):
                    sql = sql + f" {keys[i]} = '{values[i]}'"
                else:
                    sql = sql + f" {keys[i]} = {values[i]}"
                if i < len(values) - 1:
                    sql = sql + " and"
        if curPage != -1 and pageCount != -1:
            sql = sql + f' limit {curPage},{pageCount}'
        elif curPage != -1 or pageCount != -1:
            logger.error(f'database - find -  Pagination query error! curPage: {curPage}, pageCount: {pageCount}')
            return [], queryModel
        logger.info(f'database - find -  {sql}')
        queryModel.setQuery(sql)

        for row in range(queryModel.rowCount()):
            results.append(queryModel.record(row))
        return results, queryModel
    except Exception as e:
        logger.error(f'database - find -  {e}')
        return [], QSqlQueryModel()


def update(table: str, idKay: str, idValue: int, keys: list, values: list):
    try:
        if len(keys) != len(values):
            logger.error('database - update - The length of key and value do not match!')
            return False
        if len(values) == 0:
            logger.error('database - update - No data!')
            return False
        if table not in ['pregnant', 'doctor']:
            logger.error('database - update - Tabel name error!')
            return False

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_path)
        if not db.open():
            logger.error('database - update - Database not open!')
            return False
        query = QSqlQuery()
        sql = f"UPDATE {table} SET"
        for i in range(len(keys)):
            if isinstance(values[i], str):
                sql = sql + f" {keys[i]} = '{values[i]}'"
            else:
                sql = sql + f" {keys[i]} = {values[i]}"
            if i < len(values) - 1:
                sql = sql + ","
        sql = sql + f" WHERE {idKay} = {idValue}"
        logger.info(f'database - update - {sql}')
        query.exec(sql)
        return True
    except Exception as e:
        logger.error(f'database - update - {e}')
        return False


def delete(table: str, idKay: str, idValue: int):
    try:
        if table not in ['pregnant', 'doctor']:
            logger.error('database - delete - Tabel name error!')
            return False
        result, _ = find(table, [idKay], [idValue])
        if len(result) == 0:
            logger.error('database - delete - The data does not exist!')
            return False

        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName(db_path)
        if not db.open():
            logger.error('database - delete - Database not open!')
            return False
        query = QSqlQuery()
        sql = f"DELETE FROM {table} WHERE {idKay} = {idValue}"
        logger.info(f'database - delete - {sql}')
        query.exec(sql)
        return True
    except Exception as e:
        logger.error(f'database - delete - {e}')
        return False

# def print(queryModel):
#     print(queryModel.rowCount())
#     headers = queryModel.record()
#     for i in range(headers.count()):
#         print(headers.fieldName(i), end='\t')
#     print()  # 换行
#
#     # 遍历模型的结果并打印
#     for row in range(queryModel.rowCount()):
#         record = queryModel.record(row)
#         for column in range(record.count()):
#             print(record.value(column), end='\t')
#         print()


# print('init')
# init_database()
