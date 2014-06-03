#! /usr/bin/env python
#coding=utf-8
#capstone SQLtranslate

import MySQLdb

"""
TATS int(11), READ_USER_DICTIONARY int(11), REBOOT int(11), RECEIVE_BOOT_COMPLETED int(11), RECEIVE_MMS int(11), RECEIVE_SMS int(11), RECEIVE_WAP_PUSH int(11), RECORD_AUDIO int(11), REORDER_TASKS int(11), RESTART_PACKAGES int(11), SEND_RESPOND_VIA_MESSAGE int(11), SEND_SMS int(11), SET_ACTIVITY_WATCHER int(11), SET_ALARM int(11), SET_ALWAYS_FINISH int(11), SET_ANIMATION_SCALE int(11), SET_DEBUG_APP int(11), SET_ORIENTATION int(11), SET_POINTER_SPEED int(11), SET_PREFERRED_APPLICATIONS int(11), SET_PROCESS_LIMIT int(11), SET_TIME int(11), SET_TIME_ZONE int(11), SET_WALLPAPER int(11), SET_WALLPAPER_HINTS int(11), SIGNAL_PERSISTENT_PROCESSES int(11), STATUS_BAR int(11), SUBSCRIBED_FEEDS_READ int(11), SUBSCRIBED_FEEDS_WRITE int(11), SYSTEM_ALERT_WINDOW int(11), TRANSMIT_IR int(11), UNINSTALL_SHORTCUT int(11), UPDATE_DEVICE_STATS int(11), USE_CREDENTIALS int(11), USE_SIP int(11), VIBRATE int(11), WAKE_LOCK int(11), WRITE_APN_SETTINGS int(11), WRITE_CALENDAR int(11), WRITE_CALL_LOG int(11), WRITE_CONTACTS int(11), WRITE_EXTERNAL_STORAGE int(11), WRITE_GSERVICES int(11), WRITE_HISTORY_BOOKMARKS int(11), WRITE_PROFILE int(11), WRITE_SECURE_SETTINGS int(11), WRITE_SETTINGS int(11), WRITE_SMS int(11), WRITE_SOCIAL_STREAM int(11), WRITE_SYNC_SETTINGS int(11), WRITE_USER_DICTIONARY int(11), OTHERS int(11), name_begin_other int(11), name_max_length int(11), name_count_lowcase int(11), name_end_number int(11), name_end_undderline int(11), name_count_underline int(11), name_begin_char int(11), name_count_number int(11), name_end_char int(11), name_end_underline int(11), name_count_captial int(11), name_begin_undderline int(11), name_count int(11), name_begin_number int(11), name_end_other int(11), name_begin_underline int(11), name_min_length int(11), name_last_number int(11), name_count_other int(11), name_average_length int(11), name_both_char int(11), string_begin_other int(11), string_max_length int(11), string_count_lowcase int(11), string_end_number int(11), string_end_undderline int(11), string_count_underline int(11), string_begin_char int(11), string_count_number int(11), string_end_char int(11), string_end_underline int(11), string_count_captial int(11), string_begin_undderline int(11), string_count int(11), string_begin_number int(11), string_end_other int(11), string_begin_underline int(11), string_min_length int(11), string_last_number int(11), string_count_other int(11), string_average_length int(11), string_both_char int(11))
"""
def createTable(tableName):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='nsa',port=3306,use_unicode = True, charset="utf8")
    cur=conn.cursor()
    sql = "select mykey from %s" %("qr2")
    cur.execute(sql)
    rows = cur.fetchall()
    print rows
    commandPart = ""
    for row in rows:
        commandPart += " "+row[0]+" int(11),"
    print commandPart
    sql = "create table if not exists %s (id int(11) primary key auto_increment, apkName char(200),%s)" %(tableName,commandPart[:-1])
    print sql
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()



def main(tableName):
    conn=MySQLdb.connect(host='localhost',user='root',passwd='',db='nsa',port=3306,use_unicode = True, charset="utf8")
    cur=conn.cursor()
    sql = "show tables"
    cur.execute(sql)
    rows = cur.fetchall()
    for i in range(len(rows)):
        #print rows
        if (rows[i][0][-1] == '2') and (rows[i][0][:-1] == rows[i-1][0]):
            sql1 = "select myvalue from %s where mykey = '\\\\AndroidManifest.xml\\\\manifest\\\\package'"%(rows[i-1][0])
            print sql1
            cur.execute(sql1)
            rows1 = cur.fetchall()
            if len(rows1) == 0:
                continue
            apkName = rows1[0][0][1:-1]
            print apkName
            sql1 = "select mykey,myvalue from %s"%(rows[i][0])
            cur.execute(sql1)
            rows1 = cur.fetchall()
            print rows1
            #apkName = rows[i][0][:-1]
            keys = ""
            values = ""
            keys += "apkname, "
            values += "'"+apkName+"', "
            for x,y in rows1:
                keys += x+", "
                values += "'"+str(y)+"', "
            keys = "("+keys[:-2]+")"
            values = "("+values[:-2]+")"
            #print keys
            #print values
            sql = "insert into %s %s values %s"%(tableName, keys, values)
            print sql
            cur.execute(sql)
            conn.commit()


    cur.close()
    conn.close()

if __name__ == '__main__':
    main("capstone")
    #createTable("capstone")