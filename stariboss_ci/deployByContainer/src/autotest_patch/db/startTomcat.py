# -*- coding: utf-8 -*-
import os

def start_tomcat():
    os.chdir('/usr/local/tomcat/bin')
    if os.system('sh startup.sh') == 0:
        print('exec sh startup.sh sucess.')
    else:
        print('exec sh startup.sh fail.')


if __name__ == '__main__':
    start_tomcat()