class FileModel:

    def __init__(self, id, username, file_name, repo_name, timestamp, file_count, path, uri, modified, size, extension,
                 mode, type):
        self.id = id
        self.username = username
        self.file_name = file_name
        self.repo_name = repo_name
        self.timestamp = timestamp
        self.file_count = file_count
        self.path = path
        self.uri = uri
        self.modified = modified
        self.size = size
        self.extension = extension
        self.mode = mode
        self.type = type

    @staticmethod
    def from_tuple(data_tuple):
        return FileModel(*data_tuple)

