#with open('D:/CDP/testvideo.mp4', 'rb') as input_file:
#with open('D:/CDP/download.jpg', 'rb') as input_file:
with open('D:/CDP/mest.txt', 'rb') as input_file:
    text = input_file.read()

'''
print(text)
print(str(text))

# Convert string to bytes using the bytes() method
bytes_literal = bytes(str(text)[2:-1], 'utf-8')
print(bytes_literal)
'''

with open('D:/CDP/output.txt', "w") as output_file:
    print(str(text))
    output_file.write(str(text))