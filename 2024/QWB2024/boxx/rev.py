import hashlib


def generate_md5(input_string):
    md5_hash = hashlib.md5()
    md5_hash.update(input_string.encode('utf-8'))
    return md5_hash.hexdigest()

input_string = "212139211325313"
md5_value = generate_md5(input_string)
print(f"MD5 value: {md5_value}")

str4 = 'qwb!'
flag = "flag{" + str4 + '_' + md5_value + "}"
print(flag)
