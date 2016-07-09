#coding:utf8
import os
import sys
license = '''
/*
Author: liyonghelpme
Email: 233242872@qq.com
*/
'''
#将代码转换成UTF8格式并且增加文件头

formats = {}

def UTF8(ret, name):
    if ret.find('ASCII') != -1:
        os.system('iconv -f US -t UTF8 %s > %s' % (name, name+".temp"))
        os.system('mv %s %s' % (name+'.temp', name))
    elif ret.find('UTF-16') != -1:
        os.system('iconv -f UTF-16 -t UTF8 %s > %s' % (name, name+".temp"))
        os.system('mv %s %s' % (name+'.temp', name))
    elif ret.find('ISO-8859') != -1:
        print ret
        os.system('iconv -f GBK -t UTF8 %s > %s ' % (name, name+'.temp'))
        os.system('mv %s %s' % (name+'.temp', name))
    elif ret.find('Perl') != -1:
        print ret
        os.system('iconv -f GBK -t UTF8 %s > %s ' % (name, name+'.temp'))
        os.system('mv %s %s' % (name+'.temp', name))
        

def BOM(ret, name):
    if ret.find('BOM') == -1:
        temp = open(name).read()
        temp = chr(0xef)+chr(0xbb)+chr(0xbf)+temp
        nf = open(name, 'w')
        nf.write(temp)
        nf.close()

def Licen(ret, name):
    con = open(name).read()
    #if con[0] == 0xef and con[1] == 0xbb and con[2] == 0xbf:
    if con.find('liyonghelpme') != '-1':
        return
    
    out = con[:3]+license+con[3:]
    #else:
    #    out = license+con
    nf = open(name, 'w')
    nf.write(out)
    nf.close()
    
def trans(cur, func):
    global formats
    f = os.listdir(cur)
    for i in f:
        name = os.path.join(cur, i)
        if os.path.isdir(name):
            trans(name, func)
        else:
            if  name.find('.proto') != -1 and name.find('.dump') == -1:
                os.system('file %s > test.txt' % (name))
                ret = open('test.txt').read()
                func(ret, name)

                formats[ret.split(':')[1]] = True
                
    for f in formats:
        print f
    formats = {}

'''
trans('Assets/scripts', UTF8)
trans('Assets/scripts', BOM)
trans('Assets/scripts', Licen)
'''

trans('.', UTF8)
#trans('Assets/Editor', BOM)
#trans('Assets/Editor', Licen)


