# -*- coding: utf-8 -*-
'''
Created on 2017年3月1日

@author: Simba
'''


import tool
import log.logService as logService
import logging
import exception.myException as myException
import config.config as CONFIG
import sys


# 修改master的时间
def changeMasterTime(newTime, masterIp):
    newTime = newTime + '.07'
    cmds = []
    cmdStr = 'date %s' % newTime
    cmds.append(cmdStr)
    print "**************************"
    resTup = tool.sshAndRun(cmds, masterIp)
    print len(resTup[0][cmdStr])
    logging.info(' '.join(resTup[0][cmdStr]))
    if resTup[1][cmdStr]:
        logging.error(' '.join(resTup[1][cmdStr]))
        raise myException.MyException(' '.join(resTup[1][cmdStr]))
    logging.info("Time of master %s has been changed successfully." % masterIp)


# 时间同步
def syncTimeWithMater(nodeIpList, masterIp):
    for nodeIp in nodeIpList:
        cmdStrList = []
        print masterIp
        print nodeIp
        cmdStr = 'ntpdate -u %s' % masterIp
        cmdStrList.append(cmdStr)
        print cmdStrList
        resTup = tool.sshAndRun(cmdStrList, nodeIp)
        logging.info(' '.join(resTup[0][cmdStr]))
        if resTup[1][cmdStr]:
            logging.error(' '.join(resTup[1][cmdStr]))
            raise myException.MyException(' '.join(resTup[1][cmdStr]))
        logging.info("Time of node %s has been changed successfully." % nodeIp)


# 打印各机器的时间
def showTimeOfEveryMachine(masterIpList, nodeIpList):
    ipList = masterIpList + nodeIpList
    strList = []
    for ipAddr in ipList:
        cmdList = []
        cmdStr = 'date'
        cmdList.append(cmdStr)
        resTup = tool.sshAndRun(cmdList, ipAddr)
        res = ' '.join(resTup[0][cmdStr])
        wholeRes = ('Time of %s' % ipAddr) + ":" + res
        strList.append(wholeRes)
    for infoStr in strList:
        logging.info(infoStr)


# date命令修改时间
def changeTimeByDateCmd(machineList, newTime):
    newTime = newTime + '.07'
    cmdStr = 'date %s' % newTime
    cmdList = []
    cmdList.append(cmdStr)
    for machine in machineList:
        resTup = tool.sshAndRun(cmdList, machine)
        logging.info(' '.join(resTup[0][cmdStr]))
        if resTup[1][cmdStr]:
            logging.error(' '.join(resTup[1][cmdStr]))
            raise myException.MyException(' '.join(resTup[1][cmdStr]))
        logging.info("Time of node %s has been changed successfully." % machine)


def run():
    parameterList = sys.argv
    # 各节点与master进行时间同步
    machineList = CONFIG.MASTERIP + CONFIG.NODEMACHINE
    changeTimeByDateCmd(machineList, parameterList[1])
    # 打印集群各机器的时间
    showTimeOfEveryMachine(CONFIG.MASTERIP, CONFIG.NODEMACHINE)


if __name__ == '__main__':
    logService.initLogging()
    '''
    :param 脚本本身
    :param newTime:   想要更改的时间，格式：月日时分年:MMDDHHMIYYYY
    '''
    run()
    logService.destoryLogging()
    