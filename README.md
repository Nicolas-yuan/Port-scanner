# Port-scanner
端口扫描    
通过调用optparse库解析命令行参数，通过socket进行TCP全连接扫描，通过webdriver自动将扫描报告显示在浏览器上  
命令行参数解析：-H 主机IP，如192.168.0.1 -P 要扫描的端口列表，如2,22,80 -p 要扫描的端口范围，如21-1000  
for example  
release.exe -H 192.168.0.1 -P 21,22,80  
release.exe -H 192.168.0.1 -p 21-1000  
