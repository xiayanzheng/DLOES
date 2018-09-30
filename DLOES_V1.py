import os,time

class dloscs():
    global current_time
    current_time = int(time.time())

    def iter_all_file(path,expiredTime):
        for obj in os.listdir(path):
            objpath = os.path.join(path,obj)
            if os.path.isfile(objpath):
                # dloscs.dexpiredfile(objpath,expiredTime)
                dloscs.filter_by_Extention(objpath,expiredTime)
            elif os.path.isdir(objpath):
                dloscs.iter_all_file(objpath,expiredTime)

    def filter_by_Extention(objpath,expiredTime):
        file = objpath
        expiredTime = expiredTime
        list = ['.txt','.bat']
        if os.path.splitext(file)[1] in list:
            dloscs.filter_by_Time(file,expiredTime)
        else:pass

    def filter_by_Time(objpath,expiredTime):
        file = objpath
        file_create_time = int(os.path.getctime(file))
        time_diff = int((current_time - file_create_time)/(3600*24))
        if time_diff > expiredTime:
            dloscs.delExpiredfile(file,time_diff)
        else:pass

    def delExpiredfile(objpath,time_diff):
        print(time_diff,objpath)

        # expiredsec =  expiredTime * 24 * 3600
        # stat_result =  os.stat(filepath)
        # ctime =  stat_result.st_mtime
        # ntime = time.time()
        # if (ntime-ctime)>expiredsec:
        # try:
        #     os.remove(filepath)
        # except Exception as e:
        #     log.writelog(e,'CRITICAL')
        # except:
        #     pass
        # else:
        #     return False
if __name__ == '__main__':
   dloscs.iter_all_file(r'D:\DLO',30)