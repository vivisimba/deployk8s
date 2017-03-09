# -*- coding: utf-8 -*-
'''
Created on 2016年5月11日

@author: Simba
'''
import os
import logging
import config.config as CONFIG
import urllib2
import fnmatch
import utils.util as utils


# 获得配置文件和数据库脚本
def getBuildConfigAndDBScript(env_Dic, dbDailyVersion):
    dbNames = env_Dic['DB_LISTNAME'].keys()
    for t in dbNames:
        logging.info(t)
    
    os.chdir(CONFIG.tempFolder)
    os.system('rm -rf *')
    
    logging.info('start to download all dbScript and config file.')
    for dbName in dbNames:
        logging.info('start to download ' + dbName)
        url = CONFIG.NEW_BOSS_BUILD_DBSCRIPT + env_Dic['NEW_BOSS_FTPDIR'] + dbDailyVersion + "/" + "ConfigAndDbscript/" + dbName + "-" + dbDailyVersion + ".zip"
        logging.info('url = ' + url)
        dataFile = urllib2.urlopen(url)
        data = dataFile.read()
        with open(dbName + ".zip", "wb") as download:
            download.write(data)
        logging.info('sucess download ' + dbName)
    logging.info('sucessful download all dbScript and config file.')


# 解压数据库脚本文件
def unzipDailyDBScriptFile():
    os.chdir(CONFIG.tempFolder)
    dirs = os.listdir(CONFIG.tempFolder)
    dbScritpNames = []
    for dirr in dirs:
        if fnmatch.fnmatch(dirr, '*-dbscript.zip'):
            dbScritpNames.append(dirr)
    logging.info('start to unzip all dbScript zip file.')
    for dbScritpName in dbScritpNames:
        os.chdir(CONFIG.tempFolder)
        dbScriptfileDir = CONFIG.tempFolder + '/' + dbScritpName.split('.zip')[0] + '/'
        logging.info('unzip dbScript zip file: ' + dbScritpName + ' success.')
        utils.unzipFile(dbScritpName, dbScriptfileDir)
    logging.info('successful unzip all dbScript zip file.')
    
    
# 从ftp获得文件对应环境的指定版本的文件
def getFileFromFtp(flag_env, version, fileName):
    if "1" == flag_env:
        falgDir = "TEST"
    elif "2" == flag_env:
        falgDir = "DAILYAUTOTEST"
    elif "3" == flag_env:
        falgDir = "DEVELOP"
    wholeFileName = fileName + '-' + version + '.zip'
    logging.info('start to download ' + wholeFileName)
    "ftp://buildftp:buildftp@10.0.250.250/Stariboss-7.X/"
    url = CONFIG.NEW_BOSS_BUILD_DBSCRIPT + falgDir + os.sep + version + '/ConfigAndDbscript' + os.sep + wholeFileName
    logging.info("Download from %s" % url)
