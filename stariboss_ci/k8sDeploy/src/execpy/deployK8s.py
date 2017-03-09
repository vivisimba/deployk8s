# -*- coding: utf-8 -*-
'''
Created on 2016年10月13日

@author: Simba
'''


import logging
import os
import config.config as CONFIG
import log.logService as logService
import subprocess
import time
import exception.myException as myException
import deployFunction
import datetime
import sys
import updateTag
import deleteRcAndSvc
import scpRedisAndZkFile
import tool
import tomcatLogDirCheck


# 获得所有以.yaml或者.YAML结尾的文件
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


# 组织命令
# def makeCmdList(prefixList, fileDir, suffix):
#     cmdList = []
#     for prefixName in prefixList:
#         cmdStr = 'kubectl create -f ' + fileDir + prefixName + suffix
#         cmdList.append(cmdStr)
#     return cmdList


# 组织命令
def makeCmdList(prefix, rcFileDir, svcFileDir):
    cmdList = []
    rcCmd = 'kubectl create -f ' + rcFileDir + prefix + '_dpm.yaml'
    cmdList.append(rcCmd)
    svcCmd = 'kubectl create -f ' + svcFileDir + prefix + '_svc.yaml'
    cmdList.append(svcCmd)
    return cmdList


# 启动RC和SVC
def startRcAndSvc(prefix):
    zkCmdList = makeCmdList(prefix, CONFIG.TEMP_RCDIR, CONFIG.TEMP_SVCDIR)
    for cmdStr in zkCmdList:
            p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            str1 = p.stdout.read()
            str2 = p.stderr.read()
            if len(str1) > 0:
                logging.info("%s" % str1)
            else:
                logging.error("%s" % str2)


# 组织deployment和svc启动命令
def makeDpmCmdList(prefix, dpmFileDir, svcFileDir):
    cmdList = []
    rcCmd = 'kubectl create -f ' + dpmFileDir + prefix + '_dpm.yaml'
    cmdList.append(rcCmd)
    svcCmd = 'kubectl create -f ' + svcFileDir + prefix + '_svc.yaml'
    cmdList.append(svcCmd)
    return cmdList


# 启动deployment和svc
def startDpmAndSvc(prefix):
    zkCmdList = makeCmdList(prefix, CONFIG.TEMP_DPMDIR, CONFIG.TEMP_SVCDIR)
    for cmdStr in zkCmdList:
            p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            str1 = p.stdout.read()
            str2 = p.stderr.read()
            if len(str1) > 0:
                logging.info("%s" % str1)
            else:
                logging.error("%s" % str2)
 

# # 启动推送配置的zkpushpod
# def startZkPushPod():
#     zkPushCmdList = makeCmdList('pushzkconfig', CONFIG.RCDIR, CONFIG.SVCDIR)
#     for cmdStr in zkPushCmdList:
#             p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#             str1 = p.stdout.read()
#             str2 = p.stderr.read()
#             if len(str1) > 0:
#                 logging.info("%s" % str1)
#             else:
#                 logging.error("%s" % str2)


# 获得pod名称
def getZkPushPodName(prefixStr, namespace):
    cmdStr = 'kubectl get pods -o name --namespace=%s' % namespace
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    podList = p.stdout.readlines()
    podStr = ''
    for i in podList:
        if prefixStr in i:
            podStr = i
    if podStr != '':
        prefixList = podStr.split('pod/')
        prefixtmp = prefixList[1]
        prefix = prefixtmp.strip()
        return prefix
    else:
        raise myException.MyException("There is no pod named %s" % prefixStr)


# 同上面的方法，获得pod名称，但返回值不同
def getPodName(prefixStr, namespace):
    cmdStr = 'kubectl get pods -o name --namespace=%s' % namespace
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    podList = p.stdout.readlines()
    podStr = ''
    for i in podList:
        if prefixStr in i:
            podStr = i
    if podStr != '':
        prefixList = podStr.split('pod/')
        prefixtmp = prefixList[1]
        prefix = prefixtmp.strip()
        return prefix
    else:
        return 'N'


# 获得集群命名空间
def getNamespace(spaceName):
    cmdStr = 'kubectl get namespace -o name'
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    resList = p.stdout.readlines()
    flagStr = ''
    for i in resList:
        if spaceName in i:
            logging.info("There is namespace named %s" % spaceName)
            flagStr = 'Y'
    if flagStr == 'Y':
        return 'Y'
    else:
        return 'N'


# 查询指定命名空间下的,指定名称的secret是否存在
def isExistSecret(secretName, namespace):
    cmdStr = 'kubectl get secret -o name --namespace=%s' % namespace
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    resList = p.stdout.readlines()
    flagStr = ''
    for i in resList:
        if secretName in i:
            logging.info("There is secret named %s in %s" % (secretName, namespace))
            flagStr = 'Y'
    if flagStr == 'Y':
        return 'Y'
    else:
        return 'N'


# 创建命名空间
def createNamespace():
    cmdStr = 'kubectl create -f %snamespace.yaml' % CONFIG.TEMP_DPMDIR
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    str1 = p.stdout.read()
    str2 = p.stderr.read()
    if len(str1) > 0:
        logging.info("%s" % str1)
    else:
        logging.error("%s" % str2)
        raise myException.MyException("%s" % str2)


# 创建指定命名空间下的secret
def createSecret():
    cmdStr = 'kubectl create -f %smysecret.yaml' % CONFIG.TEMP_DPMDIR
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    str1 = p.stdout.read()
    str2 = p.stderr.read()
    if len(str1) > 0:
        logging.info("%s" % str1)
    else:
        logging.error("%s" % str2)
        raise myException.MyException("%s" % str2)


# 在pod中执行命令
def runCmdInPod(podName, cmd):
    cmdStr = 'kubectl exec %s --namespace=%s -- %s' % (podName, CONFIG.NAME_SPACE, cmd)
    logging.info("Exec: %s" % cmdStr)
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    str1 = p.stdout.read()
    str2 = p.stderr.read()
    if len(str2) > 0:
        logging.error("%s" % str2)
    else:
        logging.info("Successful")
        logging.info("%s" % str1)


# 获得POD的运行状态
def getPodStatus(podName, spaceName):
    cmdStr = 'kubectl get pods -o wide --namespace=%s' % spaceName
    p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
    resList = p.stdout.readlines()
    if len(resList) > 1:
        for line in resList:
            if podName in line:
                podStatusTmpList = line.split(' ')
                podStatusList = []
                for i in podStatusTmpList:
                    if i == ' ':
                        pass
                    elif i == '':
                        pass
                    else:
                        podStatusList.append(i)
                print podStatusList
                return podStatusList[2]
    else:
        logging.info("There is no pod named %s on any node!" % podName)
        return 'N'


# 判断是否所有pod均为运行状态
# def allPodIfRunning():
#     cmdStr = 'kubectl get pods -o wide --namespace=kube-system'
#     p = subprocess.Popen(cmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
#     resList = p.stdout.readlines()
#     if len(resList) > 1:
#         for line in resList:
#             if podName in line:
#                 podStatusTmpList = line.split(' ')
#         podStatusList = []
#         for i in podStatusTmpList:
#             if i == ' ':
#                 pass
#             elif i == '':
#                 pass
#             else:
#                 podStatusList.append(i)
#         print podStatusList
#         return podStatusList[2]
#     else:
#         logging.info("There is no pod on any node!")
#         return 'N'


# 检查temp_Dir目录是否存在，如果存在则删除该目录后再创建该目录，如果不存在则直接创建
def checkTemp_Dir(temp_Dir):
    if os.path.exists(temp_Dir):
        rmDirStr = "rm -rf %s" % temp_Dir
        p = subprocess.Popen(rmDirStr, shell=True)
        p.wait()
        os.makedirs(temp_Dir)
    else:
        os.makedirs(temp_Dir)
    return "ok"


# 拷贝rc文件到CONFIG.TEMP_RCDIR目录
def cpRcToTemp(fromDir, toDir):
    cpStr = "cp %s* %s" % (fromDir, toDir)
    logging.info("Exec: %s" % cpStr)
    p = subprocess.Popen(cpStr, shell=True)
    p.wait()
    return "ok"


# 更新temp_dpm目录下的skydns文件
def updateSkydnsDpm():
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, "{masterip}", CONFIG.MASTERIP[0])
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, "{domain}", CONFIG.NAME_SPACE)


# 检查宿主机NFS目录下各模块目录是否存在，如果不存在则创建
def checkModuleDir(hostNfsDir, moduleList, excludeList):
    for moduleName in moduleList:
        if moduleName not in excludeList:
            moduleWholeDir = hostNfsDir + os.sep + 'moduledir' + os.sep + moduleName
            if os.path.exists(moduleWholeDir):
                pass
            else:
                os.makedirs(moduleWholeDir)


# 在不同节点分别启动redis的master、slave、sentinel：node1:sentinel;node2:master;node3:slave
def startRedis():
    masterStr = 'docker-compose -f %s/redismaster-compose.yml up -d' % (CONFIG.NFS_HOST_DIR + os.sep + 'compose-yml')
    masterStrList = []
    masterStrList.append(masterStr)
    masterResTup = tool.sshAndRun(masterStrList, CONFIG.NODEMACHINE[1], port=22, username='root', password='123456')
    logging.info(masterResTup[0][masterStr])
    logging.info(masterResTup[1][masterStr])
    
    slaveStr = 'docker-compose -f %s/redisslave-compose.yml up -d' % (CONFIG.NFS_HOST_DIR + os.sep + 'compose-yml')
    slaveStrList = []
    slaveStrList.append(slaveStr)
    slaveResTup = tool.sshAndRun(slaveStrList, CONFIG.NODEMACHINE[2], port=22, username='root', password='123456')
    logging.info(slaveResTup[0][slaveStr])
    logging.info(slaveResTup[1][slaveStr])
    
    sentinelStr = 'docker-compose -f %s/redissentinel-compose.yml up -d' % (CONFIG.NFS_HOST_DIR + os.sep + 'compose-yml')
    sentinelStrList = []
    sentinelStrList.append(sentinelStr)
    sentinelResTup = tool.sshAndRun(sentinelStrList, CONFIG.NODEMACHINE[0], port=22, username='root', password='123456')
    logging.info(sentinelResTup[0][sentinelStr])
    logging.info(sentinelResTup[1][sentinelStr])


# 停止各节点上的redis容器
def stopRedis():
    masterStr = 'docker-compose -f %s/redismaster-compose.yml down' % (CONFIG.NFS_HOST_DIR + os.sep + 'compose-yml')
    masterStrList = []
    masterStrList.append(masterStr)
    masterResTup = tool.sshAndRun(masterStrList, CONFIG.NODEMACHINE[1], port=22, username='root', password='123456')
    logging.info(masterResTup[0][masterStr])
    logging.info(masterResTup[1][masterStr])
    
    slaveStr = 'docker-compose -f %s/redisslave-compose.yml down' % (CONFIG.NFS_HOST_DIR + os.sep + 'compose-yml')
    slaveStrList = []
    slaveStrList.append(slaveStr)
    slaveResTup = tool.sshAndRun(slaveStrList, CONFIG.NODEMACHINE[2], port=22, username='root', password='123456')
    logging.info(slaveResTup[0][slaveStr])
    logging.info(slaveResTup[1][slaveStr])
    
    sentinelStr = 'docker-compose -f %s/redissentinel-compose.yml down' % (CONFIG.NFS_HOST_DIR + os.sep + 'compose-yml')
    sentinelStrList = []
    sentinelStrList.append(sentinelStr)
    sentinelResTup = tool.sshAndRun(sentinelStrList, CONFIG.NODEMACHINE[0], port=22, username='root', password='123456')
    logging.info(sentinelResTup[0][sentinelStr])
    logging.info(sentinelResTup[1][sentinelStr])


def run(newTag, dubboHostIp, version, flywayFlag):
    tomcatLogDirCheck.tomcatLogDirCheck()
    # checkModuleDir(CONFIG.NFS_HOST_DIR, CONFIG.RC_SVC_PREFIX, CONFIG.EXCLUDE_RC_LIST)
    # 检查temp_rc_yaml目录是否存在，如果存在则删除该目录后再创建该目录，如果不存在则直接创建
    checkTemp_Dir(CONFIG.TEMP_DPMDIR)
    # 拷贝原始deployment文件到CONFIG.TEMP_DPMDIR目录
    cpRcToTemp(CONFIG.DPMDIR, CONFIG.TEMP_DPMDIR)
    # 更新CONFIG.TEMP_DPMDIR目录下的deployment文件的镜像标签
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, CONFIG.TAG_OCCUPY, newTag)
    # 更新CONFIG.TEMP_DPMDIR目录下的deployment文件的dubbo_host地址（本分支不存在该地址）
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, CONFIG.DUBBO_HOST, dubboHostIp)
    # 更新CONFIG.TEMP_DPMDIR目录下的deployment文件的{NFS_HOST_DIR}
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, "{NFS_HOST_DIR}", CONFIG.NFS_HOST_DIR)
    # 更新CONFIG.TEMP_DPMDIR目录下的deployment文件的{NFS_CONTAINER_DIR}
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, "{NFS_CONTAINER_DIR}", CONFIG.NFS_CONTAINER_DIR)
    # 更新CONFIG.TEMP_DPMDIR目录下的deployment文件的命名空间
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, "{NAME_SPACE}", CONFIG.NAME_SPACE)
    # 更新CONFIG.TEMP_DPMDIR目录下的deployment文件的版本号
    updateTag.updateYamlTag(CONFIG.TEMP_DPMDIR, "{VERSION}", newTag)
    # 更新redis的配置文件：slave和sentinel的
    scpRedisAndZkFile.modifyRedisConfigFile()
    
    # 检查temp_svc_yaml目录是否存在,如果存在则删除该目录后再创建该目录，如果不存在则直接创建
    checkTemp_Dir(CONFIG.TEMP_SVCDIR)
    # 拷贝原始SVC文件到CONFIG.TEMP_SVCDIR
    cpRcToTemp(CONFIG.SVCDIR, CONFIG.TEMP_SVCDIR)
    # 更新CONFIG.TEMP_SVCDIR目录下的svc文件的命名空间
    updateTag.updateYamlTag(CONFIG.TEMP_SVCDIR, "{NAME_SPACE}", CONFIG.NAME_SPACE)
    # 更新skydns的dpm文件
    updateSkydnsDpm()

    
#     # 判断dns的pod是否存在
#     dnsStr = getPodStatus(getZkPushPodName('kube-dns', 'kube-system'), 'kube-system')
#     if dnsStr != 'Running':
#         logging.error("There is no dns pod running!")
#     elif getPodName('kube-dns', 'kube-system') == 'N':
#         logging.info("There is no dns pod,now start to create dns deployment.")
#         startDpmAndSvc('skydns')
    # 判断BOSS服务的命名空间是否存在
    appNamespaceFlag = getNamespace(CONFIG.NAME_SPACE)
    if appNamespaceFlag == 'N':
        createNamespace()
    # 判断与应用同命名空间的secret是否存在
    appSecret = isExistSecret('mysecret', CONFIG.NAME_SPACE)
    if appSecret == 'N':
        createSecret()
    # 删除原deployment以及SVC
    # deleteRcAndSvc.deleteRcAndSvc()
    stopRedis()
    deleteRcAndSvc.deleteDpmandSvc()
    time.sleep(120)

    # 准备推送zk配置的文件
    scpRedisAndZkFile.prepareZkConfig(version, flywayFlag)
    
#     # 检查dns的pod是否为running状态
#     dnsPodName = getZkPushPodName('kube-dns', CONFIG.NAME_SPACE)
#     while True:
#         dnsPodStatus = getPodStatus(dnsPodName, CONFIG.NAME_SPACE)
#         if 'Running' == dnsPodStatus:
#             logging.info('dns is running, start pod of zookeeper now.')
#             break
#         else:
#             logging.info('Status of dns is %s, please wait 5 seconds.' % dnsPodStatus)
#             time.sleep(5)
            
    # 启动zk的RC和SVC
    startDpmAndSvc('zookeeper')
    # 待zookeeper容器运行后，启动zkpush的RC和SVC
    zkPodName = getZkPushPodName('zookeeper', CONFIG.NAME_SPACE)
    while True:
        zkPodStatus = getPodStatus(zkPodName, CONFIG.NAME_SPACE)
        if 'Running' == zkPodStatus:
            logging.info('zookeeper is running, start pod of pushzkconfig now.')
            startDpmAndSvc('pushzkconfig')
            break
        else:
            logging.info('Status of zookeeper is %s, please wait 5 seconds.' % zkPodStatus)
            time.sleep(5)
    # 获得zkpush的pod名称
    zkpushPodName = getZkPushPodName('pushzkconfig', CONFIG.NAME_SPACE)
    # 判断zkpush的pod的状态，状态为Running再继续往下进行
    statusFlag = 0
    while True:
        statusFlag += 1
        zkpushPodStatus = getPodStatus(zkpushPodName, CONFIG.NAME_SPACE)
        if zkpushPodStatus == 'Running':
            logging.info("pushzkconfigpod has been running.")
            break
        elif statusFlag == 20:
            raise myException.MyException("Please check the status of pushzkconfigPod.")
        else:
            logging.info("The status of pushzkconfigPod is %s now,please wait a moment." % zkpushPodStatus)
            time.sleep(7)
    # 授权
    runCmdInPod(zkpushPodName, "chmod 777 platform-config")
    os.system("pause")
    # 在pod中推送zk配置
    runCmdInPod(zkpushPodName, "sh platform-config BASIC.groovy CONFIG.groovy zookeeper1:2181")
    # 删除zkpush的deployment和SVC
    svcDelCmdStr = 'kubectl delete svc pushzkconfig --namespace=%s' % CONFIG.NAME_SPACE
    svcDelp = subprocess.Popen(svcDelCmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    svcDelstr1 = svcDelp.stdout.read()
    svcDelstr2 = svcDelp.stderr.read()
    if len(svcDelstr2) > 0:
        logging.error("%s" % svcDelstr2)
    else:
        logging.info("Successful")
        logging.info("%s" % svcDelstr1)
    rcDelCmdStr = 'kubectl delete deployment pushzkconfig --namespace=%s' % CONFIG.NAME_SPACE
    rcDelp = subprocess.Popen(rcDelCmdStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    rcDelstr1 = rcDelp.stdout.read()
    rcDelstr2 = rcDelp.stderr.read()
    if len(rcDelstr2) > 0:
        logging.error("%s" % rcDelstr2)
    else:
        logging.info("Successful")
        logging.info("%s" % rcDelstr1)
    # 启动redismaster的RC和SVC
#     startDpmAndSvc('redismaster')
#     # 启动redisslave的RC和SVC
#     startDpmAndSvc('redisslave')
#     # 启动redis哨兵的RC和SVC
#     startDpmAndSvc('redissentinel')
    # 依次启动redis的master、slave、sentinel
    startRedis()
    
    time.sleep(2)
    # 启动platform-cache-config的RC和SVC
    startDpmAndSvc('platform-cache-config')
    time.sleep(10)
    # 从前缀列表中弹出已处理的前缀
    prefixList = CONFIG.RC_SVC_PREFIX
    prefixList.remove('zookeeper')
    prefixList.remove('pushzkconfig')
#     prefixList.remove('redismaster')
#     prefixList.remove('redisslave')
#     prefixList.remove('redissentinel')
    prefixList.remove('platform-cache-config')
    # 启动剩余的RC和SVC
    flagNum = 0
    for prefix in prefixList:
        flagNum += 1
        logging.info("===================================================")
        logging.info("%s :Create deployment and SVC for %s" % (flagNum, prefix))
        startDpmAndSvc(prefix)


# 数据库升级
def start(versionNumber):
    env_Dic = CONFIG.DB_ENV_DIC
    db_update_date = datetime.datetime.today().date().strftime('%Y%m%d')
    # 数据库快照处理
    # logging.info("Start to treat snapshot of DB.")
    # deployFunction.gotoTestSystemEnvSnapshot(env_Dic)
    # 同步时间
    # logging.info("Start to sysnc time of all machines of cluster.")
    # deployFunction.sysncTime()
    # 获得配置文件和数据库脚本
    logging.info("Start to get DBScript files.")
    deployFunction.getBuildConfigAndDBScript(env_Dic, versionNumber)
    # 解压数据库文件
    logging.info("Start to unzip DBfiles.")
    deployFunction.unzipDailyDBScriptFile(env_Dic)
    # 升级数据库
    logging.info("Start update the DB.")
    deployFunction.dailyUpdateDB(env_Dic, db_update_date)


# 调用数据库升级和环境部署
def updateDbAndDeploy():
    '''
    :param 脚本本身
    :param processFlag:   1.数据库升级 2.部署环境 3.数据库升级并且部署环境
    :param version    :   e.g:7.1.1.152
    :param newTag     :   本次部署对应的tag号
    :param dubbo_host :   外网直接访问服务的IP（集群中任意一个节点IP即可
    :param flywayFlag :   是否启用flyway：0:不启用;1:启用
    '''
    parameterList = sys.argv
    processFlag = parameterList[1]
    if processFlag == '1':
        start(parameterList[2])
    elif processFlag == '2':
        run(parameterList[3], parameterList[4], parameterList[2], parameterList[5])
    else:
        start(parameterList[2])
        run(parameterList[3], parameterList[4], parameterList[2], parameterList[5])
        

if __name__ == '__main__':
    logService.initLogging()
    '''
    :param 脚本本身
    :param processFlag:   1.数据库升级 2.部署环境 3.数据库升级并且部署环境
    :param version:       e.g:7.1.1.152
    :param newTag:        本次部署对应的tag号
    :param dubbo_host :   外网直接访问服务的IP（集群中任意一个节点IP即可）
    :param flywayFlag :   是否启用flyway：0:不启用;1:启用
    '''
    updateDbAndDeploy()
    logService.destoryLogging()
