# -*- coding: utf-8 -*-
'''
Created on 2016年4月29日

@author: Simba
'''
import os


# 脚本存放根目录
ROOT_HOME = '/simba/src'


# 脚本日志存放根目录
LOG_HOME = ROOT_HOME + '/logfile/'


# masterIP
MASTERIP = ['10.0.251.165']


# 节点列表
NODEMACHINE = ['10.0.251.215',
               '10.0.251.216',
               '10.0.251.220',
               ]

# 命名空间
NAME_SPACE = 'nanqb165'


# sentinel_name
sentinel_name = 'masterk8s165'


# RC原始文件存放目录
RCDIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'rc_yaml' + os.sep

# deployment原始文件存放目录
DPMDIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'deployments' + os.sep
# SVC原始文件存放目录
SVCDIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'svc_yaml' + os.sep


# 实际使用的RC文件目录
TEMP_RCDIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'temp_rc_yaml' + os.sep


# 实际使用的deployment文件目录
TEMP_DPMDIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'temp_dpm_yaml' + os.sep
# 实际使用的SVC文件目录
TEMP_SVCDIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'temp_svc_yaml' + os.sep
# 镜像标签占位符`
TAG_OCCUPY = "{IMAGE_TAG}"
# dubbo_host占位符
DUBBO_HOST = "{DUBBO_HOST}"
# 宿主机NFS目录 ！！！！！！！！！！！！需要作为NFS服务器的master节点的NFS目录，与作为客户端的各个节点的挂载的目录，路径一致！！！！！！！！！！！！
# master和node都需要具有NFS_HOST_DIR目录
NFS_HOST_DIR = "/home/nfs"
# 容器内NFS目录,该路径需要与zookeeper中的nfs_server_dir目录一致
NFS_CONTAINER_DIR = "/home/nfs"


# SVC文件存放目录
SVCDIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'svc_yaml' + os.sep


# replace_rc文件存放目录
REPLACE_RC_DIR = ROOT_HOME + os.sep + 'execpy' + os.sep + 'replace_rc_yaml' + os.sep


# 更新镜像排除的RC列表
EXCLUDE_RC_LIST = ['pushzkconfig',
                   'zookeeper',
                   'redisslave',
                   'redismaster',
                   'redissentinel',
                   'zkdash',
                   'platform-cache-config',
                   'dubbomonitor']


# 文件前缀列表
RC_SVC_PREFIX = ['zookeeper',
                 'pushzkconfig',
#                 'redismaster',
#                 'redisslave',
#                 'redissentinel',
                 'platform-cache-config',
                 'zkdash',
                 'zookeeperui',
                 'account-center-service',
                 'activiti-rest',
                 'account-service',
                 'area-service',
                 'card-center-service',
                 'card-service',
                 'channel-service',
                 'check-service',
                 'collection-center-service',
                 'collection-service',
                 'customer-center-service',
                 'customer-service',
                 'iom-center-service',
                 'iom-service',
                 'job-service',
                 'knowledge-service',
                 'message-center-service',
                 'note-center-service',
                 'note-service',
                 'order-center-service',
                 'order-service',
                 'partner-service',
                 'pms-center-service',
                 'pms-partition-service',
                 'problem-center-service',
                 'problem-service',
                 'product-service',
                 'resource-center-service',
                 'resource-service',
                 'system-service',
                 'stariboss-callcenter_proxy',
                 'pms-frontend-conax-service',
                 'admin-billing-ui',
                 'admin-crm-ui',
                 'admin-oss-ui',
                 'admin-product-ui',
                 'admin-public-ui',
                 'customer-ui',
                 'knowledge-ui',
                 'operator-ui',
                 'partner-ui',
                 'portal-ui',
                 'resource-ui',
                 'worker-ui',
                 'mysql',
#                 'swagger-validator',
#                 'swagger-ui',
                 'dubbomonitor',
                 'api',
                 'order-job',
                 'stariboss-haiwai_proxy'
                 ]


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


# 数据库环境信息
DB_ENV_DIC = {'DICNAME': 'MANAUL',  # 区分自动化环境使用
              'NEW_BOSS_DB_IP': '10.0.250.165',  # 数据库IP
              'NEW_BOSS_DB_VMNAME': 'DB-250.169-hourl',  # 数据库虚拟机名称
              'NEW_BOSS_DB_SNAPSHOTNAME': 'NewBoss-1000',  # 自动化测试数据库快照名
              'NEW_BOSS_DB_LOCALNAME': 'newboss_250_165',  # 数据库本地服务名
              'NEW_BOSS_DB_SERVICE_NAME': 'starboss',  # 数据库servicename
              'NEW_BOSS_DB_SYSTEM_PWD': '123456',  # 数据库的sytem用户密码
              'NEW_BOSS_DB_DATA_FILE_DIR': '/oracle/oradata/orcl/',  # 数据库的data_file路径
              'DB_LISTNAME': DB_DIC,  # 数据库用户名列表
              'NEW_BOSS_VMWARE_IP': '10.0.250.50',  # 虚拟机服务器IP，vmware ESXi服务器信息
              'NEW_BOSS_VMWARE_USERNAME': 'root',  # 虚拟机服务器用户名，vmware ESXi服务器信息
              'NEW_BOSS_VMWARE_PASSWORD': 'qwer1234',  # 虚拟机服务器密码，vmware ESXi服务器信息
              'NEW_BOSS_FTPDIR': "RC1/",  # 下载数据库脚本时拼接FTP目录时使用
              'tempFolder': ROOT_HOME + '/temp',  # 存放下载的数据库脚本的目录
              'NEW_BOSS_BUILD_DBSCRIPT': "ftp://buildftp:buildftp@10.0.250.250/stariboss-10.X/",
              'NEW_BOSS_DB_SCRIPT_PATCH': ROOT_HOME + '/autotest_patch/db/'  # NewBOss 数据库补丁
              }



