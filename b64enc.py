import base64

string = input("")
encoded = base64.b64encode(bytes(string, 'utf-8'))
f = open('pw', 'w')
f.write(str(encoded))
f.close()