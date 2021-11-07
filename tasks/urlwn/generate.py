#!/usr/bin/env python3

import hmac
import json
import sys

# Remember to change the secret!
SECRET1 = b'f4I26uuQKGk18uTZxQRMALZwuNOesPra'
SALT1_SIZE = 16


def get_user_token(user_id):
    return hmac.new(SECRET1, user_id.encode(),
                    "sha256").hexdigest()[:SALT1_SIZE]


def generate():
    if len(sys.argv) < 3:
        print('Usage: generate.py user_id target_dir', file=sys.stderr)
        sys.exit(1)

    user_id = sys.argv[1]
    token = get_user_token(user_id)

    json.dump({'urls': [f'https://urlwn.{{hostname}}/{token}']}, sys.stdout)


if __name__ == '__main__':
    generate()
