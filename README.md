# Project
This is a cryptography hybrid consisting of [RSA](https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjX26zW2Or6AhVX_7sIHTNDAlEQFnoECBIQAQ&url=https%3A%2F%2Fen.wikipedia.org%2Fwiki%2FRSA_(cryptosystem)&usg=AOvVaw0xQnBGXDCOx-cmcc2D4d9O) and [Vigenère](https://en.wikipedia.org/wiki/Vigen%C3%A8re_cipher). 
Vigenère is a symmetric cryptography system, while RSA is asymmetric. That means that Vigenère uses the same key for both encryption and decryption. RSA uses two corresponding keys, one for encryption and one for decryption. Those are usually dubbed
the public key and the private key respectively.

This hybrid system works like this: The program generates a random keyword. The message is encrypted with that keyword using Vigenère.
the keyword is then encrypted with this public key. In order to get the message again, one has to decrypt the keyword using the private key first,
then decrypt the message with this now decrypted keyword.
