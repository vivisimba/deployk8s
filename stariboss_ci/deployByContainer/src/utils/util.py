# -*- coding: utf-8 -*-
'''
Created on 2015-3-17

@author: jk_2
'''
from email.header import decode_header
from email.parser import Parser
from email.utils import parseaddr
import email
import logging
import shutil
import os
import paramiko
import poplib
import scp
import smtplib
import time
import zipfile
import PySTAF
import exception.myException as myException
import datetime
import urllib2


def getFileList(rootDir):
    '''
           遍历参数指定的路径，获取该路径下所有的文件夹和文件信息
           返回list_dirs，为三元组： root(路径), dirs(文件夹名), files(文件名)
    :param rootDir:
    '''
    list_dirs = os.walk(rootDir)
    return list_dirs


def copyDeployFiles(src, dst, level=1):
    '''
    
    :param src:
    :param dst:
    :param level: 0：递归拷贝所有文件；   1：仅拷贝第一层目录下的文件
    '''
    if os.path.isdir(dst) == False:
        os.makedirs(dst)
    list_dirs = getFileList(src)
    for root, _, files in list_dirs:
        for f in files:
            src = root + '/' + f
            shutil.copy(src, dst)
            logging.info('copy ' + f + ' ok!')
        if level == 1:
            break  # 只拷贝第一层目录下的文件，即忽略构建包内simplify文件夹内的jar简包


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

'''通过FTP上传文件'''
# def uploadViaFTP(filePathList, uploadPathList, ip, port='21', username='root', password='123456'):
#    ftp = ftplib.FTP()
#    ftp.connect(ip, port)
#    ftp.login(username, password)
#    bufsize = 1024
#    for (filePath, uploadPath) in zip(filePathList, uploadPathList):
#        ftp.cwd(uploadPath)
#        file_handler = open(filePath,'rb')#以读模式在本地打开文件
#        ftp.storbinary('STOR %s' % os.path.basename(filePath),file_handler,bufsize)#上传文件
# #    ftp.set_debuglevel(0)
#    file_handler.close()
#    ftp.quit()
#    print "ftp up OK"

'''通过FTP下载文件'''
# def downloadViaFTP(downloadPath, fileName, ip, port='21', username='autotest', password='autotest'):
#    ftp = ftplib.FTP()
#    ftp.connect(ip, port)
#    ftp.login(username, password)
# #    ftp.set_pasv(0)
#    bufsize = 1024
#    ftp.cwd(downloadPath + fileName)
#    fileList = ftp.nlst()
#    print fileList
#    pass


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


def downloadViaSCP(remotePathList, downloadPathList, ip, port=22, username='root', password='123456'):
    '''
          通过SCP下载文件
    remotePathList 和  downloadPathList 成对使用,即remotePathList[0]中的文件下载至downloadPathList[0]指定的路径下
    :param remotePathList : 列表,要拷贝的远程文件路径
    :param downloadPathList : 列表，拷贝到本地存放的文件路径
    :param ip : 远程服务器IP地址
    :param port : 远程服务器端口,默认22
    :param username : 远程服务器登录用户名,默认root
    :param password : 远程服务器登录密码,默认123456
    '''
    try:
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ip, port=port, username=username, password=password)
        doScp = scp.SCPClient(ssh.get_transport())
        for (remotePath, downloadPath) in zip(remotePathList, downloadPathList):
            doScp.get(remotePath, downloadPath, True)
            logging.info('SCP get ' + remotePath + ' ok')
    except Exception, e:
        logging.warn(e)
    finally:
        ssh.close()


def sshAndRun(cmds, ip, port=22, username='root', password='123456'):
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
        for cmd in cmds:
            ssh.exec_command(cmd)
            logging.info('exec cmd: ' + cmd)
#            print 'exec cmd: ' + cmd
#            stdin, stdout, stderr = ssh.exec_command(cmd)
#            print stdin.readlines()
#            print stdout.readlines()
#            print stderr.readlines()
    except Exception, e:
        logging.warn(e)
    finally:
        ssh.close()


def runLocalCmd(cmd):
    fp = os.popen(cmd)
    res = fp.read()
    logging.info(res)
    fp.close()
    return res


def stafCopyDirectory(handle, sourceDirPath, sourceMachine, destinationDirPath, destinationMachine):
    '''
           通过STAF复制文件夹
    '''
    try:
        request = "copy DIRECTORY  %s TODIRECTORY %s TOMACHINE %s RECURSE KEEPEMPTYDIRECTORIES" % (sourceDirPath, destinationDirPath, destinationMachine)
        handle.submit(sourceMachine, "FS", request)
    except PySTAF.STAFException, e:
        logging.error("Error registering with STAF, RC: %d" % e.rc)
        raise myException.MyException("Error registering with STAF, RC: %d" % e.rc)


def stafCopyFile(handle, sourcePath, sourceMachine, destinationPath, destinationMachine):
    '''
          通过STAF复制文件
    '''
    try:
        request = "copy file  %s TOFILE %s TOMACHINE %s" % (sourcePath, destinationPath, destinationMachine)
        handle.submit(sourceMachine, "FS", request)
    except PySTAF.STAFException, e:
        logging.error("Error registering with STAF, RC: %d" % e.rc)
        raise myException.MyException("Error registering with STAF, RC: %d" % e.rc)


# 拷贝文件到目录
def stafCopyFileToDir(handle, sourcePath, destinationMachine, destinationPath, sourceMachine='192.168.32.94'):
    '''
                该方法默认通过STAF将用例文件从本地复制到soapui所在服务器（32.95）
                也可调用该方法传入源文件地址和目标机器地址进行文件copy
    '''
    try:
        request = "copy file %s TODIRECTORY %s TOMACHINE %s" % (sourcePath, destinationPath, destinationMachine)
        handle.submit(sourceMachine, "FS", request)
    except PySTAF.STAFException, e:
        logging.error("#stafCopyFile()# -- Error registering with STAF, RC: %d" % e.rc)
        raise myException.MyException("#stafCopyFile()# -- Error registering with STAF, RC: %d" % e.rc)


def testLocalServiceIsRunning(serviceName, command_str):
    if serviceName != '':
        command_str = 'ps -ef |grep ' + serviceName + ' |wc -l'
    fp = os.popen(command_str).read()
    return fp


def testSTAFStatus():
    '''
           测试STAF是否启动，如果没启动，则启动STAF服务
    '''
    i = 0
    while i < 3:
        res = testLocalServiceIsRunning('staf', '')
        '''
                     有两条记录，因此应大于2
        root     19658 19655  0 10:53 pts/1    00:00:00 sh -c ps -ef |grep staf
        root     19660 19658  0 10:53 pts/1    00:00:00 grep staf
        '''
        if int(res) > 2:
            logging.info('STAF service startup successfully.')
            break
        else:
            logging.info('STAF service is down, prepare to start it.')
            os.popen('/usr/local/staf/bin/STAFProc &')
            i = i + 1
            time.sleep(10)
    if i >= 3:
        logging.error('STAF service start failed, please check it.')
        raise myException.MyException('STAF service start failed, please check it.')


# 检测远程STAF是否启动
def pingSTAF(ip):
    try:
        handle = PySTAF.STAFHandle("PatchTest")
        request = "ping"
        res = str(handle.submit(ip, "ping", request).resultContext)
        handle.unregister()
        return res
    except PySTAF.STAFException, e:
        logging.error("#pingSTAF()# -- Error registering with STAF, RC: %d" % e.rc)
        raise myException.MyException("#pingSTAF()# -- Error registering with STAF, RC: %d" % e.rc)


def sendEmail(addresseeList, attachmentPath, subject='autotest report', message="附件是自动化测试报告，请查阅！"):
    sender = 'autotest@startimes.com.cn'
    server = smtplib.SMTP("218.205.167.18")
#    server = smtplib.SMTP('mail.startimes.com.cn')
#    server.set_debuglevel(1)
    server.login("autotest@startimes.com.cn", "autotest123")  # 仅smtp服务器需要验证时

    # 构造MIMEMultipart对象做为根容器
    main_msg = email.MIMEMultipart.MIMEMultipart()

    # 构造MIMEText对象做为邮件显示内容并附加到根容器
    message = message.decode('utf-8')
    text_msg = email.MIMEText.MIMEText(message, _subtype='plain', _charset='utf-8')
    main_msg.attach(text_msg)

    # 构造MIMEBase对象做为文件附件内容并附加到根容器
    contype = 'application/octet-stream'
    maintype, subtype = contype.split('/', 1)

    if attachmentPath != '':
        # 读入文件内容并格式化
        data = open(attachmentPath, 'rb')
        file_msg = email.MIMEBase.MIMEBase(maintype, subtype)
        file_msg.set_payload(data.read())
        data.close()
        email.Encoders.encode_base64(file_msg)
    
        # 设置附件头
        basename = os.path.basename(attachmentPath)
        file_msg.add_header('Content-Disposition', 'attachment', filename=basename)
        main_msg.attach(file_msg)

    # 设置根容器属性
    main_msg['From'] = sender
    main_msg['To'] = ";".join(addresseeList)
    main_msg['Subject'] = subject
    main_msg['Date'] = email.Utils.formatdate()

    # 得到格式化后的完整文本
    fullText = main_msg.as_string()

    # 用smtp发送邮件
    try:
        logging.info('start sending email')
        server.sendmail(sender, addresseeList, fullText)
        server.close()
        logging.info('Send email successfully!')
    except Exception, e:
        logging.error(e)
        logging.error('Send email failed!')


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(message):
    # 先从message对象获取编码
    charset = message.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取
        content_type = message.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def get_email_info(message):
    if(message.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象
        parts = message.get_payload()
        for _, part in enumerate(parts):
            # 递归获取每一个子对象
            return get_email_info(part)
    else:
        # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断
        content_type = message.get_content_type()
        content = ''
        if content_type == 'text/plain':  # or content_type == 'text/html':
            # 纯文本(text/plain)或HTML内容(text/html)
            content = message.get_payload(decode=True)
            # 检测文本编码
            charset = guess_charset(message)
            if charset:
                content = content.decode(charset)
        else:
            # 不是文本,增加处理逻辑
            pass
        return content


def get_email_sender(message):
    _, sender = parseaddr(message.get('From', ''))
    return sender


def receiveEmail(host='mail.startimes.com.cn', username='autotest@startimes.com.cn', password='autotest123'):
    '''
           根据输入的POP3服务器地址, 用户名和口令收取邮件
    :param host:
    :param username:
    :param password:
    '''
    # 连接到POP3服务器
    mailServer = poplib.POP3(host)
    # 打开调试信息
#    mailServer.set_debuglevel(1)
    # 身份认证
    mailServer.user(username)
    mailServer.pass_(password)
    
    mailList = []
    sender = ''
    # stat()返回邮件数量和占用空间
    (mailCount, _) = mailServer.stat()
    # 邮件ID从1开始，所以mailCount+1
    for index in range(1, mailCount + 1):
        # 根据ID获取邮件
        (_, lines, _) = mailServer.retr(index)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本
        msg_content = '\r\n'.join(lines)
        # Create a message structure from a string
        msg = Parser().parsestr(msg_content)
        
        # 解析出发件人
        sender = get_email_sender(msg)

        # 解析出邮件
#        msgList.append(get_email_info(msg))
        mailContent = get_email_info(msg)
        # 解析出标题
        mailSubjectTup = decode_header(msg.get("subject", ''))
        subList = []
        for subjectTup in mailSubjectTup:
            if subjectTup[1]:
                mailSubjectPart = unicode(subjectTup[0], subjectTup[1])
            else:
                mailSubjectPart = unicode(subjectTup[0], 'gb2312')
            subList.append(mailSubjectPart)
        mailSubject = ''.join(subList)
        mailTupple = (sender, mailContent, mailSubject)
        mailList.append(mailTupple)
                           
    # 关闭连接
    mailServer.quit()
    
    return mailList


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


# 下载文件，支持ftp和http
def downloadFile(localPath, url):
    index = url.rfind('/')
    fileName = url[index + 1:]
    os.chdir(localPath)
    print fileName
    dataFile = urllib2.urlopen(url)
    data = dataFile.read()
    with open(localPath + fileName, "wb") as download:
        download.write(data)
    logging.info('sucess download ' + fileName)


if __name__ == '__main__':
    print receiveEmail()
    