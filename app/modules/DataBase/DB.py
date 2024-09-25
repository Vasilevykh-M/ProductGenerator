class DB:
    def __init__(self, url, port, user, password, database):
        self._url = url
        self._port = port
        self._user = user
        self._password = password
        self._database = database
    def getRows(self, args):
        pass

    def getRow(self, args):
        pass