import pyodbc
import datetime
password = '{avidorgilTheBest2022}'
connectionString='Driver={ODBC Driver 17 for SQL Server};Server=tcp:optimusbgudb.database.windows.net,1433;Database=Optimus-BGU-db;Uid=Optimus-BGU-db;Pwd=' + password + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'


def MainTrigger(id:str):
    with pyodbc.connect(connectionString) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
            INSERT INTO
            connections(Date, UserID)
            VALUES('{0}', '{1}');
            """.format(datetime.datetime.now().strftime('%Y%m%d %H:%M:%S'),id))



