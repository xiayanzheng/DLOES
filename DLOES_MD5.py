#! /usr/bin/env python
#coding=utf-8

import os
import hashlib
def Getfilemd5(path):
    fp = open(path,'rb')
    checksum = hashlib.md5()
    while True:
        buffer = fp.read(8192)
        if not buffer:break
        checksum.update(buffer)
    fp.close()
    checksum = checksum.digest()
    return checksum

def main(top_dir):
    size_md5={}   #键是文件大小，值是拥有该文件大小的文件的md5值列表（为了减少计算md5的次数，当出现新的不同大小的文件时
                  #并不是立马去计算新文件的md5值，而是将文件路径保存在值中。等到再次出现该大小的文件时再计算第一个文件
                  #的MD5值再来比较）
    #思路：先获取文件大小，看是否存在相同大小存在，如不存在，将大小添加到file_size字典中，值是文件路径
    #若存在，则再判断本文件是否是第二个相同大小的文件，如是，则计算原来保存路径文件的md5进行比较，若已经不是第二个，
    #则直接计算本文件md5判断是否在列表中
    if os.path.isdir(top_dir)==False:
        print ("wrong dir_path")
        return
    for dirname,dirs,filenames in os.walk(top_dir):
        for file in filenames:
            file_path=os.path.join(dirname,file)
            filepath_and_md5=[file_path]
            #获取大小
            file_size=os.path.getsize(file_path)
            if file_size in size_md5.keys():
                if len(size_md5[file_size])==1:
                    #计算保存的文件的md5值，保存在列表的[1]处
                    size_md5[file_size].append(Getfilemd5(size_md5[file_size][0]))
                #计算本文件的md5值
                now_md5=Getfilemd5(file_path)
                if now_md5 in size_md5[file_size]:   #不用怕，MD5值不会和保存的文件路径匹配，因为路径中有\等字符。
                    #发现相同文件，删除
                    print ("delete"+file_path)
                    os.remove(file_path)
                else:
                    size_md5[file_size].append(now_md5)
            else:
                size_md5[file_size]=filepath_and_md5

#调用函数
main(r"E:\Resources")