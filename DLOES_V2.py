import os,time,sqlite3,hashlib

class dloscs():
    global end_time,extention_list

    end_time = int(time.time())
    extention_list = ['.txt','.bat','.docx','.pptx']
    def cli(self):
        get_target_path = input("DLOSCS:按<1>使用默认路径、按<2>自定义路径.")
        # get_start_time = input("DLOSCS:Hit <1> to Use Last Runtime Plus one day course or Hit <2> to Customise Starttime.")
        if get_target_path == "1":
            def_path = 'E:\Resources'
            start_time_source ='2017-1-5 00:00:00'
            start_time = time.mktime(time.strptime(start_time_source,"%Y-%m-%d %H:%M:%S")) + 86400
            dloscs.file_counter(def_path)
            dloscs.iter_all_file(def_path,start_time)

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

    # def iter_all_file(file_path, start_time):
    #     hashpool = []
    #     # del hashpool[:]
    #     for file in os.listdir(file_path):
    #         objpath = os.path.join(file_path, file)
    #         if os.path.isfile(objpath):
    #             file_create_time = int(os.path.getctime(objpath))
    #             filehash = dloscs.Getfilemd5(file_path)
    #             # time_diff = int((end_time - file_create_time)/(3600*24))
    #             if (os.path.splitext(objpath)[1] in extention_list) \
    #                     and (start_time < file_create_time < end_time) \
    #                     and (filehash in hashpool):
    #                 # dloscs.dexpiredfile(objpath)
    #                 print(objpath, "exist! delete")
    #             else:
    #                 hashpool.append(filehash)
    #                 print(objpath, "Save")
    #         elif os.path.isdir(objpath):
    #             dloscs.iter_all_file(objpath, start_time)

    # def iter_all_file(path,start_time):
    #     for obj in os.listdir(path):
    #         objpath = os.path.join(path,obj)
    #         if os.path.isfile(objpath):
    #             file_create_time = int(os.path.getctime(objpath))
    #             # time_diff = int((end_time - file_create_time)/(3600*24))
    #             if file_create_time < end_time:
    #                 dloscs.dexpiredfile(objpath)
    #             else:pass
    #         elif os.path.isdir(objpath):
    #             dloscs.iter_all_file(objpath,start_time)

    def delExpiredfile(objpath):
        print(objpath)
        # expiredsec =  expiredTime * 24 * 3600
        # stat_result =  os.stat(filepath)
        # ctime =  stat_result.st_mtime
        # ntime = time.time()
        # if (ntime-ctime)>expiredsec:
        # try:
        #     os.remove(filepath)
        # except Exception as e:
        #     # log.writelog(e,'CRITICAL')
        #
        # except:
        #     pass
        # else:
        #     return False

    def file_counter(objpath):
        count = 0
        for root,dirs,files in os.walk(objpath):    #遍历统计
            for each in files:
                 count += 1   #统计文件夹下文件个数
        print (count)               #输出结果

    def cidb_read(self, sql_data_r):
        get_old_path = os.getcwd()
        connect_db = sqlite3.connect("%s\cimt.db"%get_old_path)
        # connect_db = sqlite3.connect('/Users/xiayanzheng/Onedriver/OneDrive/Lib-Sandbox/cimt.db')
        cursor_db = connect_db.cursor()
        sql = cursor_db.execute(sql_data_r)
        fetchall_sql = sql.fetchall()
        return fetchall_sql

    def cidb_write(self,db_sql,db_data):
        get_old_path = os.getcwd()
        connect_db = sqlite3.connect("%s\cimt.db"%get_old_path)
        # connect_db = sqlite3.connect('/Users/xiayanzheng/Onedriver/OneDrive/Lib-Sandbox/cimt.db')
        c = connect_db.cursor()
        #Create table
        # c.execute('''Create TABLE if not exists sql_target_table("NA")''')
        #Insert links into table
        c.execute(db_sql,db_data)
        connect_db.commit()

    def get_last_column_in_cidb(self,data):
        list = []
        for traversal in data:
            list.append(traversal)
        result = (list[-1])[0]
        return result

if __name__ == '__main__':
    dloscs.cli(object)