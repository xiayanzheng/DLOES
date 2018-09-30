#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,time,sqlite3,difflib,hashlib,sys
from stat import S_ISREG, ST_CTIME, ST_MODE

class DLOExtendService():
    def ExtensionListDataSource(self):
        RawData = DLOExtendService.ReadDataBase(self=None, SQL="SELECT * FROM extension")
        ExtensionList = []
        for data in RawData:
            ExtensionList.append(data[0])
        return ExtensionList

    def CommandLineInterface(self):
        global GetTargetPathInput,GetStartTime,GetEndTime,NumberOfDeletedFiles
        # ContinueOrQuite = input("DLOSCS:按<1>开始进程--|--按任意键结束进程\nAdmin:")
        # if ContinueOrQuite == "1":pass
        # else:exit()
        # GetTargetPath = input("DLOSCS:按<1>使用默认路径--|--按<2>自定义路径--|--按任意键回到主菜单\nAdmin:")
        # if GetTargetPath == "1":GetTargetPath = "E:\Resources\视频"
        # elif GetTargetPath == "2":
        #     GetTargetPath = input("DLOSCS:请输入自定义路径\nAdmin:")
        #     if os.path.exists(GetTargetPath) != False:
        #         GetTargetPathInput = GetTargetPath
        #     else:
        #         print("DLOSCS:路径不存在或无法访问,请重试.")
        #         DLOExtendService.Flow(self)
        # else:DLOExtendService.Flow(self)
        # ChoiceForTime= input("DLOSCS:按<1>设定开始与结束时间--|--按任意键回到主菜单\nAdmin:")
        # if ChoiceForTime == ('1'):
        #     GetStartTime = input("DLOSCS:请输入开始时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
        #     GetEndTime = input("DLOSCS:请输入结束时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
        # else:DLOExtendService.Flow(self)
        # try:
        #     time.strptime(GetStartTime, "%Y-%m-%d")
        #     time.strptime(GetEndTime, "%Y-%m-%d")
        #     StartTime = time.mktime(time.strptime(GetStartTime, "%Y-%m-%d"))
        #     EndTime = time.mktime(time.strptime(GetEndTime, "%Y-%m-%d"))
        #     if EndTime < StartTime:
        #         print("DLOSCS:开始时间大于结束时间,请重试.")
        #         DLOExtendService.Flow(self)
        # except:
        #     print("DLOSCS:输入的格式错误,请重试.")
        #     DLOExtendService.Flow(self)
        # ConformInfo = input('''请确认设定:\n目标文件夹及所有子文件夹:<<<%s>>>>\n开始时间:<<<%s>>>>\n结束时间:<<<%s>>>>\n输入"conform"开始文件清除进程\nAdmin: ''' % (GetTargetPath, GetStartTime, GetEndTime))
        # if ConformInfo == ("conform"):
        #     pass
        # else:
        #     print("DLOSCS:输入错误,请重试.")
        #     DLOExtendService.Flow(self)
        # RootPath = GetTargetPath
        # StartTime = time.mktime(time.strptime(GetStartTime, "%Y-%m-%d"))
        # EndTime = time.mktime(time.strptime(GetEndTime, "%Y-%m-%d"))
        # NumberOfDeletedFiles = 0
        # print("=======================Start=======================")
        # DLOExtendService.FileFilterKeepLatestVersion(self, RootPath, StartTime, EndTime)
        # print("+++++++++++++++++++++++Done++++++++++++++++++++++++")
        # print(NumberOfDeletedFiles)

        # ########################Shortcut For Dev########################
        start_time_source ='2017-01-01'
        StartTime = time.mktime(time.strptime(start_time_source,"%Y-%m-%d"))
        end_time_source ='2017-10-10'
        EndTime = time.mktime(time.strptime(end_time_source,"%Y-%m-%d"))
        RootPath = 'E:\Resources'
        NumberOfDeletedFiles = 0
        DLOExtendService.FileFilter(self, RootPath, StartTime, EndTime)
        print(NumberOfDeletedFiles)
        # ########################Shortcut For Dev########################

    def FileFilter(self, RootPath, StartDate, EndDate):
        global NumberOfDeletedFiles
        ExtensionList = DLOExtendService.ExtensionListDataSource(self)
        DedupeFilePathContain = []
        SortFilesByCreateTime = lambda File: os.stat(os.path.join(RootPath, File)).st_ctime
        # for Object in list(sorted(os.listdir(RootPath), key=SortFilesByCreateTime)):
        for Object in os.listdir(RootPath):
            FilePath = os.path.join(RootPath, Object)
            if len(DedupeFilePathContain) < 1:pass
            else:
                if difflib.SequenceMatcher(None, Object, DedupeFilePathContain[-1]).ratio() > 0.4:
                    TargetPath = os.path.join(DedupeFilePathContain[0], DedupeFilePathContain[1])
                    DLOExtendService.DeleteExpiredFile(self, TargetPath)
                    NumberOfDeletedFiles += 1
                else:pass
            if os.path.isfile(FilePath):
                del DedupeFilePathContain[:]
                if (os.path.splitext(FilePath)[1] in ExtensionList) and (StartDate < int(os.path.getctime(FilePath)) < EndDate):
                    DedupeFilePathContain.append(RootPath)
                    DedupeFilePathContain.append(Object)
                else:pass
            elif os.path.isdir(FilePath):
                DLOExtendService.FileFilter(self, FilePath, StartDate, EndDate)

    def DeleteExpiredFile(self, FilePath):
        print('--File deleted-->>>', FilePath)
        # try:
        #     os.remove(file_path)
        #     print("Deleting",file_path)
        # except Exception as e:
        #     log.writelog(e,'CRITICAL')

    def ReadDataBase(self, SQL):
        GetCurrentPath = os.getcwd()
        # AbsPath = os.path.abspath()
        ConnectDataBase = sqlite3.connect("%s\dloes.db" % GetCurrentPath)
        CursorDataBase = ConnectDataBase.cursor()
        SQL = CursorDataBase.execute(SQL)
        return SQL.fetchall()

    def WriteDataBase(self, DataBaseSQL, Data):
        GetCurrentPath = os.getcwd()
        ConnectDataBase = sqlite3.connect("%s\dloes.db" % GetCurrentPath)
        CursorDataBase = ConnectDataBase.cursor()
        #Create table
        # c.execute('''Create TABLE if not exists sql_target_table("NA")''')
        #Insert links into table
        CursorDataBase.execute(DataBaseSQL, Data)
        ConnectDataBase.commit()

    def GetLastColumn(self, data):
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
                        size_md5[file_size].append(DLOExtendService.Getfilemd5(size_md5[file_size][0]))
                    # 计算本文件的md5值
                    now_md5 = DLOExtendService.Getfilemd5(file_path)
                    if now_md5 in size_md5[file_size]:  # 不用怕，MD5值不会和保存的文件路径匹配，因为路径中有\等字符。
                        # 发现相同文件，删除
                        print("delete" + file_path)
                        os.remove(file_path)
                    else:
                        size_md5[file_size].append(now_md5)
                else:
                    size_md5[file_size] = filepath_and_md5

if __name__ == '__main__':
    DLOExtendService.CommandLineInterface(object)


