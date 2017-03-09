# -*- coding: utf-8 -*-
import os
import time

def startupPlatformCacheConfig():
    os.chdir('/usr/local/')
    os.system("unzip -o -d /usr/local /usr/local/platform-cache-config.zip")
    time.sleep(30)
    os.system("chmod 777 /usr/local/platform-cache-config/bin/platform-cache-config")
    os.system("bash -lc /usr/local/platform-cache-config/bin/platform-cache-config &")
    

if __name__ == '__main__':
    startupPlatformCacheConfig()