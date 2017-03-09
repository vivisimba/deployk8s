# -*- coding: utf-8 -*-
'''
Created on 2016年5月11日

@author: Simba
'''
import vmSnapshotOperation
import logging
import time
import exception.myException as myException


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
            res_db = vmSnapshotOperation.createSnapshot(env_dic['NEW_BOSS_DB_VMNAME'],
                                                        'snapshot_' + str(time.strftime('%Y%m%d%H%M', time.localtime())),
                                                        env_dic['NEW_BOSS_VMWARE_IP'],
                                                        env_dic['NEW_BOSS_VMWARE_USERNAME'],
                                                        env_dic['NEW_BOSS_VMWARE_PASSWORD']
                                                        )
            if res_db == 'ok':
                logging.info('===================== sucessful createSnapshot db server. =====================')
                break
        while True:
            delRes = deleteDBFirstSnapshot(env_dic)
            if delRes == 'ok':
                logging.info('===================== sucessful remove snapshot of db server. =====================')
                break
#         countFlag = 0
#         while True:
#             res_db = vmSnapshotOperation.createSnapshot(env_dic['NEW_BOSS_DB_VMNAME'],
#                                                         'snapshot_' + str(time.strftime('%Y%m%d%H%M', time.localtime())),
#                                                         env_dic['NEW_BOSS_VMWARE_IP'],
#                                                         env_dic['NEW_BOSS_VMWARE_USERNAME'],
#                                                         env_dic['NEW_BOSS_VMWARE_PASSWORD']
#                                                         )
#             countFlag += 1
#             if res_db == 'ok':
#                 # 删除最早的一个数据库快照，防止数据库快照太多，占用磁盘空间
#                 deleteDBFirstSnapshot(env_dic)
#                 break
#             elif countFlag > 3:
#                 break
#     if res_db == 'ok':
#         logging.info('===================== sucessful createSnapshot db server. =====================')
#     else:
#         err = '===================== ERROR! Please contact admin to check the virtual machine environment! ====================='
#         raise myException.MyException(err)
    
    
    
#     if '1' == flag_env:  # 手工测试环境
#         '''创建新Boss手工测试的数据库快照'''
#         res_db = vmSnapshotOperation.createSnapshot(CONFIG.MANAUL_ENV_DIC['NEW_BOSS_DB_VMNAME'],
#                                                     'snapshot_' + str(time.strftime('%Y%m%d%H%M', time.localtime())),
#                                                     CONFIG.MANAUL_ENV_DIC['NEW_BOSS_VMWARE_IP'],
#                                                     CONFIG.MANAUL_ENV_DIC['NEW_BOSS_VMWARE_USERNAME'],
#                                                     CONFIG.MANAUL_ENV_DIC['NEW_BOSS_VMWARE_PASSWORD']
#                                                     )
#         # 删除最早的一个数据库快照
#         deleteDBFirstSnapshot(flag_env)
#     elif '2' == flag_env:  # 自动化测试环境
#         '''恢复新Boss自动化测试的数据库快照'''
#         res_db = vmSnapshotOperation.gotoSnapshot(CONFIG.AUTO_ENV_DIC['NEW_BOSS_DB_VMNAME'],
#                                                   CONFIG.AUTO_ENV_DIC['NEW_BOSS_DB_SNAPSHOTNAME'],
#                                                   CONFIG.AUTO_ENV_DIC['NEW_BOSS_VMWARE_IP'],
#                                                   CONFIG.AUTO_ENV_DIC['NEW_BOSS_VMWARE_USERNAME'],
#                                                   CONFIG.AUTO_ENV_DIC['NEW_BOSS_VMWARE_PASSWORD']
#                                                   )
#     elif '3' == flag_env:  # 研发测试环境
#         '''创建新Boss研发测试的数据库快照'''
#         res_db = vmSnapshotOperation.createSnapshot(CONFIG.DEV_ENV_DIC['NEW_BOSS_DB_VMNAME'],
#                                                     'snapshot_' + str(time.strftime('%Y%m%d%H%M', time.localtime())),
#                                                     CONFIG.DEV_ENV_DIC['NEW_BOSS_VMWARE_IP'],
#                                                     CONFIG.DEV_ENV_DIC['NEW_BOSS_VMWARE_USERNAME'],
#                                                     CONFIG.DEV_ENV_DIC['NEW_BOSS_VMWARE_PASSWORD']
#                                                     )
#         # 删除最早的一个数据库快照
#         deleteDBFirstSnapshot(flag_env)
#     if res_db == 'ok':
#         logging.info('sucessful gotoSnapshot db server.')
#     else:
#         err = 'ERROR! Please contact admin to check the virtual machine environment!'
#         raise myException.MyException(err)


# 根据环境代号，获得虚拟机名称
# def getDBVMName(flag_env):
#     vmName = ''
#     if flag_env == '1':
#         vmName = CONFIG.MANAUL_ENV_DIC['NEW_BOSS_DB_VMNAME']
#     elif flag_env == '2':
#         vmName = CONFIG.AUTO_ENV_DIC['NEW_BOSS_DB_VMNAME']
#     elif flag_env == '3':
#         vmName = CONFIG.DEV_ENV_DIC['NEW_BOSS_DB_VMNAME']
#     return vmName


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
    res_db = vmSnapshotOperation.gotoSnapshot(envDic['NEW_BOSS_DB_VMNAME'],
                                              snapshotName[0],
                                              envDic['NEW_BOSS_VMWARE_IP'],
                                              envDic['NEW_BOSS_VMWARE_USERNAME'],
                                              envDic['NEW_BOSS_VMWARE_PASSWORD']
                                              )
    if snapStatus != '1':
        res_stat = poweronDevDBVmare(envDic)
        if res_db == 'ok' and res_stat == 'ok':
            logging.info('because the new boss test environment start faild, so back db snashot to the last stat: %s' % snapshotName[0])
        else:
            err = 'ERROR! Please contact admin to check the virtual machine environment! gotoSnapshot error or poweron error'
            raise myException.MyException(err)


# # 将指定名称的虚拟机恢复到最新的快照，参数：虚拟机名称
# def recoverLastestSnapshot(vmName):
#     lastestSnapshotName = vmSnapshotOperation.getLastAndFirstSnapshotName(vmName,
#                                                                           CONFIG.NEW_BOSS_VMWARE_IP,
#                                                                           CONFIG.NEW_BOSS_VMWARE_USERNAME,
#                                                                           CONFIG.NEW_BOSS_VMWARE_PASSWORD
#                                                                           )
