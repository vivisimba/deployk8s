# -*- coding: utf-8 -*-
'''
Created on 2016年4月29日

@author: Simba
'''
import os


'''
脚本存放根目录
'''
ROOT_HOME = '/simba/deployByContainer'


'''
脚本日志存放根目录
'''
LOG_HOME = ROOT_HOME + '/logfile/'


# NewBoss 脚本构建服务器,以'/'结尾
NEW_BOSS_BUILD_DBSCRIPT = "ftp://buildftp:buildftp@10.0.250.250/Stariboss-7.X/"


# 文件处理临时文件夹
tempFolder = ROOT_HOME + '/temp'


# NewBOss 数据库补丁
NEW_BOSS_DB_SCRIPT_PATCH = ROOT_HOME + '/autotest_patch/db/'


'''
DOCKER仓库
'''
DOCKERREPOSITORY = 'registry:5000/library'


# 本地TOMCAT配置文件目录,不能以'/'结尾
TOMCATSERVERDIR = ROOT_HOME + '/tomcatserverdir'


# server.xml在容器内的位置
INNER_SERVERXML_PATH = '/usr/local/tomcat/conf/server.xml'


# redis和zookeeper配置文件的相对路径，不能以'/'开始
# REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR = 'configerFile'
# 以下两个字典的键需要与250.250上的目录名称一致
REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR = {'TEST': 'TESTconfigerFile',
                                          'DAILYAUTOTEST': 'AUTOconfigerFile',
                                          'DEVELOP': 'DEVconfigerFile',
                                          'BYRC': 'BYRCconfigerfile'
                                          }

# redis和zookeeper配置文件在脚本目录中的存放位置
REDIS_AND_ZOOKEEPER_CONFIG_ABSOLUTEDIR = {'TEST': ROOT_HOME + os.sep + 'TESTconfigerFile',
                                          'DAILYAUTOTEST': ROOT_HOME + os.sep + 'AUTOconfigerFile',
                                          'DEVELOP': ROOT_HOME + os.sep + 'DEVconfigerFile',
                                          'BYRC': ROOT_HOME + os.sep + 'BYRCconfigerfile'
                                          }
# ROOT_HOME + os.sep + REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR


# 容器服务器存放redis和zookeeper配置文件的目录，需以'/'结尾
REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER = '/'


# 容器服务器存放tomcatserver文件的目录,不建议以'/'结尾
# CONTAINER_MACHINE_TOMCAT_SERVER_DIR = REDIS_AND_ZOOKEEPER_CONFIG_DIR_IN_CONTAINER + REDIS_AND_ZOOKEEPER_CONFIG_RELATIVEDIR


# 容器服务器redis的data映射目录
REDIS_MASTER_DATA = '/redis/6380'
REDIS_SLAVE_DATA = '/redis/6381'
REDIS_SENTINEL_DATA = '/redis/26379'


# 容器时区
CONTAINER_TZ = 'Asia/Shanghai'


# 需启动非平台类容器名称列表
CONTAINERLIST = ['account-center-service',
                 'account-service',
                 'area-service',
                 'collection-center-service',
                 'collection-service',
                 'customer-center-service',
                 'customer-service',
                 'order-center-service',
                 'resource-center-service',
                 'order-service',
                 'product-service',
                 'resource-service',
                 'system-service',
                 'card-center-service',
                 'card-service',
                 'channel-service',
                 'partner-service',
                 'ui'
#                  'admin-billing-ui',
#                  'admin-crm-ui',
#                  'admin-product-ui',
#                  'admin-public-ui',
#                  'customer-ui',
#                  'portal-ui'
                 ]


# 各模块映射端口配置,War模块为8080端口映射，dubbo为8090端口映射
PORT_DIC = {'platform-cache-config': '49019',
            'dubbo': '49001',
            'account-center-service': '49002',
            'account-service': '49003',
            'area-service': '49004',
            'collection-center-service': '49005',
            'collection-service': '49006',
            'customer-center-service': '49007',
            'customer-service': '49008',
            'order-center-service': '49009',
            'order-service': '49010',
            'product-service': '49011',
            'resource-service': '49012',
            'system-service': '49013',
            'admin-billing-ui': '49014',
            'admin-crm-ui': '49015',
            'admin-product-ui': '49016',
            'admin-public-ui': '49017',
            'customer-ui': '49018',
            'portal-ui': '49000',
            'api': '49020',
            'ui': '49007'
            }


# 数据库用户名列表(数据库用户名，数据库密码，数据文件名称，表空间名称)
DB_DIC = {'product-dbscript': ('productuser', 'productuser', 'tblbossproduct.dbf', 'TBLBOSSPRODUCT'),  # 产品管理用户名
          'order-dbscript': ('orderuser', 'orderuser', 'tblbossorder.dbf', 'TBLBOSSORDER'),  # 定单管理用户名
          'customer-dbscript': ('customeruser', 'customeruser', 'tblbosscustomer.dbf', 'TBLBOSSCUSTOMER'),  # 客户管理用户名
          'area-dbscript': ('areauser', 'areauser', 'tblbossarea.dbf', 'TBLBOSSAREA'),  # 区域管理用户名
          'customer-center-dbscript': ('custcenteruser', 'custcenteruser', 'tblbosscustcenter.dbf', 'TBLBOSSCUSTCENTER'),  # 客户中心管理用户名
          'system-dbscript': ('systemuser', 'systemuser', 'tblbosssystem.dbf', 'TBLBOSSSYSTEM'),  # 系统管理用户名
          'collection-dbscript': ('collectionuser', 'collectionuser', 'tblbosscollection.dbf', 'TBLBOSSCOLLECTION'),
          'collection-center-dbscript': ('collectioncenteruser', 'collectioncenteruser', 'tblbosscollectioncenter.dbf', 'TBLBOSSCOLLECTIONCENTER'),
          'account-dbscript': ('accountuser', 'accountuser', 'tblbossaccount.dbf', 'TBLBOSSACCOUNT'),
          'account-center-dbscript': ('accountcenteruser', 'accountcenteruser', 'tblbossaccountcenter.dbf', 'TBLBOSSACCOUNTCENTER'),
          'order-center-dbscript': ('ordercenteruser', 'ordercenteruser', 'tblbossordercenter.dbf', 'TBLBOSSORDERCENTER'),
          'resource-dbscript': ('resourceuser', 'resourceuser', 'tblbossresource.dbf', 'TBLBOSSRESOURCE'),
          'resource-center-dbscript': ('RESOURCECENTERUSER', 'RESOURCECENTERUSER', 'tblbossrescenter.dbf', 'TBLBOSSRESCENTER'),
          'channel-dbscript': ('CHANNELUSER', 'CHANNELUSER', 'tblbosschannel.dbf', 'TBLBOSSCHANNEL'),
          'partner-dbscript': ('PARTNERUSER', 'PARTNERUSER', 'tblbosspartner.dbf', 'TBLBOSSPARTNER'),
          'card-dbscript': ('carduser', 'carduser', 'tblbosscard.dbf', 'TBLBOSSCARD'),
          'card-center-dbscript': ('cardcenteruser', 'cardcenteruser', 'tblbosscardcenter.dbf', 'TBLBOSSCARDCENTER'),
          'job-dbscript': ('jobuser', 'jobuser', 'tblbossjob.dbf', 'TBLBOSSJOB'),
          'note-dbscript': ('noteuser', 'noteuser', 'tblbossnote.dbf', 'TBLBOSSNOTE'),
          'note-center-dbscript': ('notecenteruser', 'notecenteruser', 'tblbossnotecenter.dbf', 'TBLBOSSNOTECENTER'),
          'problem-dbscript': ('problemuser', 'problemuser', 'tblbossproblem.dbf', 'TBLBOSSPROBLEM'),
          'problem-center-dbscript': ('problemcenteruser', 'problemcenteruser', 'tblbossproblemcenter.dbf', 'TBLBOSSPROBLEMCENTER'),
          'message-center-dbscript': ('messagecenteruser', 'messagecenteruser', 'tblbossmessagecenter.dbf', 'TBLBOSSMESSAGECENTER'),
          'knowledge-dbscript': ('knowledgeuser', 'knowledgeuser', 'tblbossknowledge.dbf', 'TBLBOSSKNOWLEDGE'),
          'check-dbscript': ('checkuser', 'checkuser', 'tblbosscheck.dbf', 'TBLBOSSCHECK'),
          'iom-center-dbscript': ('iomcenteruser', 'iomcenteruser', 'tblbossiomcenter.dbf', 'TBLBOSSIOMCENTER'),
          'iom-dbscript': ('iomuser', 'iomuser', 'tblbossiom.dbf', 'TBLBOSSIOM'),
          'pms-center-dbscript': ('pmscenteruser', 'pmscenteruser', 'tblbosspmscenter.dbf', 'TBLBOSSPMSCENTER'),
          'pms-partition-dbscript': ('pmspartitionuser', 'pmspartitionuser', 'tblbosspmspartition.dbf', 'TBLBOSSPMSPARTITION')
          }


'''
================================================虚拟机信息==========================================
'''
VM_DIC = {'vcenter_ip': '10.0.250.50',
          'vcenter_password': 'qwer1234',
          'vcenter_user': 'root',
          'vm_name': 'DB-checkin-162',
          'operation': 'list_all',
          'snapshot_name': 'snap1',
          'ignore_ssl': True
          }
'''
================================================NewBoss测试环境======================================
'''


# 手工测试环境
MANAUL_ENV_DIC = {'DICNAME': 'MANAUL',
                  'MACHINE_LIST': ['10.0.251.207', '10.0.251.202', '10.0.251.206', '10.0.251.203'],  # 测试环境设备资源ip列表
                  'NEW_BOSS_DB_IP': '10.0.250.169',  # 测试数据库IP
                  'NEW_BOSS_DB_VMNAME': 'DB-250.169',  # 测试数据库虚拟机名称
                  'NEW_BOSS_DB_SNAPSHOTNAME': 'NewBoss-1000',  # 自动化测试数据库快照名
                  'NEW_BOSS_DB_LOCALNAME': 'newboss_250_169',  # 测试数据库本地服务名
                  'NEW_BOSS_DB_SYSTEM_PWD': '123456',  # 数据库的sytem用户密码
                  'NEW_BOSS_DB_DATA_FILE_DIR': '/oracle/oradata/orcl/',  # 数据库的data_file路径
                  'DB_LISTNAME': DB_DIC,  # 数据库用户名列表
                  # 'DB_PWD_LISTNAME': DB_PWD_LIST,  # 数据库密码列表
                  'NEW_BOSS_VMWARE_IP': '10.0.250.50',  # 虚拟机服务器IP，vmware ESXi服务器信息
                  'NEW_BOSS_VMWARE_USERNAME': 'root',  # 虚拟机服务器用户名，vmware ESXi服务器信息
                  'NEW_BOSS_VMWARE_PASSWORD': 'qwer1234',  # 虚拟机服务器密码，vmware ESXi服务器信息
                  'NEW_BOSS_FTPDIR': "TEST/"  # 下载数据库脚本时拼接FTP目录时使用
                  }


# 自动化环境
AUTO_ENV_DIC = {'DICNAME': 'AUTO',
                'MACHINE_LIST': ['10.0.251.214', '10.0.251.215', '10.0.251.216'],  # 测试环境设备资源ip列表
                'NEW_BOSS_DB_IP': '10.0.250.126',  # 测试数据库IP
                'NEW_BOSS_DB_VMNAME': 'Docker-AUTO-DB-126',  # 测试数据库虚拟机名称
                'NEW_BOSS_DB_SNAPSHOTNAME': '20160620',  # 测试数据库快照名
                'NEW_BOSS_DB_LOCALNAME': 'newboss_126',  # 测试数据库本地服务名
                'NEW_BOSS_DB_SYSTEM_PWD': '123456',  # 数据库的sytem用户密码
                'NEW_BOSS_DB_DATA_FILE_DIR': '/oracle/oradata/orcl/',  # 数据库的data_file路径
                'DB_LISTNAME': DB_DIC,
                'NEW_BOSS_VMWARE_IP': '10.0.250.50',  # 虚拟机服务器IP，vmware ESXi服务器信息
                'NEW_BOSS_VMWARE_USERNAME': 'root',  # 虚拟机服务器用户名，vmware ESXi服务器信息
                'NEW_BOSS_VMWARE_PASSWORD': 'qwer1234',  # 虚拟机服务器密码，vmware ESXi服务器信息
                'NEW_BOSS_FTPDIR': "DAILYAUTOTEST/"  # 下载数据库脚本时拼接FTP目录时使用
                }


'''
NewBoss 研发环境
'''
DEV_ENV_DIC = {'DICNAME': 'DEV',
               'MACHINE_LIST': ['10.0.251.217', '10.0.251.218', '10.0.251.208', '10.0.251.219'],  # 测试环境设备资源ip列表
               'NEW_BOSS_DB_IP': '10.0.250.146',  # 测试数据库IP
               'NEW_BOSS_DB_VMNAME': 'Docker-DEV-DB-146',  # 测试数据库虚拟机名称
               'NEW_BOSS_DB_SNAPSHOTNAME': 'inital',  # 测试数据库快照名
               'NEW_BOSS_DB_LOCALNAME': 'newboss_250_146',  # 测试数据库本地服务名
               'NEW_BOSS_DB_SYSTEM_PWD': '123456',  # 数据库的sytem用户密码
               'NEW_BOSS_DB_DATA_FILE_DIR': '/oracle/oradata/orcl/',  # 数据库的data_file路径
               'DB_LISTNAME': DB_DIC,  # 数据库用户名列表
               'NEW_BOSS_VMWARE_IP': '10.0.250.50',  # 虚拟机服务器IP，vmware ESXi服务器信息
               'NEW_BOSS_VMWARE_USERNAME': 'root',  # 虚拟机服务器用户名，vmware ESXi服务器信息
               'NEW_BOSS_VMWARE_PASSWORD': 'qwer1234',  # 虚拟机服务器密码，vmware ESXi服务器信息
               'NEW_BOSS_FTPDIR': "DEVELOP/"  # 下载数据库脚本时拼接FTP目录时使用
               }


BYRC_ENV_DIC = {'DICNAME': 'BYRC',
                'MACHINE_LIST': ['10.0.251.214', '10.0.251.215', '10.0.251.216', '10.0.251.209'],  # 测试环境设备资源ip列表
                'NEW_BOSS_DB_IP': '10.0.250.110',  # 测试数据库IP
                'NEW_BOSS_DB_VMNAME': 'NewBossDB-110',  # 测试数据库虚拟机名称
                'NEW_BOSS_DB_SNAPSHOTNAME': 'NewBoss-1000',  # 自动化测试数据库快照名
                'NEW_BOSS_DB_LOCALNAME': 'newboss_110',  # 测试数据库在72的本地服务名
                'NEW_BOSS_DB_SYSTEM_PWD': '123456',  # 数据库的sytem用户密码
                'NEW_BOSS_DB_DATA_FILE_DIR': '/oracle/oradata/orcl/',  # 数据库的data_file路径
                'DB_LISTNAME': DB_DIC,  # 数据库用户名列表
                # 'DB_PWD_LISTNAME': DB_PWD_LIST,  # 数据库密码列表
                'NEW_BOSS_VMWARE_IP': '10.0.250.50',  # 虚拟机服务器IP，vmware ESXi服务器信息
                'NEW_BOSS_VMWARE_USERNAME': 'root',  # 虚拟机服务器用户名，vmware ESXi服务器信息
                'NEW_BOSS_VMWARE_PASSWORD': 'qwer1234',  # 虚拟机服务器密码，vmware ESXi服务器信息
                'NEW_BOSS_FTPDIR': "TEST/"  # 下载数据库脚本时拼接FTP目录时使用
                }


CHECKIN_ENV_DIC = {'DICNAME': 'MANAUL',
                   'MACHINE_LIST': ['10.0.251.207', '10.0.251.202', '10.0.251.206', '10.0.251.203'],  # 测试环境设备资源ip列表
                   'NEW_BOSS_DB_IP': '10.0.250.162',  # 测试数据库IP
                   'NEW_BOSS_DB_VMNAME': 'DB-checkin-162',  # 测试数据库虚拟机名称
                   'NEW_BOSS_DB_SNAPSHOTNAME': 'NewBoss-1000',  # 自动化测试数据库快照名
                   'NEW_BOSS_DB_LOCALNAME': 'newboss_162',  # 测试数据库本地服务名
                   'NEW_BOSS_DB_SYSTEM_PWD': '123456',  # 数据库的sytem用户密码
                   'NEW_BOSS_DB_DATA_FILE_DIR': '/oracle/oradata/orcl/',  # 数据库的data_file路径
                   'DB_LISTNAME': DB_DIC,  # 数据库用户名列表
                   # 'DB_PWD_LISTNAME': DB_PWD_LIST,  # 数据库密码列表
                   'NEW_BOSS_VMWARE_IP': '10.0.250.50',  # 虚拟机服务器IP，vmware ESXi服务器信息
                   'NEW_BOSS_VMWARE_USERNAME': 'root',  # 虚拟机服务器用户名，vmware ESXi服务器信息
                   'NEW_BOSS_VMWARE_PASSWORD': 'qwer1234',  # 虚拟机服务器密码，vmware ESXi服务器信息
                   'NEW_BOSS_FTPDIR': "TEST/"  # 下载数据库脚本时拼接FTP目录时使用
                   }
