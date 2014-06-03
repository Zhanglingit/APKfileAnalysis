#! /usr/bin/env python
#coding=utf-8
#capstone automatic translate to 2
import os

javaPath = "H:\\Java\\bin\\java"
apkToolPath = "F:\\Android\\lib\\apktool\\apktool.jar"

def autoTranslateApk(rootPath):
    """F:\Android\lib\apktool\apktool d F:\QR2.apk"""
    apkTool = "H:\\Java\\bin\\java -jar F:\\Android\\lib\\apktool\\apktool.jar d "
    for root,dirs,files in os.walk(rootPath):
        for fn in files:
            src = os.path.join(root,fn)
            dst = root
            #command = apkTool+src+" "+dst
            #os.popen(command)
            print os.path.join(root,fn)
            apkPath = os.path.join(root,fn)
            print root
            folderPath = root
            command = apkTool+"\""+apkPath+"\" \""+root+fn[:-4]+"\""
            print command
            os.system(command)




if __name__ == "__main__":
    rootPath = "F:\\APKs"
    autoTranslateApk(rootPath)
    command = "H:\\Java\\bin\\java -jar \"F:\\Android\\lib\\apktool\\apktool.jar\" d \"F:\\QR2.apk\" \"F:\\QR\""
    print command
    #os.system(command)



