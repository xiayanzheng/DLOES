#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,time,sqlite3,difflib,hashlib

class dloscs():
    def extension_list_data(self):
        raw_data = dloscs.DLOSCS_DB_read(self=None,sql_data_r="SELECT * FROM extension")
        extention_list = []
        for data in raw_data:
            extention_list.append(data[0])
        return extention_list

    def cli(self):
        global get_target_path_input,get_start_time,get_end_time
        continue_or_quite = input("DLOSCS:按<1>开始进程--|--按任意键结束进程\nAdmin:")
        if continue_or_quite == "1":pass
        else:exit()
        get_target_path = input("DLOSCS:按<1>使用默认路径--|--按<2>自定义路径--|--按任意键回到主菜单\nAdmin:")
        if get_target_path == "1":get_target_path = "E:\Resources"
        elif get_target_path == "2":
            get_target_path = input("DLOSCS:请输入自定义路径\nAdmin:")
            if os.path.exists(get_target_path) != False:
                get_target_path_input = get_target_path
            else:
                print("DLOSCS:路径不存在或无法访问,请重试.")
                dloscs.cli(self)
        else:dloscs.cli(self)
        choice_for_time= input("DLOSCS:按<1>设定开始与结束时间--|--按任意键回到主菜单\nAdmin:")
        if choice_for_time == ('1'):
            get_start_time = input("DLOSCS:请输入开始时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
            get_end_time = input("DLOSCS:请输入结束时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
        else:dloscs.cli(self)
        try:
            time.strptime(get_start_time, "%Y-%m-%d")
            time.strptime(get_end_time, "%Y-%m-%d")
            start_time = time.mktime(time.strptime(get_start_time, "%Y-%m-%d"))
            end_time = time.mktime(time.strptime(get_end_time, "%Y-%m-%d"))
            if end_time < start_time:
                print("DLOSCS:开始时间大于结束时间,请重试.")
                dloscs.cli(self)
        except:
            print("DLOSCS:输入的格式错误,请重试.")
            dloscs.cli(self)
        conform_info = input('''请确认设定:\n目标文件夹及所有子文件夹:<<<%s>>>>\n开始时间:<<<%s>>>>\n结束时间:<<<%s>>>>\n输入"conform"开始文件清除进程\nAdmin: ''' % (get_target_path, get_start_time, get_end_time))
        if conform_info == ("conform"):
            pass
        else:
            print("DLOSCS:输入错误,请重试.")
            dloscs.cli(self)
        root_path = get_target_path
        start_time = time.mktime(time.strptime(get_start_time, "%Y-%m-%d"))
        end_time = time.mktime(time.strptime(get_end_time, "%Y-%m-%d"))
        print("=======================Start=======================")
        dloscs.iter_all_file_V2(self,root_path,start_time,end_time)
        # start_time_source ='2017-1-1 00:00:00'
        # start_time = time.mktime(time.strptime(start_time_source,"%Y-%m-%d %H:%M:%S"))
        # dloscs.FileCounterFileCounter(def_path)
        # def_path = 'E:\Resources'
        # dloscs.FileFilterFileFilter(get_target_path_input, get_start_time_input, get_end_time_input)

    def iter_all_file_V2(self,root_path,start_time,end_time):
        extention_list = dloscs.extension_list_data(object)
        DedupeFilePasthContain = []
        for file in os.listdir(root_path):
            file_path = os.path.join(root_path, file)
            if len(DedupeFilePasthContain) < 1 :pass
            else:
                if difflib.SequenceMatcher(None, file, DedupeFilePasthContain[-1]).ratio() > 0.7:
                    # print(file_path,"__Will Be Del Cause:Same File ")
                    del_path = os.path.join(DedupeFilePasthContain[0],DedupeFilePasthContain[1])
                    dloscs.del_expired_file(self, del_path)
                else:pass
            if os.path.isfile(file_path):
                del DedupeFilePasthContain[:]
                # print(file_path)
                file_create_time = int(os.path.getctime(file_path))
                if (os.path.splitext(file_path)[1] in extention_list) and (start_time < file_create_time < end_time):
                    DedupeFilePasthContain.append(root_path)
                    DedupeFilePasthContain.append(file)
                else:pass
            elif os.path.isdir(file_path):
                dloscs.iter_all_file_V2(self,file_path,start_time,end_time)

    def del_expired_file(self, file_path):
        print('--File deleted-->>>',file_path)
        # try:
        #     os.remove(file_path)
        #     print("Deleting",file_path)
        # except Exception as e:
        #     log.writelog(e,'CRITICAL')

    def file_counter(file_path):
        count = 0
        for root,dirs,files in os.walk(file_path):    #遍历统计
            for each in files:
                 count += 1   #统计文件夹下文件个数
        print (count)               #输出结果

    def DLOSCS_DB_read(self, sql_data_r):
        get_old_path = os.getcwd()
        connect_db = sqlite3.connect("%s\DLOSCS_Data.db"%get_old_path)
        # connect_db = sqlite3.connect('/Users/xiayanzheng/Onedriver/OneDrive/Lib-Sandbox/cimt.db')
        cursor_db = connect_db.cursor()
        sql = cursor_db.execute(sql_data_r)
        fetchall_sql = sql.fetchall()
        return fetchall_sql

    def DLOSCS_DB_write(self,db_sql,db_data):
        get_old_path = os.getcwd()
        connect_db = sqlite3.connect("%s\DLOSCS_Data.db"%get_old_path)
        # connect_db = sqlite3.connect('/Users/xiayanzheng/Onedriver/OneDrive/Lib-Sandbox/cimt.db')
        c = connect_db.cursor()
        #Create table
        # c.execute('''Create TABLE if not exists sql_target_table("NA")''')
        #Insert links into table
        c.execute(db_sql,db_data)
        connect_db.commit()

    def DLOSCS_DB_get_last_column(self,data):
        list = []
        for traversal in data:
            list.append(traversal)
        result = (list[-1])[0]
        return result

    def Getfilemd5(path):
        fp = open(path, 'rb')
        checksum = hashlib.md5()
        while True:
            buffer = fp.read(8192)
            if not buffer: break
            checksum.update(buffer)
        fp.close()
        checksum = checksum.digest()
        return checksum

    def iter_all_file_by_MD5(top_dir):
        size_md5 = {}  # 键是文件大小，值是拥有该文件大小的文件的md5值列表（为了减少计算md5的次数，当出现新的不同大小的文件时
        # 并不是立马去计算新文件的md5值，而是将文件路径保存在值中。等到再次出现该大小的文件时再计算第一个文件
        # 的MD5值再来比较）
        # 思路：先获取文件大小，看是否存在相同大小存在，如不存在，将大小添加到file_size字典中，值是文件路径
        # 若存在，则再判断本文件是否是第二个相同大小的文件，如是，则计算原来保存路径文件的md5进行比较，若已经不是第二个，
        # 则直接计算本文件md5判断是否在列表中
        if os.path.isdir(top_dir) == False:
            print("wrong dir_path")
            return
        for dirname, dirs, filenames in os.walk(top_dir):
            for file in filenames:
                file_path = os.path.join(dirname, file)
                filepath_and_md5 = [file_path]
                # 获取大小
                file_size = os.path.getsize(file_path)
                if file_size in size_md5.keys():
                    if len(size_md5[file_size]) == 1:
                        # 计算保存的文件的md5值，保存在列表的[1]处
                        size_md5[file_size].append(dloscs.Getfilemd5(size_md5[file_size][0]))
                    # 计算本文件的md5值
                    now_md5 = dloscs.Getfilemd5(file_path)
                    if now_md5 in size_md5[file_size]:  # 不用怕，MD5值不会和保存的文件路径匹配，因为路径中有\等字符。
                        # 发现相同文件，删除
                        print("delete" + file_path)
                        os.remove(file_path)
                    else:
                        size_md5[file_size].append(now_md5)
                else:
                    size_md5[file_size] = filepath_and_md5

if __name__ == '__main__':
    dloscs.cli(object)


