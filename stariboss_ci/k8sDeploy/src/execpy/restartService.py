# -*- coding: utf-8 -*-
'''
Created on 2016年10月9日

@author: Simba
'''


import config.config as CONFIG
import tool
import logging
import log.logService as logService
import time


# 依次重启各节点上的服务
def restartService():
    masterList = ['systemctl restart kube-apiserver.service',
                  'systemctl restart kube-controller-manager.service',
                  'systemctl restart kube-scheduler.service'
                  ]
    nodeCmdList = ['systemctl restart flanneld.service',
                   'systemctl restart docker.service',
                   'systemctl restart kubelet.service',
                   'systemctl restart kube-proxy.service'
                   ]
    # 重启master上的服务
    tool.sshAndRun(masterList, CONFIG.MASTERIP[0])
    logging.info("Services of Master restart over")
    # 重启Node上的服务
    for ip in CONFIG.NODEMACHINE:
        for cmd in nodeCmdList:
            cmdList = []
            if 'flanneld' in cmd:
                cmdList.append(cmd)
                tool.sshAndRun(cmdList, ip)
                logging.info('%s on %s has been restarted,please wait 10 seds' % ('flanneld.service', ip))
                time.sleep(10)
            else:
                cmdList.append(cmd)
                tool.sshAndRun(cmdList, ip)
        logging.info("Services of Node:%s restart over" % ip)


if __name__ == '__main__':
    logService.initLogging()
    restartService()
    # start()
    logService.destoryLogging()
    
    