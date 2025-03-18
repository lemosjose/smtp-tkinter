from fabric import Connection
import typing

class ConnectionObj:

    def __init__(self, host, user, password=None, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.conn = None

    def connect(self):
        self.conn = Connection(
            host=self.host,
            user=self.user,
            port=self.port,
            #deixando para eventualmente poder usar a chave ssh
            connect_kwargs={"password": self.password}
        )

        return self.conn

    def runUname(self) -> str:
        
        comando = self.conn.run("uname -a", hide=True)
        return comando.stdout.strip
        
