# -*- coding: utf-8 -*-
'''
Created on 2016年5月5日

@author: Simba
'''


import subprocess
import datetime
import buildDockerImage
import urllib2
import logging
import os
import zipfile
import config.config as CONFIG
import paramiko
import myException
from buildDockerImage import delAllLocalImages
import log.logService as logService
import buildDockerImage


buildDockerImage.unzipFile('/root/.jenkins/jobs/Manutestbuild_TEST_BR_STARIBOSS-7_1_1_TEST/workspace/Fordockerfile/partner-ui.war', '/root/.jenkins/jobs/Manutestbuild_TEST_BR_STARIBOSS-7_1_1_TEST/workspace/Fordockerfile/partner-ui')