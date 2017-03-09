# -*- coding: utf-8 -*-
'''
Created on 2016年5月11日

@author: Simba
'''
import log.logService as logService
import vmManager
import sys
import datetime
import os
import config.config as CONFIG
import logging
import time
import fnmatch
import fileDispose
import utils.util as utils
import exception.myException as myException
import linecache
import manageContainerMachine
import vmSnapshotOperation
import checkDbUpdate


# 修改文件
def modifyConfigFile(filePath, originalList, modifiedList):
    old = open(filePath)
    texts = old.readlines()
    new_texts = []
    
    for line in texts:
        for (original, modified) in zip(originalList, modifiedList):
            if original.lower() in line.lower():
                line = modified
                logging.info('modify : "' + original + '" to "' + modified + '" ok!')
                break
        new_texts.append(line)
    new = open(filePath, 'w')
    new.writelines(new_texts)
    new.close()
    old.close()


def dailyUpdateDB(env_dic, db_update_date):
    dbScriptNames, dbScriptFileDirs = dailyGetDBScriptNamesAndDBScriptFileDirs()
    for (dbScritpName, dbFileDir) in zip(dbScriptNames, dbScriptFileDirs):
        logging.info('start to update data base: ' + dbScritpName)
        dataFile = env_dic['NEW_BOSS_DB_DATA_FILE_DIR']
        dbsid = env_dic['NEW_BOSS_DB_LOCALNAME']
        systemPassword = env_dic['NEW_BOSS_DB_SYSTEM_PWD']
        # =========================================================================
        for key in CONFIG.DB_DIC.keys():
            if dbScritpName == key:
                dbUserName, dbUserPwd, dbfName, tablespaceName = CONFIG.DB_DIC[key]
        # =========================================================================
        
        dbFileDir = dbFileDir + '/daily-update/'
        os.chdir(dbFileDir)
        dirs = os.listdir(dbFileDir)
        
        # 查看数据库中是否已经存在该用户
        flagDBUser = isDBUser(env_dic, dbUserName)
        dbEndDate = db_update_date
        dbDates = []  # 列表中的元素的类型是 datetime.date
        if flagDBUser == '0':
            logging.info('database no user: ' + dbUserName + ', so we create this db user.')
            endDate = (datetime.datetime.strptime(dbEndDate, '%Y%m%d')).date()
            dbDates.append(endDate)
            i = 366
            while i > 0:
                yesterday = endDate - utils.getTimeDelta()
                if (yesterday.strftime('%Y%m%d') + '.sql') in dirs:
                    dbDates.append(yesterday)
                i = i - 1
                endDate = yesterday
        elif flagDBUser == '1':
            logging.info('database already exist user: ' + dbUserName + ', so we update this db user.')
            dbStartVersion = getDBCurrentVersion(env_dic, dbUserName, dbUserPwd)
            logging.info('database ' + dbUserName + ' current version is: ' + dbStartVersion)
            endDate = (datetime.datetime.strptime(dbEndDate, '%Y%m%d')).date()
            startDate = (datetime.datetime.strptime(dbStartVersion, '%Y%m%d')).date()
            if endDate == startDate:
                dbDates.append(endDate)
            elif endDate > startDate:
                dbDates.append(endDate)
                i = 366
                while i > 0:
                    yesterday = endDate - utils.getTimeDelta()
                    if yesterday == startDate:
                        dbDates.append(yesterday)
                        break
                    if (yesterday.strftime('%Y%m%d') + '.sql') in dirs:
                        dbDates.append(yesterday)
                    i = i - 1
                    endDate = yesterday
        # s需要对日期列表进行翻转，因为现在列表中的元素是按照日期进行倒序排的
        dailySysSQLs = []
        dailyNormalSQLs = []
        dbDates.reverse()
        for dbDate in dbDates:
            for dira in dirs:
                if fnmatch.fnmatch(dira, (dbDate.strftime('%Y%m%d') + '*.sql')):
                    if '_sys' in dira:
                        if flagDBUser == '0':  # 加上 flagDBUser == 0 因为：一天部署多次，不能重复执行创建用户的sys脚本
                            dailySysSQLs.append(dira)
                    else:
                        dailyNormalSQLs.append(dira)
        print('---------------------------end-------------------------')
        
        # 转换文件格式，赋执行权限
        logging.info('start to dos2unix all .sql file.')
        os.system('chmod +x %s*.sql' % dbFileDir)
        os.system('dos2unix %s*.sql' % dbFileDir)
        logging.info('success to dos2unix all .sql file.')
        
        for dailySysSQL in dailySysSQLs:
            logging.info('start to set the input parameter of ' + dbFileDir + dailySysSQL + ' eg:datafile path; dbUserName; dbPassWord......')
            originalList = []
            modifiedList = []
            filePath = dbFileDir + dailySysSQL
            # 将脚本文件编码转换成GBK
            utils.convertFileEncodingToGBK(filePath)
            os.system('dos2unix %s' % filePath)
            # 修改数据文件路径
            originalList.append("datafile '&sms_data/")
            modifiedList.append("datafile '" + dataFile + "/" + dbfName + "' size 5m reuse\n")
            # 修改数据库用户名密码
            originalList.append("create user")
            modifiedList.append("create user " + dbUserName + " identified by " + dbUserPwd + " default tablespace " + tablespaceName + "\n")
            # 修改数据库用户名
            originalList.append("grant create session")
            modifiedList.append("grant create session,resource,create table,create sequence,create view,create synonym,dba to " + dbUserName + ";\n")
            modifyConfigFile(filePath, originalList, modifiedList)
            # 给.sql文件的末尾加上 exit;
            fp = open(filePath, 'a+')
            fp.write("\nexit;\n")
            fp.close()
            logging.info('success to set the input parameter of ' + filePath + ' eg:datafile path; dbUserName; dbPassWord......')
            logging.info('start to use sqlplus run ' + filePath)
            updateDBLogFileName = dbScritpName + '-' + dailySysSQL.split('.')[0] + '.log'
            os.system('sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % ('system',
                                                                systemPassword,
                                                                dbsid,
                                                                dbFileDir,
                                                                dailySysSQL,
                                                                CONFIG.LOG_HOME,
                                                                updateDBLogFileName)
                      )
            try:
                fp = open(CONFIG.LOG_HOME + updateDBLogFileName)
                res_op = fp.read()
                logging.info(res_op)
                if 'ORA-' in res_op:
                    if env_dic['DICNAME'] == 'MANAUL' or env_dic['DICNAME'] == 'DEV':
                        checkDbUpdate.gotoDBLastSnapshot(env_dic)
                    raise myException.MyException('faild to use sqlplus run ' + filePath + ' file !')
                else:
                    logging.info('sucessful use sqlplus run ' + filePath)
            except IOError, e:
                raise myException.MyException(e)
            finally:
                fp.close()
        for dailyNormalSQL in dailyNormalSQLs:
            filePath = dbFileDir + dailyNormalSQL
            # 将脚本文件编码转换成GBK
            utils.convertFileEncodingToGBK(filePath)
            os.system('dos2unix %s' % filePath)
            logging.info('start to use sqlplus run ' + filePath)
            # =======================================================================================
            # ================================================================================
            # 获取脚本中的标识位
            old = open(filePath, 'r')
            texts = old.readlines()
            execFlag = ''  # 执行的标记
            for line in texts:
                if line.strip().upper().startswith('--TAG'):
                    execFlag = line.strip()  # 获取脚本中的最后一个执行标记
            if '' == execFlag:  # 若未查到标志位，则：这个脚本不符合规范，直接抛异常，恢复快照，发部署失败邮件，让研发去改脚本
                logging.info('==================== ' + filePath + ' :这个脚本文件不符合规范, 缺少执行标志位 --TAGHHMM，请研发修改。修改完成后再次构建即可。')
                old.close()
                checkDbUpdate.gotoDBLastSnapshot(env_dic)
                raise myException.MyException('==================== ' + filePath + ' :这个脚本文件不符合规范, 缺少执行标志位 --TAGHHMM，请研发修改。修改完成后再次构建即可。')
            else:
                old.close()
                # 给.sql文件的末尾加上 插入每日构建版本号、commit、exit;
                fp = open(filePath, 'a+')
                fp.write("\nINSERT INTO DAILY_BUILD_VERSION(SEQ_NO, VERSION_NO, VERSION_DESCRIPTIONS, CREATEDATE, CREATEBY) VALUES(seq_daily_build_version.nextval, '" + dailyNormalSQL.split('.')[0] + "', '" + execFlag + "', sysdate, 'autoDeploy');\n")
                fp.write("commit;\n")
                fp.write("exit;\n")
                fp.close()
            
            # 数据库最后一次升级的日期对应的脚本要进行增量执行（即：判断上次执行到了那一行，只需执行该行之后的脚本）
            if getDBCurrentVersion(env_dic, dbUserName, dbUserPwd) in dailyNormalSQL:
                # 从数据库中获取上次执行标志位
                lastSqlFlag = getLastSqlFlag(env_dic, dbUserName, dbUserPwd)
                logging.info("Last sqltag is : %s" % lastSqlFlag)
                old = open(filePath, 'r')
                texts = old.readlines()
                new_texts = []
                
                flag = False  # 是否找到上次执行的标记
                startSqlFlag = ''  # 本次开始行的标记位，即：本次从这行开始执行
                for line in texts:
                    if lastSqlFlag == line.strip():
                        flag = True
                    if (flag is True) and (line.strip().upper().startswith('--TAG')) and (lastSqlFlag != line.strip()):
                        startSqlFlag = line.strip()
                        break  # 找到上次执行标记之后的下一个标记，则：代表本次从这个标记处执行
                if flag is False:  # 若未查到标志位，则：表示这个脚本上次执行的标志在研发提交代码的过程中被覆盖了，直接恢复快照，发部署失败邮件，让研发去改
                    logging.info('==================== ' + filePath + ':这个脚本的上次执行标志  ' + lastSqlFlag + ' 在研发提交代码的过程中丢失了，请研发修改。修改完成后再次构建即可。')
                    old.close()
                    checkDbUpdate.gotoDBLastSnapshot(env_dic)
                    raise myException.MyException('==================== ' + filePath + ':这个脚本的上次执行标志  ' + lastSqlFlag + ' 在研发提交代码的过程中丢失了，请研发修改。修改完成后再次构建即可。')
                if '' == startSqlFlag:  # 表示上次数据库升级之后没有再对该脚本进行追加内容，因此无需执行该脚本
                    old.close()
                    continue
                # 编辑脚本文件，将文件内容从开头至本次执行标记处之间的内容删除，即：将不需要执行的内容太去掉，只留下本次需要执行的内容
                flag = False
                for line in texts:
                    if line.strip() == startSqlFlag:
                        flag = True
                    if flag is True:
                        new_texts.append(line)
                new = open(filePath, 'w')
                new.writelines(new_texts)
                new.close()
                old.close()
            # nanqb==========================================================================
            # ======================================================================================
            updateDBLogFileName = dbScritpName + '-' + dailyNormalSQL.split('.')[0] + '.log'
            os.system('sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % (dbUserName,
                                                                dbUserPwd,
                                                                dbsid,
                                                                dbFileDir,
                                                                dailyNormalSQL,
                                                                CONFIG.LOG_HOME,
                                                                updateDBLogFileName)
                      )
            try:
                fp = open(CONFIG.LOG_HOME + updateDBLogFileName)
                res_op = fp.read()
                logging.info(res_op)
                if 'ORA-' in res_op:
                    if env_dic['DICNAME'] == 'MANAUL' or env_dic['DICNAME'] == 'DEV':
                        checkDbUpdate.gotoDBLastSnapshot(env_dic)
                    raise myException.MyException('faild to use sqlplus run ' + filePath + ' file !')
                else:
                    logging.info('sucessful use sqlplus run ' + filePath + ' file !')
            except IOError, e:
                raise myException.MyException(e)
            finally:
                fp.close()
        logging.info('success update data base: ' + dbScritpName.split('-')[0])
    # 数据库升级成功，对自动化的数据库拍一个快照，便于手工执行用例，排查问题
    if 'AUTO' == env_dic['DICNAME']:
        res_db = vmSnapshotOperation.createSnapshot(env_dic['NEW_BOSS_DB_VMNAME'],
                                                    'snapshot_' + str(time.strftime('%Y%m%d%H%M', time.localtime())),
                                                    env_dic['NEW_BOSS_VMWARE_IP'],
                                                    env_dic['NEW_BOSS_VMWARE_USERNAME'],
                                                    env_dic['NEW_BOSS_VMWARE_PASSWORD']
                                                    )
        if res_db == 'ok':
            logging.info('sucessful create db snapshot.')
        else:
            err = 'ERROR! Please contact admin to check the virtual machine environment! '
            raise myException.MyException(err)


# 获得每日需执行的配置文件以及数据库脚本
def dailyGetDBScriptNamesAndDBScriptFileDirs():
    os.chdir(CONFIG.tempFolder)
    dirs = os.listdir(CONFIG.tempFolder)
    dbScriptNames = []
    for dirr in dirs:
        if fnmatch.fnmatch(dirr, '*-dbscript'):
            if '.zip' in dirr:
                continue
            dbScriptNames.append(dirr)
    
    dbScriptFileDirs = []
    for dbScriptName in dbScriptNames:
        dbScriptFileDirs.append(os.path.abspath(dbScriptName))
        
    logging.info('dbScriptNames = ')
    logging.info(dbScriptNames)
    logging.info('dbScriptFileDirs = ')
    logging.info(dbScriptFileDirs)
    
    return dbScriptNames, dbScriptFileDirs


def isDBUser(env_Dic, dbUserName):
    logging.info('xxxxxxxxxxxxxxxxxxxxxxx=' + dbUserName)
    originalList = ['SELECT COUNT(*)']
    modifiedList = ["SELECT COUNT(*) FROM Dba_Users du WHERE du.username = '" + dbUserName.upper() + "';\n"]
    modifyConfigFile(CONFIG.NEW_BOSS_DB_SCRIPT_PATCH + 'queryDBUser.sql', originalList, modifiedList)
    
    dbLocalName = env_Dic['NEW_BOSS_DB_LOCALNAME']
    systemPassword = env_Dic['NEW_BOSS_DB_SYSTEM_PWD']
    logName = 'queryDBUser.log'
    os.system('export LANG=zh_CN.GBK;sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % ('system',
                                                                              systemPassword,
                                                                              dbLocalName,
                                                                              CONFIG.NEW_BOSS_DB_SCRIPT_PATCH,
                                                                              'queryDBUser.sql',
                                                                              CONFIG.LOG_HOME,
                                                                              logName))
    linecache.checkcache(CONFIG.LOG_HOME + logName)
    flagDBUser = linecache.getline(CONFIG.LOG_HOME + logName, 14)
    flagDBUser = flagDBUser.strip()
    
    return flagDBUser


# 获得数据库当前版本
def getDBCurrentVersion(env_Dic, dbUserName, dbUserPwd):
    dbLocalName = env_Dic['NEW_BOSS_DB_LOCALNAME']
    logName = 'queryDBCurrentVersion.log'
    os.system('export LANG=zh_CN.GBK;sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % (dbUserName,
                                                                              dbUserPwd,
                                                                              dbLocalName,
                                                                              CONFIG.NEW_BOSS_DB_SCRIPT_PATCH,
                                                                              'queryDBCurrentVersion.sql',
                                                                              CONFIG.LOG_HOME,
                                                                              logName))
    linecache.checkcache(CONFIG.LOG_HOME + logName)
    dbVersion = linecache.getline(CONFIG.LOG_HOME + logName, 14)
    dbVersion = dbVersion.strip()
    
    return dbVersion


# 查询脚本文件执行到哪一行
def getLastSqlFlag(env_dic, dbUserName, dbUserPwd):
    dbsid = env_dic['NEW_BOSS_DB_LOCALNAME']
    logName = 'queryDBLastSqlFlag.log'
    os.system('sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % (dbUserName,
                                                        dbUserPwd,
                                                        dbsid,
                                                        CONFIG.NEW_BOSS_DB_SCRIPT_PATCH,
                                                        'queryDBLastSqlFlag.sql',
                                                        CONFIG.LOG_HOME,
                                                        logName))
    linecache.checkcache(CONFIG.LOG_HOME + logName)
    lastSqlFlag = linecache.getline(CONFIG.LOG_HOME + logName, 14)  # 查询结果在日志文件中的第14行
    
    return lastSqlFlag.strip()

# 上传PlatformCacheConfig配置
# def newUploadPlatformCacheConfig(flag_env):
#     # tempFolder = "/home/nanqb/py/temp/7.1.1.44-1/"
#     foregroundServerIP = getDbUserAndPasswd.getPlatformCacheEnvIP(flag_env)
#     logging.info('start to upload platform-cache-config.zip to remote server: %s ' % (foregroundServerIP))
#     utils.uploadViaSCP(["/home/nanqb/autotest_patch/db/startupPlatformCacheConfig.py"], ["/usr/local/"], foregroundServerIP)
#     filePath = CONFIG.tempFolder + "platform-cache-config.zip"
#     utils.uploadViaSCP([filePath], ["/usr/local/"], foregroundServerIP)
#     logging.info('sucess to upload to remote server: %s ' % (foregroundServerIP))


# 与时间服务器同步时间
def sysncTime(flag_env):
    if '1' == flag_env:
        timeIpList = CONFIG.MANAUL_ENV_DIC['MACHINE_LIST']
    elif '2' == flag_env:
        timeIpList = CONFIG.AUTO_ENV_DIC['MACHINE_LIST']
    elif '3' == flag_env:
        timeIpList = CONFIG.DEV_ENV_DIC['MACHINE_LIST']
    elif '4' == flag_env:
        timeIpList = CONFIG.DEV_ENV_DIC['MACHINE_LIST']
    logging.info('start to sysnc time from timeserver.')
    for timeIp in timeIpList:
        utils.sshAndRun(['ntpdate -u 10.0.250.132'], timeIp)
    logging.info('sucess to sysnc time from timeserver.')


# 清理对应容器服务器
def cleanContainerServer(ip):
    # 停止运行中的容器
    manageContainerMachine.stopRunningList(ip)
    # 删除所有容器
    manageContainerMachine.deleteStoppedContainerList(ip)
    # 删除所有镜像
    manageContainerMachine.deleteAllImages(ip)
    

# 清理指定环境的所有设备上的容器和镜像
def cleanContainersAndImagesOfAllMachine(ipList):
    for ip in ipList:
        cleanContainerServer(ip)


# 获得war包镜像与分配ip的对应关系字典
def getWarAndIpMap(ipList, warContainersList):
    nameAndIpMap = {}
    ipListLength = len(ipList)
    if ipListLength == 0:
        raise myException.MyException("There is no machine can be used, please check the config of MACHINE_LIST")
#    nameAndIpMap['ui'] = ipList[len(ipList) - 1]
    warNameList = warContainersList[:]
    warNameList.remove('ui')
    for name in warNameList:
        i = warNameList.index(name)
        j = i % ipListLength
        nameAndIpMap[name] = ipList[j]
    return nameAndIpMap


# 将对应的镜像获得到对应的IP上
def pullProperImageForProperIp(mapDic, tagName):
    for name in mapDic.keys():
        manageContainerMachine.getImage(mapDic[name], CONFIG.DOCKERREPOSITORY + '/' + name, tagName)
        logging.info("Pulled %s:%s to %s success." % (CONFIG.DOCKERREPOSITORY + '/' + name, tagName, mapDic[name]))
        
    
# 运行
def run():
    # 获得传入参数,传入参数列表：[脚本名称(不填),环境标志,标签,版本,serviceWarListFile]
    # 参数4是由jenkins中部署的上级job：构建，传过来的serviceWarListFile文件的目录
    parameterList = sys.argv
    db_update_date = datetime.datetime.today().date().strftime('%Y%m%d')
    if parameterList[1] == '1':
        env_Dic = CONFIG.MANAUL_ENV_DIC
        configerFileDirStr = 'TEST'
    elif parameterList[1] == '2':
        env_Dic = CONFIG.AUTO_ENV_DIC
        configerFileDirStr = 'DAILYAUTOTEST'
    elif parameterList[1] == '3':
        env_Dic = CONFIG.DEV_ENV_DIC
        configerFileDirStr = 'DEVELOP'
    elif parameterList[1] == '4':
        env_Dic = CONFIG.BYRC_ENV_DIC
        configerFileDirStr = 'BYRC'
    # 数据库快照处理
    vmManager.gotoTestSystemEnvSnapshot(env_Dic)
    # 同步时间
    sysncTime(parameterList[1])
    # 获得配置文件和数据库脚本
    fileDispose.getBuildConfigAndDBScript(env_Dic, parameterList[3])
    # 解压数据库文件
    fileDispose.unzipDailyDBScriptFile()
    # 升级数据库
    dailyUpdateDB(env_Dic, db_update_date)
    # 清理环境设备中的容器和镜像
    cleanContainersAndImagesOfAllMachine(env_Dic['MACHINE_LIST'])
    logging.info("All machine of %s have been cleanning" % env_Dic['DICNAME'])
    logging.info("The machine:%s is chosen to be platform-sever-machine" % env_Dic['MACHINE_LIST'][0])
    logging.info("Delete DIR :configerFile on %s,if it exist." % env_Dic['MACHINE_LIST'][0])
    # 删除配置文件目录
    manageContainerMachine.delRemoteDir(env_Dic['MACHINE_LIST'][0], CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER + CONFIG.REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR[configerFileDirStr])
    # 在平台机器上获得zookeeper镜像
    manageContainerMachine.getImage(env_Dic['MACHINE_LIST'][0], 'registry:5000/library/zookeeper', 'basal')
    # 在平台机器上获得redis镜像
    manageContainerMachine.getImage(env_Dic['MACHINE_LIST'][0], 'registry:5000/library/redis', 'basal')
    # 在平台机器上获得dubbo镜像
    manageContainerMachine.getImage(env_Dic['MACHINE_LIST'][0], 'registry:5000/library/dubbo', 'basal')
    # 在平台机器上获得对应标签的platform-cache-config镜像
    manageContainerMachine.getImage(env_Dic['MACHINE_LIST'][0], 'registry:5000/library/platform-cache-config', parameterList[2])
    # 在平台机器上获得zookeeper——ui的镜像
    manageContainerMachine.getImage(env_Dic['MACHINE_LIST'][0], 'registry:5000/library/zookeeperui', 'basal')
    # 在平台机器上获得redis_stat镜像
    manageContainerMachine.getImage(env_Dic['MACHINE_LIST'][0], 'registry:5000/library/redis-stat', 'basal')
    # 获得部署war包镜像的服务器列表
    warIpList = env_Dic['MACHINE_LIST'][1:]
    # 需要部署的容器名称列表
    # 参数4是由jenkins中部署的上级job：构建，传过来的serviceWarListFile文件的目录
    nameFile = open(parameterList[4] + os.sep + 'Fordockerfile' + os.sep + 'serviceWarListFile')
    tempContainersNameList = nameFile.readlines()
    nameFile.close()
    tempContainersNameList.append('ui')
    warContainersNameList = []
    for n in tempContainersNameList:
        warContainersNameList.append(n.strip())
    # warContainersNameList = tempContainersNameList
    # 获得容器与部署容器的ip的对应关系
    containerNameAndIpMap = getWarAndIpMap(warIpList, warContainersNameList)
    # 增加ui容器的所属机器
    containerNameAndIpMap['ui'] = env_Dic['MACHINE_LIST'][0]
    # 在对应的IP上获得对应的镜像，注意镜像的TAG
    pullProperImageForProperIp(containerNameAndIpMap, parameterList[2])
    manageContainerMachine.prepareConfig(env_Dic['MACHINE_LIST'][0], parameterList[3], configerFileDirStr, env_Dic)
    # 启动平台容器
    manageContainerMachine.startPlatContainer(env_Dic, parameterList[2], configerFileDirStr)
    # 启动war容器
    manageContainerMachine.startWarContainers(env_Dic['MACHINE_LIST'][0], containerNameAndIpMap, parameterList[2], warContainersNameList)
    logging.info("Deployment completed successfully")


if __name__ == '__main__':
    logService.initLogging()
    run()
    # start()
    logService.destoryLogging()
    