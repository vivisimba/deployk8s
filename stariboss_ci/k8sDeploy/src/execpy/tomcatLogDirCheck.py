# -*- coding: utf-8 -*-
'''
Created on 2017年2月16日

@author: Simba
'''
import config.config as CONFIG
import os
import logging


# 检查目录是否存在，如果不存在则级联创建
def checkAndCreateDir(dirName):
    if os.path.exists(dirName):
        logging.info("The dir %s exists." % dirName)
    else:
        os.makedirs(dirName)
        logging.info("The dir %s doesn't exist,Now it has been created successfully." % dirName)


# 检查宿主机，各模块tomcat的日志目录是否存在，如果不存在，则创建
def tomcatLogDirCheck():
    # 获得模块名称列表
    dpmList = CONFIG.RC_SVC_PREFIX[:]
    dpmList.remove('zookeeper')
    dpmList.remove('pushzkconfig')
#    dpmList.remove('platform-cache-config')
    dpmList.remove('zkdash')
    dpmList.remove('mysql')
    dpmList.remove('zookeeperui')
    
    moduleList = dpmList[:]
    for moduleName in moduleList:
        dirName = CONFIG.NFS_HOST_DIR + os.sep + 'moduleLogs' + os.sep + moduleName + os.sep + 'logs'
        checkAndCreateDir(dirName)
