value = 0

with open('D:/CDP/output.txt', 'r') as input_file:
    text = input_file.read()
    print('received               ', text)
    string = text[2:-1]
    print('original               ', string)
    string = r"{}".format(string)
    print('raw                    ', string)

# Convert string to bytes using the bytes() method
bytes_literal = bytes(string, 'utf-8')
print('byte conversion        ', bytes_literal)

'''
bytes_literal = string.encode("utf-8")
print('byte conversion        ', bytes_literal)
'''

'''
json_string = json.dumps(string)
bytes_literal = json.loads(json_string)
print('json                   ', bytes_literal)
'''

#writing the file

if value == 0:
    with open('D:/CDP/reciever_output.txt', 'wb') as file:
        file.write(bytes_literal)

elif value == 1:
    with open('D:/CDP/reciever_output.jpg', 'wb') as file:
        file.write(bytes_literal)

elif value == 2:
    with open('D:/CDP/reciever_output.mp4', 'wb') as file:
        file.write(bytes_literal)
