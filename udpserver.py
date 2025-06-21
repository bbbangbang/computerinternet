import socket
import struct
import random
import threading
import time

#flags是标志位，SYN=1;ACK=2;SYN-ACK=3;data=4;FIN=5；FIN-ACK=6
class TCPserver():
    def __init__(self, port):
        self.UDPsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.UDPsock.bind(('0.0.0.0', port))
        self.connections = {}  # 保存所有客户端连接状态
#connections结构：
# self.connections = {
#     ('192.168.1.100', 54321): {
#         'state': 'ESTABLISHED',
#         'expectseq': 100,
#         'syn_ack_seq': 500,
#
#     },
#     ('10.0.0.2', 12345): {
#         'state': 'SYN_RCVD',
#         'expectseq': 150,
#         'syn_ack_seq': 50,
#
#     }
# }
        print(f"服务器端已启动，监听端口 {port}")

    def header(self, seq, ack, flags, len):
        return struct.pack('!IIHH', seq, ack, flags, len)

    def checkheader(self, header):
        return struct.unpack('!IIHH', header)

    def handlepacket(self, data, addr):#检查数据包类型和状态
        #检查数据包长度是否足够
        if len(data) < 12:
            print(f"来自 {addr} 的数据包长度不足（{len(data)}字节），忽略")
            return

        #为每个客户端创建独立状态
        if addr not in self.connections:
            self.connections[addr] = {
                'state': 'LISTEN',
                'expectseq': 0,
                'syn_ack_seq': None,
                'recvtime': time.time()
            }#State就是状态，expectseq是期望收到的第一个字节；syn_ack_seq是用于检查连接状态是否建立的；
        conn = self.connections[addr]
        conn['recvtime'] = time.time()  #更新最后活动时间

        #解析header
        try:
            seq, ack, flags, length = self.checkheader(data[:12])
        except struct.error as e:
            print(f"解析 {addr} 的包头时出错: {e}")
            return

        #处理不同类型的包(针对这一个addr）
        if flags == 1:  #SYN包
            self.handlesyn(conn, seq, addr)
        elif flags == 2:  #ACK包
            self.handleack(conn, seq, ack, addr)
        elif flags == 4:  #data包
            self.handledata(conn, seq, length, addr)
        elif flags == 5:  #FIN包
            self.handlefin(conn, seq, addr)
        else:
            print(f"来自 {addr} 的未知包类型: flags={flags}")

    def handlesyn(self, conn, seq, addr):

        print(f"来自 {addr} 的SYN包已收到")
        syn_ack_seq = random.randint(0, 1000)
        conn['syn_ack_seq'] = syn_ack_seq
        conn['state'] = 'SYNRECVED'

        # 发送SYN-ACK
        ackheader = self.header(seq=syn_ack_seq, ack=seq + 1, flags=3, len=0)
        self.UDPsock.sendto(ackheader, addr)
        print(f"向 {addr} 发送SYN-ACK, seq={syn_ack_seq}, ack={seq + 1}")

    def handleack(self, conn, seq, ack, addr):#处理连接时的ACK包

        if conn['state'] == 'SYNRECVED' and ack == conn['syn_ack_seq'] + 1:
            print(f"与 {addr} 的连接已建立")
            conn['state'] = 'ESTABLISHED'
            conn['expectseq'] = 0
        else:
            print(f"来自 {addr} 的无效ACK包: 状态state={conn['state']}, ack={ack}")

    def handledata(self, conn, seq, length, addr):

        if conn['state'] != 'ESTABLISHED':
            print(f"来自 {addr} 的数据包但连接未建立")
            return

        if seq == conn['expectseq']:
            if random.random() > 0.2:  # 模拟丢包，0.8的概率成功接收
                conn['expectseq'] += length
                ack_packet = self.header(0, conn['expectseq'], 2, 0)#这里也是回复ack，但是是针对数据包的
                self.UDPsock.sendto(ack_packet, addr)
                print(f"已确认 {addr} 的数据包 {seq} ~ {seq + length - 1}")
            else:
                print(f"模拟丢包: 忽略 {addr} 的数据包 {seq}")
        else:
            print(f"来自 {addr} 的乱序数据包: 期望 {conn['expectseq']}, 收到 {seq}")

    def handlefin(self, conn, seq, addr):

        print(f"收到来自 {addr} 的FIN请求")

        # 发送ACK
        ack_pkt = self.header(0, seq + 1, 2, 0)
        self.UDPsock.sendto(ack_pkt, addr)

        # 发送FIN
        fin_seq = random.randint(1000, 9999)
        fin_pkt = self.header(fin_seq, 0, 5, 0)
        self.UDPsock.sendto(fin_pkt, addr)
        #conn['state'] = 'FIN_WAIT_1'
        print(f"向 {addr} 发送FIN, seq={fin_seq}")

        # 更新连接状态
        conn['state'] = 'DISCONNECTED'
        print(f"与{addr}的连接已断开")
    def start(self):
        print("服务器端已启动")
        while True:
            try:
                data, addr = self.UDPsock.recvfrom(92)#数据包最多92字节
                threading.Thread(target=self.handlepacket, args=(data, addr), daemon=True).start()#daemon=True：设为守护线程（主线程退出时自动终止
            except Exception as e:
                print(f"服务器错误: {e}")


port = int(input("请输入端口号: "))
serverTCP = TCPserver(port)
serverTCP.start()