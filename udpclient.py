import socket
import struct
import time
import random
import pandas as pd
import threading

#flags是标志位，SYN=1;ACK=2;SYN-ACK=3;data=4;FIN=5；FIN-ACK=6

class TCP:
    def __init__(self,serverip,serverport):
        self.UDPsock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.serverip = serverip
        self.serverport = serverport
        self.UDPsock.settimeout(0.3)#初始设置超时为300ms

        self.seqnum = random.randint(0,1000)#初始序列号是随机的 RFC 793
        self.baseseq = 0
        self.nextseq = 0

        self.sendwindow = 400
        self.packets = []#存储已经发送的数据包的信息

        self.starttime = 0#总发送的起始时间
        self.timeout = 0#超时计数
        self.totalsend = 0#已发送的包
        self.rttlist = []#
        self.UDPsock.setblocking(True)
        self.lock = threading.Lock()  # 控制共享数据访问的锁

    def header(self,seq,ack,flags,length):#length是数据长度
        return struct.pack('!IIHH',seq,ack,flags,length)

    def checkheader(self,header):
        return struct.unpack('!IIHH', header)

    def handsshaking(self):
        #创建SYN报文并发送
        for attempt in range(10):
            try:
                synheader = self.header(seq = self.seqnum, ack = 0,flags = 1,length = 0)
                self.UDPsock.sendto(synheader, (self.serverip, self.serverport))
                print(f"SYN包已发送,seqnum为{self.seqnum}")
                break
            except socket.timeout:
                print("超时等待，重发发送")
        else:
            print("3次发送SYN连接TCP失败")
            return

        #接收服务发来的SYN+ACK
        synackheader,addr = self.UDPsock.recvfrom(12)#recvfrom用于UDP，因为不知道是谁发来的数据
        seq,ack,flags,length = self.checkheader(synackheader)
        if flags == 3 and ack == self.seqnum + 1:
            print(f"SYN-ACK包收到，ack={ack}")
        #发送ACK包
        for attempt in range(10):
            try:
                ackheader = self.header(seq = ack,ack = seq+1,flags = 2,length = 0)
                self.UDPsock.sendto(ackheader, (self.serverip, self.serverport))
                print(f"建立连接：seqnum更新为{ack}")
                break
            except socket.timeout:
                print("超时等待，重发发送")
                self.totalsend+=1
                self.timeout += 1
        else:
            print("3次发送ACK连接TCP失败")
            return

    def sendmessage(self,message):
        totalpackets = int(input("你想发给server的数据包个数"))
        packetsize = 80 #80字节每个数据包
        packets = []
        for i in range(0,len(message),packetsize):
            packets.append(message[i:i+packetsize])
        packets = packets[:totalpackets]#只发送规定的包数

        self.starttime = time.time()#开始计时

        windowpacketnum = self.sendwindow // packetsize#窗口里一次最多放这么多的包（5个）

        while self.baseseq < len(packets):#TCP是按字节的，但是这里已经分好包了，就按包来分
            self.lock.acquire()#防止其他线程来打扰搅乱信息
            while self.nextseq < min(self.baseseq + windowpacketnum,len(packets)):
                perdata = packets[self.nextseq]#每个数据包的内容数据
                header = self.header(seq = self.nextseq * packetsize,ack = 0,flags = 4,length = len(perdata))
                datapacket = header + perdata
                self.UDPsock.sendto(datapacket,(self.serverip,self.serverport))#发过去了
                #发送的包信息
                startbyte = self.nextseq * packetsize#开始字节
                endbyte = startbyte + len(perdata) - 1#length把0看作1
                print(f"第{self.nextseq}个(第{startbyte}~{endbyte}字节)client端已经发送")
                self.packets.append((startbyte,datapacket,time.perf_counter()))#存已经发送过的包的信息
                self.nextseq += 1
                self.totalsend += 1
            self.lock.release()
            #发完五个包后等server回ACK
            try:
                ackheader, addr = self.UDPsock.recvfrom(12)
                seq, ack, flags, length = self.checkheader(ackheader)
                if flags == 2:
                    for seqnum, pkt, send_time in self.packets:
                        datalen = len(pkt) - 12
                        if ack == seqnum + datalen:#累计确认的
                            rtt = (time.perf_counter() - send_time) * 1000
                            self.rttlist.append(rtt)#加入rtt队列用于最后总结计算

                            startbyte = seqnum
                            endbyte = ack - 1
                            print(f"ACK 对应包 (第{startbyte}~{endbyte}字节) server端已经收到，RTT 是 {rtt:.2f} ms")
                            break
                    #开始移动窗口
                    if ack > self.baseseq * packetsize:
                        self.baseseq = ack // packetsize
                    #实时监控网络
                    if self.rttlist:
                        averrtt = sum(self.rttlist) / len(self.rttlist)
                        timeout_ms = min(averrtt * 5, 1000)  # 最多1秒
                        self.UDPsock.settimeout(timeout_ms / 1000)


            except socket.timeout:
                #触发超时重传
                self.lock.acquire()
                self.timeout += 1#超时包计数
                for i in range(self.baseseq,self.nextseq):
                    packet = self.packets[i][1]#数据(包括了头)
                    self.UDPsock.sendto(packet,(self.serverip,self.serverport))#重传
                    self.totalsend += 1
                    startbyte = i * packetsize
                    endbyte = startbyte + len(packet) - 12 - 1
                    self.packets[i] = (startbyte, packet, time.perf_counter())#更新一下列表里的信息rtt
                    print(f"重传第{i}个(第{startbyte}~{endbyte}字节)client端已经发送")
                self.lock.release()

        # FIN报文（flags = 5）
        BIAOSHIFU = input("输入任意字符以开始发送FIN")
        # 1. 客户端发送 FIN
        fin_header = self.header(seq=self.nextseq * 80, ack=0, flags=5, length=0)
        for attempt in range(10):
            try:
                self.UDPsock.sendto(fin_header, (self.serverip, self.serverport))
                print("FIN 包已发送，请求关闭连接")
                break
            except socket.timeout:
                print("超时，重发FIN包")
                self.totalsend += 1
                self.timeout += 1

        # 2. 等待服务器的 ACK 和 FIN
        isACK = False
        while True:
            try:
                finack_pkt, _ = self.UDPsock.recvfrom(12)
                seq, ack, flags, length = self.checkheader(finack_pkt)

                # if flags == 2:  # ACK
                #     print("收到服务器对 FIN 的 ACK")
                #     isACK = True
                if flags == 5 :  # 服务器的 FIN
                    print("收到服务器发来的 FIN")
                    break
                    # 3. 客户端回 ACK 作为最后确认
                    # ack_pkt = self.header(seq=ack, ack=seq + 1, flags=2, length=0)
                    # self.UDPsock.sendto(ack_pkt, (self.serverip, self.serverport))
                    # print("客户端发送最终 ACK，连接关闭完成")
                    # break
            except socket.timeout:
                print("等待服务器的 ACK/FIN 超时")
            except BlockingIOError:
                # 对于非阻塞套接字，没有数据时就继续等
                continue

    def RTTcount(self):
        if(self.rttlist):
            RTT = pd.DataFrame(self.rttlist,columns=["RTT(ms)"])
            maxrtt = RTT['RTT(ms)'].max()
            minrtt = RTT['RTT(ms)'].min()
            meanrtt = RTT['RTT(ms)'].mean()
            biaozhunrtt = RTT['RTT(ms)'].std()

            print("\n--- RTT 统计信息 ---")
            print(f"最大 RTT: {maxrtt:.2f} ms")
            print(f"最小 RTT: {minrtt:.2f} ms")
            print(f"平均 RTT: {meanrtt:.2f} ms")
            print(f"RTT 标准差: {biaozhunrtt:.2f} ms")
            print(f"丢包率: {30 / self.totalsend} %")
            print(f"实际丢包率：{self.timeout / self.totalsend * 100}%")
        else:
            print("无RTT信息")




def startclient():
    serverport = int(input("输入服务器端口号"))
    serverip = input("输入服务器ip地址")
    TCPclient = TCP(serverip,serverport)
    TCPclient.handsshaking()#建立连接
    with open('input.txt',encoding='ascii') as f:
        text = f.read()#str类型
    bytetext = bytes(text,encoding = 'ascii')
    TCPclient.sendmessage(bytetext)
    TCPclient.RTTcount()


startclient()