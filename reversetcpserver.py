# s.recv()            #接收TCP数据
# s.send()            #发送TCP数据(send在待发送数据量大于己端缓存区剩余空间时,数据丢失,不会发完)
# s.sendall()         #发送完整的TCP数据(本质就是循环调用send,sendall在待发送数据量大于己端缓存区剩余空间时,数据不丢失,循环调用send直到发完)
# s.recvfrom()        #接收UDP数据
# s.sendto()          #发送UDP数据
# s.getpeername()     #连接到当前套接字的远端的地址
# s.getsockname()     #当前套接字的地址
# s.getsockopt()      #返回指定套接字的参数
# s.setsockopt()      #设置指定套接字的参数
# s.close()           #关闭套接字

import socket
import struct #自定义数据包结构
import threading #多线程同时进行

# def recv_header(connection):
#     #一次性还不能完整发过来
#     header = b''
#     while len(header) < 6:
#         chunk = connection.recv(6 - len(header))
#         if not chunk:
#             raise ConnectionError("连接断开，无法接收完整头部")
#         header += chunk
#
#     if(len(header) != 6):
#         print("header出错!!")
#         connection.close()
#
#     return header

def Initialization(connection,addr):
    header = connection.recv(6)
    # header = recv_header(connection)#socket.recv(n) 不保证一定能收到 n 个字节
    # if(header.length() < 6):
    #     print("错误，initialization包头部错误")
    #     connection.close()
    #     return

    recvtype , N = struct.unpack('!HI',header)#'!'表示网络字节序大端序
    if(recvtype!=1):
        print(f"{addr}错误，第一个包应该是Initialization包")
        connection.close()
        return

    print(f"成功接收{addr}Initialization包,type={recvtype},N={N}")

    # try:
    response = struct.pack('!H',2)
    # except Exception as e:
    #     print(f"发送agree错误:{e}")
    connection.sendall(response)

    # N个reverseRequest包
    for i in range(N):
        # 接收每个 reverseRequest 的头部
        header = connection.recv(6)
        # header = recv_header(connection)
        # if len(header) < 6:
        #     print("reverseRequest包头接收不完整")
        #     return

        recvtype, length = struct.unpack('!HI', header)

        if recvtype != 3:
            print(f"{addr}第{i}个包类型错误，应为3")
            return


        # data_bytes = b''
        # while len(data_bytes) < length:
        #     part = connection.recv(length - len(data_bytes))#recv的是二进制
        #     if not part:
        #         print("数据接收中断")
        #         return
        #     data_bytes += part
        data_bytes = b''
        part = connection.recv(length)
        data_bytes += part

        data_str = data_bytes.decode('ascii')
        reversed_str = data_str[::-1]
        print(f"{addr}第{i}个包反转：{reversed_str}")

        reversed_bytes = reversed_str.encode('ascii')
        reply = struct.pack('!HI', 4, len(reversed_bytes)) + reversed_bytes
        connection.sendall(reply)

    print(f"{addr}全部处理完毕，关闭连接")

def client_message(addr,connection):
    print(f"{addr}建立连接")
    try:
        Initialization(connection,addr)#尝试去处理Initialization包
    except Exception as e:
        print(f"{addr}发生错误{e}")
    finally:
        connection.close()

def startTCPserver():
    serversocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    host = '0.0.0.0'
    serverport = 12001
    serversocket.bind((host,serverport))#bind接收元组
    serversocket.listen()
    print("TCP服务器已启动，正在监听")
    while True:
        #填写运行的信息
        connection , addr = serversocket.accept()#accept返回连接请求socket对象和client的（ip，端口号）元组
        thread = threading.Thread(target=client_message, args=(addr, connection))#创建新的线程并且交给clientmessage函数,不能直接在函数后加括号，不是立即执行的
        thread.start()#开启线程

startTCPserver()
