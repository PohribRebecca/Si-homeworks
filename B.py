import socket
from Crypto.Cipher import AES


k3 = b'maNumescRebeccaa'

SERVER = "127.0.0.1"
PORT = 7000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))


#se primeste cheia de criptat
key =  client.recv(1024)
decipher = AES.new(k3, AES.MODE_ECB)
key_deciphered=decipher.decrypt(key)
print("The key received is :" , key_deciphered)

#se primeste vectorul de initializare
iv =  client.recv(1024)
decipher_iv = AES.new(k3, AES.MODE_ECB)
iv_deciphered=decipher_iv.decrypt(iv)
print("The iv received is :" , iv_deciphered)

#aici am vrut sa trimit de la KM modul de criptare, insa nu am reusit deoarece nu era o sincronizare in trimiterea pachetelor, asa ca am cerut reintroducerea modului
print("Reenter the chosen mode ")
mode = input()

confirmation_message= b'maLumescBebeccaa'

#se cripteaza mesajul de confirmare
if mode == 'CBC':
    cipher_CBC = AES.new(key_deciphered,AES.MODE_CBC,iv_deciphered)
    confirmation_message_cyphered=cipher_CBC.encrypt(confirmation_message)


    client.sendall(confirmation_message_cyphered)
elif mode == 'CFB':
    cipher_CFB = AES.new(key_deciphered,AES.MODE_CFB,iv_deciphered)
    confirmation_message_cyphered=cipher_CFB.encrypt(confirmation_message)
    client.sendall(confirmation_message_cyphered)

#se primeste mesajul de confirmare de la KM sau de infirmare
data3 = client.recv(1024)
msg=data3.decode()
print(msg)
clientA = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
PORT2 = 7075

#se initializeaza o comunicare directa cu nodul A in cazul in care raspunsul de la KM este afirmativ
if msg=='Initiate communication':
    blocks=[]
    clientA.connect((SERVER, PORT2))
    block_recv=clientA.recv(1024)
    #se decripteaza fiecare bloc si se recreeaza mesajul printr-o lista la care apendeaza fiecare bloc dupa decriptare
    if mode == 'CBC':
        cipher_CBC = AES.new(key_deciphered,AES.MODE_CBC,iv_deciphered)
        block_dec=cipher_CBC.decrypt(block_recv)
        blocks.append(block_dec)
    if mode == 'CFB':
        cipher_CFB = AES.new(key_deciphered,AES.MODE_CFB,iv_deciphered)
        block_dec=cipher_CFB.decrypt(block_recv)
        blocks.append(block_dec)
    client.sendall(bytes(len(blocks)))
    for block in blocks:
        print (block)
    clientA.close()
    


client.close()