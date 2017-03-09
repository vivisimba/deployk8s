# -*- coding: utf-8 -*-
'''
Created on 2016年12月23日

@author: Simba
'''
import log.logService as logService
import vmOperationByPython
import config.config as CONFIG
import shutil
import os
import sys
import subprocess
import datetime
import fileDispose
import deployByContainer
import time
import logging


# 清空temp文件夹
def clearTemp(tempDir):
    shutil.rmtree(tempDir)
    os.makedirs(tempDir)


# 传入字典的方式传入参数
def gotoDBLastSnapshot(db_Dic):
    vmOperationByPython.snapshotManager(db_Dic['NEW_BOSS_VMWARE_IP'],
                                        db_Dic['NEW_BOSS_VMWARE_USERNAME'],
                                        db_Dic['NEW_BOSS_VMWARE_PASSWORD'],
                                        'revert',
                                        db_Dic['NEW_BOSS_DB_VMNAME'],
                                        '20161220'
                                        )


# 参数：脚本本身，构建目录下的脚本zip包目录, 版本+构建次数字符串例如：-7.1.1.DEV.4017
def run():
    parameterList = sys.argv
    db_update_date = datetime.datetime.today().date().strftime('%Y%m%d')
    # 恢复快照
    logging.info("******************************")
    vmOperationByPython.snapshotManager(CONFIG.VM_DIC['vcenter_ip'],
                                        CONFIG.VM_DIC['vcenter_user'],
                                        CONFIG.VM_DIC['vcenter_password'],
                                        'revert',
                                        'DB-checkin-162',
                                        '20161220')
    logging.info("******************************")
    time.sleep(60)
    # 清空temp文件夹
    tempDir = CONFIG.ROOT_HOME + os.sep + 'temp'
    clearTemp(tempDir)
    # 将数据库脚本zip文件拷贝到temp目录
    cpStr = "cp %s/* %s" % (parameterList[1], tempDir)
    p = subprocess.Popen(cpStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    p.wait()
#     dbFileList = os.listdir(tempDir)
    localDbList = CONFIG.DB_DIC.keys()
    # 判断python脚本中的数据库模块数量与刚构建出来的数据库脚本文件数量是否相等
#     if len(dbFileList) != len(localDbList):
#         raise myexception.MyException("Number of pythonScript db is not equal to which were built.")
    # 重命名temp文件夹下的所有zip文件
    for dbName in localDbList:
        originalName = tempDir + os.sep + dbName + parameterList[2] + '.zip'
        newName = tempDir + os.sep + dbName + '.zip'
        os.rename(originalName, newName)
    # 解压数据库文件
    fileDispose.unzipDailyDBScriptFile()
    # 执行数据库升级
    deployByContainer.dailyUpdateDB(CONFIG.CHECKIN_ENV_DIC, db_update_date)
    

if __name__ == '__main__':
    logService.initLogging()
    run()
    logService.destoryLogging()
