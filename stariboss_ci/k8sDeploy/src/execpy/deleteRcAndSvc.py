# -*- coding: utf-8 -*-
'''
Created on 2016年10月24日

@author: Simba
'''
import subprocess
import exception.myException as myException
import log.logService as logService
import logging
import config.config as CONFIG


# 获得RC列表
def getRcName():
    cmdStr = 'kubectl get rc -o name --namespace=%s' % CONFIG.NAME_SPACE
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if p.stdout:
        rcNameList = p.stdout.readlines()
    else:
        raise myException.MyException("%s" % p.stderr)
    rcRealNameList = []
    for rcName in rcNameList:
        if 'replicationcontroller/' in rcName:
            rcRealName = rcName.split('replicationcontroller/')[1]
            rcRealNameList.append(rcRealName)
    # 去掉换行符
    rcLastList = []
    for i in rcRealNameList:
        newName = i.strip()
        rcLastList.append(newName)
#     # 排除不需要更新镜像的RC
#     exincludeList = []
#     for rc in rcLastList:
#         if rc in CONFIG.EXCLUDE_RC_LIST:
#             pass
#         else:
#             exincludeList.append(rc)
    return rcLastList


# 获得deployment列表
def getDpmName():
    cmdStr = 'kubectl get deployment -o name --namespace=%s' % CONFIG.NAME_SPACE
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if p.stdout:
        rcNameList = p.stdout.readlines()
    else:
        raise myException.MyException("%s" % p.stderr)
    rcRealNameList = []
    for rcName in rcNameList:
        if 'deployment/' in rcName:
            rcRealName = rcName.split('deployment/')[1]
            rcRealNameList.append(rcRealName)
    # 去掉换行符
    rcLastList = []
    for i in rcRealNameList:
        newName = i.strip()
        rcLastList.append(newName)
#     # 排除不需要更新镜像的RC
#     exincludeList = []
#     for rc in rcLastList:
#         if rc in CONFIG.EXCLUDE_RC_LIST:
#             pass
#         else:
#             exincludeList.append(rc)
    return rcLastList


# 获得SVC列表
def getSVCName():
    cmdStr = 'kubectl get svc -o name --namespace=%s' % CONFIG.NAME_SPACE
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if p.stdout:
        svcNameList = p.stdout.readlines()
    else:
        raise myException.MyException("%s" % p.stderr)
    svcRealNameList = []
    for svcName in svcNameList:
        if 'service/' in svcName:
            svcRealName = svcName.split('service/')[1]
            svcRealNameList.append(svcRealName)
    # 去掉换行符
    svcLastList = []
    for i in svcRealNameList:
        newName = i.strip()
        svcLastList.append(newName)
    return svcLastList


# 删除RC和SVC
def deleteRcAndSvc():
    rcList = getRcName()
    svcList = getSVCName()
    if 'kube-dns' in rcList:
        rcList.remove('kube-dns')
    if 'kube-dns' in svcList:
        svcList.remove('kube-dns')
    # 删除SVC
    for svcName in svcList:
        logging.info('kubectl delete svc %s --namespace=%s' % (svcName, CONFIG.NAME_SPACE))
        p = subprocess.Popen('kubectl delete svc %s --namespace=%s' % (svcName, CONFIG.NAME_SPACE), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        str1 = p.stdout.read()
        str2 = p.stderr.read()
        if len(str1) > 0:
            logging.info("%s" % str1)
        else:
            logging.error("%s" % str2)
    # 删除RC
    for rcName in rcList:
        logging.info('kubectl delete rc %s --namespace=%s' % (rcName, CONFIG.NAME_SPACE))
        rcP = subprocess.Popen('kubectl delete rc %s --namespace=%s' % (rcName, CONFIG.NAME_SPACE), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        str3 = rcP.stdout.read()
        str4 = rcP.stderr.read()
        if len(str1) > 0:
            logging.info("%s" % str3)
        else:
            logging.error("%s" % str4)


# 删除deployment和svc
def deleteDpmandSvc():
    dpmList = getDpmName()
    svcList = getSVCName()
    # 删除SVC
    for svcName in svcList:
        logging.info('kubectl delete svc %s --namespace=%s' % (svcName, CONFIG.NAME_SPACE))
        p = subprocess.Popen('kubectl delete svc %s --namespace=%s' % (svcName, CONFIG.NAME_SPACE), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        str1 = p.stdout.read()
        str2 = p.stderr.read()
        if len(str1) > 0:
            logging.info("%s" % str1)
        else:
            logging.error("%s" % str2)
    # 删除deployment
    for dpmName in dpmList:
        logging.info('kubectl delete deployment %s --namespace=%s' % (dpmName, CONFIG.NAME_SPACE))
        rcP = subprocess.Popen('kubectl delete deployment %s --namespace=%s' % (dpmName, CONFIG.NAME_SPACE), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        str3 = rcP.stdout.read()
        str4 = rcP.stderr.read()
        if len(str3) > 0:
            logging.info("%s" % str3)
        else:
            logging.error("%s" % str4)


# 运行
def run():
    # deleteRcAndSvc()
    deleteDpmandSvc()
    
    
if __name__ == '__main__':
    logService.initLogging()
    run()
    logService.destoryLogging()
