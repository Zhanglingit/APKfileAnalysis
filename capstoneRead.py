#! /usr/bin/env python
#coding=utf-8
#XXX project statisitc data
import MySQLdb
import re

class styleS:
    length = 0
    withLowcase = False
    withCaptial = False
    withUnderline = False
    withNumber = False
    withOther = False

    beginWithNumber = False
    beginWithChar = False
    beginWithUnderline = False
    beginWithOther = False

    endWithNumber = False
    endWithChar = False
    endWithUnderline = False
    endWithOther = False

    numberLast = False

    def __init__(self, str):
        self.length = len(str)
        reLowcase = re.compile("[a-z]")
        reCaptial = re.compile("[A-Z]")
        reNumber = re.compile("[0-9]")
        reUnderline = re.compile("_")
        reOther = re.compile("[^a-zA-Z0-9_]")
        reNumberLast = re.compile("\D+?\d+?$")

        if re.search(reLowcase,str) != None:
            self.withLowcase = True
        if re.search(reCaptial,str) != None:
            self.withCaptial = True
        if re.search(reNumber,str) != None:
            self.withNumber = True
        if re.search(reUnderline,str) != None:
            self.withUnderline = True
        if re.search(reOther,str) != None:
            self.withOther = True

        if str[0] == '_':
            self.beginWithUnderline = True
        elif ((str[0] >= 'a') and (str[0] <= 'z')) or ((str[0] >= 'A') and (str[0] <= 'Z')):
            self.beginWithChar = True
        elif (str[0] >= '0') and (str[0] <= '9'):
            self.beginWithNumber = True
        else:
            self.beginWithOther = True

        if str[-1] == '_':
            self.endWithUnderline = True
        elif ((str[-1] >= 'a') and (str[-1] <= 'z')) or ((str[-1] >= 'A') and (str[-1] <= 'Z')):
            self.endWithChar = True
        elif (str[-1] >= '0') and (str[-1] <= '9'):
            self.endWithNumber = True
        else:
            self.endWithOther = True

        if re.match(reNumberLast,str):
            self.numberLast = True



def permissionState(cur,tablename):
    permissionList = ['ACCESS_CHECKIN_PROPERTIES', 'ACCESS_COARSE_LOCATION', 'ACCESS_FINE_LOCATION', 'ACCESS_LOCATION_EXTRA_COMMANDS', 'ACCESS_MOCK_LOCATION', 'ACCESS_NETWORK_STATE', 'ACCESS_SURFACE_FLINGER', 'ACCESS_WIFI_STATE', 'ACCOUNT_MANAGER', 'ADD_VOICEMAIL', 'AUTHENTICATE_ACCOUNTS', 'BATTERY_STATS', 'BIND_ACCESSIBILITY_SERVICE', 'BIND_APPWIDGET', 'BIND_DEVICE_ADMIN', 'BIND_INPUT_METHOD', 'BIND_NFC_SERVICE', 'BIND_NOTIFICATION_LISTENER_SERVICE', 'BIND_PRINT_SERVICE', 'BIND_REMOTEVIEWS', 'BIND_TEXT_SERVICE', 'BIND_VPN_SERVICE', 'BIND_WALLPAPER', 'BLUETOOTH', 'BLUETOOTH_ADMIN', 'BLUETOOTH_PRIVILEGED', 'BRICK', 'BROADCAST_PACKAGE_REMOVED', 'BROADCAST_SMS', 'BROADCAST_STICKY', 'BROADCAST_WAP_PUSH', 'CALL_PHONE', 'CALL_PRIVILEGED', 'CAMERA', 'CAPTURE_AUDIO_OUTPUT', 'CAPTURE_SECURE_VIDEO_OUTPUT', 'CAPTURE_VIDEO_OUTPUT', 'CHANGE_COMPONENT_ENABLED_STATE', 'CHANGE_CONFIGURATION', 'CHANGE_NETWORK_STATE', 'CHANGE_WIFI_MULTICAST_STATE', 'CHANGE_WIFI_STATE', 'CLEAR_APP_CACHE', 'CLEAR_APP_USER_DATA', 'CONTROL_LOCATION_UPDATES', 'DELETE_CACHE_FILES', 'DELETE_PACKAGES', 'DEVICE_POWER', 'DIAGNOSTIC', 'DISABLE_KEYGUARD', 'DUMP', 'EXPAND_STATUS_BAR', 'FACTORY_TEST', 'FLASHLIGHT', 'FORCE_BACK', 'GET_ACCOUNTS', 'GET_PACKAGE_SIZE', 'GET_TASKS', 'GET_TOP_ACTIVITY_INFO', 'GLOBAL_SEARCH', 'HARDWARE_TEST', 'INJECT_EVENTS', 'INSTALL_LOCATION_PROVIDER', 'INSTALL_PACKAGES', 'INSTALL_SHORTCUT', 'INTERNAL_SYSTEM_WINDOW', 'INTERNET', 'KILL_BACKGROUND_PROCESSES', 'LOCATION_HARDWARE', 'MANAGE_ACCOUNTS', 'MANAGE_APP_TOKENS', 'MANAGE_DOCUMENTS', 'MASTER_CLEAR', 'MEDIA_CONTENT_CONTROL', 'MODIFY_AUDIO_SETTINGS', 'MODIFY_PHONE_STATE', 'MOUNT_FORMAT_FILESYSTEMS', 'MOUNT_UNMOUNT_FILESYSTEMS', 'NFC', 'PERSISTENT_ACTIVITY', 'PROCESS_OUTGOING_CALLS', 'READ_CALENDAR', 'READ_CALL_LOG', 'READ_CONTACTS', 'READ_EXTERNAL_STORAGE', 'READ_FRAME_BUFFER', 'READ_HISTORY_BOOKMARKS', 'READ_INPUT_STATE', 'READ_LOGS', 'READ_PHONE_STATE', 'READ_PROFILE', 'READ_SMS', 'READ_SOCIAL_STREAM', 'READ_SYNC_SETTINGS', 'READ_SYNC_STATS', 'READ_USER_DICTIONARY', 'REBOOT', 'RECEIVE_BOOT_COMPLETED', 'RECEIVE_MMS', 'RECEIVE_SMS', 'RECEIVE_WAP_PUSH', 'RECORD_AUDIO', 'REORDER_TASKS', 'RESTART_PACKAGES', 'SEND_RESPOND_VIA_MESSAGE', 'SEND_SMS', 'SET_ACTIVITY_WATCHER', 'SET_ALARM', 'SET_ALWAYS_FINISH', 'SET_ANIMATION_SCALE', 'SET_DEBUG_APP', 'SET_ORIENTATION', 'SET_POINTER_SPEED', 'SET_PREFERRED_APPLICATIONS', 'SET_PROCESS_LIMIT', 'SET_TIME', 'SET_TIME_ZONE', 'SET_WALLPAPER', 'SET_WALLPAPER_HINTS', 'SIGNAL_PERSISTENT_PROCESSES', 'STATUS_BAR', 'SUBSCRIBED_FEEDS_READ', 'SUBSCRIBED_FEEDS_WRITE', 'SYSTEM_ALERT_WINDOW', 'TRANSMIT_IR', 'UNINSTALL_SHORTCUT', 'UPDATE_DEVICE_STATS', 'USE_CREDENTIALS', 'USE_SIP', 'VIBRATE', 'WAKE_LOCK', 'WRITE_APN_SETTINGS', 'WRITE_CALENDAR', 'WRITE_CALL_LOG', 'WRITE_CONTACTS', 'WRITE_EXTERNAL_STORAGE', 'WRITE_GSERVICES', 'WRITE_HISTORY_BOOKMARKS', 'WRITE_PROFILE', 'WRITE_SECURE_SETTINGS', 'WRITE_SETTINGS', 'WRITE_SMS', 'WRITE_SOCIAL_STREAM', 'WRITE_SYNC_SETTINGS', 'WRITE_USER_DICTIONARY', 'OTHERS']
    sql = "select * from %s where mykey like '%s'" %(tablename,"%permission")
    cur.execute(sql)
    rows = cur.fetchall()
    print rows
    checkList = []
    for i in range(len(permissionList)):
        checkList.append(0)
    for row in rows:
        i = row[2].replace("\"","")
        i = i[i.rfind(".")+1:]
        if i in permissionList:
            checkList[permissionList.index(i)] = 1
        else:
            checkList[-1] += 1
    for i in range(len(permissionList)):
        sql = "insert into %s ( mykey, myvalue) values ( '%s' , '%s' )"%(tablename+"2", permissionList[i],checkList[i])
        #print permissionList[i],checkList[i]
        cur.execute(sql)

def nameStyle(nameList):
    styleList = ['name_count', 'name_average_length', 'name_max_length', 'name_min_length', 'name_count_lowcase', 'name_count_captial', 'name_count_number', 'name_count_other', 'name_count_underline', 'name_begin_number', 'name_begin_underline', 'name_begin_char', 'name_end_number', 'name_end_other', 'name_end_char', 'name_end_underline', 'name_last_number', 'name_both_char']
    resultDic = {}
    objectList = []

    totalLength = 0
    maxLength = 0
    minLength = 100

    nameCountLowcase = 0
    nameCountCaptial = 0
    nameCountNumber = 0
    nameCountOther = 0
    nameCountUnderline = 0

    nameBeginChar = 0
    nameBeginNumber = 0
    nameBeginOther = 0
    nameBeginUnderline = 0

    nameEndChar = 0
    nameEndOther = 0
    nameEndUnderline = 0
    nameEndNumber = 0

    nameLastNumber = 0
    nameBothChar = 0

    for i in range(len(styleList)):
        resultDic[styleList[i]] = 0
    for i in range(len(nameList)):
        #resultList.append(0)
        objectList.append(styleS(nameList[i]))
    for i in range(len(nameList)):
        totalLength += objectList[i].length
        if maxLength < objectList[i].length:
            maxLength = objectList[i].length
        if minLength > objectList[i].length:
            minLength = objectList[i].length

        if objectList[i].withCaptial == True:
            nameCountCaptial += 1
        if objectList[i].withLowcase == True:
            nameCountLowcase += 1
        if objectList[i].withNumber == True:
            nameCountNumber += 1
        if objectList[i].withUnderline == True:
            nameCountUnderline += 1
        if objectList[i].withOther == True:
            nameCountOther += 1
        if (objectList[i].withLowcase == True) and (objectList[i].withCaptial == True):
            nameBothChar += 1

        if objectList[i].beginWithChar == True:
            nameBeginChar += 1
        if objectList[i].beginWithNumber == True:
            nameBeginNumber += 1
        if objectList[i].beginWithUnderline == True:
            nameBeginUnderline += 1
        if objectList[i].beginWithOther == True:
            nameBeginOther += 1

        if objectList[i].endWithChar == True:
            nameEndChar += 1
        if objectList[i].endWithNumber == True:
            nameEndNumber += 1
        if objectList[i].endWithUnderline == True:
            nameEndUnderline += 1
        if objectList[i].endWithOther == True:
            nameEndOther += 1

        if objectList[i].numberLast == True:
            nameLastNumber += 1

    resultDic['name_count'] = len(nameList)

    resultDic['name_count_captial'] = nameCountCaptial
    resultDic['name_count_lowcase'] = nameCountLowcase
    resultDic['name_count_underline'] = nameCountUnderline
    resultDic['name_count_number'] = nameCountNumber
    resultDic['name_count_other'] = nameCountOther
    resultDic['name_both_char'] = nameBothChar

    resultDic['name_max_length'] = maxLength
    resultDic['name_min_length'] = minLength

    resultDic['name_begin_char'] = nameBeginChar
    resultDic['name_begin_number'] = nameBeginNumber
    resultDic['name_begin_undderline'] = nameBeginUnderline
    resultDic['name_begin_other'] = nameBeginOther

    resultDic['name_end_char'] = nameEndChar
    resultDic['name_end_number'] = nameEndNumber
    resultDic['name_end_undderline'] = nameEndUnderline
    resultDic['name_end_other'] = nameEndOther

    resultDic['name_last_number'] = nameLastNumber

    if len(nameList) != 0:
        resultDic['name_average_length'] = totalLength/len(nameList)
        resultDic['name_count_captial'] = nameCountCaptial*100/len(nameList)
        resultDic['name_count_lowcase'] = nameCountLowcase*100/len(nameList)
        resultDic['name_count_underline'] = nameCountUnderline*100/len(nameList)
        resultDic['name_count_number'] = nameCountNumber*100/len(nameList)
        resultDic['name_count_other'] = nameCountOther*100/len(nameList)
        resultDic['name_both_char'] = nameBothChar*100/len(nameList)


        resultDic['name_begin_char'] = nameBeginChar*100/len(nameList)
        resultDic['name_begin_number'] = nameBeginNumber*100/len(nameList)
        resultDic['name_begin_undderline'] = nameBeginUnderline*100/len(nameList)
        resultDic['name_begin_other'] = nameBeginOther*100/len(nameList)

        resultDic['name_end_char'] = nameEndChar*100/len(nameList)
        resultDic['name_end_number'] = nameEndNumber*100/len(nameList)
        resultDic['name_end_undderline'] = nameEndUnderline*100/len(nameList)
        resultDic['name_end_other'] = nameEndOther*100/len(nameList)

        resultDic['name_last_number'] = nameLastNumber*100/len(nameList)
    else:
        resultDic['name_average_length'] = 0
        resultDic['name_min_length'] = 0

    return resultDic
#    for i in resultDic.items():
#        print i

def idStyle(cur,tablename):
    sql = "select myvalue from %s where myvalue like '%s'" %(tablename,"%@id/%")
    cur.execute(sql)
    rows = cur.fetchall()
    #print rows
    list = []
    for row in rows:
        #print row
        list.append(row[0][5:-1])
    #print list
    dic = nameStyle(list)
    for i in dic.items():
        sql = "insert into %s ( mykey, myvalue) values ( '%s' , '%s' )"%(tablename+"2", i[0].replace("\\","\\\\"),i[1])
        print sql
        n = cur.execute(sql)

def stringNameStyle(cur,tablename):
    sql = "select myvalue from %s where myvalue like '%s'" %(tablename,"%@string/%")
    cur.execute(sql)
    rows = cur.fetchall()
    #print rows
    list = []
    for row in rows:
        print row[0][9:-1]
        list.append(row[0][9:-1])
    print list
    dic = nameStyle(list)
    for i in dic.items():
        sql = "insert into %s ( mykey, myvalue) values ( '%s' , '%s' )"%(tablename+"2", i[0].replace("\\","\\\\").replace("name","string"),i[1])
        print sql
        n = cur.execute(sql)

def main(tablename):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='nsa',port=3306,use_unicode = True, charset="utf8")
    cur=conn.cursor()
    #tablename = "comaitypeandroid"
    sql = "create table if not exists %s (id int(11) primary key auto_increment, mykey varchar(200), myvalue int(11))" %(tablename+"2")
    cur.execute(sql)

    permissionState(cur,tablename)

    idStyle(cur,tablename)
    stringNameStyle(cur,tablename)
    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    main("qr")
#    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='nsa',port=3306,use_unicode = True, charset="utf8")
#    cur=conn.cursor()
#    tablename = "comaitypeandroid"
#    sql = "create table if not exists %s (id int(11) primary key auto_increment, mykey varchar(200), myvalue int(11))" %(tablename+"2")
#    cur.execute(sql)
#
#    permissionState(cur,tablename)
#    #a = styleS("asf_ssa22aaaass2")
#    #print a.length,a.withLowcase,a.withCaptial,a.withNumber,a.withUnderline,a.beginWithChar,a.withOther,a.numberLast
#    idStyle(cur,tablename)
#    stringNameStyle(cur,tablename)
#    conn.commit()
#    cur.close()
#    conn.close()
#
