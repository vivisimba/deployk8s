# -*- coding: utf-8 -*-
'''
Created on 2016年12月19日

@author: Simba
'''


import atexit
import argparse
import sys
import time
import ssl
from pyVmomi import vim, vmodl
from pyVim.task import WaitForTask
from pyVim import connect
from pyVim.connect import Disconnect, SmartConnect, GetSi
import config.config as CONFIG
import exception.myException as myexception


def get_obj(content, vimtype, name):
    """
     Get the vsphere object associated with a given text name
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if c.name == name:
            obj = c
            break
    return obj


def list_snapshots_recursively(snapshots):
    snapshot_data = []
    snap_text = ""
    for snapshot in snapshots:
        snap_text = "Name: %s; Description: %s; CreateTime: %s; State: %s" % (snapshot.name,
                                                                              snapshot.description,
                                                                              snapshot.createTime,
                                                                              snapshot.state)
        snapshot_data.append(snap_text)
        snapshot_data = snapshot_data + list_snapshots_recursively(snapshot.childSnapshotList)
    return snapshot_data


def get_snapshots_by_name_recursively(snapshots, snapname):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.name == snapname:
            snap_obj.append(snapshot)
        else:
            snap_obj = snap_obj + get_snapshots_by_name_recursively(snapshot.childSnapshotList, snapname)
    return snap_obj


def get_current_snap_obj(snapshots, snapob):
    snap_obj = []
    for snapshot in snapshots:
        if snapshot.snapshot == snapob:
            snap_obj.append(snapshot)
        snap_obj = snap_obj + get_current_snap_obj(snapshot.childSnapshotList, snapob)
    return snap_obj


def main(inputs):

    si = None

    print("Trying to connect to VCENTER SERVER . . .")

    context = None
    if inputs['ignore_ssl'] and hasattr(ssl, "_create_unverified_context"):
        context = ssl._create_unverified_context()

    si = connect.Connect(inputs['vcenter_ip'], 443,
                         inputs['vcenter_user'],
                         inputs['vcenter_password'],
                         sslContext=context)

    atexit.register(Disconnect, si)

    print("Connected to VCENTER SERVER !")

    content = si.RetrieveContent()

    operation = inputs['operation']
    vm_name = inputs['vm_name']

    vm = get_obj(content, [vim.VirtualMachine], vm_name)

    if not vm:
        print("Virtual Machine %s doesn't exists" % vm_name)
        raise myexception.MyException("Virtual Machine %s doesn't exists" % vm_name)

    if operation != 'create' and vm.snapshot is None:
        print("Virtual Machine %s doesn't have any snapshots" % vm.name)
        raise myexception.MyException("Virtual Machine %s doesn't have any snapshots" % vm.name)

    if operation == 'create':
        snapshot_name = inputs['snapshot_name']
        description = "Test snapshot"
        dumpMemory = False
        quiesce = False

        print("Creating snapshot %s for virtual machine %s" % (snapshot_name, vm.name))
        WaitForTask(vm.CreateSnapshot(snapshot_name, description, dumpMemory, quiesce))
        return 'ok'

    elif operation in ['remove', 'revert']:
        snapshot_name = inputs['snapshot_name']
        snap_obj = get_snapshots_by_name_recursively(vm.snapshot.rootSnapshotList, snapshot_name)
        # if len(snap_obj) is 0; then no snapshots with specified name
        if len(snap_obj) == 1:
            snap_obj = snap_obj[0].snapshot
            if operation == 'remove':
                print("Removing snapshot %s" % snapshot_name)
                WaitForTask(snap_obj.RemoveSnapshot_Task(True))
                return 'ok'
            else:
                print("Reverting to snapshot %s" % snapshot_name)
                WaitForTask(snap_obj.RevertToSnapshot_Task())
                return 'ok'
        else:
            print("No snapshots found with name: %s on VM: %s" % (snapshot_name, vm.name))
            raise myexception.MyException("No snapshots found with name: %s on VM: %s" % (snapshot_name, vm.name))

    elif operation == 'list_all':
        print("Display list of snapshots on virtual machine %s" % vm.name)
        snapshot_paths = list_snapshots_recursively(vm.snapshot.rootSnapshotList)
        print type(snapshot_paths)
#         for snapshot in snapshot_paths:
#             print(snapshot)
        return snapshot_paths

    elif operation == 'list_current':
        current_snapref = vm.snapshot.currentSnapshot
        current_snap_obj = get_current_snap_obj(vm.snapshot.rootSnapshotList, current_snapref)
        current_snapshot = "Name: %s; Description: %s; " \
                           "CreateTime: %s; State: %s" % (current_snap_obj[0].name,
                                                          current_snap_obj[0].description,
                                                          current_snap_obj[0].createTime,
                                                          current_snap_obj[0].state)
        print("Virtual machine %s current snapshot is:" % vm.name)
        print(current_snapshot)
        return 'ok'

    elif operation == 'remove_all':
        print("Removing all snapshots for virtual machine %s" % vm.name)
        WaitForTask(vm.RemoveAllSnapshots())
        return 'ok'

    elif operation == 'power_on':
        if vm.runtime.powerState == vim.VirtualMachinePowerState.poweredOn:
            print("The state of virtual machine %s is already power_on, need do nothing" % vm.name)
            return 'ok'
        else:
            vm.PowerOn()
            print("Virtual machine %s powerOn successfully." % vm.name)
            return 'ok'

    else:
        print("Specify operation in "
              "<list_all> | <list_current> | <create> | <revert> | <remove>' | <remove_all> | <power_on>")

# Start program
if __name__ == "__main__":
    main(CONFIG.inputs)
