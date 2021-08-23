import socketserver
import sys
import os
import pathlib
import html
import re
from base64 import b64encode
from hashlib import sha1
import pymysql
import binascii
from binascii import unhexlify
import bcrypt
import secrets

db = pymysql.connect(db="userdb",host='db', user='root', password='Hbcheng?51' , charset='utf8mb4')
cur = db.cursor()
cur.execute("create table  IF NOT EXISTS chat (username varchar(200) NOT NULL);")
cur.execute("create table  IF NOT EXISTS Register (username varchar(200) NOT NULL, password varchar(200) NOT NULL,token varchar(200) NOT NULL);")

db.commit()
cur.execute("alter table userdb.chat convert to character set utf8mb4 collate utf8mb4_bin;")
cur.execute("alter table userdb.Register convert to character set utf8mb4 collate utf8mb4_bin;")

class MyTCPHandler(socketserver.BaseRequestHandler):
    clients=[]
    client_sockets=[]
    port=[]
    old_history=bytearray()
    cookie_list=[]
    user_cookie=[]
    user_token=[]
    login_user=[]
    current_user_token=[]
    current_token=''
    def handle(self):


                data =self.request.recv(2048)
                client_id = self.client_address[0] + ":" + str(self.client_address[1])
                #print(client_id+ " is sending data:")              
                #print("\n\n")
                new = data.decode('UTF-8') 
                #print(new)
                sys.stdout.flush()
                lines =((new).splitlines())
                requestLine = lines[0]
                parts= (requestLine).split(' ')
                requestType = parts[0]
                requestPath =parts[1]
                version = parts[2]
                #print(requestLine)
                #print (requestType)
                #print (requestPath)
                #print (version)
                list_tem=[]
                new1=[]
                key=["name=","images="]
                p_name=["Mitch"]
                for path in pathlib.Path("images").iterdir():
                    if path.is_file() and str(path).endswith(".jpg") :
                        list_tem+=[os.path.splitext(str(path))]
                        new =os.path.basename(str(path))
                        new1.append(os.path.splitext(new)[0])

                if requestType=="GET" and requestPath=="/":
                    path ="static/index.html" 
                    current_file=open(path)
                    l=current_file.read()
                    self.request.sendall("HTTP/1.1 200 ok\r\nContent-Type: Text/html;charset=utf-8;\r\n".encode())
                    self.request.sendall("X-Content-Type-Options: nosniff\r\n".encode())
                    print(self.current_user_token)

                    if not self.current_user_token:
                        self.request.sendall(b"Set-Cookie:id=X6kAwpgW29M;\r\n")
                    else:
                        print('delete')
                        cur.execute("SELECT * FROM Register WHERE username =(%s)", self.login_user[-1])
                        name=cur.fetchone()
                        if 'id=X6kAwpgW29M' in self.user_cookie:
                                self.user_cookie.remove('id=X6kAwpgW29M')
                                self.user_cookie.append(name[2])
                                self.current_token=name[2]
                            
                    self.request.sendall("Content-length:".encode() + (str(len(l))).encode() + "\r\n\r\n".encode())
                    if not self.user_cookie:
                        print("it is empty")
                        with open('static/index.html','r') as pic_html:
                            content=pic_html.read()
                        self.request.sendall(content.encode())
                    else:
                        print("it is not empty")
                
                        print(self.user_cookie)
                        print(self.current_token)
                        if 'id=X6kAwpgW29M' in self.user_cookie:
                                print('in id')
                                with open('static/index.html','r') as pic_html:
                                    content1=pic_html.read()
                                    content1 = content1.replace(re.findall("<h2 id=\"A\">welcome!</h2>",content1)[0],"<h2 id=\"A\">welcome back!</h2>")
                                    pic_html.close()
                                self.request.sendall(content1.encode())
                        else:
                                    with open('static/index.html','r') as pic_html:
                                        print('enter1')
                                        content1=pic_html.read()
                                        content1 = content1.replace(re.findall("<h2 id=\"A\">welcome!</h2>",content1)[0],"<h2 id=\"A\"> "+name[0]+" welcome back!</h2>")
                                        pic_html.close()
                                    self.request.sendall(content1.encode())


                    header=b'Cookie'
                    print("received header:")
                    new = data.split(b'\r\n')
                    cookie_str=next((s for s in new if header in s), None)
                    string= cookie_str.decode('UTF-8').replace('Cookie: ','')
                    cookie=string.split('; ')
                    i=0
                    while i<len(cookie):
                        if cookie[i] in self.user_cookie:
                            continue
                        else:
                            self.user_cookie.append(cookie[i])
                        i+=1
                    print(self.user_cookie)
                    #browser set the cookie and remember                

                if requestType=="GET" and (requestPath=="/bonus" ):
                    path ="bonus/bonus.html" 
                    current_file=open(path,"rb")
                    l=current_file.read()
                    self.request.sendall("HTTP/1.1 200 ok\r\nContent-Type: Text/html;charset=utf-8;\r\n".encode())
                    self.request.sendall("X-Content-Type-Options: nosniff\r\n".encode())
                    self.request.sendall("Content-length: ".encode() + str(len(l)).encode() + "\r\n\r\n".encode())
                    self.request.sendall(l) 
                    current_file.close()

                if requestType=="GET" and requestPath=="/hello":
                    self.request.sendall("HTTP/1.1 200 ok\r\nContent-Type: Text/plain\r\nContent-length: 5\r\n\r\nhello".encode())

                
                if requestType=="GET" and requestPath=="/hi":
                    self.request.sendall("HTTP/1.1 301 Move Permanently\r\nLocation: /hello\r\nContent-Type: Text/plain\r\nContent-length: 5\r\n\r\nhello".encode())
            
                if requestType=="GET" and requestPath=="/utf.txt":
                    filename= 'static/utf.txt'
                    f= open(filename,'rb')
                    l=f.read()
                    self.request.sendall("HTTP/1.1 200 ok\r\nContent-Type: Text/plain;charseT=UTF-8\r\n".encode())
                    self.request.sendall("Content-length: ".encode() +str(len(l)).encode()+"\r\n\r\n".encode())
                    self.request.sendall(l)


                if requestType=="GET" and requestPath.endswith(".jpg") :
                    if "images" not in requestPath and 'bonus' not in  requestPath:
                            print(requestPath)
                            current_file=open("image/flamingo.jpg","rb")
                            l=current_file.read()
                            self.request.sendall("HTTP/1.1 200 ok\r\nContent-Type: image/jpg;charset=utf-8\r\n".encode())
                            self.request.sendall("X-Content-Type-Options: nosniff\r\n".encode())
                            self.request.sendall("Content-length: ".encode() + str(len(l)).encode() + "\r\n\r\n".encode())
                            self.request.sendall(l) 
                            current_file.close()
                    
                    if "bonus" in requestPath:      
                            if path.is_file() :
                                current_file=open('bonus/bonus.jpg',"rb")
                                l=current_file.read()
                                self.request.send("HTTP/1.1 200 ok\r\nContent-Type: image/jpg;charset=utf-8;\r\n".encode())
                                self.request.sendall("X-Content-Type-Options: nosniff\r\n".encode())
                                self.request.send("Content-length: ".encode() + str(len(l)).encode() + "\r\n\r\n".encode())
                                self.request.send(l) 
                                current_file.close()
                    else:
                        for path in pathlib.Path("images").iterdir():        # get the any image  
                            if path.is_file() and 'images'  in requestPath:
                                new=data.decode('UTF-8')
                                lines=new.split('\r\n')
                                name=lines[0].split(' ')
                                filename =name[1]
                                newpath= str(path)
                                pathname = newpath.replace("\\","/")
                                if pathname == filename[1:]:
                                    current_file=open(path,"rb")
                                    l=current_file.read()
                                    self.request.send("HTTP/1.1 200 ok\r\nContent-Type: image/jpg;charset=utf-8;\r\n".encode())
                                    self.request.sendall("X-Content-Type-Options: nosniff\r\n".encode())
                                    self.request.send("Content-length: ".encode() + str(len(l)).encode() + "\r\n\r\n".encode())
                                    self.request.send(l) 
                                    current_file.close()

                if requestType=="GET" and requestPath.endswith(".js") :  
                    for path in pathlib.Path("static").iterdir():        
                        if path.is_file() and str(path).endswith(".js") :
                            current_file=open(path,"rb")
                            l=current_file.read()
                            self.request.send("HTTP/1.1 200 ok\r\nContent-Type: text/javascript;charset=utf-8;\r\n".encode())
                            self.request.sendall("X-Content-Type-Options: nosniff\r\n".encode())
                            self.request.send("Content-length: ".encode() + str(len(l)).encode() + "\r\n\r\n".encode())
                            self.request.send(l) 
                            current_file.close()
                
                if requestType=="GET" and requestPath.endswith(".css") :  
                    for path in pathlib.Path("static").iterdir():        
                        if path.is_file() and str(path).endswith(".css") :
                            current_file=open(path,"rb")
                            l=current_file.read()
                            self.request.send("HTTP/1.1 200 ok\r\nContent-Type: text/css;charset=utf-8;\r\n".encode())
                            self.request.sendall("X-Content-Type-Options: nosniff\r\n".encode())
                            self.request.send("Content-length: ".encode() + str(len(l)).encode() + "\r\n\r\n".encode())
                            self.request.send(l) 
                            current_file.close()



            #HW3
                if requestType=="POST"  and requestPath=="/comment" :
                    self.request.sendall(b' HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n')
                    new = data.decode('UTF-8') 
                    sys.stdout.flush()
                    lines =((new).split('\r\n\r\n'))
                    name =lines[2].split('\r\n')    
                    comment =lines[3].split('\r\n') 
                    f= open('static/data.txt','wb')
                    l=f.write(data)
                    f.close()
                    self.request.sendall(html.escape((name[0])+'\r\n'+comment[0]).encode())

                if requestType=="POST"  and requestPath=="/comment1" :
                    self.request.sendall(b' HTTP/1.1 301 Move Permanently\r\nLocation: / \r\nContent-Type:text/html\r\n\r\n')
                    new = data.decode('UTF-8') 
                    lines =((new).split('\r\n\r\n'))
                    name =lines[2].split('\r\n')    
                    comment =lines[3].split('\r\n') 
                    f= open('static/data.txt','a')
                    l=f.write('\r\n'+name[0]+' '+comment[0])
                    f.close()
                    self.request.sendall(html.escape((name[0])+'\r\n'+comment[0]).encode())
            
            
                if requestType=="POST"  and requestPath=="/image-upload" : 
                            self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\n\r\n')
                            body =b''   
                            new=data
                            while True:   # keep receive file 
                                if(len(new)>=1000 and len(new)<=1093):
                                    
                                    print("not enter")       
                                    data1 =self.request.recv(1024)                        
                                    print(" enter")
                                    if data1.endswith(b"--\r\n") :
                                        body+=(data1)
                                        break
                                    body+=(data1)                 
                                else:
                                    break
                            #print(body)
                            all_data=new+body
                            #print(all_data)
                            caption=''
                            bound1=''
                            if(len(body)!=0):
                                new1=new.split(b'\r\n')
                                lines =((body).split(b'\r\n\r\n'))
                                bound1=lines[-1].split(b'\r\n')
                                picture=lines[1].split(b'\r\n')
                                caption=bound1[0].decode('UTF-8')
                                pic_part=lines[0].split(b'\r\n\r\n')
                                pic_part1=pic_part[-1].split(b';')
                                pic_name=pic_part1[2].split(b'"')
                                path= 'images/'+pic_name[1].decode('UTF-8')
                                fout=open(path,'wb')
                                fout.write(picture[0])
                                fout.close()
                                with open('static/image-upload.html','r') as pic_html:
                                    len_html=pic_html.read().format(pictures=pic_name[1].decode('UTF-8'),caption=html.escape(caption))
                                print(pic_name[1])
                                self.request.sendall(len_html.encode())

                            else:
                                lines=all_data.split(b'\r\n\r\n')
                                bound1=lines[-1].split(b'\r\n')
                                caption=bound1[0].decode('UTF-8')
                                self.request.sendall(html.escape(caption).encode())

                #HW3 OBJ4
                if requestType=="POST"  and requestPath=="/image-upload":   
                            self.request.sendall(b'HTTP/1.1 301 Move Permanently\r\nLocation: / \r\n\r\n')
                            body =b''   
                            new=data
                            while True:   # keep receive file 
                                if(len(new)>=1090 and len(new)<=1093):
                                    
                                    data1 =self.request.recv(1024)                        
                                    if data1.endswith(b"--\r\n") :
                                        body+=(data1)
                                        break
                                    body+=(data1)                 
                                else:
                                    break
                            #print(body)
                            all_data=new+body
                            #print(all_data)
                            caption=''
                            bound1=''
                            if(len(body)!=0):
                                new1=new.split(b'\r\n')
                                lines =((body).split(b'\r\n\r\n'))
                                bound1=lines[-1].split(b'\r\n')
                                picture=lines[1].split(b'\r\n')
                                caption=bound1[0].decode('UTF-8')
                                pic_part=lines[0].split(b'\r\n\r\n')
                                pic_part1=pic_part[-1].split(b';')
                                pic_name=pic_part1[2].split(b'"')
                                path= 'images/'+pic_name[1].decode('UTF-8')
                                fout=open(path,'wb')
                                fout.write(picture[0])
                                fout.close()
                                with open('static/index.html','r') as pic_html:
                                    len_html=pic_html.read().format(pictures=pic_name[1].decode('UTF-8'),caption=html.escape(caption))
                                    
                                self.request.sendall(len_html.encode())
                                
                            else:
                                lines=all_data.split(b'\r\n\r\n')
                                bound1=lines[-1].split(b'\r\n')
                                caption=bound1[0].decode('UTF-8')
                                self.request.sendall(html.escape(caption).encode())


           
        # Hw4

                if requestType=="GET"  and requestPath=="/websocket":
                        self.clients.append(client_id)
                        self.client_sockets.append(self.request)
                        self.port.append(self.client_address[1])
                        # print("Client:")
                        # print(self.clients)
                        # print(str(self.client_address[1]))
                        current_port =str(self.client_address[1]) 
                        GUID = b"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
                        key =(re.search(b'Sec-WebSocket-Key:\s+(.*?)[\r\n]+', data).groups()[0].strip())
                        print("database:")
                        response_key = b64encode(sha1(key + GUID).digest())
                        self.request.sendall(b"HTTP/1.1 101 Switching Protocols\r\n")
                        self.request.sendall(b'Upgrade: websocket\r\nConnection: Upgrade\r\n')
                        self.request.sendall(b"Sec-WebSocket-Accept:"+response_key +b"\r\n\r\n")                     
                        # cur.execute("SELECT username FROM chat")
                        #fect data from the local data structure
                        self.request.sendall((self.old_history))


                        #fetch data from the database
                        row = cur.fetchall()                     
                        for tuple_row in row:
                            for y in tuple_row:
                                print(y)
                                self.request.sendall(unhexlify(y))
                        print("Get the history")
                        try:

                            while(True):
                                current_port =str(self.client_address[1]) 
                                # print("current port:" + current_port)
                                # print(self.port)
                                message=bytearray()
                                demessage=bytearray()
                                raw_data=bytearray()
                                masks_key=bytearray()
                                data1 =self.request.recv(2048)
                                # print(data1)
                                # print(len(data1))
                                payload =data1[1] & 0x7F
                                index_position=2
                                if data1[0]!=129:
                                    continue
                                #Client-Server
                                message.append(129)
                                mask_position=0
                                if payload<126:
                                    message.append(0x80+payload)
                                   
                                if payload==126:
                                    index_position=4
                                    message.append(126)
                                    message.append(payload)
                                
                                if payload==127:
                                    index_position=10
                                l=0
                                index_mask=index_position+4
                                while index_position<index_mask:
                                    masks_key.append(data1[index_position])
                                    message.append(data1[index_position])
                                    index_position+=1
                                    print(bin(masks_key[l]))
                                    l+=1

                                # print('\n')
                                # print(index_position)
                                # print("\n masked data:") 
                                while index_position < len(data1): # get the masked data
                                    masked_data =data1[index_position] ^ masks_key[mask_position % 4]
                                    print("_"+ bin(masked_data),end='')
                                    message.append(masked_data)
                                    raw_data.append(masked_data)
                                    index_position+=1
                                    mask_position+=1  
                                    

                                ## Server-client
                                # print('\nServer-client\n')
                                # print(len(raw_data))
                                demessage.append(129)
                                index=0
                                if len(raw_data)<126:
                                    demessage.append(len(raw_data))
                                    index=2
                                elif payload>=126 and payload<=65535:
                                    demessage.append(126)
                                    demessage.append((len(raw_data) >>8) & 255)
                                    demessage.append(len(raw_data) & 255)
                                    index=4
                                else:
                                    demessage.append(127)
                                    demessage.append((len(raw_data)>> 56)& 255)
                                    demessage.append((len(raw_data)>> 48)& 255)
                                    demessage.append((len(raw_data)>> 40)& 255)
                                    demessage.append((len(raw_data)>> 32)& 255)
                                    demessage.append((len(raw_data)>> 24)& 255)
                                    demessage.append((len(raw_data)>> 16)& 255)
                                    demessage.append((len(raw_data)>> 8)& 255)
                                    demessage.append((len(raw_data)>> 0)& 255)
                                    index=10
                                
                                demessage+=raw_data
                                self.request.sendall(demessage)
                                # store data to local data structure
                                self.old_history+=demessage
                                # print(demessage)
                                # print("the length of raw_data")
                                # print(self.old_history)
                                # print(raw_data)



                                #store data to SQL database
                                if len(raw_data)!=0:
                                     byte_demessage=bytes(demessage)
                                     hex_demessage=binascii.hexlify(byte_demessage).decode('utf-8')
                                     cur.execute("INSERT INTO chat(username) VALUES(%s)",hex_demessage)
                                     db.commit()

                        except:
                            print("connection is close by client")
                            pass
        


        #HW5

                if requestType=="POST"  and requestPath=="/Register" : 
                        print('register')
                        print(data)
                        new = data
                        sys.stdout.flush()
                        lines =((new).split(b'\r\n\r\n'))
                        pass_str =lines[3].split(b'\r\n') 
                        user_str =lines[2].split(b'\r\n')   
                        salt= bcrypt.gensalt() 
                        print(pass_str[0])
                        print(user_str[0])
                        print((bcrypt.hashpw(pass_str[0],salt)))
                        print((bcrypt.hashpw(pass_str[0],salt)).decode('utf-8'))
                        username=user_str[0]
                        password=bcrypt.hashpw(pass_str[0],salt)
                        if not pass_str[0] or not user_str[0]:
                            self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-length: 52\r\n\r\n<h1>Fail: Username or Password can not be empty</h1>')
                        else:
                            token = secrets.token_urlsafe(81)
                            self.current_user_token.append(token)
  
                            self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-length: 30\r\n\r\n<h1>Register Successfully</h1>')

                            cur.execute("SELECT * FROM Register")
                            password=password.decode('utf-8')
                            cur.execute("INSERT INTO Register(username,password,token) VALUES(%s,%s,%s)",(username,password,token))
                            db.commit()

                            #check same registration
                            #if the token with no username, it is vaild user send 403
                if requestType=="POST"  and requestPath=="/Login" : 
                        
       
                        print('Login')
                        new = data
                        sys.stdout.flush()
                        lines =((new).split(b'\r\n\r\n'))
                        pass_str =lines[3].split(b'\r\n') 
                        user_str =lines[2].split(b'\r\n')   
                        print(pass_str[0])
                        print(user_str[0])
                        username=user_str[0]
                        password=pass_str[0]       
                        username1 =username.decode('utf-8')
                        print('password')
                        print(password)               
                        if not pass_str[0] or not user_str[0]:
                            self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-length: 52\r\n\r\n<h1>Fail: Username or Password can not be empty</h1>')
                        

                        else:
                            cur.execute("SELECT * FROM Register WHERE username =(%s)", username)
                            name=cur.fetchone()

                            print("fectch name")
                            print(name)
                            print("going")

                            if name is None:
                                print("name is none")
                                self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-length: 31\r\n\r\n<h1>Username does not exit</h1>')
                            print('username')
                            print(name[0])
                            print(username1)
                            if bcrypt.checkpw(password, name[1].encode()):
                                    print("matched")
                                    token = secrets.token_urlsafe(81)
                                    if not self.login_user:
                                        print("none")
                                    print(self.login_user)
                                    if username1 in self.login_user:
                                        self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-length: '+ str(len(username1)+36).encode()+b'\r\n\r\n<h1>User '+username+b' is already logged in!</h1>')                                  
                                    else:
                                        self.login_user.append(username1)
                                    print(name[2])
                                    self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nSet-Cookie:id='+name[2].encode()+b';\r\nContent-length:'+str(len(username1)+28).encode()+b'\r\n\r\n<h1>'+username+b' Login successfully</h1>')
                                    self.current_user_token.append(name[2])
                            else:
                                self.request.sendall(b'HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-length: 48\r\n\r\n<h1>Fail: Username or Password is incorrect</h1>')

                                    

                            
if __name__=="__main__":
    host= "0.0.0.0"
    port = 8000

    server=socketserver.ThreadingTCPServer((host,port),MyTCPHandler)
    server.serve_forever()