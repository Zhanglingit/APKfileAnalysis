#! /usr/bin/env python
#coding=utf-8
#For Capstone project - Zhanglin
#intergation tool

import os
import re
import MySQLdb

g_javaPath = "H:\\Java\\bin\\java"
g_apkToolPath = "lib\\apktool.jar"

def translateAPK(path):
    #apkTool = "H:\\Java\\bin\\java -jar F:\\Android\\lib\\apktool\\apktool.jar d "
    apkTool = g_javaPath+" -jar "+g_apkToolPath+" d "
    command = apkTool+path+" "+path[:-4]
    print command
    os.system(command)

def multipleTranslateAPK(path):
    for root,dirs,files in os.walk(path):
        for fn in files:
            src = os.path.join(root,fn)
            if (os.path.isfile(src)) and (src[-4:]==".apk"):
                translateAPK(src)

def autoConfig():
    f = file("config.txt", "r")
    page = f.read()
    f.close()


if __name__ == "__main__":
    #translateAPK("F:\\QR2.apk")
    multipleTranslateAPK("F:\\APKs")7



