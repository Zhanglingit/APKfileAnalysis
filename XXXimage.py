#! /usr/bin/env python
#coding=utf-8
#XXX Project image function

import os
from Crypto.Hash import MD5
import re
import MySQLdb
import capstoneRead

#dic = []

def xmlHandler(filePath):
    dic = []
    #print "xmlfile:",filePath
    f = file(filePath,"r")
    page = f.read()
    f.close()
    page = page.replace("'","\"")
    list = page.split(">\n")
    for i in list:
        i = i+">"
        #print "i:",i
        tagre = re.compile(r"<.*?>", re.DOTALL)
        l2 = tagre.findall(i)
        #print "l2:",l2
        if len(l2) == 0:
            continue
        closetagre = re.compile("< *?/")
        if re.match(closetagre,l2[0]) != None:
            continue
        l2[0] = l2[0][1:-1]
        tagname = l2[0][:l2[0].find(" ")]
        #print "l2[0]=",l2[0],"tagname=",tagname
        valuere = re.compile(" .*? *?= *?\".*?\"")
        valuepairs = valuere.findall(l2[0])
        #print "pairs:",valuepairs
        for pair in valuepairs:
            key = pair[1:pair.find("=")]
            value = pair[pair.find("=")+1:]
            dic.append((filePath+"\\"+tagname+"\\"+key,value))
        if len(l2) == 2:
            if i.rfind("<") != (i.find(">")+1):
                dic.append((filePath+"\\"+tagname+"\\value",i[i.find(">")+1:i.rfind("<")]))
            if re.match(closetagre,l2[1]) != None:
                continue
            else:
                list.append(l2[1])

    #print dic
    return dic

    '''
    page = page.replace("\n","")
    tagre = re.compile("<.*?>")
    list = tagre.findall(page)
    for i in list:
        #check close tag
        page = page.replace(i,"",1)
        closetagre = re.compile("< *?/")
        if re.match(closetagre,i) != None:
            continue

        i = i.replace("\n"," ")
        valuere = re.compile(" .*? *?= *?\".*?\"")

        i = i[1:-1]
        #print i
        valueBlankList = valuere.findall(i)

        #check tag without feature
        if len(valueBlankList)==0:
            continue
        #print valueBlankList
        #print "location:",i.find(valueBlankList[0])
        tagname = i[:i.find(valueBlankList[0])]
        #print "tagname=",tagname

        for item in valueBlankList:
            key = item[1:item.find("=")]
            value = item[item.find("=")+1:]
            #print "tagname:",tagname,"key:",key,"value:",value
            #dic[filePath+"\\"+tagname+"\\"+key] = value
            dic.append((filePath+"\\"+tagname+"\\"+key,value))
    #print filePath,"PPPPPPPPPPPPPP:",page,"EEEEEEE\n"
    listRest = page.split(" ")
    for i in listRest:
        if i != "":
            dic.append((filePath+"\\RestValues",i ))
    '''

def ymlHandler(filePath):
    dic = []
    f = file(filePath,"r")
    page = f.read()
    f.close()
    page = page.replace(" ","")
    list = page.split("\n")
    #print list
    for i in range(len(list)-1,-1,-1):
        if list[i].find(":") == -1:
            list[i-1] = list[i-1]+list[i]
            del list[i]

    for i in list:
        if i == "":
            continue
        if i[-1] != ":":
            key = i[:i.find(":")]
            value = i[i.find(":")+1:]
            dic.append((filePath+"\\"+key,value))
    return dic

def apkHandler(path):
    dic = []
    #dictertory = "F:\\QR\\res"
    xmlFileRe = re.compile(".*\.xml")
    ymlFileRe = re.compile(".*\.yml")
    javaFileRe = re.compile(".*\.java")
    smaliFileRe = re.compile(".*\.smali")
    for root,dirs,files in os.walk(path):
        for fn in files:
            #print root,fn
            objFile = os.path.join(root,fn)
            if re.match(xmlFileRe,objFile)!=None:
                dic += xmlHandler(objFile)
                continue
            if re.match(ymlFileRe,objFile)!=None:
                dic += ymlHandler(objFile)
                continue
            if re.match(javaFileRe,objFile)!=None:
                print "java file:",objFile
                continue
            if re.match(smaliFileRe,objFile)!=None:
                print "smali file:",objFile
                continue

            f = file(objFile,"rb")
            page = f.read()
            h = MD5.new(page)
            #dic.append((objFile,h.hexdigest()))
    return dic

def saveDic(root, dic):
    tableName = root[root.rfind("\\")+1:].replace(".","").replace(" ","")
    print "begin to write to database..."
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='nsa',port=3306,use_unicode = True, charset="utf8")
    cur=conn.cursor()
    sql = "create table if not exists %s (id int(11) primary key auto_increment, mykey varchar(200), myvalue varchar(500))" %(tableName)
    #print "SSSSSSS:",sql
    cur.execute(sql)

    for i in dic:
        print i[0][len(root):],i[1]
        sql = "insert into %s ( mykey, myvalue) values ( '%s' , '%s' )"%(tableName, i[0][len(root):].replace("\\","\\\\"),i[1].replace("'","\"").replace("\\","\\\\"))
        print sql
        try:
            n = cur.execute(sql)
            #print n
        except:
            print "error appear with sql ==",sql
    conn.commit()
    cur.close()
    conn.close()

    print "Done"

def checkExist(root):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='nsa',port=3306,use_unicode = True, charset="utf8")
    cur=conn.cursor()
    tableName = root[root.rfind("\\")+1:].replace(".","").replace(" ","")
    tableName = (tableName.lower(),)
    #print tableName
    sql = "show tables"
    cur.execute(sql)
    rows = cur.fetchall()
    #print rows
    cur.close()
    conn.close()
    if tableName in rows:
        return True
    else:
        return False



def main(rootPath):
    '''
    if checkExist(rootPath):
        print "Data exist:",rootPath
        return
    dic = apkHandler(rootPath)
    saveDic(rootPath, dic)
    '''
    tableName = rootPath[rootPath.rfind("\\")+1:].replace(".","").replace(" ","")
    capstoneRead.main(tableName)


def multipleTranslate(rootPath, sub):
    for root,dirs,files in os.walk(rootPath):
        if root.count("\\") == (sub+1):
            print root
            main(root)



if __name__ == "__main__":
#
#    root = "F:\\capstoneproject\\1\\com.aitype.android"
#    tablename = root[root.rfind("\\")+1:].replace(".","")
#    apkHandler(root)
#    #print len(root)
#    #xmlHandler("F:\\Android\\lib\\apktool\\QR\\AndroidManifest.xml")
#    #xmlHandler("F:\\Android\\lib\\apktool\\QR\\res\\menu\\main.xml")
#    #print dic
#    print "begin to write to database..."
#    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='nsa',port=3306,use_unicode = True, charset="utf8")
#    cur=conn.cursor()
#
#    sql = "create table if not exists %s (id int(11) primary key auto_increment, mykey varchar(200), myvalue varchar(500))" %(tablename)
#    print "SSSSSSS:",sql
#    cur.execute(sql)
#
#    for i in dic:
#        print i[0][len(root):],i[1]
#        sql = "insert into %s ( mykey, myvalue) values ( '%s' , '%s' )"%(tablename, i[0][len(root):].replace("\\","\\\\"),i[1].replace("'","\"").replace("\\","\\\\"))
#        print sql
#        n = cur.execute(sql)
#        print n
#    conn.commit()
#    cur.close()
#    conn.close()
##    print "Done"
    multipleTranslate("F:\\APKs", 2)
    #print checkExist("F:\\APKs\\Bill Charla\\Bill Charlalisan.hindi.sexstories")
    #main("F:\\APKs\\Bill Charla\\Bill Charlalisan.hindi.sexstories")
    #xmlHandler("F:\\APKs\\Bill Charla\\Bill Charlalisan.hindi.sexstories\\AndroidManifest.xml")