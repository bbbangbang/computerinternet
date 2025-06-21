# computerinternet
course design
计网课程设计：

本机配置以及运行环境

Platform: "win-amd64"
Python version: "3.12"
Current installation scheme: "nt"

Paths:
        data = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        include = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Include"
        platinclude = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Include"
        platlib = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Lib\site-packages"
        platstdlib = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Lib"
        purelib = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Lib\site-packages"
        scripts = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Scripts"
        stdlib = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Lib"

Variables:
        BINDIR = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        BINLIBDEST = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Lib"
        EXE = ".exe"
        EXT_SUFFIX = ".cp312-win_amd64.pyd"
        INCLUDEPY = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Include"
        LIBDEST = "C:\Users\bb、\AppData\Local\Programs\Python\Python312\Lib"
        TZPATH = ""
        VERSION = "312"
        VPATH = "..\.."
        abiflags = ""
        base = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        exec_prefix = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        installed_base = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        installed_platbase = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        platbase = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        platlibdir = "DLLs"
        prefix = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        projectbase = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        py_version = "3.12.4"
        py_version_nodot = "312"
        py_version_nodot_plat = "312"
        py_version_short = "3.12"
        srcdir = "C:\Users\bb、\AppData\Local\Programs\Python\Python312"
        userbase = "C:\Users\bb、\AppData\Roaming\Python"
        

Package            Version
------------------ -----------
attrs              24.2.0
Automat            22.10.0
beautifulsoup4     4.12.3
certifi            2024.7.4
cffi               1.17.0
charset-normalizer 3.3.2
constantly         23.10.4
contourpy          1.3.0
cryptography       43.0.0
cssselect          1.2.0
cycler             0.12.1
DateTime           5.5
defusedxml         0.7.1
etreetools         0.1.2
filelock           3.15.4
fonttools          4.54.1
fsspec             2024.9.0
h11                0.14.0
hyperlink          21.0.0
idna               3.7
incremental        24.7.2
itemadapter        0.9.0
itemloaders        1.3.1
Jinja2             3.1.4
jmespath           1.0.1
joblib             1.4.2
kiwisolver         1.4.7
lxml               5.3.0
MarkupSafe         3.0.1
matplotlib         3.9.2
matplotlib_Chinese 0.0.4
MouseInfo          0.1.3
mpmath             1.3.0
networkx           3.3
numpy              2.1.0
onnx               1.17.0
onnx-tf            1.6.0
outcome            1.3.0.post0
packaging          24.1
pandas             2.2.2
parsel             1.9.1
pillow             10.3.0
pip                25.1
Protego            0.3.1
protobuf           5.28.2
pyasn1             0.6.0
pyasn1_modules     0.4.0
PyAutoGUI          0.9.54
pycparser          2.22
PyDispatcher       2.0.7
PyGetWindow        0.0.9
PyMsgBox           1.0.9
pyOpenSSL          24.2.1
pyparsing          3.2.0
pyperclip          1.9.0
PyRect             0.2.0
PyScreeze          1.0.1
PySocks            1.7.1
python-dateutil    2.9.0.post0
python-docx        1.1.2
pytweening         1.2.0
pytz               2024.1
PyYAML             6.0.2
queuelib           1.7.0
requests           2.32.3
requests-file      2.1.0
scikit-learn       1.5.2
scipy              1.14.1
Scrapy             2.11.2
selenium           4.23.1
service-identity   24.1.0
setuptools         72.1.0
six                1.16.0
sniffio            1.3.1
sortedcontainers   2.4.0
soupsieve          2.5
sympy              1.13.3
threadpoolctl      3.5.0
tldextract         5.1.2
torch              2.4.1
trio               0.26.2
trio-websocket     0.11.1
Twisted            24.7.0
typing_extensions  4.12.2
tzdata             2024.1
urljoin            1.0.0
urllib3            2.2.2
w3lib              2.2.1
websocket-client   1.8.0
wsproto            1.2.0
xpath-helper       0.1.3
zope.interface     7.0.1


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