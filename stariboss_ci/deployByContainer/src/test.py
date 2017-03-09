# -*- coding: utf-8 -*-
'''
Created on 2016年5月5日

@author: Simba
'''


import subprocess
import datetime
import urllib2
import logging
import os
import zipfile
import config.config as CONFIG
import paramiko
import exception.myException as myException
import utils.util as utils
import deployByContainer
import vmManager
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
import vmOperationByPython
import checkDbUpdate


tempDir = CONFIG.ROOT_HOME + os.sep + 'temp'
checkDbUpdate.clearTemp(tempDir)


