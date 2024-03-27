class Message:

    def __init__(self, id,username,name,message,timestamp,isMine):
        self.id = id
        self.username = username
        self.name = name
        self.message = message
        self.timestamp = timestamp
        self.isMine = isMine

    @staticmethod
    def from_tuple(data_tuple):
        return Message(*data_tuple)
