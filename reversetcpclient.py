import socket
import random
import struct #自定义数据包结构

def reverseRequest(clientsocket  , pieces):
    count = 0#包的序号（从零开始）
    reversefile = []#翻转的数据块
    for i in pieces:


        data_bytes = i.encode('ascii')
        Length = len(data_bytes)
        pack = struct.pack('!HI',3,Length) + data_bytes
        clientsocket.sendall(pack)


        header = clientsocket.recv(6)
        recvtype, length = struct.unpack('!HI', header)
        if recvtype != 4:
            print(f"收到的第{count}个包类型错误，应为4")
            return

        data_bytes = b''
        part = clientsocket.recv(length)
        data_bytes += part

        data_str = data_bytes.decode('ascii')
        print(f"收到了第{count}块倒转文件：{data_str}")

        count += 1

        reversefile.insert(0,data_str)

    outputtext = ''.join(reversefile)

    with open('output.txt','w',encoding='ascii') as f:
        f.write(outputtext)
    print("文件已保存")

def Initilization(clientsocket , N):
    pack = struct.pack('!HI',1,N)#H	unsigned short	2	0 ~ 65,535#I	unsigned int	4	0 ~ 4,294,967,295
    clientsocket.sendall(pack)

    agreeheader = clientsocket.recv(2)
    (agreetype,) = struct.unpack('!H',agreeheader)
    if(agreetype != 2):
        print("收到的不是agree包，连接失败")
        clientsocket.close()
        return False

    return True


def startclient():

    clientsocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#AF_INET 表示使用 IPv4 地址族（Address Family）SOCK_STREAM 表示使用 面向连接的 TCP 协议。
    serverip = input("请输入服务器ip")
    serverport = int(input("请输入服务器端口号"))
    clientsocket.connect((serverip,serverport))

    with open('input1.txt','r',encoding='ascii') as f:
        text = f.read()#str类型

    lmin = int(input("请输入传输最小字节流大小"))
    lmax = int(input("请输入传输最大字节流大小"))

    if lmin > lmax or lmin <= 0:
        print("输入的大小范围不正确")
        return

    pieces = []
    totalsize = len(text)
    currsize = 0
    while currsize < totalsize:
        remain = totalsize - currsize
        if remain < lmin:
            piece = remain#最后一块不足了直接全给
        else:
            piece = random.randint(lmin, lmax)#随机大小的块

        pieces.append(text[currsize:currsize+piece])
        currsize += piece

    N = len(pieces)
    print(f"文件被切成{N}个数据块发送")
    if not Initilization(clientsocket , N):
        return

    else:
        reverseRequest(clientsocket,pieces)

    clientsocket.close()
    print("连接运行结束")

startclient()