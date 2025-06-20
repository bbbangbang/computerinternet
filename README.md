# computerinternet
course design
计网课程设计：
task1文件包括：
    input1.txt——用于初始翻转字符文件；
    reversetcpclient.py是task1的客户端文件
    reversetcpserver.py是task1的服务器端文件
    output.txt是客户端输出翻转后的文件（其中列表存储采取了倒序插入，否则会因为随机分包而难以分析）
task1操作：
    先启动服务器才能启动socket；
    客户端要输入ip地址和端口号；
    经过测试，虚拟机可以使用ip地址进行连接操作；
    经过测试，空文件传入时reverse后输出空文件；
    经过测试，中文字符会报错，原因是用ascii码encoding时无法解析中文字符；

task2文件包括：
    input.txt属于长文件，test.py用于生成input.txt；
    udpclient.py是客户端代码；
    udpserver.py是服务器端代码；
task2操作：
    要先启动服务器输入端口号后才能进行下一步；
    客户端进入后要输入端口号和ip地址；
    客户端发送完信息后，会自动阻塞，必须输入任意字符才能继续发送Fin报文以进行连接断开；
    test.py仅仅用于生成随机ASCII码字符；
    经测试，input.txt文件为空时，不会发送包，因为数据是空的，切割后列表内无内容可以发送，所以没有RTT内容；