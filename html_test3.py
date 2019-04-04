import optparse
from socket import *
from threading import *
import time
import os
from selenium import webdriver

class Scan():

    def __init__(self):
        self.Port_state = []
        self.locker = Semaphore(value=1)
        self.time_spend = 0
        self.tgtIP = ''
        self.tgtName = []

    # 连接函数
    def connScan(self,tgtHost, tgtPort):
        try:
            # 建立连接
            connSkt = socket(AF_INET, SOCK_STREAM)
            connSkt.settimeout(10)
            connSkt.connect((tgtHost, tgtPort))
            # 获取Banner
            try:
                # 发送消息
                connSkt.send(b'ViolentPython\r\n')
                # 接受消息
                receive = connSkt.recv(100)
            except:
                receive = 'Cannot Get Banner'
            connSkt.close()
            self.locker.acquire()
            result = []
            result.append(str(tgtPort))
            result.append('open')
            result.append(receive)
            self.Port_state.append(result)
            self.locker.release()
        except:
            pass

    # 解析主机IP
    def portScan(self,tgtHost, tgtPorts):
        start_time = time.time()
        try:
            # 根据主机名获取IP
            self.tgtIP = gethostbyname(tgtHost)
        except:
            print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
            return
        try:
            # 根据IP获取主机名
            self.tgtName = gethostbyaddr(self.tgtIP)
            print('[+] Scan Results for:' + self.tgtName[0], self.tgtName[2][0])
        except:
            print('[+] Scan Results for:' + self.tgtIP)

        thread_list = []
        for tgtPort in tgtPorts:
            t = Thread(target=self.connScan, args=(self.tgtIP, int(tgtPort)))
            t.setDaemon(True)
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join(timeout=1)
        self.Port_state = sorted(self.Port_state, key=lambda x: int(x[0]))
        for i in self.Port_state:
            print(i)
        self.time_spend = time.time() - start_time
        print('一共用时：', self.time_spend)

    def portScan2(self,tgtHost, tgtPorts_left, tgtPorts_right):
        start_time = time.time()
        try:
            # 根据主机名获取IP
            self.tgtIP = gethostbyname(tgtHost)
        except:
            print("[-] Cannot resolve '%s': Unknown host" % tgtHost)
            return
        try:
            # 根据IP获取主机名
            self.tgtName = gethostbyaddr(self.tgtIP)
            print('[+] Scan Results for:' + self.tgtName[0], self.tgtName[2][0])
        except:
            print('[+] Scan Results for:' + self.tgtIP)

        thread_list = []
        for tgtPort in range(tgtPorts_left, tgtPorts_right + 1):
            t = Thread(target=self.connScan, args=(self.tgtIP, tgtPort))
            t.setDaemon(True)
            t.start()
            thread_list.append(t)
        for t in thread_list:
            t.join(timeout=1)
        self.Port_state = sorted(self.Port_state, key= lambda x : int(x[0]))
        for i in self.Port_state:
            print(i)
        self.time_spend = time.time() - start_time
        print('一共用时：', self.time_spend)


def convertToHtml2(Port_state,time_spend,date,tgtIP,tgtName):
    head = '''<html>
    <body>
    <h1>测试报告</h1>
    '''
    end = '''</body>
    </html>'''
    f = open(date[:10]+'_'+tgtIP+".html", "w")
    f.write(head+'<br />')
    f.write(date+'<br /><br />')
    if tgtName != []:
        f.write('Scan Results for:'+tgtName[0]+' '+tgtName[2][0]+'<br /><br />')
    else:
        f.write('Scan Results for:' + tgtIP + '<br /><br />')
    for eachline in Port_state:
        a = ' : '.join(eachline[:2])
        f.write(a)
        f.write(' : ')
        f.write('%s'%eachline[2])
        f.write('<br />')
    f.write('<br />扫描耗时:'+str(time_spend)+'<br />')
    f.write(end)
    f.close()
    webbrowser(date,tgtIP)

def webbrowser(date,tgtIP):
    driver = webdriver.Firefox()
    #driver.implicitly_wait(5)
    driver.get("file://"+os.path.dirname(os.path.realpath(__file__))+'/'+date[:10]+'_'+tgtIP+'.html')

def main():
    # 设置命令行指令
    parser = optparse.OptionParser('usage %prog -H <target host> -P <target ports> -p <target ports limit>')
    # 添加命令行参数
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host,like:192.168.0.1')
    parser.add_option('-P', dest='tgtPorts', type='string', help='specify target ports,like:21,22,80')
    parser.add_option('-p', dest='tgtPorts_limit', type='string', help='specify target ports limit,like:21-80')
    # 获取参数
    (options, args) = parser.parse_args()
    tgtHost = options.tgtHost
    tgtPorts = str(options.tgtPorts).split(',')
    tgtPorts_limit = str(options.tgtPorts_limit).split('-')

    Scan_instance = Scan()
    if tgtHost != None:
        if tgtPorts != ['None']:
            Scan_instance.portScan(tgtHost, tgtPorts)
        elif tgtPorts_limit != ['None']:
            Scan_instance.portScan2(tgtHost, int(tgtPorts_limit[0]), int(tgtPorts_limit[1]))
    else:
        print(parser.usage)
        exit(0)

    print('生成HTML报告中......')
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    convertToHtml2(Scan_instance.Port_state,Scan_instance.time_spend,date,Scan_instance.tgtIP,Scan_instance.tgtName)
    print('HTML报告已存于'+os.path.dirname(os.path.realpath(__file__))+'/'+date[:10]+'_'+Scan_instance.tgtIP+'.html')


if __name__ == '__main__':
    #main()
    #portScan('192.168.1.140',['21','22','80','443'])
    Scan_instance = Scan()
    Scan_instance.portScan2('192.168.1.166',20,1000)
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    convertToHtml2(Scan_instance.Port_state, Scan_instance.time_spend, date, Scan_instance.tgtIP, Scan_instance.tgtName)
    print('HTML报告已存于' + os.path.dirname(os.path.realpath(__file__)) + '\\' + date[:10] + '_' + Scan_instance.tgtIP + '.html')