import os,time

'''
:Sync FileExtension from DLO Database to Sqlite (optional)
:Read Config From SqliteDB,includ(ExpireDate,TargetPath,FileExtension,Property)
:Create CheckList [ExpireDate,FileExtension,
    (Property:For example [434124DT]Timetable.Xlsx "[434124DT]" is Property we called)]
:Locate TargetPath by Value TargetPath from Sqlite
:Read File's CreateTime,
'''

def cleanfile(path,expiredTime):
    for obj in os.listdir(path):
        objpath = os.path.join(path,obj)
        if os.path.isfile(objpath):
            delExpiredfile(objpath,expiredTime)
        elif os.path.isdir(objpath):
            cleanfile(objpath,expiredTime)

def delExpiredfile(filepath,expiredTime):
    expiredsec =  expiredTime * 24 * 3600
    stat_result =  os.stat(filepath)
    ctime =  stat_result.st_mtime
    ntime = time.time()
    if (ntime-ctime)>expiredsec:
        try:
            os.remove(filepath)
        # except Exception as e:
        #     log.writelog(e,'CRITICAL')
        except:
            pass
    else:
        return False
if __name__ == '__main__':
   cleanfile(r'E:\TEST',2)