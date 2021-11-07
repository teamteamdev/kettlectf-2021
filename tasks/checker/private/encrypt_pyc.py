with open('src_inner.cpython-310.pyc', 'rb') as f:
    contents = f.read()

contents = [int(v) for v in contents]

for i in range(0, len(contents), 2):
    contents[i], contents[i + 1] = contents[i + 1], contents[i]

alphabet = 'dэaдbиeф'

encoded = ''

for i in range(0, len(contents), 3):
    chunk = contents[i:i+3]
    first = chunk[0] >> 5
    second = (chunk[0] >> 2) & 7
    third = (chunk[0] & 3) << 1
    if len(chunk) == 1:
        encoded += alphabet[first]
        encoded += alphabet[second]
        encoded += alphabet[third]
        break
    third += chunk[1] >> 7
    forth = (chunk[1] >> 4) & 7
    fifth = (chunk[1] >> 1) & 7
    sixth = (chunk[1] & 1) << 2
    if len(chunk) == 2:
        encoded += alphabet[first]
        encoded += alphabet[second]
        encoded += alphabet[third]
        encoded += alphabet[forth]
        encoded += alphabet[fifth]
        encoded += alphabet[sixth]
        break
    sixth += (chunk[2] >> 6)
    seventh = (chunk[2] >> 3) & 7
    eightth = chunk[2] & 7
    encoded += alphabet[first]
    encoded += alphabet[second]
    encoded += alphabet[third]
    encoded += alphabet[forth]
    encoded += alphabet[fifth]
    encoded += alphabet[sixth]
    encoded += alphabet[seventh]
    encoded += alphabet[eightth]

encoded = encoded.encode()

with open('src_inner.cpython-310.pyc.enc', 'wb') as f:
    f.write(encoded)
