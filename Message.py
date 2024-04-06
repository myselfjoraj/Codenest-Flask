class Message:

    def __init__(self, id, username, message, timestamp):
        self.id = id
        self.username = username
        self.message = message
        self.timestamp = timestamp
        #self.isMine = isMine

    @staticmethod
    def from_tuple(data_tuple):
        return Message(*data_tuple)

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.message,
            'timestamp': self.timestamp,
            'username': self.username
        }
