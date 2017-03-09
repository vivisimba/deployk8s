# -*- coding: utf-8 -*-
'''
Created on 2016年4月29日

@author: Simba
'''
import log.logService as logService
import sys
import os
import config.config as CONFIG
import myException
import logging
import subprocess
import zipfile
import threading
import multiprocessing
# from test import imagesList


# 获得指定目录下的，指定后缀名的文件名列表
def getWarNameList(warDir, suffix):
    warNameList = []
    tempList = os.listdir(warDir)
    for i in tempList:
        tempFileName = warDir + os.sep + i
        if os.path.isfile(tempFileName) & tempFileName.endswith(suffix):
            warNameList.append(i)
    return warNameList


# 获得去掉war包列表中“.war”后缀的列表，返回war包名称列表
def getRealWarNameList(warNameList):
    realWarNameList = []
    for i in warNameList:
        realWarNameList.append(os.path.splitext(i)[0])
    return realWarNameList


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


# 生成各模块dockerfile文件，返回dockerfile列表
def createDockerfile(warDir, realWarNameList):
    serviceAndUiList = []
    for i in realWarNameList:
        if 'platform-cache-config' in i:
            logging.info("Create dockerfile for zipfile:%s" % 'platform-cache-config')
            wholeFileName = warDir + os.sep + 'platform-cache-config' + ".Dockerfile"
            # 解压缓存zip包
            unzipFile(warDir + os.sep + i + ".zip", warDir)
            f = open(wholeFileName, 'w')
            f.write("FROM %s\n" % CONFIG.IMAGE_DIC['platform-cache-config_basalimage'])
            f.write('ENV JAVA_HOME /usr/local/jdk\n')
            f.write("ADD ./platform-cache-config /usr/local/platform-cache-config\n")
            f.write("RUN chmod 777 /usr/local/platform-cache-config/bin/platform-cache-config\n")
            f.write('WORKDIR /usr/local/platform-cache-config/bin/\n')
            f.write('CMD ["/usr/local/platform-cache-config/bin/platform-cache-config"]')
            f.close()
        else:  # 创建ui和service以及api.war的dockerfile
            logging.info("Create dockerfile for warfile:%s" % i)
            wholeFileName = warDir + os.sep + i + ".Dockerfile"
            f = open(wholeFileName, 'w')
            f.write("FROM %s\n" % CONFIG.IMAGE_DIC['warBasalImage1'])
            f.write("ADD ./%s /usr/local/tomcat/webapps/\n" % (i + ".war"))
            f.close()
            serviceAndUiList.append(i)
    # 将serviceList中获得的servicewar包名称，写入文件，该文件为部署提供依据
    logging.info("Create servicewarlistfile")
    serviceWarListFileDir = warDir + os.sep + "serviceWarListFile"
    serviceWarListFile = open(serviceWarListFileDir, 'w')
    for serviceWarName in serviceAndUiList:
        serviceWarListFile.write(serviceWarName + '\n')
    serviceWarListFile.close()
    fileList = getWarNameList(warDir, 'Dockerfile')
    return fileList


# 查看本机镜像中是否存在指定镜像,如果存在，返回true
def ifImageExist(imageNameAndTag):
    logging.info("sudo docker images")
    resList = os.popen("sudo docker images").readlines()
    boolFlag = False
    for i in resList:
        t = i.split()
        localImageStr = t[0] + ":" + t[1]
        if imageNameAndTag in localImageStr:
            boolFlag = True
    return boolFlag


# 登录镜像仓库
def logInImageRegistory(userName, password):
    rightStr = 'sudo docker login -u %s  -p %s -e %s %s' % (CONFIG.IMAGE_DIC['registoryusername'],
                                                            CONFIG.IMAGE_DIC['registorypassword'],
                                                            CONFIG.IMAGE_DIC['imageemail'],
                                                            CONFIG.IMAGE_DIC['registryaddress']
                                                            )
    logging.info("exec: %s" % rightStr)
    p = subprocess.Popen(rightStr, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    resList = p.stdout.readlines()
    if len(resList) != 0:
        for i in resList:
            logging.info("%s" % i.strip())
    else:
        errStrList = p.stderr.readlines()
        errStrStripList = []
        for j in errStrList:
            errStrStripList.append(j.strip())
        errStr = ','.join(errStrStripList)
        raise myException.MyException("%s" % errStr)


# 如果目录存在则返回True，如果目录不存在则创建目录，然后返回True
def createDir(absolutePath):
    if not os.path.exists(absolutePath):
        os.makedirs(absolutePath)
    return True


# 根据dockerfile生成新的镜像
def createNewImage(fileDir, dockerfile, newTag, errImagesSet, buildLogAbsolutePath):
    warName = os.path.splitext(dockerfile)[0]
    logging.info("Create new image according to %s" % dockerfile)
    imageName = CONFIG.IMAGE_DIC['registryaddress'] + CONFIG.IMAGE_DIC['bossdir'] + warName + ':' + newTag
    rightStr = "docker build -t %s -f %s %s" % (imageName, fileDir + os.sep + dockerfile, fileDir)
    actualStr = "docker build -t %s -f %s %s 2>&1 |grep -v 'Sending build context to Docker daemon' > %s/build_%s_image.log" % (imageName, fileDir + os.sep + dockerfile, fileDir, buildLogAbsolutePath, warName)
    logging.info(rightStr)
    p = subprocess.Popen(actualStr, shell=True)
    p.wait()
    f = open((buildLogAbsolutePath + ('/build_%s_image.log' % warName)), 'r')
    lineList = f.readlines()
    f.close()
    boolFlag = False
    for line in lineList:
        if 'Successfully built' in line:
            boolFlag = True
    if boolFlag is True:
        for outLine in lineList:
            logging.info(outLine.strip())
        logging.info("Create image: %s:%s successfully." % ((CONFIG.IMAGE_DIC['registryaddress'] + CONFIG.IMAGE_DIC['bossdir'] + warName), newTag))
    else:
        for errLine in lineList:
            logging.error(errLine.strip())
        errImagesSet.add(warName)
    logging.info("")
        

# 多线程构建镜像
def createNewImagesByThreads(fileDir, dockerfileList, newTag):
    for i in dockerfileList:
        createNewImage(fileDir, i, newTag)
        t = threading.Thread(target=createNewImage, args=(fileDir, i, newTag))
        t.start()
    t.join()


# 使用进程池多进程构建镜像
def createNewImagesByProcesses(fileDir, dockerfileList, newTag, errImagesSet):
    pool = multiprocessing.Pool(processes=4)
    for i in dockerfileList:
        pool.apply_async(createNewImage, (fileDir, i, newTag, errImagesSet))
    pool.close()
    pool.join()


# 取消使用多线程或者多进程，创建镜像
def createNewImagesNoProcessAndNoSession(fileDir, dockerfileList, newTag, errImagesSet, buildLogAbsolutePath):
    createdFlag = 0
    for i in dockerfileList:
        createdFlag += 1
        logging.info("Create image : %s/%s" % (createdFlag, len(dockerfileList)))
        createNewImage(fileDir, i, newTag, errImagesSet, buildLogAbsolutePath)


# 拉取镜像
def pullNewImage(imageNameWithTag):
    p = subprocess.Popen("sudo docker pull %s" % (imageNameWithTag), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    res = p.stderr.readlines()
    if res:
        logging.info('Pull image failure,please check it')
        raise myException.MyException('Pull image failure,please check it')
    else:
        return True

            
# 推送镜像到仓库
def pushImageToRepository(warImageName, tagName, repositoryName, pushedSuccessSet, pushedErrSet):
    imageName = repositoryName + warImageName
    logging.info("Push %s to %s" % (imageName, repositoryName))
    logging.info("Command:sudo docker push %s:%s " % (imageName, tagName))
    rightStr = "sudo docker push %s:%s" % (imageName, tagName)
    p = subprocess.Popen(rightStr, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    resTup = p.communicate()
    outStr = resTup[0]
    errStr = resTup[1]
    if len(errStr) == 0:
        outList = outStr.split('\n')
        for i in outList:
            if i != '':
                logging.info(i)
        logging.info("%s pushed successfully." % (imageName + ':' + tagName))
        pushedSuccessSet.add(warImageName)
    else:
        errList = errStr.split('\n')
        for j in errList:
            logging.error(j)
    logging.info('')


# # 多线程推送镜像到仓库
# def pushImagesToRegistryByThreads(warImageList, tagName, pushedSuccessSet, pushedErrSet):
#     for warImageName in warImageList:
#         t = threading.Thread(target=pushImageToRepository, args=(warImageName, tagName, (CONFIG.IMAGE_DIC['registryaddress'] + CONFIG.IMAGE_DIC['bossdir']), pushedSuccessSet, pushedErrSet))
#         t.start()
#     t.join()
#     logging.info("Images publishing for tag:%s have done" % tagName)
    

# 删除指定目录下指定后缀的文件
def delSuffixFile(fileDir, suffix):
    temList = os.listdir(fileDir)
    for i in temList:
        tempFileName = fileDir + os.sep + i
        if os.path.isfile(tempFileName) & tempFileName.endswith(suffix):
            os.system("rm -f %s" % tempFileName)
            logging.info("Delete file:%s" % tempFileName)


# 查看指定仓库中的所有镜像,返回查询到的镜像名称列表
def searchImagesOfRepository(repository):
    p = subprocess.Popen("sudo docker search %s" % repository, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    if not p.stderr.readlines():
        outStr = p.stdout.readlines()
        tempList = outStr[1:]
        imagesNameList = []
        for i in tempList:
            j = i.split()
            imagesNameList.append(j[1])
        return imagesNameList
    else:
        outStr = p.stderr.readlines()
        for t in outStr:
            logging.info(t)


# 查看指定仓库中指定镜像的所有tag号,参数为完整镜像名称，例如：registry:5000/library/account-center-service
def searchTagOfImage(imageWholeName):
    repositoryStr = imageWholeName[0:imageWholeName.find('/')]
    dirStr = imageWholeName[imageWholeName.find('/'):]
    # logging.info("Search tags of %s in %s" % (imageWholeName, repositoryStr))
    # logging.info("curl %s/v1/repositories%s/tags" % (repositoryStr, dirStr))
    p = subprocess.Popen("curl %s/v1/repositories%s/tags" % (repositoryStr, dirStr), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    outStr = p.stdout.readlines()
    tagDic = eval(outStr[0])
    tagList = tagDic.keys()
    return tagList


# 删除本地镜像
def delAllLocalImages():
    cmdImages = 'sudo docker images'
    p = subprocess.Popen(cmdImages, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    imagesListTmp = p.stdout.readlines()
    imagesListTemp = imagesListTmp[1:]
    imagesDic = {}
    for s in imagesListTemp:
        singleList = s.split()
        imagesDic[singleList[2]] = singleList[0] + ':' + singleList[1]
    keyList = imagesDic.keys()
    
    for key in keyList:
        cmd = 'docker rmi %s' % imagesDic[key]
        m = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        errList = m.stderr.readlines()
        if len(errList) > 0:
            logging.info('Delete the image: %s ERROR' % imagesDic[key])
            for i in errList:
                logging.info(i)
            raise myException.MyException('Delete the image: %s' % imagesDic[key])
        else:
            logging.info('Delete the image: %s successfully' % imagesDic[key])
    searchImagesCmd = 'docker images -q'
    res = subprocess.Popen(searchImagesCmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    resList = res.stdout.readlines()
    if len(resList) == 0:
        logging.info("All images have been delete successful.")
    else:
        raise myException.MyException("Some images can't been delete,please check it.")
    
    
# 运行任务
def run():
    # 获得传入参数
    # 传入参数[, war包目录, 构建tag号]
    parameterList = sys.argv
    # 登录镜像仓库
    logInImageRegistory(CONFIG.IMAGE_DIC['registoryusername'], CONFIG.IMAGE_DIC['registorypassword'])
    # 查看本地是否存在war包基础镜像
    if not ifImageExist(CONFIG.IMAGE_DIC['warBasalImage1']):
        # 如果本地不存在基础镜像，从仓库pull基础镜像
        logging.info("Don't exists the image %s" % (CONFIG.IMAGE_DIC['warBasalImage1']))
        logging.info("Now start to get %s from %s" % (CONFIG.IMAGE_DIC['warBasalImage1'], CONFIG.IMAGE_DIC['registryaddress'] + CONFIG.IMAGE_DIC['commdir']))
        pullNewImage(CONFIG.IMAGE_DIC['warBasalImage1'])
        logging.info("Get the image from %s successfully" % (CONFIG.IMAGE_DIC['registryaddress'] + CONFIG.IMAGE_DIC['commdir']))
    # 获得war包真实名称列表
    realWarNameList = getRealWarNameList(getWarNameList(parameterList[1], '.war'))
    # 增加列表
    realWarNameList.append('platform-cache-config')
    # 获得列表长度，该长度即应该构建的镜像数量和应该上传的镜像数量
    numberOfImages = len(realWarNameList)
    docfileNeedCreateList = realWarNameList[:]
    logging.info("Start to create dockerfiles")
    # 查找并删除war目录下的"Dockerfile"结尾的文件
    delSuffixFile(parameterList[1], '.Dockerfile')
    # 生成新的dockerfile
    dockerfileList = createDockerfile(parameterList[1], docfileNeedCreateList)
    logging.info("Create dockerfiles finished")
    # 创建存放构建镜像日志的目录
    buildLogAbsolutePath = CONFIG.LOG_HOME + parameterList[2] + '_buildimages_log'
    createDir(buildLogAbsolutePath)
    errImagesSet = set()
    # 根据dockerfile生成新的镜像
    createNewImagesNoProcessAndNoSession(parameterList[1], dockerfileList, parameterList[2], errImagesSet, buildLogAbsolutePath)
    if len(errImagesSet) != 0:
        for errImage in errImagesSet:
            logging.error("%s was created failed!" % errImage)
        raise myException.MyException("Some images were created failed!")
    print "+++++++++++++++++++++++++++++++++++"
    # 推送新生成的镜像到私有仓库
    realDocList = getRealWarNameList(getWarNameList(parameterList[1], '.Dockerfile'))
    # 多线程推送
    # 创建集合，用于记录成功推送的镜像
    pushedSuccessSed = set()
    # 创建集合，用于记录推送失败的镜像
    pushedErrSet = set()
    pushedCount = 0
    for realDoc in realDocList:
        pushedCount += 1
        logging.info("Push image : %s/%s" % (pushedCount, len(realDocList)))
        pushImageToRepository(realDoc, parameterList[2], (CONFIG.IMAGE_DIC['registryaddress'] + CONFIG.IMAGE_DIC['bossdir']), pushedSuccessSed, pushedErrSet)
    if len(pushedSuccessSed) == numberOfImages:
        logging.info("Images of all warfile have been pushed successfully.")
        delAllLocalImages()
    else:
        logging.error("The number of pushed images is not equal to the number of should be pushed.")
        logging.info("Images pushed failed are:")
        for failedPushedImage in pushedErrSet:
            wholeImageName = CONFIG.IMAGE_DIC['registryaddress'] + CONFIG.IMAGE_DIC['bossdir'] + failedPushedImage + ':' + parameterList[2]
            logging.info(wholeImageName)
            
            
#     # 判断新生成的镜像是否存在于仓库中
#     warCount = len(realDocList)
#     imageCountInRepository = 0
#     for imageNameInRepository in realDocList:
#         imageWholeName = CONFIG.DOCKERREPOSITORY + '/' + imageNameInRepository
#         if imageWholeName in searchImagesOfRepository(CONFIG.DOCKERREPOSITORY):
#             if parameterList[2] in searchTagOfImage(imageWholeName):
#                 logging.info("Pushing %s:%s to %s has been successful" % (imageWholeName, parameterList[2], CONFIG.DOCKERREPOSITORY))
#                 imageCountInRepository = imageCountInRepository + 1
#             else:
#                 logging.info('%s:%s pushed failure' % (imageWholeName, parameterList[2]))
#     if imageCountInRepository == warCount:
#         logging.info("Images of all warfile have been pushed successfully")
#     else:
#         logging.info("Some errors happened in pushing, please check it.")
#     # 使用字典保存仓库中镜像信息：key为镜像名称，value为该镜像的所有tag的列表
#     imageDic = {}
#     # 查看仓库中所有镜像
#     finalImagesList = searchImagesOfRepository(CONFIG.DOCKERREPOSITORY)
#     for imageNameInRepository in finalImagesList:
#         imageShortName = imageNameInRepository[imageNameInRepository.rfind('/') + 1:]
#         imageDic[imageShortName] = searchTagOfImage(imageNameInRepository)
#     # 打印所有war包的tags
#     logging.info("Print all images with tags in %s" % CONFIG.DOCKERREPOSITORY)
#     imageNum = 1
#     for t in imageDic.keys():
#         logging.info('%s: Tags of %s:\n' % (str(imageNum), t))
#         tagsList = imageDic[t]
#         for tag in tagsList:
#             logging.info('  %s\n' % tag)
#         imageNum = imageNum + 1

        
if __name__ == '__main__':
    logService.initLogging()
    run()
    logService.destoryLogging()
    