# -*- coding: utf-8 -*-
'''
Created on 2015-3-17

@author: jk_2
'''
import os
import logging
import xml.dom.minidom
import exception.myException as myException
import time
import subprocess


def gotoSnapshot(vmname, snapshotName, ip, username, password):
    '''
    Operation :: Revert To Snapshot BOSS6.0.1-QTP For Virtual Machine AutoTest4DomesticBossDB-91
    completed successfully under host localhost.localdomain
    '''
    
    logging.info('goto snapshot : ' + snapshotName + ' , please wait...')
    command_str = 'perl /usr/lib/vmware-vcli/apps/vm/snapshotmanager.pl --url https://' \
                  + ip \
                  + ':443/sdk/webService --username ' \
                  + username \
                  + ' --password ' \
                  + password \
                  + ' --operation goto --vmname ' \
                  + vmname \
                  + ' --snapshotname ' \
                  + snapshotName
    fp = os.popen(command_str).read()
    logging.info(fp)
    if 'successfully' in fp:
        logging.info('goto snapshot : ' + snapshotName + ' ok!')
        return 'ok'
    else:
        logging.error('Failed! goto snapshot : ' + snapshotName + ' error!')
        return 'error'
    

def createSnapshot(vmname, snapshotName, ip, username, password):
    '''
    Operation :: Snapshot BOSS6.0.1-QTP-testtesttest for virtual machine AutoTest4DomesticBossDB-91
    created successfully under host localhost.localdomain
    '''
    
    command_str = 'perl /usr/lib/vmware-vcli/apps/vm/snapshotmanager.pl --url https://' \
                  + ip \
                  + ':443/sdk/webService --username ' \
                  + username \
                  + ' --password ' \
                  + password \
                  + ' --operation create --vmname ' \
                  + vmname \
                  + ' --snapshotname ' \
                  + snapshotName
    print command_str
    p = subprocess.Popen(command_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    fp = p.stdout.read()
    logging.info(fp)
    if 'successfully' in fp:
        logging.info('create snapshot : ' + snapshotName + ' ok!')
        return 'ok'
    else:
        logging.error('Failed! create snapshot : ' + snapshotName + ' error!')
        return 'error'
    

def listSnapshot(vmname, ip, username, password):
    '''
    Snapshots for Virtual Machine AutoTest4DomesticBossDB-91 under host localhost.localdomain
    
    Name                                 Date                 State         Quiesced
    BOSS-5.11.1-initial_version          2014-09-15T05:06     poweredOn     N
    BOSS6.0.1-QTP                        2014-09-24T05:45     poweredOn     N
    BOSS6.0.1-QTP-testtesttest           2014-12-29T01:42     poweredOff    N
    BOSS-5.11.1-add-bug-testcase         2014-11-21T01:51     poweredOn     N
    BOSS-611R2                           2014-11-28T07:26     poweredOn     N
    5.12.1-add by wenl National          2014-09-15T06:22     poweredOn     N
    '''
    
    command_str = 'perl /usr/lib/vmware-vcli/apps/vm/snapshotmanager.pl --url https://' \
                  + ip \
                  + ':443/sdk/webService --username ' \
                  + username \
                  + ' --password ' \
                  + password \
                  + ' --operation list --vmname ' \
                  + vmname
    p = subprocess.Popen(command_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    fp = p.stdout.read()
    logging.info(fp)
    return fp


def snapshotManager(ip, username, password, vmname, operation, snapshotName, newSnapshotName):
    '''
    
    :param ip:
    :param username:
    :param password:
    :param vmname:
    :param operation: support '<list> | <create> | <revert> | <goto> | <rename> | <remove>', nonsupport '<removeAll>'
    :param snapshotName:
    :param newSnapshotName: Required if operation is <rename>, otherwise set to ''
    :NOTICE: "create" snapshot DO NOT include memory dump.
    '''
    # result:
    # No Snapshot of Virtual Machine QTP-97 exists under host localhost.domain.org
    #
    # Snapshots for Virtual Machine AutoTest4DomesticBossDB-91 under host localhost.localdomain
    #
    # Name                                 Date                 State         Quiesced
    # BOSS-5.11.1-initial_version          2014-09-15T05:06     poweredOn     N
    # BOSS6.0.1-QTP                        2014-09-24T05:45     poweredOn     N
    # BOSS6.0.1-QTP-testtesttest           2014-12-29T01:42     poweredOff    N
    if 'list' == operation:
        checkStr = ''
        suffixStr = '--operation list --vmname ' + vmname
        
    # result:
    # Operation :: Snapshot BOSS6.0.1-QTP-testtesttest for virtual machine AutoTest4DomesticBossDB-91 created successfully under host localhost.localdomain
    elif 'create' == operation:
        checkStr = 'successfully'
        suffixStr = '--operation create --vmname ' + vmname + ' --snapshotname ' + snapshotName
    
    # result:
    # 1. Virtual machine does not have a current snapshot
    # 2. Operation :: Revert To Current Snapshot For Virtual Machine DomesticBossSysTestEnv-92 completed successfully under host localhost.domain.org
    elif 'revert' == operation:
        checkStr = 'successfully'
        suffixStr = '--operation revert --vmname ' + vmname
    
    # result:
    # Operation :: Revert To Snapshot BOSS6.0.1-QTP For Virtual Machine AutoTest4DomesticBossDB-91 completed successfully under host localhost.localdomain
    elif 'goto' == operation:
        checkStr = 'successfully'
        suffixStr = '--operation goto --vmname ' + vmname + ' --snapshotname ' + snapshotName
        
    # result:
    # 1. Operation:: Rename Snapshot DomesticBossSysEnv_initial_version for Virtual Machine DomesticBossSysTestEnv-92 under host localhost.domain.org completed successfully
    # 2. Snapshot Not Found with name DomesticBossSysEnv_initial_version11 in Virtual Machine DomesticBossSysTestEnv-92 under host localhost.domain.org
    elif 'rename' == operation:
        checkStr = 'successfully'
        suffixStr = '--operation rename --snapshotname ' + snapshotName + ' --newname ' + newSnapshotName + ' --vmname ' + vmname
    
    # Required. Binary value (0 or 1) that determines whether child snapshots are also removed (1) or not removed (0) for operation I <Remove>
    # default 0 , nonsupport value(1)
    # result:
    # 1. Operation :: Remove Snapshot test For Virtual Machine Linux64ES6-Billing-99 under host localhost.domain.org completed successfully
    # 2. Snapshot Not Found with name test111 in Virtual Machine Linux64ES6-Billing-99 under host localhost.domain.org
    elif 'remove' == operation:
        checkStr = 'successfully'
        suffixStr = '--operation remove --vmname ' + vmname + ' --snapshotname ' + snapshotName + ' --children 0'
    else:
        logging.info('nonsupport "' + operation + '" snapshot operation!')
        raise myException('nonsupport ' + operation + ' snapshot operation!')
    
    logging.info('do : "' + operation + '" snapshot, please wait...')
    command_str = 'perl /usr/lib/vmware-vcli/apps/vm/snapshotmanager.pl --url https://' + ip \
                  + ':443/sdk/webService --username ' + username + ' --password ' + password \
                  + ' ' + suffixStr
    print command_str
    p = subprocess.Popen(command_str, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    fp = p.stdout.read()
    logging.info(fp)
    
    if 'list' == operation:
        # 需修改，改为返回一个list，现在返回的是一个字符串
        return fp
    else:
        if checkStr in fp.lower():
            logging.info('do operation: "' + operation + '" snapshot ok!')
            return 'ok'
        else:
            logging.error('Failed! do operation: "' + operation + '" snapshot error!')
            raise myException('error' if fp == '' else fp)
#            return 'error' if fp == '' else fp


def vmControl(ip, username, password, vmname, operation):
    '''
    :param ip:
    :param username:
    :param password:
    :param vmname:
    :param operation: support '<poweron> | <poweroff> | <reboot> | <shutdown>', nonsupport '<reset> | <standby> | <suspend>'
    result:
    poweron     : virtual machine 'DomesticBossSysTestEnv-92' under host localhost.domain.org powered on
    poweroff    : virtual machine 'DomesticBossSysTestEnv-92' under host localhost.domain.org powered off
    reboot      : Guest on 'DomesticBossSysTestEnv-92' under host localhost.domain.org rebooted successfuly
    shutdown    : Guest 'DomesticBossSysTestEnv-92' under host localhost.domain.org shutdown
    when error  : Error in 'DomesticBossSysTestEnv-92' under host localhost.domain.org: The attempted operation cannot be performed in the current state
    '''
    if 'poweron' == operation:
        checkStr = 'powered on'
    elif 'poweroff' == operation:
        checkStr = 'powered off'
    elif 'reboot' == operation:
        checkStr = 'rebooted successfuly'
    elif 'shutdown' == operation:
        checkStr = 'shutdown'
    else:
        logging.info('nonsupport ' + operation + ' operation!')
        raise myException('nonsupport ' + operation + ' operation!')

    logging.info('do : ' + operation + ' , please wait...')
    command_str = 'perl /usr/lib/vmware-vcli/apps/vm/vmcontrol.pl --url https://' \
                  + ip \
                  + ':443/sdk/webService --username ' \
                  + username \
                  + ' --password ' \
                  + password \
                  + ' --operation ' \
                  + operation \
                  + ' --vmname ' \
                  + vmname

    fp = os.popen(command_str).read()
    logging.info(fp)
    
    if checkStr in fp.lower():
        logging.info('do : ' + operation + ' ok!')
        return 'ok'
    else:
        logging.error('Failed! do : ' + operation + ' error!')
        raise myException('error' if fp == '' else fp)
#        return 'error' if fp == '' else fp


'''
----------------------------------------------------------------------------
Information of Virtual Machine PlatformAndSTAF-94

Name:            PlatformAndSTAF-94
No. of CPU(s):           4
Memory Size:             4096
Virtual Disks:           1
Template:                0
vmPathName:              [datastore1] PlatformAndSTAF/PlatformAndSTAF.vmx
Guest OS:                Red Hat Enterprise Linux 6 (64-bit)
guestId:                 rhel6_64Guest
Host name:               94staf
IP Address:              192.168.32.94
VMware Tools:            VMware Tools is running and the version is current
Cpu usage:               6 MHz
Host memory usage:               1918 MB
Guest memory usage:              0 MB
Overall Status:          The entity is OK
----------------------------------------------------------------------------
Information of Virtual Machine AbroadThirdPayAndCallCenterSysTestEnv-88

Name:            AbroadThirdPayAndCallCenterSysTestEnv-88
No. of CPU(s):           2
Memory Size:             4096
Virtual Disks:           1
Template:                0
vmPathName:              [Data] jink/jink.vmx
Guest OS:                Not Known
guestId:                 Not Known
Host name:               Not Known
IP Address:              Not Known
VMware Tools:            VMware Tools is not running.
Cpu usage:               Not Known
Host memory usage:               Not Known
Guest memory usage:              Not Known
Overall Status:          The entity is OK
----------------------------------------------------------------------------
Virtual Machine QA-2008Server not found.
----------------------------------------------------------------------------
Resource pool <自动化测试资源池(86~9900)> not found.
----------------------------------------------------------------------------
No Virtual Machine found.
'''


def vmInfo(ip, username, password, vmname, pool):
    '''

    :param ip:
    :param username:
    :param password:
    :param vmname:
    :param pool:
    '''
    suffixStr = ''
    VCLI_PATH = '/usr/lib/vmware-vcli/apps/'
    if vmname != '':
        suffixStr = suffixStr + ' --vmname ' + vmname
    elif pool != '':
        suffixStr = suffixStr + ' --pool ' + pool

    logging.info('query virtual machine: ' + vmname + ', please wait...')
    command_str = 'perl ' \
                  + VCLI_PATH \
                  + 'vm/vminfo.pl --url https://' \
                  + ip \
                  + ':443/sdk/webService --username ' \
                  + username \
                  + ' --password ' \
                  + password \
                  + suffixStr \
                  + ' --out ' \
                  + VCLI_PATH \
                  + 'out.xml'
    
    fp = os.popen(command_str).read()
    
    # 成功执行vminfo.pl命令后，返回结果保存在out.xml文件中，因此fp中的内容为空，如果不为空，则执行出错
    if fp != '':
        logging.info(fp)
        raise myException(fp)
    else:
        # xml.dom.minidom.parse使用open()打开文件，路径中带有""会导致打开失败，因此需把VCLI_PATH中的""全部删掉
        outputXML = VCLI_PATH.replace('"', '') + 'out.xml'
        old = open(outputXML)
        oldXML = old.readlines()
        newXML = []
        
        for line in oldXML:
            if '&' in line:
                line = line.replace('&', '&amp;')
            newXML.append(line)
        new = open(outputXML, 'w')
        new.writelines(newXML)
        new.close()
        old.close()
                
        dom = xml.dom.minidom.parse(outputXML)
        root = dom.documentElement
        vms = root.getElementsByTagName('VM')
        vmInfoList = []
        if vms == '':
            raise myException('no virtual machine information')
        
        def getVMTagValue(vm, tag):
            element = vm.getElementsByTagName(tag)
            if element:
                if element[0].firstChild is not None:
                    vmDict[tag] = element[0].firstChild.data
                else:
                    vmDict[tag] = 'Not Known'
                
        for vm in vms:
            keyList = ['Name', 'noCPU', 'memorySize', 'virtualDisks',
                       'template', 'vmPathName', 'guestOS', 'guestId',
                       'hostName', 'ipAddress', 'VMwareTools', 'cpuUsage',
                       'hostMemoryUsage', 'guestMemoryUsage', 'overallStatus', 'state'
                       ]
            vmDict = dict.fromkeys(keyList)
            for key in keyList:
                getVMTagValue(vm, key)
                
            if vmDict['ipAddress'] == 'Not Known':
                vmDict['state'] = 'poweroff'
            elif '.' in vmDict['ipAddress']:
                vmDict['state'] = 'poweron'
                
            vmInfoList.append(vmDict)
            
        # os.remove删除文件时，路径中带有""会导致失败，因此需把VCLI_PATH中的""全部删掉
        os.remove(outputXML)
        return vmInfoList


# 获得最晚和最早的快照名称
def getLastAndFirstSnapshotName(vmname, ip, username, password):
    snapshotStr = listSnapshot(vmname, ip, username, password)
    snapshotNameList = []
    snapshotNameListTmp = snapshotStr.split('\n')
    for strTmp in snapshotNameListTmp:
        if 'snapshot_' in strTmp:
            index = strTmp.find('snapshot_')
            tmp = strTmp[index:]
            spaceindex = tmp.find(r' ')
            snapshotName = strTmp[index:index + spaceindex]
            snapshotNameList.append(snapshotName)
    snapshotList = []
    for snapshot in snapshotNameList:
        snapshot = snapshot.replace('snapshot_', '')
        snapshotList.append(snapshot)
    tup = (max(snapshotList), min(snapshotList))
    currentTup = ('snapshot_' + tup[0], 'snapshot_' + tup[1])
    return currentTup


# 获得快照状态：1：开机；0：未开机
def getSnapshotStat(snapName, ip, user, pwd, vmname):
    t = snapshotManager(ip, user, pwd, vmname, 'list', '', '')
    list1 = t.split('\n')
    statStr = ''
    for i in list1:
        if snapName in i:
            statStr = i
    if statStr == '':
        logging.info("%s is not exists" % snapName)
        raise myException.MyException("%s is not exists" % snapName)
    else:
        if 'poweredon' in statStr.lower():
            return '1'
        elif 'poweredoff' in statStr.lower():
            return '0'
        else:
            logging.info("Snapshot list Error")
            raise myException.MyException("Snapshot list Error")


# 获得新快照名称：以snapshot_开头，后接当前时间年月日时分的字符串，例如：snapshot_201512031630
def getNewSnapshotName():
    strTmp = time.strftime("%Y%m%d%H%M", time.localtime(time.time()))
    newSnapshotName = 'snapshot_' + strTmp
    return newSnapshotName
