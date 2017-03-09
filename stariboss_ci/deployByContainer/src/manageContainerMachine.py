# -*- coding: utf-8 -*-
'''
Created on 2016年5月11日

@author: Simba
'''


import paramiko
import logging
import exception.myException as myException
import config.config as CONFIG
import remoteShell
import os
import time
import utils.util as utils
import subprocess


# 远程执行shell命令，返回字典格式{命令：返回结果列表}
def sshAndRun(cmds, ip, port=22, username='root', password='123456'):
    logging.info("=============================")
    '''
    ssh登录,并依次执行cmds列表中的命令
    cmds : 执行的命令列表
    ip : 远程服务器IP地址
    port : 远程服务器端口,默认22
    username : 远程服务器登录用户名,默认root
    password : 远程服务器登录密码,默认123456
    '''
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=username, password=password)
        resDic = {}
        errDic = {}
        for cmd in cmds:
            # ssh.exec_command(cmd)
            logging.info('exec cmd: ' + cmd)
            # print 'exec cmd: ' + cmd
            (stdin, stdout, stderr) = ssh.exec_command(cmd)
            resDic[cmd] = stdout.readlines()
            errDic[cmd] = stderr.readlines()
        return resDic, errDic
    except Exception, e:
        logging.warn(e)
    finally:
        ssh.close()


# 查看指定机器上运行中的容器,返回运行容器ID列表
def checkRunningContainer(ip):
    logging.info("Start to detecte the number of running container")
    resTup = sshAndRun(['docker ps -q'], ip)
    runningContainerIdList = []
    for i in resTup[0]['docker ps -q']:
        j = i.strip()
        runningContainerIdList.append(j)
    return runningContainerIdList


# 查询指定机器上的所有容器，包含已停止的容器，返回容器ID列表
def checkAllContainer(ip):
    logging.info("Start to detecte the number of all container")
    resTup = sshAndRun(['docker ps -qa'], ip)
    containerIdList = []
    for i in resTup[0]['docker ps -qa']:
        t = i.strip()
        containerIdList.append(t)
    return containerIdList


# 停止正在运行的容器列表，返回'OK'
def stopRunningList(ip):
    runningContainerList = checkRunningContainer(ip)
    logging.info("============================")
    logging.info("Start to stop running containers on %s" % ip)
    for i in runningContainerList:
        sshAndRun(['docker stop %s' % i], ip)
    resList = checkRunningContainer(ip)
    if not resList:
        return 'OK'
    else:
        raise myException.MyException("The number of stopped is not equal to the number of detected")


# 删除所有已停止的容器，返回'OK'
def deleteStoppedContainerList(ip):
    allContainerList = checkAllContainer(ip)
    logging.info("============================")
    logging.info("Start to delete all container on %s" % ip)
    if allContainerList:
        resTup = sshAndRun(['docker ps -qa| xargs docker rm'], ip)
        for i in resTup[0]['docker ps -qa| xargs docker rm']:
            i = i.strip()
            logging.info("----------------------------")
            logging.info("The container:%s has been deleted." % i)
    else:
        logging.info("No container need to be delete.")
    time.sleep(2)
    newAllContainerList = checkAllContainer(ip)
    if not newAllContainerList:
        logging.info("All containers have been deleted success")
        return 'OK'
    else:
        for j in newAllContainerList:
            logging.info("%s can't be deleted, please check it." % j)
        raise myException.MyException("Some containers can't be deleted.")


# 查询容器所在机器的所有镜像,返回镜像名称、标签、ID组成的元组，组成的列表，如[(名称，标签，ID)]
def checkAllImages(ip):
    logging.info("Start to check all of images on %s" % ip)
    resTup = sshAndRun(['docker images'], ip)
    allImagesList = resTup[0]['docker images']
    newImagesList = []
    for i in range(len(allImagesList)):
        if i == 0:
            pass
        else:
            t = allImagesList[i].strip()
            newImagesList.append(t)
    actualImagesList = []
    for j in newImagesList:
        tempTup = (j[0], j[1], j[2])
        actualImagesList.append(tempTup)
    return actualImagesList


# 删除容器所在机器的所有镜像,返回'OK'
def deleteAllImages(ip):
    imagesList = checkAllImages(ip)
    if imagesList:
        logging.info("=====================")
        logging.info("Start to delete all images on %s" % ip)
        sshAndRun(['docker rmi -f $(docker images -q)'], ip)
        newimagesList = checkAllImages(ip)
        if newimagesList:
            raise myException.MyException("Delete images of %s error, please check it." % ip)
    logging.info("There is no image on %s." % ip)
    return 'OK'


# 获得对应环境的容器服务器（停止运行中的容器，删除所有容器，删除所有镜像），返回容器服务器IP
# def getContainerSeverIp(flag_env):
#     if '1' == flag_env:
#         ip = CONFIG.MANAUL_TEST_NEW_BOSS_CONTAINER_MACHINE_NAME
#     elif '2' == flag_env:
#         ip = CONFIG.AUTO_TEST_NEW_BOSS_CONTAINER_MACHINE_NAME
#     elif '3' == flag_env:
#         ip = CONFIG.DEV_TEST_NEW_BOSS_CONTAINER_MACHINE_NAME
#     return ip


# 传送容器启动需挂载的tomcat的server.xml文件到指定服务器
def scpTomcatServerFile(ip, fromPath, toPath):
    formPathList = []
    toPathList = []
    formPathList.append(fromPath)
    toPathList.append(toPath)
    # 如果ip上不存在指定的目录，先创建指定的目录
    for i in toPathList:
        t = 'if [ ! -d "%s" ]; then mkdir -p %s; fi' % (i, i)
        m = []
        m.append(t)
        sshAndRun(m, ip)
    if remoteShell.uploadViaSCP(formPathList, toPathList, ip) == 'ok':
        return True
    else:
        logging.info("scp server.xml to %s error" % ip)
        raise myException.MyException("scp server.xml to %s error" % ip)


# # 获得对应server.xml文件在宿主机的位置
# def getDirOfServerXml(toPath, fromPath, containerName):
#     index = fromPath.rfind('/')
#     lastName = fromPath[index + 1:]
#     newPath = toPath + os.sep + lastName + os.sep + containerName + os.sep + 'server.xml'
#     return newPath
        

# 获得启动zookeeper容器命令列表
def getStartZookeeperCmdList(mapIp, tagName='basal'):
    cmdList = []
    zookeeperStr = 'docker run -d -p 2181:2181 --name %s --add-host zookeeper1:%s --restart=always --log-driver=none --add-host redis1:%s -e ZT=%s %s/%s:%s' % ('zookeeper',
                                                                                                                                                                mapIp,
                                                                                                                                                                mapIp,
                                                                                                                                                                CONFIG.CONTAINER_TZ,
                                                                                                                                                                CONFIG.DOCKERREPOSITORY,
                                                                                                                                                                'zookeeper',
                                                                                                                                                                tagName
                                                                                                                                                                )
    cmdList.append(zookeeperStr)
    return cmdList


# 获得启动redis命令列表
def getStartRedisCmdList(mapIp, configerFileDirStr, tagName='basal'):
    cmdList = []
    # 如果CONFIG.REDIS_MASTER_DATA目录不存在，则创建目录
    str1 = 'if [ ! -d "%s" ]; then mkdir -p %s; fi' % (CONFIG.REDIS_MASTER_DATA, CONFIG.REDIS_MASTER_DATA)
    str4 = 'chmod 777 %s' % CONFIG.REDIS_MASTER_DATA
    sshAndRun([str1, str4], mapIp)
    masterStr = 'docker run -d -p 6380:6380 --name %s --add-host zookeeper1:%s --add-host redis1:%s --restart=always --log-driver=none -e TZ=%s -v /%s/6380.conf:/usr/local/etc/redis/redis.conf -v %s:/data  %s/%s:%s redis-server /usr/local/etc/redis/redis.conf' % ('redisMaster',
                                                                                                                                                                                                                                                                        mapIp,
                                                                                                                                                                                                                                                                        mapIp,
                                                                                                                                                                                                                                                                        CONFIG.CONTAINER_TZ,
                                                                                                                                                                                                                                                                        CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr],
                                                                                                                                                                                                                                                                        CONFIG.REDIS_MASTER_DATA,
                                                                                                                                                                                                                                                                        CONFIG.DOCKERREPOSITORY,
                                                                                                                                                                                                                                                                        'redis',
                                                                                                                                                                                                                                                                        tagName
                                                                                                                                                                                                                                                                        )
    cmdList.append(masterStr)
    # 如果CONFIG.REDIS_SLAVE_DATA目录不存在，则创建目录
    str2 = 'if [ ! -d "%s" ]; then mkdir -p %s; fi' % (CONFIG.REDIS_SLAVE_DATA, CONFIG.REDIS_SLAVE_DATA)
    str5 = 'chmod 777 %s' % CONFIG.REDIS_SLAVE_DATA
    sshAndRun([str2, str5], mapIp)
    slaveStr = 'docker run -d -p 6381:6381 --name %s --add-host zookeeper1:%s --add-host redis1:%s --restart=always --log-driver=none -e TZ=%s -v /%s/6381.conf:/usr/local/etc/redis/redis.conf -v %s:/data  %s/%s:%s redis-server /usr/local/etc/redis/redis.conf' % ('redisSlave',
                                                                                                                                                                                                                                                                       mapIp,
                                                                                                                                                                                                                                                                       mapIp,
                                                                                                                                                                                                                                                                       CONFIG.CONTAINER_TZ,
                                                                                                                                                                                                                                                                       CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr],
                                                                                                                                                                                                                                                                       CONFIG.REDIS_SLAVE_DATA,
                                                                                                                                                                                                                                                                       CONFIG.DOCKERREPOSITORY,
                                                                                                                                                                                                                                                                       'redis',
                                                                                                                                                                                                                                                                       tagName
                                                                                                                                                                                                                                                                       )
    cmdList.append(slaveStr)
    # 如果CONFIG.REDIS_SENTINEL_DATA目录不存在，则创建目录
    str3 = 'if [ ! -d "%s" ]; then mkdir -p %s; fi' % (CONFIG.REDIS_SENTINEL_DATA, CONFIG.REDIS_SENTINEL_DATA)
    str6 = 'chmod 777 %s' % CONFIG.REDIS_SENTINEL_DATA
    sshAndRun([str3, str6], mapIp)
    sentinelStr = 'docker run -d -p 26379:26379 --name %s --add-host zookeeper1:%s --add-host redis1:%s --restart=always --log-driver=none -e TZ=%s -v /%s/sentinel_26379.conf:/usr/local/etc/redis/sentinel_26379.conf -v %s:/data  %s/%s:%s redis-sentinel /usr/local/etc/redis/sentinel_26379.conf' % ('redisSentinel',
                                                                                                                                                                                                                                                                                                          mapIp,
                                                                                                                                                                                                                                                                                                          mapIp,
                                                                                                                                                                                                                                                                                                          CONFIG.CONTAINER_TZ,
                                                                                                                                                                                                                                                                                                          CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr],
                                                                                                                                                                                                                                                                                                          CONFIG.REDIS_SENTINEL_DATA,
                                                                                                                                                                                                                                                                                                          CONFIG.DOCKERREPOSITORY,
                                                                                                                                                                                                                                                                                                          'redis',
                                                                                                                                                                                                                                                                                                          tagName
                                                                                                                                                                                                                                                                                                          )
    cmdList.append(sentinelStr)
    return cmdList


# 如果指定远程机器上的某目录存在，则删除该目录
def delRemoteDir(ip, absoluteDir):
    str1 = 'if [ ! -d "%s" ]; then :;else rm -rf %s;fi' % (absoluteDir, absoluteDir)
    sshAndRun([str1], ip)


# 获得dubbo启动命令列表
def getStartDubboContainerCmd(mapIp, tagName='basal'):
    cmdList = []
    dubboStr = 'docker run -d -p %s:8090 --name %s --add-host zookeeper1:%s --restart=always --log-driver=none --add-host redis1:%s -e TZ=%s %s/%s:%s' % (CONFIG.PORT_DIC['dubbo'],
                                                                                                                                                          'dubbo',
                                                                                                                                                          mapIp,
                                                                                                                                                          mapIp,
                                                                                                                                                          CONFIG.CONTAINER_TZ,
                                                                                                                                                          CONFIG.DOCKERREPOSITORY,
                                                                                                                                                          'dubbo',
                                                                                                                                                          tagName
                                                                                                                                                          )
    cmdList.append(dubboStr)
    return cmdList


# 获得platform-cache-config容器启动的命令列表，返回命令列表
def getStartCacheContainerCmdList(mapIp, tagName):
    imageName = CONFIG.DOCKERREPOSITORY + '/' + 'platform-cache-config' + ':' + tagName
    cmdList = []
    cmd = 'docker run -d --name %s --add-host zookeeper1:%s --add-host redis1:%s --restart=always --log-driver=none -e TZ=%s %s ' % ('platform-cache-config',
                                                                                                                                     mapIp,
                                                                                                                                     mapIp,
                                                                                                                                     CONFIG.CONTAINER_TZ,
                                                                                                                                     imageName
                                                                                                                                     )
    cmdList.append(cmd)
    return cmdList


# 获得zookeeper——ui和redis——stat镜像的启动命令
def getStartUiContainerCmd(mapIp, tagName='basal'):
    zkUiImageName = CONFIG.DOCKERREPOSITORY + '/' + 'zookeeperui' + ':' + tagName
    redisUiImageName = CONFIG.DOCKERREPOSITORY + '/' + 'redis-stat' + ':' + tagName
    cmdList = []
    zkCmd = "docker run -d --name %s --add-host zookeeper1:%s --restart=always --log-driver=none -e TZ=%s -p 9090:9090 %s " % ('zookeeper-ui',
                                                                                                                               mapIp,
                                                                                                                               CONFIG.CONTAINER_TZ,
                                                                                                                               zkUiImageName
                                                                                                                               ) \
        + "sh -c \"sed -i -e 's/\${ZOOKEEPER_ADDRESS}/zookeeper1/g' /zkui/config.cfg && java -jar /zkui/zkui.jar /zkui/config.cfg\""
            
    cmdList.append(zkCmd)
    redisCmd = "docker run -d --name %s --add-host redis1:%s --restart=always --log-driver=none -e TZ=%s -p 63790:63790 %s " % ('redis-stat',
                                                                                                                                mapIp,
                                                                                                                                CONFIG.CONTAINER_TZ,
                                                                                                                                redisUiImageName
                                                                                                                                ) \
        + "--server redis1:6380 redis1:6381 redis1:26379"
    cmdList.append(redisCmd)
    return cmdList


def getStartWarContainerCmd(mapIp, tagName, warContainersNameList):
    cmdDic = {}
    containerList = warContainersNameList
    for containerName in containerList:
        if 'service' in containerName:
            dirCmdList = []
            dirCmd = 'if [ ! -d "%s" ]; then mkdir -p %s; else rm -f %s*; fi' % ('/' + containerName + '-' + 'logs/', '/' + containerName + '-' + 'logs/', '/' + containerName + '-' + 'logs/')
            dirCmdList.append(dirCmd)
            sshAndRun(dirCmdList, mapIp)
            cmd = 'docker run -d --name %s --add-host zookeeper1:%s --add-host redis1:%s --restart=always --log-driver=none -v %s:%s -e TZ=%s %s/%s:%s ' % (containerName,
                                                                                                                                                            mapIp,
                                                                                                                                                            mapIp,
                                                                                                                                                            '/' + containerName + '-' + 'logs/',
                                                                                                                                                            '/usr/local/tomcat/logs/',
                                                                                                                                                            CONFIG.CONTAINER_TZ,
                                                                                                                                                            CONFIG.DOCKERREPOSITORY,
                                                                                                                                                            containerName,
                                                                                                                                                            tagName
                                                                                                                                                            )

            cmdDic[containerName] = cmd
        else:
            dirCmdList = []
            dirCmd = 'if [ ! -d "%s" ]; then mkdir -p %s; else rm -f %s*; fi' % ('/' + containerName + '-' + 'logs/', '/' + containerName + '-' + 'logs/', '/' + containerName + '-' + 'logs/')
            dirCmdList.append(dirCmd)
            sshAndRun(dirCmdList, mapIp)
            cmd = 'docker run -d -p %s:8080 --name %s --add-host zookeeper1:%s --add-host redis1:%s --restart=always --log-driver=none -v %s:%s -e TZ=%s %s/%s:%s ' % (CONFIG.PORT_DIC[containerName],
                                                                                                                                                                       containerName,
                                                                                                                                                                       mapIp,
                                                                                                                                                                       mapIp,
                                                                                                                                                                       '/' + containerName + '-' + 'logs/',
                                                                                                                                                                       '/usr/local/tomcat/logs/',
                                                                                                                                                                       CONFIG.CONTAINER_TZ,
                                                                                                                                                                       CONFIG.DOCKERREPOSITORY,
                                                                                                                                                                       containerName,
                                                                                                                                                                       tagName
                                                                                                                                                                       )
            cmdDic[containerName] = cmd
    return cmdDic


# 为指定机器获得指定镜像
def getImage(ip, imageName, tagName):
    cmdList = []
    cmd = 'docker pull %s:%s' % (imageName, tagName)
    cmdList.append(cmd)
    resTup = sshAndRun(cmdList, ip)
    for i in resTup[0].keys():
        for j in resTup[0][i]:
            logging.info(j)


# 准备zookeeper配置
def prepareConfig(ip, version, configerFileDirStr, env_Dic):
    # 清理之前的文件和文件夹
    str1 = 'if [ ! -d "%s" ]; then :;else rm -rf %s;fi' % (CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config/', CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config/')
    subprocess.Popen(str1, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    str2 = 'if [ ! -f "%s" ]; then :;else rm -f %s;fi' % (CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config-%s.zip' % version, CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config-%s.zip' % version)
    subprocess.Popen(str2, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # 下载配置程序包到本地
    url = CONFIG.NEW_BOSS_BUILD_DBSCRIPT + env_Dic['NEW_BOSS_FTPDIR'] + os.sep + version + '/ConfigAndDbscript' + '/platform-config-%s.zip' % version
    utils.downloadFile(CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + os.sep, url)
    # 解压配置程序
    utils.unzipFile(CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config-%s.zip' % version, CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config')
    # 删除解压出来的文件夹中的原配置文件
    filePath = CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config/platform-config/configScripts/CONFIG.groovy'
    str3 = 'if [ ! -f "%s" ]; then :;else rm -f %s;fi' % (filePath, filePath)
    subprocess.Popen(str3, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # 拷贝文件到执行配置的程序的相应目录
    logging.info("Copy the configfile which has been set.")
    cpFromStr = CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/CONFIG.groovy'
    cpToStr = CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr] + '/platform-config/platform-config/configScripts/'
    str4 = 'cp %s %s' % (cpFromStr, cpToStr)
    subprocess.Popen(str4, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    # 生成灌注zookeeper配置的shell文件,因为platform-config文件必须在此文件所在的目录下执行
    wholeFileName = CONFIG.ROOT_HOME + os.sep + CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr] + '/execConfig.sh'
    f = open(wholeFileName, 'w')
    f.write("#!/bin/bash\n")
    f.write("source /etc/profile\n")
    f.write("chmod 777 %s" % CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER + CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr] + '/platform-config/platform-config/bin/platform-config\n')
    f.write("pushd %s/platform-config/platform-config/bin\n" % (CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER + CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr]))
    f.write("./platform-config\n")
    f.close()
    # 传输配置文件到平台服务器
    scpTomcatServerFile(ip, CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR[configerFileDirStr], CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER)
    # 为生成的执行文件在执行机器上授权
    shellCmd = 'chmod 777 ' + CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER + CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr] + '/execConfig.sh'
    sshAndRun([shellCmd], ip)
    

# 灌入zookeeper配置
def pureZookeeperConfig(ip, configerFileDirStr):
    shellPath = CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER + CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr] + '/execConfig.sh'
    cmdList = []
    # 给予文件权限
    shellChmod = 'chmod 777 %s' % shellPath
    cmdList.append(shellChmod)
    # 执行shell
    shellRun = 'sh %s' % shellPath
    cmdList.append(shellRun)
    resTup = sshAndRun(cmdList, ip)
    resDic = resTup[0]
    for i in resDic[shellRun]:
        logging.info(i)
    if resTup[1][shellRun]:
        for j in resTup[1][shellRun]:
            logging.info(j)
        raise myException.MyException("Pure config for zookeeper error.")

            
# 启动平台容器，灌入zookeeper配置，启动war包容器
def startPlatContainer(env_Dic, tagName, configerFileDirStr):
    # 启动zookeeper容器
    cmdList = getStartZookeeperCmdList(env_Dic['MACHINE_LIST'][0])
    logging.info("=======Start zookeeper containers=======")
    resTup = sshAndRun(cmdList, env_Dic['MACHINE_LIST'][0])
    keyList = resTup[0].keys()
    for key in keyList:
        if resTup[0][key]:
            if 'registry:5000/library/zookeeper' in key:
                logging.info("Start container for %s success" % 'zookeeper')
                logging.info("ContainID is %s" % resTup[0][key][0])
        else:
            raise myException.MyException(resTup[1][key])
    # 灌入zookeeper配置
    pureZookeeperConfig(env_Dic['MACHINE_LIST'][0], configerFileDirStr)
    # 启动redis容器
    redisCmdList = getStartRedisCmdList(env_Dic['MACHINE_LIST'][0], configerFileDirStr)
    logging.info("=======Start redis containers=======")
    redisTup = sshAndRun(redisCmdList, env_Dic['MACHINE_LIST'][0])
    redisKeyList = redisTup[0].keys()
    for key in redisKeyList:
        if redisTup[0][key]:
            if 'redisMaster' in key:
                logging.info("Start container for %s success" % 'redisMaster')
                logging.info("ContainID is %s" % redisTup[0][key][0])
            elif 'redisSlave' in key:
                logging.info("Start container for %s success" % 'redisSlave')
                logging.info("ContainID is %s" % redisTup[0][key][0])
            elif 'redisSentinel' in key:
                logging.info("Start container for %s success" % 'redisSentinel')
                logging.info("ContainID is %s" % redisTup[0][key][0])
        else:
            raise myException.MyException(resTup[1][key])
  
    # 启动dubbo容器
    # time.sleep(120)
    dubboCmdList = getStartDubboContainerCmd(env_Dic['MACHINE_LIST'][0])
    logging.info("=======Start redis containers=======")
    dubboTup = sshAndRun(dubboCmdList, env_Dic['MACHINE_LIST'][0])
    dubboKeyList = dubboTup[0].keys()
    for key in dubboKeyList:
        if dubboTup[0][key]:
            logging.info("Start container for %s success" % 'dubbo')
            logging.info("ContainID is %s" % dubboTup[0][key][0])
        else:
            raise myException.MyException("Exec cmd: %s error, please check it" % key)
    # 启动platform-cache-config容器
    cacheCmdList = getStartCacheContainerCmdList(env_Dic['MACHINE_LIST'][0], tagName)
    logging.info("=======Start platform-cache-config container=======")
    cacheTup = sshAndRun(cacheCmdList, env_Dic['MACHINE_LIST'][0])
    cacheKeyList = cacheTup[0].keys()
    if cacheTup[0][cacheKeyList[0]]:
        logging.info("Start container for %s success" % 'dubbo')
        logging.info("ContainID is %s" % cacheTup[0][cacheKeyList[0]][0])
    else:
        raise myException.MyException(cacheTup[1][cacheKeyList[0]])
    # 启动zookeeper和redis的ui容器
    zkAndRedisUiCmdList = getStartUiContainerCmd(env_Dic['MACHINE_LIST'][0])
    zrUiTup = sshAndRun(zkAndRedisUiCmdList, env_Dic['MACHINE_LIST'][0])
    zrUiKeyList = zrUiTup[0].keys()
    for zrKey in zrUiKeyList:
        # 如果sshAndRun方法返回的resDic不为空
        if zrUiTup[0][zrKey]:
            logging.info("Start container for %s success" % 'dubbo')
            logging.info("ContainID is %s" % zrUiTup[0][zrKey][0])
        # 如果sshAndRun方法返回的resDic为空，则errDic不为空，则将errDic[zrKey]抛出
        else:
            raise myException.MyException(zrUiTup[1][zrUiKeyList[zrKey]])
        
        
# 启动war包容器
def startWarContainers(mapIp, mapWarAndIpDic, tagName, warContainersNameList):
    cmdDic = getStartWarContainerCmd(mapIp, tagName, warContainersNameList)
    containersList = warContainersNameList
    for container in containersList:
        cmdList = []
        cmdList.append(cmdDic[container])
        resTup = sshAndRun(cmdList, mapWarAndIpDic[container])
        resKeyList = resTup[0].keys()
        if resTup[0][resKeyList[0]]:
            logging.info("Start container for %s success on %s" % (container, mapWarAndIpDic[container]))
            logging.info("ContainID is %s" % resTup[0][resKeyList[0]][0])
        else:
            raise myException.MyException(resTup[1][resKeyList[0]])
    
    
    
