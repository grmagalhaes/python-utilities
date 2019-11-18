import mimetypes

full_file_name = 'teste'
mime = mimetypes.guess_type(full_file_name)
print(mime)

full_file_name = 'teste.jpg'
mime = mimetypes.guess_type(full_file_name)
print(mime)
