# -*- coding: utf-8 -*-
'''
Created on 2016年10月28日

@author: Simba
'''
import vmSnapshotOperation
import time
import logging
import config.config as CONFIG
import tool
import os
import urllib2
import fnmatch
import datetime
import linecache
import exception.myException as myException


# 删除指定环境对应的第一个快照
def deleteDBFirstSnapshot(envDic):
    snapshotName = vmSnapshotOperation.getLastAndFirstSnapshotName(envDic['NEW_BOSS_DB_VMNAME'],
                                                                   envDic['NEW_BOSS_VMWARE_IP'],
                                                                   envDic['NEW_BOSS_VMWARE_USERNAME'],
                                                                   envDic['NEW_BOSS_VMWARE_PASSWORD'])
    logging.info('first snapshot name = ' + snapshotName[1])
    
#    res_db = 'ok'
#    if '0000' not in snapshotName[1]:
    logging.info('===================== start to remove first snapshot: ' + snapshotName[1] + '=====================')
    res_db = vmSnapshotOperation.snapshotManager(envDic['NEW_BOSS_VMWARE_IP'],
                                                 envDic['NEW_BOSS_VMWARE_USERNAME'],
                                                 envDic['NEW_BOSS_VMWARE_PASSWORD'],
                                                 envDic['NEW_BOSS_DB_VMNAME'],
                                                 'remove',
                                                 snapshotName[1],
                                                 snapshotName[1])
    logging.info('===================== sucess remove first snapshot: ' + snapshotName[1] + '=====================')
    return res_db


# 指定环境对应的数据库快照处理流程
def gotoTestSystemEnvSnapshot(env_dic):
    if 'AUTO' == env_dic['DICNAME']:
        res_db = vmSnapshotOperation.gotoSnapshot(env_dic['NEW_BOSS_DB_VMNAME'],
                                                  env_dic['NEW_BOSS_DB_SNAPSHOTNAME'],
                                                  env_dic['NEW_BOSS_VMWARE_IP'],
                                                  env_dic['NEW_BOSS_VMWARE_USERNAME'],
                                                  env_dic['NEW_BOSS_VMWARE_PASSWORD']
                                                  )
    else:
        while True:
            print "************"
            res_db = vmSnapshotOperation.createSnapshot(env_dic['NEW_BOSS_DB_VMNAME'],
                                                        'snapshot_' + str(time.strftime('%Y%m%d%H%M', time.localtime())),
                                                        env_dic['NEW_BOSS_VMWARE_IP'],
                                                        env_dic['NEW_BOSS_VMWARE_USERNAME'],
                                                        env_dic['NEW_BOSS_VMWARE_PASSWORD']
                                                        )
            print "============================="
            if res_db == 'ok':
                logging.info('===================== sucessful createSnapshot db server. =====================')
                break
        while True:
            delRes = deleteDBFirstSnapshot(env_dic)
            if delRes == 'ok':
                logging.info('===================== sucessful remove snapshot of db server. =====================')
                break


# 同步时间
def sysncTime():
    timeIpList = CONFIG.MASTERIP + CONFIG.NODEMACHINE
    timeIpList.append(CONFIG.DB_ENV_DIC['NEW_BOSS_DB_IP'])
    logging.info('start to sysnc time from timeserver.')
    for timeIp in timeIpList:
        tool.sshAndRun(['ntpdate -u 10.0.250.132'], timeIp)
    logging.info('sucess to sysnc time from timeserver.')


# 获得数据库脚本
def getBuildConfigAndDBScript(env_Dic, dbDailyVersion):
    dbNames = env_Dic['DB_LISTNAME'].keys()
    for t in dbNames:
        logging.info(t)
    
    os.chdir(env_Dic['tempFolder'])
    os.system('rm -rf *')
    
    logging.info('start to download all dbScript and config file.')
    for dbName in dbNames:
        logging.info('start to download ' + dbName)
        url = env_Dic['NEW_BOSS_BUILD_DBSCRIPT'] + env_Dic['NEW_BOSS_FTPDIR'] + dbDailyVersion + "/" + "ConfigAndDbscript/" + dbName + "-" + dbDailyVersion + ".zip"
        logging.info('url = ' + url)
        dataFile = urllib2.urlopen(url)
        data = dataFile.read()
        with open(dbName + ".zip", "wb") as download:
            download.write(data)
        logging.info('sucess download ' + dbName)
    logging.info('sucessful download all dbScript and config file.')


# 解压数据库脚本文件
def unzipDailyDBScriptFile(env_Dic):
    os.chdir(env_Dic['tempFolder'])
    dirs = os.listdir(env_Dic['tempFolder'])
    dbScritpNames = []
    for dirr in dirs:
        if fnmatch.fnmatch(dirr, '*-dbscript.zip'):
            dbScritpNames.append(dirr)
    logging.info('start to unzip all dbScript zip file.')
    for dbScritpName in dbScritpNames:
        os.chdir(env_Dic['tempFolder'])
        dbScriptfileDir = env_Dic['tempFolder'] + '/' + dbScritpName.split('.zip')[0] + '/'
        logging.info('unzip dbScript zip file: ' + dbScritpName + ' success.')
        tool.unzipFile(dbScritpName, dbScriptfileDir)
    logging.info('successful unzip all dbScript zip file.')


# 获得每日需执行的配置文件以及数据库脚本
def dailyGetDBScriptNamesAndDBScriptFileDirs(env_Dic):
    os.chdir(env_Dic['tempFolder'])
    dirs = os.listdir(env_Dic['tempFolder'])
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


def isDBUser(env_Dic, dbUserName):
    logging.info('xxxxxxxxxxxxxxxxxxxxxxx=' + dbUserName)
    originalList = ['SELECT COUNT(*)']
    modifiedList = ["SELECT COUNT(*) FROM Dba_Users du WHERE du.username = '" + dbUserName.upper() + "';\n"]
    modifyConfigFile(env_Dic['NEW_BOSS_DB_SCRIPT_PATCH'] + 'queryDBUser.sql', originalList, modifiedList)
    
    dbLocalName = env_Dic['NEW_BOSS_DB_LOCALNAME']
    systemPassword = env_Dic['NEW_BOSS_DB_SYSTEM_PWD']
    logName = 'queryDBUser.log'
    os.system('export LANG=zh_CN.GBK;sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % ('system',
                                                                              systemPassword,
                                                                              dbLocalName,
                                                                              env_Dic['NEW_BOSS_DB_SCRIPT_PATCH'],
                                                                              'queryDBUser.sql',
                                                                              CONFIG.LOG_HOME,
                                                                              logName))
    linecache.checkcache(CONFIG.LOG_HOME + logName)
    flagDBUser = linecache.getline(CONFIG.LOG_HOME + logName, 14)
    flagDBUser = flagDBUser.strip()
    
    return flagDBUser


# 获得数据库当前版本
def getDBCurrentVersion(env_Dic, dbUserName, dbUserPwd):
    print "******************************************************************************************************"
    dbLocalName = env_Dic['NEW_BOSS_DB_LOCALNAME']
    logName = 'queryDBCurrentVersion.log'
    print dbUserName
    os.system('export LANG=zh_CN.GBK;sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % (dbUserName,
                                                                              dbUserPwd,
                                                                              dbLocalName,
                                                                              env_Dic['NEW_BOSS_DB_SCRIPT_PATCH'],
                                                                              'queryDBCurrentVersion.sql',
                                                                              CONFIG.LOG_HOME,
                                                                              logName))
    linecache.checkcache(CONFIG.LOG_HOME + logName)
    dbVersion = linecache.getline(CONFIG.LOG_HOME + logName, 14)
    dbVersion = dbVersion.strip()
    
    return dbVersion


# 快照开机
def poweronDevDBVmare(envDic):
    flag = vmSnapshotOperation.vmControl(envDic['NEW_BOSS_VMWARE_IP'],
                                         envDic['NEW_BOSS_VMWARE_USERNAME'],
                                         envDic['NEW_BOSS_VMWARE_PASSWORD'],
                                         envDic['NEW_BOSS_DB_VMNAME'],
                                         'poweron')
    return flag


# 将数据库快照恢复到最后一个快照
def gotoDBLastSnapshot(envDic):
    snapshotName = vmSnapshotOperation.getLastAndFirstSnapshotName(envDic['NEW_BOSS_DB_VMNAME'],
                                                                   envDic['NEW_BOSS_VMWARE_IP'],
                                                                   envDic['NEW_BOSS_VMWARE_USERNAME'],
                                                                   envDic['NEW_BOSS_VMWARE_PASSWORD']
                                                                   )
    logging.info('last snapshot name = ' + snapshotName[0])
    snapStatus = vmSnapshotOperation.getSnapshotStat(snapshotName[0],
                                                     envDic['NEW_BOSS_VMWARE_IP'],
                                                     envDic['NEW_BOSS_VMWARE_USERNAME'],
                                                     envDic['NEW_BOSS_VMWARE_PASSWORD'],
                                                     envDic['NEW_BOSS_DB_VMNAME'])
    while True:
        res_db = vmSnapshotOperation.gotoSnapshot(envDic['NEW_BOSS_DB_VMNAME'],
                                                  snapshotName[0],
                                                  envDic['NEW_BOSS_VMWARE_IP'],
                                                  envDic['NEW_BOSS_VMWARE_USERNAME'],
                                                  envDic['NEW_BOSS_VMWARE_PASSWORD']
                                                  )
        if res_db == 'ok':
            break
    if snapStatus != '1':
        while True:
            res_stat = poweronDevDBVmare(envDic)
            if res_stat == 'ok':
                break
        if res_db == 'ok' and res_stat == 'ok':
            logging.info('because the new boss test environment start faild, so back db snashot to the last stat: %s' % snapshotName[0])
        else:
            err = 'ERROR! Please contact admin to check the virtual machine environment! gotoSnapshot error or poweron error'
            raise myException.MyException(err)


# 查询脚本文件执行到哪一行
def getLastSqlFlag(env_dic, dbUserName, dbUserPwd):
    dbsid = env_dic['NEW_BOSS_DB_LOCALNAME']
    logName = 'queryDBLastSqlFlag.log'
    os.system('sqlplus %s/%s@%s @%s%s 1 > %s%s 2>&1' % (dbUserName,
                                                        dbUserPwd,
                                                        dbsid,
                                                        env_dic['NEW_BOSS_DB_SCRIPT_PATCH'],
                                                        'queryDBLastSqlFlag.sql',
                                                        CONFIG.LOG_HOME,
                                                        logName))
    linecache.checkcache(CONFIG.LOG_HOME + logName)
    lastSqlFlag = linecache.getline(CONFIG.LOG_HOME + logName, 14)  # 查询结果在日志文件中的第14行
    
    return lastSqlFlag.strip()


# 升级数据库
def dailyUpdateDB(env_dic, db_update_date):
    dbScriptNames, dbScriptFileDirs = dailyGetDBScriptNamesAndDBScriptFileDirs(env_dic)
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
                yesterday = endDate - tool.getTimeDelta()
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
                    yesterday = endDate - tool.getTimeDelta()
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
            tool.convertFileEncodingToGBK(filePath)
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
                        gotoDBLastSnapshot(env_dic)
                    raise myException.MyException('faild to use sqlplus run ' + filePath + ' file !')
                else:
                    logging.info('sucessful use sqlplus run ' + filePath)
            except IOError, e:
                raise myException.MyException(e)
            finally:
                fp.close()
        print dailyNormalSQLs
        for dailyNormalSQL in dailyNormalSQLs:
            filePath = dbFileDir + dailyNormalSQL
            # 将脚本文件编码转换成GBK
            tool.convertFileEncodingToGBK(filePath)
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
                gotoDBLastSnapshot(env_dic)
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
            print "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
            if flagDBUser == '1' and getDBCurrentVersion(env_dic, dbUserName, dbUserPwd) in dailyNormalSQL:
                print "============================================================================================================================================="
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
                    gotoDBLastSnapshot(env_dic)
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
                        pass
                        #gotoDBLastSnapshot(env_dic)
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

