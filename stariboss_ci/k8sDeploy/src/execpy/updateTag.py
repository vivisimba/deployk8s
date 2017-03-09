# -*- coding: utf-8 -*-
'''
Created on 2016年10月26日

@author: Simba
'''


import replace_rc
import log.logService as logService
import sys


# 更新某目录下的所有YAML文件中的镜像标签
def updateYamlTag(rcDir, oldTag, newTag):
    fileList = replace_rc.getAllYamlFile(rcDir)
    replace_rc.updateImageTag(fileList, oldTag, newTag)


def run():
    # (脚本名称，要更新的RC文件目录, 旧标签, 新标签)
    parameterList = sys.argv
    updateYamlTag(parameterList[1], parameterList[2], parameterList[3])


if __name__ == '__main__':
    logService.initLogging()
    run()
    logService.destoryLogging()
