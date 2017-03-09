# -*- coding: utf-8 -*- 
import os
import socket
import subprocess

conf_path='/usr/local/zabbix-2.2.2/etc/zabbix_agentd.conf'
redisIPs=['10.0.250.120']
appIPs=['10.0.250.121','10.0.250.122']
zookeeperIPs=[]
comdlists=[]
cmdlist2=[]
cmdlist3=[]
#部署zabbix agent
cmd1='groupadd zabbix'
cmd2='useradd -g zabbix zabbix'
cmd3='tar -zxvf /usr/local/zabbix-2.2.2.tar.gz'
cmd4= 'cp -r ./zabbix-2.2.2/ /usr/local/'
cmd5='cp -r /usr/local/zabbix-2.2.2/script/ /home/zabbix/script'
cmd14='chmod a+x /home/zabbix/script/*'
#启动zabbixagent
cmd6='chmod a+x /usr/local/zabbix-2.2.2/sbin/zabbix_agentd'
cmd7 = '/usr/local/zabbix-2.2.2/sbin/zabbix_agentd'
#安装simplejson
#cmd17='cd /usr/local/zabbix-2.2.2/simplejson-3.5.2/'
cmd18='python setup.py install'
#cmd18='python test.py'

#配置sudo
cmd19='echo "zabbix ALL=(root) NOPASSWD:/bin/netstat">>/etc/sudoers'
cmd20="sed -i 's/^Defaults.*.requiretty/#Defaults    requiretty/' /etc/sudoers"
comdlists.append(cmd1)
comdlists.append(cmd2)
comdlists.append(cmd3)
comdlists.append(cmd4)
comdlists.append(cmd5)
comdlists.append(cmd14)
cmdlist2.append(cmd6)
cmdlist2.append(cmd7)
#cmdlist3.append(cmd17)
cmdlist3.append(cmd18)
cmdlist3.append(cmd19)
cmdlist3.append(cmd20)



def exceCommands(comdlists):
    for comd in comdlists:
        os.system(comd)
        print comd

def get_pid(servername):
    if servername == 'zookeeper':
        pidarg = '''ps -ef|grep java|grep zookeeper|grep -v grep|awk '{print $2}' '''
    elif servername == 'redis':
        pidarg = '''ps -ef|grep redis-server|grep -v grep|awk '{print $2}' '''
    pidout = subprocess.Popen(pidarg,shell=True,stdout=subprocess.PIPE)
    pid = pidout.stdout.readline().strip('\n')
    return pid

#根据服务情况进行不同部署
def deployByServerType(ip):
    pid = get_pid('zookeeper')
    if pid:
        addRedisMonitor(ip)
        installSimpleJson()
    pid = get_pid('redis')
    if pid:
        addZookeeperMonitor()

def addZookeeperMonitor():
    f = open(conf_path,'a+')
    f.write('UserParameter=zookeeper.status[*],/usr/local/zabbix-2.2.2/etc/check_zookeeper.py $1 \n')
    f.close()
        

def installSimpleJson():
    os.chdir('/usr/local/zabbix-2.2.2/simplejson-3.5.2/')
    #print os.getcwd()
    exceCommands(cmdlist3)
    #print os.getcwd()
    
def getLocalIP():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"
def modifyZabbixConf(name):
    f = open(conf_path,'r+')
    line = f.readlines()
    for i in line:
        if i.startswith('Hostname'):
            ind = line.index(i)
            line[ind]="Hostname="+name+'\n'

    f = open(conf_path,'w+')
    f.writelines(line)
    f.close()

def addRedisMonitor(ip):
    f = open(conf_path,'a+')
    f.write('UserParameter=redis.discovery,/usr/local/zabbix-2.2.2/etc/redis_port.py \n')
    f.write('UserParameter=redis_stats[*],redis-cli -h '+ip+' -a redis_passwd -p $1 info|grep $2|cut -d : -f2 \n')
    f.close()

if __name__ =='__main__':
    exceCommands(comdlists)
    ip = getLocalIP()
    modifyZabbixConf(ip)
    deployByServerType(ip)
    exceCommands(cmdlist2)

def start():
    exceCommands(comdlists)
    ip = getLocalIP()
    modifyZabbixConf(ip)
    deployByServerType(ip)
    print 'hello'
    exceCommands(cmdlist2)
    


