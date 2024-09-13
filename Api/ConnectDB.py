import pymysql

def Connect():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='tourneyhub_db',
            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception:
        pass
def ConnectSocial():
    try:
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='social',
            cursorclass=pymysql.cursors.DictCursor)
        return connection
    except Exception:
        pass