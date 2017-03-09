# -*- coding: utf-8 -*-
'''
Created on 2016年10月19日

@author: Simba
'''


import config.config as CONFIG
import logging
import log.logService as logService
import sys
import subprocess
import exception.myException as myException
import os


# 更新文件中的镜像tag号
def updateImageTag(fileList, oldTag, newTag):
    needUpdateList = []
    for fileWholeNameTmp in fileList:
        fReadTmp = open(fileWholeNameTmp, 'r')
        lineListTmp = fReadTmp.readlines()
        for lineTmp in lineListTmp:
            if oldTag in lineTmp:
                needUpdateList.append(fileWholeNameTmp)
    for fileWholeName in needUpdateList:
        fRead = open(fileWholeName, 'r')
        lineList = fRead.readlines()
        fWrite = open(fileWholeName, 'w')
        for line in lineList:
            if oldTag in line:
                newLine = line.replace(oldTag, newTag)
                fWrite.write(newLine)
            else:
                fWrite.write(line)
        fRead.close()
        fWrite.close()
        logging.info("%s has been updated" % fileWholeName)
        logging.info("=======")


# 获得所有以.yaml或.YAML结尾的文件
def getAllYamlFile(fileDir):
    yamlFileList = []
    # 递归获得fileDir下的所有目录和文件
    pointer = os.walk(fileDir)
    # 依次处理每个元组
    for fileTup in pointer:
        # 如果当前目录下有文件
        if len(fileTup[2]) > 0:
            # 组合当前目录和当前目录下的文件名，获得文件完成路径
            for yamlFile in fileTup[2]:
                fileWholeName = os.path.join(fileTup[0], yamlFile)
                # 如果文件以yaml或者YAML结尾，则添加完成文件名称到文件列表中
                if (fileWholeName.endswith('.yaml') or fileWholeName.endswith('.YAML')):
                    yamlFileList.append(fileWholeName)
    return yamlFileList


# 获得需要更新镜像的rc名称
def getRcName():
    cmdStr = 'kubectl get rc -o name --namespace=kube-system'
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
    # 排除不需要更新镜像的RC
    # 去掉换行符
    rcLastList = []
    for i in rcRealNameList:
        newName = i.strip()
        rcLastList.append(newName)
    exincludeList = []
    for rc in rcLastList:
        if rc in CONFIG.EXCLUDE_RC_LIST:
            pass
        else:
            exincludeList.append(rc)
    return exincludeList


# 更新RC镜像
def updateRC(rcNameList, newTag):
    print rcNameList
    for rc in rcNameList:
        cmdStr = 'kubectl rolling-update %s --image=registry:5000/library/%s:%s --namespace=kube-system' % (rc, rc, newTag)
        logging.info(cmdStr)
        p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        str1 = p.stdout.read()
        str2 = p.stderr.read()
        if len(str1) > 0:
            logging.info("%s" % str1)
        else:
            logging.error("%s" % str2)


# 参数：(脚本名称，被rolling的RC文件所在绝对路径，旧标签，新TAG)
def run():
    parameterList = sys.argv
    while True:
        if len(parameterList) != 4:
            logging.info("Please input the following parameters one by one, for example: absolute path of RC files, original tag number, new tag number")
            absolutePath = raw_input("Please input the absolutePath:")
            oldtag = raw_input("Please input the oldtag:")
            newtag = raw_input("Please input the newtag:")
            parameterList.insert(1, absolutePath)
            parameterList.insert(2, oldtag)
            parameterList.insert(3, newtag)
        else:
            break
    # 更新RC文件中的镜像标签
    updateImageTag(getAllYamlFile(parameterList[1]), parameterList[2], parameterList[3])
    # 获取需要更新的RC列表
    rcList = getRcName()
    # 更新RC
    updateRC(rcList, parameterList[3])
    logging.info("Update finished")
    # 执行命令
            

if __name__ == '__main__':
    logService.initLogging()
    run()
    logService.destoryLogging()
