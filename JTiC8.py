# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 22:08:24 2019

@author: Yang Guoming,hyLee,Tian Jilin
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 13:56:40 2019

@author: Yang Guoming,hyLee,Tian Jilin
"""

import pprint

import requests
import re
import time,datetime
import os,os.path
from uuid import uuid4


def spider(startDay:int):
  url = 'http://jwxt.upc.edu.cn/jsxsd/xskb/xskb_list.do?Ves632DSdyV=NEW_XSD_PYGL'
  pp = r'<div[^i]*id=[^-]*.([^-])-."[^c]*class="kbcontent"[^>]*>([^<]*)<br/><font title=\'老师\'>([^<]*)</font><br/>[^>]*.([^<]*)</font><br/><font title=\'教室\'>([^<]*)|\-{21}<br>([^<]*)<br/><font title=\'老师\'>([^<]*)</font><br/>[^>]*.([^<]*)</font><br/><font title=\'教室\'>([^<]*)'
  comment = re.compile(pp)
  f = comment.findall(html.text)
  pprint.pprint(f)
  n = len(f)
  classTable = [[" " for i in range(7)] for i in range(n)]
  i = int(0)
  for each in f:
    j = int(1)
    if each[0] == '':
      classTable[i][0] = classTable[i - 1][0]
      j = 5
    else:
      classTable[i][0] = each[0]
    for k in range(4):
      classTable[i][k + 1] = each[j + k]
    i += 1
  flag = '0'
  classTime = 0
  startTime = ('080000', '101000', '140000', '161000', '190000', '210000')
  endTime = ('095000', '120000', '155000', '180000', '210000', '215000')
  for each in classTable:
    tian = []
    weekday = each[0] + ''
    if each[0] == '7':
      each[0] = '0'
      weekday='0'
    zhou = each[3].split('(周)')[0]
    zhou1 = zhou.split(',')
    for each2 in zhou1:
      if '-' in each2:
        zhou2 = each2.split('-')
        i1 = zhou2[0] + ''
        i2 = zhou2[1] + ''
        for i in range(int(i1), int(i2) + 1):
          tian.append(i * 7 + startDay + int(weekday))
      else:
        zhouNum = each2 + ''
        tian.append(int(zhouNum) * 7 + startDay + int(weekday))
    each[3] = tian
    if flag > each[0]:
      classTime += 1
    each[5] = startTime[classTime]
    each[6] = endTime[classTime]
    flag = each[0]
  ics(classTable)

def ics(classTable):
  # if os.path.exists("i"+"1707020110"+".ics"):
  #   os.remove("i"+"1707020110"+".ics")
  newfile="i"+"1707020110"+".ics"#学号换成传入的参数：学号
  b_new_file=open(newfile,'w')
  t_n=b_new_file.write("BEGIN:VCALENDAR\n"+
        "METHOD:PUBLISH\n"+
        "VERSION:2.0\n"+
        "COMMENT:本软件服务由中国石油大学（华东）网络信息协会提供，代码编写人员：李恒源，杨国铭，田继林，本代码半开源，使用本软件造成的法律后果由使用者承担。需要代码请联系李恒源：870575989@qq.com\n"
        "X-WR-CALNAME:课程\n"+
        "PRODID:-//Apple Inc.//Mac OS X 10.14.6//EN\n"+
        "X-APPLE-CALENDAR-COLOR:#1D9BF6\n"+
        "X-WR-TIMEZONE:Asia/Shanghai\n"+
        "CALSCALE:GREGORIAN\n"+
        "BEGIN:VTIMEZONE\n"+
        "TZID:Asia/Shanghai\n"+
        "BEGIN:STANDARD\n"+
        "TZOFFSETFROM:+0900\n"+
        "RRULE:FREQ=YEARLY;UNTIL=19910914T170000Z;BYMONTH=9;BYDAY=3SU\n"+
        "DTSTART:19890917T020000\n"+
        "TZNAME:GMT+8\n"+
        "TZOFFSETTO:+0800\n"+
        "END:STANDARD\n"+
        "BEGIN:DAYLIGHT\n"+
        "TZOFFSETFROM:+0800\n"+
        "DTSTART:19910414T020000\n"+
        "TZNAME:GMT+8\n"+
        "TZOFFSETTO:+0900\n"+
        "RDATE:19910414T020000\n"+
        "END:DAYLIGHT\n"+
        "END:VTIMEZONE\n")#ics固定格式
  for each in classTable:#每个EVENT的实现
    t_n=b_new_file.write("BEGIN:VEVENT\n")
    t_n=b_new_file.write("CREATED:"+time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())+"\n")
    t_n=b_new_file.write("UID:"+"1707020110"+"-"+short_uuid()+"&hylee.xyz\n")#(更新)学号仅做实验用途
    t_n=b_new_file.write("RRULE:FREQ=YEARLY;BYYEARDAY="+listtostr(each[3])+";UNTIL=20200111T000000Z\n")#(更新)截止到2020年1月11日
    t_n=b_new_file.write("DTEND;TZID=Asia/Shanghai:"+out_date(2019,each[3][0])+"T"+each[6]+"\n")
    t_n=b_new_file.write("TRANSP:OPAQUE\n")
    t_n=b_new_file.write("X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\n")
    t_n=b_new_file.write("SUMMARY:"+each[1]+"@"+each[4]+"\n")
    t_n=b_new_file.write("LOCATION:"+each[4]+" "+each[2]+"\n")
    t_n=b_new_file.write("LAST-MODIFIED:"+time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())+"\n")
    t_n=b_new_file.write("DTSTAMP:"+time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())+"\n")
    t_n=b_new_file.write("DTSTART;TZID=Asia/Shanghai:"+out_date(2019,each[3][0])+"T"+each[5]+"\n")
    t_n=b_new_file.write("SEQUENCE:0\n")
    t_n=b_new_file.write("END:VEVENT\n")
  t_n=b_new_file.write("END:VCALENDAR\n")
  b_new_file.close()

def prt(classTable):#这是一个测试函数，用来测试classTable的数据结构
  for each in classTable:
    print(each)


def short_uuid():
    uuidChars = ("a", "b", "c", "d", "e", "f",
               "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s",
               "t", "u", "v", "w", "x", "y", "z", "0", "1", "2", "3", "4", "5",
               "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I",
               "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V",
               "W", "X", "Y", "Z")
    uuid = str(uuid4()).replace('-', '')
    result = ''
    for i in range(0,8):
        sub = uuid[i * 4: i * 4 + 4]
        x = int(sub,16)
        result += uuidChars[x % 0x3E]
    return result


import datetime
def out_date(year, day):
  fir_day = datetime.datetime(year, 1, 1)
  zone = datetime.timedelta(days=day - 1)
  return datetime.datetime.strftime(fir_day + zone, "%Y%m%d")

def listtostr(list):
  daylist = ""
  for day in list:
    daylist = daylist + str(day) + ","
  return daylist[:-1]



if __name__ == '__main__':
  spider(244)#(修改)244是2019-2020学年上半学期开始的日期

