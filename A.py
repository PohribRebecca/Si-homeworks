import socket
from Crypto.Cipher import AES

#aceasta functie este cea de padare. calculeaza cate caractere mai sunt necesare pana cand lungimea fisierului va fi multiplu de 16, apoi completeaza cu caracterele 0
def padding(string):
    nr_blocs = (16 - len(text_to_pad) % 16) % 16
    string += chr(0) * nr_blocs
    return string

k3 = b'maNumescRebeccaa'


SERVER = "127.0.0.1"
PORT = 7000
PORT2 = 7075
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))

#se trimite modul de criptare dorit
mode = input()
client.sendall(bytes(mode,'UTF-8'))

#se primeste cheia de la KM
key =  client.recv(1024)
decipher_key = AES.new(k3, AES.MODE_ECB)
key_deciphered=decipher_key.decrypt(key)
print("The key received is :" ,key_deciphered)

#se primeste iv de la KM
iv =  client.recv(1024)
decipher_iv = AES.new(k3, AES.MODE_ECB)
iv_deciphered=decipher_iv.decrypt(iv)
print("The iv received is :" ,iv_deciphered)

confirmation_message= b'maLumescBebeccaa'

#Se trimite mesajul de confirmare criptat in functie de modul dorit
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

#se initializeaza o comunicare directa cu nodul B in cazul in care raspunsul de la KM este afirmativ
if msg=='Initiate communication':
   
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((SERVER, PORT))
    server.listen(1)

    clientB, clientAddress = server.accept()
  
    #se creaza o lista ce va primi blocurile de text
    fileBlocks=[]
    #se deschide fisierul si se aplica functia de padare
    uncrypted_file=open('textDeCriptat', 'r')
    padding(uncrypted_file)
    #se imparte fisierul in blocuri de 16 biti atata timp cat este posibil
    while(uncrypted_file):
        block = file.read(16)
        fileBlocks.append(block)
    #se cripteaza fiecare bloc individual si se trimit individual catre B
    if mode == 'CBC':
       cipher_CBC = AES.new(key_deciphered,AES.MODE_CBC,iv_deciphered)
       for block in fileBlocks:
          block=cipher_CBC.encrypt(block)
          clientB.sendall(block)
    if mode == 'CFB':
       cipher_CFB = AES.new(key_deciphered,AES.MODE_CFB,iv_deciphered)
       for block in fileBlocks:
          block=cipher_CFB.encrypt(block)
          clientB.sendall(block)
    clientB.close()
    #se trimite catre KM numarul de blocuri criptate
    client.sendall(bytes(len(fileBlocks)))
else:
    print('We cant communicate any further')

client.close()

