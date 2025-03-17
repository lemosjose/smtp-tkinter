from fabric import Connection
        
class Connection:

    def __init__(self, host, user, password=None, port=22):
        self.host = host
        self.user = user
        self.password = password
        self.port = port
