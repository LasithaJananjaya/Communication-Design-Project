def to_raw_string(s):
    return r"{}".format(s)


string = r"C:\Users\john\file.txt"
print(string)
raw_string = to_raw_string(string)
print(raw_string)  # Prints 'C:\\Users\\john\\file.txt'