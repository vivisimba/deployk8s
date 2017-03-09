# -*- coding: utf-8 -*-
'''
Created on 2016年10月18日

@author: Simba
'''


import config.config as CONFIG
import tool
import logging
import log.logService as logService
import urllib2
import os
import subprocess
import sys
import replace_rc


def scpRedisAndZkFile(ip):
    # 删除节点上原文件夹
    cmdList = []
    redisCmdStr = 'rm -rf /redis'
    zkconfigStr = 'rm -rf /platform-config'
    nginxDirStr = 'rm -rf /nginx'
    dubboStr = 'rm -rf /dubbo'
    swaggerStr = 'rm -rf /swagger'
    cmdList.append(redisCmdStr)
    cmdList.append(zkconfigStr)
    cmdList.append(nginxDirStr)
    cmdList.append(dubboStr)
    cmdList.append(swaggerStr)
    tool.sshAndRun(cmdList, ip)
    # 传送redis的新的文件到节点上
    filePathList = []
    uploadPathList = []
    redisFilePath = '%s/redis' % CONFIG.ROOT_HOME
    redisUploadPath = '/'
    filePathList.append(redisFilePath)
    uploadPathList.append(redisUploadPath)
    tool.uploadViaSCP(filePathList, uploadPathList, ip)
    # 传送zk的新的配置到节点上
    zkPathList = []
    zkuploadPathList = []
    zkFilePath = '%s/platform-config' % (CONFIG.ROOT_HOME + os.sep + 'zkconfig')
    zkUploadPath = '/'
    zkPathList.append(zkFilePath)
    zkuploadPathList.append(zkUploadPath)
    tool.uploadViaSCP(zkPathList, zkuploadPathList, ip)
    # 传送nginx文件到节点上
    nginxDirPathList = []
    nginxDiruploadPathList = []
    nginxDirPath = CONFIG.ROOT_HOME + os.sep + 'nginx'
    nginxDiruploadPath = '/'
    nginxDirPathList.append(nginxDirPath)
    nginxDiruploadPathList.append(nginxDiruploadPath)
    tool.uploadViaSCP(nginxDirPathList, nginxDiruploadPathList, ip)
    # 传送dubbo文件到节点上
    dubboDirPathList = []
    dubboDiruploadPathList = []
    dubboDirPath = CONFIG.ROOT_HOME + os.sep + 'dubbo'
    dubboDiruploadPath = '/'
    dubboDirPathList.append(dubboDirPath)
    dubboDiruploadPathList.append(dubboDiruploadPath)
    tool.uploadViaSCP(dubboDirPathList, dubboDiruploadPathList, ip)
    # 传送swagger文件到节点上
    swaggerPathList = []
    swaggeruploadPathList = []
    swaggerPath = CONFIG.ROOT_HOME + os.sep + 'swagger'
    swaggeruploadPath = '/'
    swaggerPathList.append(swaggerPath)
    swaggeruploadPathList.append(swaggeruploadPath)
    tool.uploadViaSCP(swaggerPathList, swaggeruploadPathList, ip)


# 下载platform-config文件
def getPlatformconfig(url, fileName):
    f = urllib2.urlopen(url)
    data = f.read()
    with open(fileName, "wb") as code:
        code.write(data)


# 修改BASIC.groovy文件
def modifyBasicGroovyFile():
    fileDir = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'BASIC.groovy'
#    fileDir = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'platform-config' + os.sep + 'configScripts' + os.sep + 'BASIC.groovy'
    fileList = []
    fileList.append(fileDir)
    replace_rc.updateImageTag(fileList, '{sentinel_ip}', CONFIG.NODEMACHINE[0])
    replace_rc.updateImageTag(fileList, '{sentinel_name}', CONFIG.sentinel_name)
    replace_rc.updateImageTag(fileList, '{oracle_ip}', CONFIG.DB_ENV_DIC['NEW_BOSS_DB_IP'])
    replace_rc.updateImageTag(fileList, '{oracle_service_name}', CONFIG.DB_ENV_DIC['NEW_BOSS_DB_SERVICE_NAME'])
    


# 修改CONFIG.groovy文件
def modifyConfigGroovyFile(flywayFlag):
    fileDir = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'platform-config' + os.sep + 'configScripts' + os.sep + 'CONFIG.groovy'
    fileList = []
    fileList.append(fileDir)
    if flywayFlag == 0:
        replace_rc.updateImageTag(fileList, 'auto_migrate = "true"', 'auto_migrate = "false"')
    else:
        replace_rc.updateImageTag(fileList, 'auto_migrate = "false"', 'auto_migrate = "true"')


# 修改redis的配置文件
def modifyRedisConfigFile():
    fileList = []
    slaveFileDir = CONFIG.NFS_HOST_DIR + os.sep + 'redis' + os.sep + 'slave' + os.sep + '6381.conf'
    sentinelFileDir = CONFIG.NFS_HOST_DIR + os.sep + 'redis' + os.sep + 'sentinel' + os.sep + 'sentinel_26379.conf'
    fileList.append(slaveFileDir)
    fileList.append(sentinelFileDir)
    replace_rc.updateImageTag(fileList, '{redismaster_ip}', CONFIG.NODEMACHINE[1])
    replace_rc.updateImageTag(fileList, '{sentinel_name}', CONFIG.sentinel_name)
    
    
def prepareZkConfig(version, flywayFlag):
    # 编辑Basic.groovy文件
    modifyBasicGroovyFile()
    # 删除本地zk文件
    logging.info("Del local platform-config dir and zip file.")
    cmdStr1 = 'rm -rf %s' % (CONFIG.NFS_HOST_DIR + '/zkconfig' + os.sep + 'platform-config')
    cmdStr2 = 'rm -f %s' % (CONFIG.NFS_HOST_DIR + '/zkconfig' + os.sep + '*.zip')
    p1 = subprocess.Popen(cmdStr1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p1.wait()
    p2 = subprocess.Popen(cmdStr2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p2.wait()
    # 下载zkconfig包
    logging.info("Download platform-config.zip file.")
    url = 'ftp://10.0.250.250/stariboss-10.X/%s%s/ConfigAndDbscript/platform-config-%s.zip' % (CONFIG.DB_ENV_DIC['NEW_BOSS_FTPDIR'], version, version)
    fileName = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'platform-config.zip'
    getPlatformconfig(url, fileName)
    # 解压
    logging.info("Unzip platform-config.zip file.")
    tool.unzipFile(fileName, CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep)

    # 更换配置文件
#     # 删除config.groovy
#     logging.info("Change file CONFIG.groovy with local one.")
#     groovyConfigFile = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'platform-config' + os.sep + 'configScripts' + os.sep + 'CONFIG.groovy'
#     delgroovyConfigStr = 'rm -f %s' % groovyConfigFile
#     p3 = subprocess.Popen(delgroovyConfigStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     p3.wait()

    # 删除basic.groovy
    groovyBasicFile = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'platform-config' + os.sep + 'configScripts' + os.sep + 'BASIC.groovy'
    delgroovyBasicStr = 'rm -f %s' % groovyBasicFile
    p5 = subprocess.Popen(delgroovyBasicStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p5.wait()
    
    
#     if flywayFlag == '0':
#        cpFrom = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'CONFIG.groovy'
#     else:
#         cpFrom = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'flyway' + os.sep + 'CONFIG.groovy'
#     cpTo = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'platform-config' + os.sep + 'configScripts' + os.sep
#     cpStr = 'cp %s %s' % (cpFrom, cpTo)
#     p4 = subprocess.Popen(cpStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     p4.wait()
    
    cpFromBasic = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep  + 'BASIC.groovy'
    cpToBasic = CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep + 'platform-config' + os.sep + 'configScripts' + os.sep
    cpStrBasic = 'cp %s %s' % (cpFromBasic, cpToBasic)
    p6 = subprocess.Popen(cpStrBasic, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p6.wait()
    # 编辑CONFIG.groovy文件
    modifyConfigGroovyFile(flywayFlag)
#    modifyBasicGroovyFile()

#    machineList = CONFIG.NODEMACHINE
    # 使用NFS硬盘后，不需要下面的代码往各个节点拷贝文件
#     for i in machineList:
#         logging.info("Copy file to %s" % i)
#         scpRedisAndZkFile(i)


def run():
    # (脚本名称，版本号例如：7.1.1.100，获取配置的ftp目录如：TEST或者system-TEST)
    parameterList = sys.argv
    prepareZkConfig(parameterList[1])


def start():
    parameterList = sys.argv
    url = 'ftp://10.0.250.250/Stariboss-7.X/TEST/%s/ConfigAndDbscript/platform-config-%s.zip' % (parameterList[1], parameterList[1])
    fileName = CONFIG.ROOT_HOME + os.sep + 'zkconfig' + os.sep + 'platform-config.zip'
    getPlatformconfig(url, fileName)
        
if __name__ == '__main__':
    logService.initLogging()
    run()
    # start()
    logService.destoryLogging()
    
    