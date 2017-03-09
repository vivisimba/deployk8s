# -*- coding: utf-8 -*-
'''
Created on 2016年10月9日

@author: Simba
'''
import logging
import paramiko
import scp
import time
import zipfile
import datetime
import os


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


def uploadViaSCP(filePathList, uploadPathList, ip, port=22, username='root', password='123456'):
    '''
           通过SCP上传文件,默认尝试5次,上传成功,返回'ok';上传失败,返回'error';
    filePathList 和 uploadPathList 成对使用,即filePathList[0]中的文件上传至uploadPathList[0]指定的路径下
    uploadPathList中指定的目录如果不存在,则自动创建该目录
    :param filePathList : 列表,依次存放要上传的文件路径
    :param uploadPathList : 列表，依次存放上传的目的路径
    :param ip : 目的服务器IP地址
    :param port : 目的服务器端口,默认22
    :param username : 目的服务器登录用户名,默认root
    :param password : 目的服务器登录密码,默认123456
    '''
    i = 0
    while i < 5:
        try:
            ssh = paramiko.SSHClient()
            ssh.load_system_host_keys()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(ip, port=port, username=username, password=password)
            doScp = scp.SCPClient(ssh.get_transport())
            for (filePath, uploadPath) in zip(filePathList, uploadPathList):
                doScp.put(filePath, uploadPath, True)
                logging.info('SCP ' + filePath + ' to ' + ip + ' : ' + uploadPath + ' ok')
            return 'ok'
        except paramiko.SSHException, e:
            if 'No such file or directory' in e:
                logging.info('create dir ' + uploadPath)
                ssh.exec_command('mkdir ' + uploadPath)
                i = i + 1
                continue
            else:
                logging.warn(e)
                logging.info('wait 15s and try scp again ...')
                time.sleep(15)
                i = i + 1
                continue
        finally:
            ssh.close()
    return 'error'


# 解压
def unzipFile(unzipFile, path):
    '''
    
    :param unzipFile:被解压缩文件的绝对路径
    :param path:解压后存放的绝对路径
    '''
    if zipfile.is_zipfile(unzipFile):
        fz = zipfile.ZipFile(unzipFile, 'r')
        for f in fz.namelist():
            fz.extract(f, path)
        return 'ok'
    else:
        msg = 'This file is not zip file'
        logging.warn('This file is not zip file')
        return msg


# 下载进度
def Schedule(a, b, c):
    '''''
    a:已经下载的数据块
    b:数据块的大小
    c:远程文件的大小
   '''
    per = 100.0 * a * b / c
    if per > 100:
        per = 100
    print '%.2f%%' % per


# 返回值是 1 天的时间间隔，用于日期的加减运算，对应的类型是 datetime.timedelta
def getTimeDelta():
    start = '20160301'
    end = '20160302'
    startDateTime = datetime.datetime.strptime(start, '%Y%m%d')
    endDateTime = datetime.datetime.strptime(end, '%Y%m%d')
    startDate = startDateTime.date()
    endDate = endDateTime.date()
    delta = endDate - startDate
    
    # str = endDate.strftime('%Y%m%d')
    # print(type(str))
    # print(str)
    return delta


# 转换文件编码格式 由 UTF-8 转换为 GBK
def convertFileEncodingToGBK(filePath):
    logging.info('start to convert file encoding to gbk: ' + filePath)
    convertPath = filePath + '.bak'
    os.system("iconv -f UTF-8 -t GBK " + filePath + " -o " + convertPath)
    os.system("mv " + convertPath + " " + filePath)
    logging.info('sucess to convert file encoding to gbk: ' + filePath)
