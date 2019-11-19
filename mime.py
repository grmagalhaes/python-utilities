import filetype

full_file_name = 'teste'
kind = filetype.guess(full_file_name)
print(kind.extension)
print(kind.mime)

full_file_name = 'teste.jpg'
kind = filetype.guess(full_file_name)
print(kind.extension)
print(kind.mime)
