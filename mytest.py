#!/usr/bin/python
#coding=utf-8

import sys
import os
import time
import serial
import urllib2
import optparse
from bs4 import BeautifulSoup

def sendmsg(options, records):
    ser = serial.Serial()  # connect to serial port
    ser.port     = options.port
    ser.baudrate = options.baudrate
    ser.parity   = options.parity
    ser.timeout  = 10     # required so that the reader thread can exit

    if not options.quiet:
        sys.stderr.write("--- %s %s,%s,%s,%s ---\n" % (ser.portstr, ser.baudrate, 8, ser.parity, 1))

    try:
        ser.open()
    except serial.SerialException, e:
        sys.stderr.write("%s\n" % e)
        return -1

    for i in range(1, 11):
        record = records[i - 1]
        ser.write("%%n#%s,%s%%" % (i, record.encode('gbk')))
        time.sleep(0.5)
        ret = ser.read(ser.inWaiting())
        if not options.quiet:
            sys.stderr.write(u"信息设置：%s 【返回值：%s】\n" % (record, ret))
        ser.write("%%r#%s%%" % i)
        time.sleep(0.5)
        ret = ser.read(ser.inWaiting()).decode('gbk')
        if ret == record:
            sys.stderr.write(u"读取序号%s：%s 【设置成功】\n" % (i, ret))
        else:
            sys.stderr.write(u"读取序号%s：%s 【设置失败】\n" % (i, ret))

    ser.close()
    return 0	

if __name__ == '__main__':
    parser = optparse.OptionParser(
        usage = "%prog [options] [port [baudrate]]",
        description = u"衡阳人力资源网数据抓取程序。")

    parser.add_option("-q", "--quiet",
        dest = "quiet",
        action = "store_true",
        help = u"屏蔽不重要的提示信息",
        default = False
    )

    group = optparse.OptionGroup(parser,
        u"串口参数设置"
    )
    parser.add_option_group(group)

    group.add_option("-p", "--port",
        dest = "port",
        help = u"设置端口名称，默认：%default",
        default = "COM1"
    )

    group.add_option("-b", "--baud",
        dest = "baudrate",
        action = "store",
        type = 'int',
        help = u"设置波特率，默认：%default",
        default = 9600
    )

    group.add_option("", "--parity",
        dest = "parity",
        action = "store",
        help = u"设置校验位 [N, E, O]，默认：%default",
        default = 'N'
    )
    (options, args) = parser.parse_args()

    response = urllib2.urlopen("http://www.hysrlzy.com/injob.aspx?hy=all")
    html = response.read()
    soup = BeautifulSoup(html, from_encoding="gbk")
    rmzp = soup.find("div", {"class" : "rmzp_hot"})
    records = []  # store all of the records in this list
    for row in rmzp.findAll('li'):
        title = row.a.string.strip()
        content = row.p.string.strip()
        if content != u"诚聘：":
            record = "%s %s" % (title, content)
            records.append(record)

    sendmsg(options, records)
	
    for record in records:
        file = open('c:\LEDTEST.txt', 'w') 
        file.write('      %s' % record.encode('gbk')) 
        file.close() 
        sys.stderr.write(u"c:\LEDTEST.txt 已刷新：      %s\n" % record)
        time.sleep(60)

    if not options.quiet:
        sys.stderr.write("\n--- exit ---\n")
