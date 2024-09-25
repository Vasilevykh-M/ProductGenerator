import psycopg2

from app.modules.DataBase.DB import DB


class Postgre(DB):
    def __init__(self, url, port, user, password, database):
        super().__init__(url, port, user, password, database)
    def getRows(self, query):

        conn = psycopg2.connect(
            dbname=self._database,
            user=self._user,
            password=self._password,
            host=self._url,
            port=self._port,
        )

        super().getRows(query)

        cursor = conn.cursor()
        cursor.execute(query)

        records = cursor.fetchall()

        cursor.close()
        conn.close()

        return records


    def getRow(self, query):

        conn = psycopg2.connect(
            dbname=self._database,
            user=self._user,
            password=self._password,
            host=self._url,
            port=self._port,
        )

        super().getRow(query)

        cursor = conn.cursor()
        cursor.execute(query)

        record = cursor.fetchone()

        cursor.close()
        conn.close()

        return record


