# -*- coding: utf-8 -*-
'''
Created on 2016年5月19日

@author: Simba
'''


import logging
import scp
import paramiko
import time


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
        
        
        