import mimetypes


def get_media_type(name):
    file_extension = name.split('.')[-1]
    media_type, _ = mimetypes.guess_type(f"file.{file_extension}")
    return media_type
