# DIP-Steganography

This implementation focuses on using the LSB steganography algorithms to encode secret data in images. The GUI is built using Tkinter. I used the [Stegano library](https://pypi.org/project/stegano/) for implementing most of the LSB algorithms and respective sets. I also used the [DCT algorithm](https://github.com/neivin/stego/blob/master/DCT.py) for encoding and decoding data. In my implementation setup I have two folders *'image'* and *'secret'* for storing raw image/text files and encoded/decoded image/text files. You will find the corresponding storage/retrieval code in window.py.