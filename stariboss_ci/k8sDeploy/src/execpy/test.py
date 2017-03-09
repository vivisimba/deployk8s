# -*- coding: utf-8 -*-
'''
Created on 2016年5月5日

@author: Simba
'''

import os
import sys
import subprocess
import config.config as CONFIG
import replace_rc
import deployK8s
import deleteRcAndSvc
import tool
from pip._vendor.distlib.compat import ZipFile
import exception.myException as myException



def getAllFile(fileDir):
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
                if (fileWholeName.endswith('.war') or fileWholeName.endswith('.WAR')):
                    yamlFileList.append(fileWholeName)
    return yamlFileList
zipList = getAllFile(r'D:\DB')
#print zipList
for zipzip in zipList:
    print zipzip
    indexfirst = zipzip.rfind('\\')
    strLength = len(zipzip)
    indexlast = strLength - 4
    nameStr = zipzip[indexfirst:indexlast]
    toDir = r'D:\DB' + '\\%s' % nameStr
    os.makedirs(toDir)
    tool.unzipFile(zipzip, toDir)

#tool.unzipFile(fileName, CONFIG.NFS_HOST_DIR + os.sep + 'zkconfig' + os.sep)


# cmdList = []
# cmd = 'ntpdate -u 10.0.251.221'
# cmdList.append(cmd)
# resTup = tool.sshAndRun(cmdList, '10.0.251.220')
# print ' '.join(resTup[0][cmd])
# if resTup[1][cmd]:
#     print ' '.join(resTup[1][cmd])
#     raise myException.MyException(' '.join(resTup[1][cmd]))
# print ("Time of node %s has been changed successfully." % '10.0.251.220')
