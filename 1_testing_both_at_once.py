value = 0

#reading the file

if value==2:
    with open('D:/CDP/testvideo.mp4', 'rb') as input_file:
        text = input_file.read()

elif value==1:
    with open('D:/CDP/download.jpg', 'rb') as input_file:
        text = input_file.read()

elif value==0:
    with open('D:/CDP/mest.txt', 'rb') as input_file:
        text = input_file.read()

print(text)


#writing the file

if value == 0:
    with open('D:/CDP/reciever_output.txt', 'wb') as file:
        file.write(text)

elif value == 1:
    with open('D:/CDP/reciever_output.jpg', 'wb') as file:
        file.write(text)

elif value == 2:
    with open('D:/CDP/reciever_output.mp4', 'wb') as file:
        file.write(text)