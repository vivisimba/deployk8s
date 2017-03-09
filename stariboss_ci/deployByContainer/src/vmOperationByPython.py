# -*- coding: utf-8 -*-
'''
Created on 2016年12月23日

@author: Simba
'''


import vmManagerByPython


def snapshotManager(ip, username, password, operation, vmname, snapshotName=None):
    '''
    
    :param ip:
    :param username:
    :param password:
    :param vmname:
    :param operation: support '<list_all> | <list_current> | <create> | <revert> | <remove>' | <remove_all> | <power_on> '
    :param snapshotName:
    :param newSnapshotName: Required if operation is <rename>, otherwise set to ''
    :NOTICE: "create" snapshot DO NOT include memory dump.
    '''
    inputs = {'vcenter_ip': ip,
              'vcenter_password': password,
              'vcenter_user': username,
              'vm_name': vmname,
              'operation': operation,
              'snapshot_name': snapshotName,
              'ignore_ssl': True
              }
    res = vmManagerByPython.main(inputs)
    return res

