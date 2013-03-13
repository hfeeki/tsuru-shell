#!/usr/bin/env python
# -*- coding:utf-8-*-
#名字:more.py
#功能：
#           实现linux中more的基本功能，当more 后加一个文件名参数时候，分屏显示，按空格换页，按回车换行',在左下角显示百分比;
#           可以处理管道参数的输入，处理选项+num:从指定行开始显示，+/string :查找字符串，从指定字符串之后开始显示
#运行环境：
#           安装有PYTHON的linux系统
#调用示例：
#            more.py [+num ]     [+/pattern]  filename
#            command|./more.py [+num ] [+/pattern]
#            more.p  --help     输出帮助信息
#            num 是 要从第几行开始显示，pattern是要在文件中查找的字符串
           

import os
import sys
import curses      #用于获取终端的尺寸
import re              #用于字符匹配
import signal      #用于处理ctrl+c中断
import fcntl        # 处理显示过程中屏幕的变化
import termios  #获取终端信息
import struct


page_len = 0   #满屏时可以显示的最大行数
line_len = 0   #满屏时每行可以显示的最大字节数
sig_up = 0    #中断信号标志
winsz_chg = 0   #窗口大小改变标志


def win_sz_chg(signum, frame):
    '''  函数功能：本函数是屏幕变化信号的处理函数'''
    global page_len, line_len, winsz_chg
    winsz_chg = 1
    signal.signal(signal.SIGWINCH, signal.SIG_IGN)
    s = struct.pack("HHHH", 0, 0, 0, 0)  
    a = struct.unpack('hhhh', fcntl.ioctl(sys.stdout.fileno(), termios.TIOCGWINSZ , s))
    #获取当前窗口的大小
    page_len = int(a[0]) - 1  #留一行显示进度
    line_len = int(a[1])
    signal.signal(signal.SIGWINCH, win_sz_chg) #不调用会导致只能检测一次屏幕变化
    
    
signal.signal(signal.SIGWINCH, win_sz_chg)  #接收处理窗口改变信号


def term_do_exit(signum, frame):
    '''  函数功能：键盘中断信号的响应函数'''
    global sig_up
    sig_up = 1           #将键盘中断标志置1
    os.system("stty -F /dev/tty echo") #恢复终端输出回车有效状态
    os.system("stty -F /dev/tty -cbreak")#重新设着屏幕为输入字符回显状态
    return
    
    
signal.signal(signal.SIGINT, term_do_exit)   #接收并处理键盘中断信号


def usage():
    '''显示脚本的各参数的含义和调用格式'''
    print "-----------------usage-----------------"
    print "1./more.py [+num] [+/pattern] filename"
    print "2 command | ./more.py"
    print "num: Start at line number num. "
    print "pattern:Start at line number num."
    print "space: next page"
    print "q :do_exit the program"
    print "enter:next line"
    print"----------------------------------------"
    sys.exit()


def do_exit():
    '''用于系统退出 '''
    os.system("stty -F /dev/tty echo") #恢复终端输出回车有效状态
    os.system("stty -F /dev/tty -cbreak")#重新设着屏幕为输入字符回显状态
    sys.exit()
    

def is_input():
    ''' 检测是否有管道数据输入 '''
    try:
        f = sys.stdin.fileno()  #判断时候有管道输入
        init_tty = termios.tcgetattr(f)     #当没有管道输入，也没有参数时候，显示提示
        return 0
    except:
        return 1
    

def get_line_num(args):
    ''' 从命令行参数中获取开始显示的指定行
    参数：args:从命令行获取的参数返回值：要开始显示的指定行  '''
    line_num = 1
    for i in args:            #匹配要从第几行开始的行数
        ln = re.search(r'\+\d+', str(i))
        if ln:
            line_num = int(ln.group().lstrip('+'))#采用正则表达式处理去掉‘+’，得到开始显示的行号
            break
    return line_num
          
           
def get_patstr(args):
    '''从命令行中获取要查找的字符串
     参数：args:从命令行中获取的参数为返回值：要查找的字符串:  '''
    patstr = ""
    for i in args:            #获取要匹配的字符串
        pa = re.search(r'(\+\/\w*[^\s])', str(i))
        if pa:
            break
    if pa:
        patstr = str(pa.group().lstrip('+/'))
    return patstr
    
    
def get_args():
    '''用于从命令行获取参数，解析各参数
    返回值：(line_num,patstr,fp):要开始显示的指定行，要查找的字符串，要操作的文件对象 '''
    line_num = 1
    patstr = ""
    args = sys.argv[1:]
    if not args:
        if is_input():      #在没有参数时候，判断是否为管道命令输入，不是提示正确输入参数
            fp = sys.stdin
            return (line_num, patstr, fp)
        else:
            usage()
    else:
        if args[-1] == "--help":
            usage()
        line_num = get_line_num(args)
        patstr = get_patstr(args)
        if '+' not in args[-1]:
            filename = args[-1]
            if not os.path.exists(filename):
                print " 没有那个文件或目录"
                do_exit()
            else:
                fp = open(filename)
        else:
            if not is_input():
                usage()
            else:
                fp = sys.stdin
    return (line_num, patstr, fp)


def get_screen_size():
    ''' 用于获取文件显示终端的尺寸   '''
    global page_len, line_len       
    screen = curses.initscr()       
    page_len, line_len = screen.getmaxyx()#获取屏幕显示尺寸
    page_len = page_len - 2   #去掉输入命令那行，和最后要显示more的那一行
    curses.endwin()     #此处不结束会导致后面显示的乱码

    
def show_more(pre_pg_len):
    ''' 等待键盘输入命令 ，进行相应的处理。
    :param pre_pg_len:屏幕改变以前保存的可显示的最大行数'''
    global  sig_up, winsz_chg, page_len
    ft = open('/dev/tty')   #打开标准终端输入
    sys.stdout.flush()    #刷新缓存输出，否则显示会出现问题
    c = ''
    while True:
        try:
            c = ft.read(1)#读取一个字符
        except IOError:
            if sig_up:
                do_exit()   #键盘中断退出程序
        if c == " ":
            print "\033[20D\033[K" #控制光标回到more--反白字体的行首，删除此行以达到more不随文字滚动效果
            if winsz_chg:        #如果此时屏幕大小变化，第一次返回之前屏幕满屏行数
                winsz_chg = 0
                return pre_pg_len
            else:
                return page_len     #当输入是空格时候，分屏显示，显示下一屏
        elif c == "q":
            print "\033[20D\033[K"
            return 0          #当输入是"q"时，退出显示
        elif c == '\n':
            print "\033[20D\033[K",
            return 1           #当输入是换行符时候，多显示一行
      
      
def skip_ln(fp, line_num):
    ''' 读取文件到指定开始显示的行  '''
    n = line_num - 1
    while n:
        fp.readline()
        if not fp:
            return
        n = n - 1


def search(fp, patstr):
    ''' 在文件中寻找要查找的字符串。
    :param fp:要显示的文件对象    
    :param patstr:要查找的检索词  '''
    global  sig_up
    text = ' '
    while True:
        try:
            s = fp.read(1)         
            if not s:
                print "can not find the string in the file"
                do_exit()
            text = text + s
            if patstr in text:
                return
        except IOError:
            if sig_up:
                do_exit()
   
   
def show_prog(read_size, total_size):         
    '''  在显示屏幕的左下角显示反显的"More"
        当要显示的是一个文件时，同时显示已经显示文件的百分比
        当显示的是一个管道输入时，只显示“More”
    :param read_size: 已经显示的文件
    :param total_size:要显示的文件的总大小  '''
    if total_size:
        prog = int(read_size * 100 / float(total_size))
        print  "\033[7m --More--" + str(prog) + '%' + "\033[0m", #输出反白的文字“more”和显示百分数
    else:
        print  "\033[7m --More--" + "\033[0m", #输出反白的文字“more”
    return
            

def do_more(fp , line_num , patstr):
    '''分屏显示文件内容
    :param fp:要显示的文件对象
    :param page_len: 可显示的最大行数
    :param line_len:可每行可显示的最大字节数   '''
    global page_len, line_len
    read_size = 0
    total_size = 0
    os.system("stty -F /dev/tty cbreak") #调用linux命令设置屏幕为不等回车
    os.system("stty -F /dev/tty -echo ")#设置屏幕为输入字符不回显
    if fp != sys.stdin:
            fp.seek(0, 2)  #获取文件的总字节数，以便后来显示输出的百分比
            total_size = fp.tell()
            fp.seek(0, 0)
    if line_num != 1:
        skip_ln(fp, line_num)
    if patstr:
        search(fp, patstr)
    try:
        line = fp.readline(line_len)#按行读取文件，可以设置最大读取字数，当遇到“\n”时候，将"\n"读入结束。
        read_size = len(line)
        num_lns = 0
        while line:
            if num_lns == page_len: #每次输出满屏后，等待指令
                pre_pg_len = page_len
                show_prog(read_size, total_size)
                reply = show_more(pre_pg_len)           
                if reply == 0:
                    break
                num_lns -= reply
            print line.strip('\n') #用,来消除print 输出的换行符
            sys.stdout.flush()    #刷新缓存，否则会出现文件显示迟缓的问题
            read_size = read_size + len(line)
            num_lns += 1
            line = fp.readline(line_len)
        fp.close()
    except IOError:
        if sig_up:
            do_exit()
   
            
if __name__ == '__main__':
    get_screen_size()  #获取显示终端的尺寸
    (line_num, patstr, fp) = get_args()
    do_more(fp, line_num, patstr)
    do_exit()


