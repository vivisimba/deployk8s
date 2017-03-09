# -*- coding: utf-8 -*-
'''
Created on 2016年4月29日

@author: Simba
'''


'''
脚本存放根目录
'''
ROOT_HOME = '/simba/fornewregitry'


'''
脚本日志存放根目录
'''
LOG_HOME = ROOT_HOME + '/logfile/'


'''
日志是否打印线程号和进程号
0:不打印
1:只打印线程号
2:只打印进程号
3：打印线程号，并且打印进程号
'''
LOG_THREAD_PROCESS = 0


# 镜像相关配置字典
IMAGE_DIC = {'registryaddress': '10.0.251.196',  # 仓库地址
             'bossdir': '/boss/',  # 仓库BOSS目录
             'platformdir': '/platform/',  # 仓库平台类镜像目录
             'commdir': '/comm/',  # 公共jar包镜像目录
             'warBasalImage1': '10.0.251.196/comm/tomcat:v8.0.33',  # WAR包基础镜像名称
             'platform-cache-config_basalimage': '10.0.251.196/comm/bossos:721511jdk8u66',  # platform-cache-config包基础镜像名称
             'registoryusername': 'admin',  # 镜像仓库用户名
             'registorypassword': 'asdf1234',  # 镜像仓库密码
             'imageemail': 'jenkins@startimes.com.cn',  # 镜像仓库登录信箱
             'numberOfImages': '44'  # 应该构建或推送的镜像数量
             }


