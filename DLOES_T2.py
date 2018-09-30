import os,time,sqlite3,difflib,hashlib

class dloscs(object):
    global end_time,extention_list
    end_time = int(time.time())
    extention_list = ['.txt','.bat','.docx','.pptx','.bmp','.xlsx']
    def cli(self):
        get_target_path = input("DLOSCS:按<1>使用默认路径、按<2>自定义路径.")
        # get_start_time = input("DLOSCS:Hit <1> to Use Last Runtime Plus one day course or Hit <2> to Customise Starttime.")
        if get_target_path == "":
            def_path = 'E:\Resources'
            start_time_source ='2017-1-1 00:00:00'
            start_time = time.mktime(time.strptime(start_time_source,"%Y-%m-%d %H:%M:%S"))
            # dloscs.FileCounterFileCounter(def_path)
            dloscs.iter_all_file_V2(self,def_path,start_time)
        else:
            pass

    def Getfilemd5(FilePath):
        '''获取文件的消息摘要值'''
        fp = open(FilePath, 'rb')
        inf = fp.read()
        md = hashlib.new(inf)
        return md.hexdigest()

    def iter_all_file_V2(self,root_path,start_time):
        check_list_fe = []
        size_md5 = {}
        for file in os.listdir(root_path):
            file_path = os.path.join(root_path, file)
            if len(check_list_fe) < 1 :pass
            else:
                if difflib.SequenceMatcher(None, file, check_list_fe[-1]).ratio() > 0.9:
                    # print(file_path,"__Will Be Del Cause:Same File ")
                    del_path = os.path.join(check_list_fe[0],check_list_fe[1])
                    dloscs.delExpiredfile(self,del_path)
                else:pass;
            if os.path.isfile(file_path):
                del check_list_fe[:]
                # print(file_path)
                file_create_time = int(os.path.getctime(file_path))
                if (os.path.splitext(file_path)[1] in extention_list) and (start_time < file_create_time < end_time):
                    check_list_fe.append(root_path)
                    check_list_fe.append(file)
                else:pass
            elif os.path.isdir(file_path):
                dloscs.iter_all_file_V2(self,file_path,start_time)


    # def iter_all_file(file_path, start_time):
    #     hashpool = []
    #     # del hashpool[:]
    #     for file in os.listdir(file_path):
    #         objpath = os.path.join(file_path, file)
    #         if os.path.isfile(objpath):
    #             file_create_time = int(os.path.getctime(objpath))
    #             filehash = dloscs.file_md5(file_path)
    #             # time_diff = int((end_time - file_create_time)/(3600*24))
    #             if (os.path.splitext(objpath)[1] in extention_list) \
    #                     and (start_time < file_create_time < end_time) \
    #                     and (filehash in hashpool):
    #                 # dloscs.dexpiredfile(objpath)
    #                 print(objpath,"exist! delete")
    #             else:
    #                 hashpool.append(filehash)
    #                 print(objpath, "Save")
    #         elif os.path.isdir(objpath):
    #             dloscs.iter_all_file(objpath,start_time)

    def delExpiredfile(self,file_path):
        print('--File deleted',file_path)
        # expiredsec =  expiredTime * 24 * 3600
        # stat_result =  os.stat(filepath)
        # ctime =  stat_result.st_mtime
        # ntime = time.time()
        # if (ntime-ctime)>expiredsec:
        # try:
        #     os.remove(file_path)
        #     print("Deleting",file_path)
        # # except Exception as e:
        # #     # log.writelog(e,'CRITICAL')
        # #
        # except:
        #     pass
        # # else:
        #     return False

    def file_counter(file_path):
        count = 0
        for root,dirs,files in os.walk(file_path):    #遍历统计
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

    # def iter_all_file_by_filename(self):
    #     for obj in os.listdir(path):
    #         list_of_per_file = os.listdir(path)
    #         #obj is file name
    #         for uuc in list_of_per_file:
    #             fdr = difflib.SequenceMatcher(None,obj,uuc).ratio()
    #             if fdr > 0.4:
    #                 objpath = os.path.join(path,obj)
    #             # elif fdr ==1:print()
    #         if os.path.isfile(objpath):
    #             file_create_time = int(os.path.getctime(objpath))
    #             # time_diff = int((end_time - file_create_time)/(3600*24))
    #             if os.path.splitext(objpath)[1] in extention_list and start_time < file_create_time < end_time:
    #                 dloscs.dexpiredfile(objpath)
    #             else:pass
    #         elif os.path.isdir(objpath):
    #             dloscs.iter_all_file(objpath,start_time)

if __name__ == '__main__':
    dloscs.cli(object)


