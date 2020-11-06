import socket, threading
from Crypto.Cipher import AES


LOCALHOST = "127.0.0.1"
PORT = 7000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))


k3 = b'maNumescRebeccaa'
k1_CBC = b'numeleMeuEsteRbk'
k2_CFB = b'nuStiuSaFacTema!'
iv = b'amNevoieDeAjutor'

#creez cifrul pentru criptarea cheilor si a lui iv
aes = AES.new(k3, AES.MODE_ECB)


#criptarea cheilor si a iv
k1_CBC=aes.encrypt(k1_CBC)
#print ("cheia1 criptata este ",k1_CBC)

k2_CFB=aes.encrypt(k2_CFB)
#print ("cheia2 criptata este ",k2_CFB)

iv=aes.encrypt(iv)
#print ("iv-ul criptat este ",iv)

#decipher = AES.new(k3, AES.MODE_ECB)
#print("cheia1 decriptata este",decipher.decrypt(k1_ECB))

#pornirea comunicarii
server.listen(2)
print("Server started")
print("Waiting for client request..")

#creez conexiunea cu nodul A
clientsockA, clientAddress = server.accept()
print ("New connection added: ", clientAddress)
print("Choose between CBC or CFB")
nodeA =  threading.Thread()
nodeA.start()

#primesc modul de criptare dorit
data = clientsockA.recv(1024)
received_enc_mode = data.decode()
print ("Wanted ecryption mode ", received_enc_mode)


#creez conexiunea cu nodul B
clientsockB, clientAddress = server.accept()
print ("New connection added: ", clientAddress)
nodeB = threading.Thread()
nodeB.start()


#trimit cheia corecta modului ales
if received_enc_mode == 'CBC':
    
    clientsockA.sendall(k1_CBC)
    clientsockA.sendall(iv) 
    clientsockB.sendall(k1_CBC)
    clientsockB.sendall(iv)
elif received_enc_mode == 'CFB':
    
    clientsockA.sendall(k2_CFB)
    clientsockA.sendall(iv) 
    clientsockB.sendall(k2_CFB)
    clientsockB.sendall(iv)
  
mode2=received_enc_mode

confirmation_message_cyphered_CBC=''
confirmation_message_cyphered_CFB=''

#se compara mesajele primite de la fiecare nod si se da ok-ul pentru comunicarea securizata
if mode2 == 'CBC':
   
    testA_recv = clientsockA.recv(1024)
    cipher_CBC = AES.new(k1_CBC,AES.MODE_CBC,iv)
    testA = cipher_CBC.decrypt(testA_recv)

    testB_recv = clientsockB.recv(1024)
    cipher_CBC = AES.new(k1_CBC,AES.MODE_CBC,iv)
    testB = cipher_CBC.decrypt(testB_recv)
  
    if testA == testB:
         print("criptare cu succes")
         clientsockA.sendall(bytes('Initiate communication','UTF-8'))
    else:
        print("nu a avut loc o criptare corecta")
elif mode2 == 'CFB':
    testA_recv = clientsockA.recv(1024)
    cipher_CFB = AES.new(k2_CFB,AES.MODE_CFB,iv)
    testA = cipher_CFB.decrypt(testA_recv)

    testB_recv = clientsockB.recv(1024)
    cipher_CFB = AES.new(k2_CFB,AES.MODE_CFB,iv)
    testB = cipher_CFB.decrypt(testB_recv)

    if testA == testB:
         print("criptare cu succes")
         clientsockA.sendall(bytes('Initiate communication','UTF-8'))
         clientsockB.sendall(bytes('Initiate communication','UTF-8'))

    else:
        print("nu a avut loc o criptare corecta")

#se primeste numarul de blocuri criptate de la A

blocksA=clientsockA.recv(1024)
nr_blocksA=blocksA.decode()
print(nr_blocksA," were send and decrypted from A")

#se primeste numarul de blocuri criptate de la B
blocksB=clientsockB.recv(1024)
nr_blocksB=blocksB.decode()
print(nr_blocksB," were send and decrypted from A")

#se compara numarul de blocuri criptate de la fiecare nod si se ofera un mesaj specific
if nr_blocksA == nr_blocksB:
  print("File successfully encrypted")
else:
  print("Failed to encrypt the file")


nodeA.join()
nodeB.join()

