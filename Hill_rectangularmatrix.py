#IMPLEMENTING KEY MATRIX AS RECTANGULAR MATRIX (I.E 1X3 MATRIX):

from tkinter import *
from tkinter.font import BOLD
from PIL import ImageTk, Image
import numpy as np
import math

root = Tk()
root.title('Hill Cipher GUI')
root.geometry("959x535")
root.resizable(False,False)

background_image = ImageTk.PhotoImage(Image.open("bg.jpg"))
background_label = Label(image=background_image,height=400,width=400)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

def pad_message(message, n):  #message, block size - n, Returns padded message i.e the length of the text should be divisible by order of key matrix
    mes_len = len(message)
    if (mes_len % 3) != 0:
        pad_len = 3 - (mes_len % 3)
        message_padded = message + pad_len*'z'
        return message_padded
    return message

def convert_msg(message, n): #Converts a message into corresponding numbers and returns a list of the blocks of message.
    mes = convert_to_num(message)
    mes_blocks = [] 
    #print(mes)
    temp = np.reshape(mes, (1, 3))
    print(temp)
    mes_blocks.append(temp)
    print(mes_blocks)
    #print(np.array(mes_blocks))
    return mes_blocks

def convert_msg1(message, n): #Converts a message into corresponding numbers and returns a list of the blocks of message.
    mes = convert_to_num(message)
    mes_blocks = [] 
    #print(mes)
    temp = np.reshape(mes, (3, 3))
    print(temp)
    mes_blocks.append(temp)
    print(mes_blocks)
    #print(np.array(mes_blocks))
    return mes_blocks

def convert_to_num(l): #Returns a list of corresponding numbers. Eg, abz -> [0, 1, 25]
    return [(ord(c)-97) for c in l]

def invert_key(k): #Returns the inverted key matrix accouding to Hill Cipher algorithm.
    #det=np.linalg.solve(k.T.dot(k), k.T)
    #det = int(np.round(np.linalg.det(k)))
    det = np.linalg.pinv(k)
    #print(det)
   # det_inv = multiplicative_inverse(det % 26)
    #print(det_inv)
    #k_inv = det_inv * np.round(det*np.linalg.inv(k)).astype(int) % 26
    #print(k_inv)
    det=np.reshape(det, (1, 3))
    return det

def multiplicative_inverse(det): # Returns d_inv according to (d*d_inv = 1 mod 26)
    mul_inv = -1
    for i in range(26):
        inverse = det * i
        if inverse % 26 == 1:
            mul_inv = i
            break
    return mul_inv

def encrypt(k, m): #Argument: key matrix k, list of message blocks m, Returns encrypted message
    msg = []
    print(m)
    for block in m:
        print(block)
        temp = k.dot(block) % 26 + 97  #dot product of key and message matrix
        msg.append(temp)
        #print(k)
    msg = np.array(msg).flatten()
    enc_msg = [chr(n) for n in msg]  #converting to chr from number
    #print(enc_msg)
    return "".join(enc_msg)


def show_encrypt():
    key = 'nhi'          #Key text that is converted to key matrix
    key_len = len(key)
    n = int(math.sqrt(key_len))  #Since the length of text to be square because we are using key matrix as square

    # convert key text to matrix
    k = np.array(convert_to_num(key))
    k = np.reshape(k, (3, 1))
    print(k)

    message = text_entry.get()     #to get string entered in gui
    text_entry.delete(0,END)       #to delete the entered text in entered place
    decrypt_entry.delete(0,END)    #to delete the entered text encrypted text place
    message = message.replace(" ","") #to remove all spaces
    mes_len = len(message)      #to find the length of the entered string
    message_padded = pad_message(message,n)
    mes = message_padded.lower() #To convert all to lowercase
    m = convert_msg(mes, n)

    encrypted_msg = encrypt(k, m)
    decrypt_entry.insert(0,encrypted_msg)

def decrypt(k, m): #Argument: key matrix k, list of encrypted message blocks m,  Returns decrypted message
    k_inv = invert_key(k)
    msg = []
    for block in m:
        #print(block)
        temp = k_inv.dot(block) % 26 + 97  #To get back string by finding dot product of key matrix and cipher text
        msg.append(temp)
    msg = np.array(msg).flatten()
    dec_msg = [chr(int(n)) for n in msg]
    return "".join(dec_msg)  #to return decrypted text


def show_decrypt():
    key = 'nhi'  #Key text that is converted to key matrix
    key_len = len(key)
    n = int(math.sqrt(key_len)) #Since the length of text to be square because we are using key matrix as square
    # convert key to matrix
    k = np.array(convert_to_num(key))
    k = np.reshape(k, (1, 3)) #to reshape into square matrix

    msg_received = decrypt_entry.get()  #to get encrypted string
    text_entry.delete(0,END)  #to delete the entered text in entered place
    decrypt_entry.delete(0,END) #to delete the encrypted text in entered place
    mr = convert_msg1(msg_received, 3)
    decrypted_msg = decrypt(k, mr)

    text_entry.insert(0,decrypted_msg)

text_entry = Entry(root,width=30,font=("Helvetica",20),)  #To enter a string that has to be encrypted
text_entry.grid(row=0,column=1,padx=250,pady=(200,0))

text_entry_label = Label(root,text="Enter Text: ",font=("Helvetica",20,BOLD),background="#ffccb3",foreground="#660033") 
text_entry_label.grid(row=0,column=0,padx=5,pady=(200,0))

encrypt_btn = Button(root,text="Encrypt Text",font=("Helvetica",15,BOLD),bg="black",fg="white",command=show_encrypt)  #Button to encrypt the typed string
encrypt_btn.grid(row=1,column=1,pady=(8,0))


decrypt_entry = Entry(root,width=30,font=("Helvetica",20))  #Encrypted cipher text will be displayed here, these text can be decrypted using decrypt button
decrypt_entry.grid(row=5,column=1,padx=20,pady=(20,0))

decrypt_entry_label = Label(root,text="Encrypted Text: ",font=("Helvetica",20,BOLD),background="#ffccb3",foreground="#660033")
decrypt_entry_label.grid(row=5,column=0,padx=5,pady=(20,0))

decrypt_btn = Button(root,text="Decrypt Text",font=("Helvetica",15,BOLD),bg="black",fg="white",command=show_decrypt)   #Button to decrypt the typed string
decrypt_btn.grid(row=6,column=1,pady=(8,0))

root.mainloop()