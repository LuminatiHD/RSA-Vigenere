"""An implementation of a Vigenère-RSA-hybrid encryption scheme"""
from rsa import Keys
from rsa import encrypt
from rsa import decrypt

while True:
    mode = int(input("Mode: (generate keys [0], encrypt [1], decrypt [2]), or exit [3]: "))

    if mode == 0:
        public = input("public key path: ")
        private = input("private key path: ")
        min_len = int(input("minimum bit length: "))
        Keys.main(public, private, min_len)

    elif mode == 1:
        key_path = input("key path: ")
        msg_path = input("message path: ")
        out_path = input("output path: ")
        keyword_path = input("keyword path: ")
        encrypt.main(msg_path, out_path, key_path, keyword_path)

    elif mode == 2:
        key_path = input("key path: ")
        msg_path = input("message path: ")
        out_path = input("output path: ")
        keyword_path = input("keyword path: ")
        decrypt.main(msg_path, out_path, key_path, keyword_path)

    else:
        print("shutting down...")
        break
