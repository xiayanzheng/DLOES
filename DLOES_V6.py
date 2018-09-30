#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sqlite3,time
from functools import reduce
global DataBasePath
DataBaseFile = "dloes.db"
DataBasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataBaseFile)

class DLOExtendService():
    def ExtensionListDataSource(self):
        RawData = DLOExtendService.ReadDataBase(self, SQL="SELECT * FROM extension")
        ExtensionList = []
        for data in RawData:
            ExtensionList.append(data[0])
        return ExtensionList

    def CommandLineInterface(self):
        global GetStartTime,GetEndTime,NumberOfDeletedFiles
        ContinueOrQuite = input("DLOSCS:按<1>开始进程--|--按任意键结束进程\nAdmin:")
        if ContinueOrQuite == "1":pass
        else:exit()
        GetTargetPath = input("DLOSCS:按<1>使用默认路径--|--按<2>自定义路径--|--按任意键回到主菜单\nAdmin:")
        if GetTargetPath == "1":GetTargetPath = "E:\Resources\视频"
        elif GetTargetPath == "2":
            GetTargetPath = input("DLOSCS:请输入自定义路径\nAdmin:")
            if os.path.exists(GetTargetPath) != False:
                GetTargetPathInput = GetTargetPath
            else:
                print("DLOSCS:路径不存在或无法访问,请重试.")
                DLOExtendService.CommandLineInterface(self)
        else:DLOExtendService.CommandLineInterface(self)
        ChoiceForTime= input("DLOSCS:按<1>设定开始与结束时间--|--按任意键回到主菜单\nAdmin:")
        if ChoiceForTime == ('1'):
            GetStartTime = input("DLOSCS:请输入开始时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
            GetEndTime = input("DLOSCS:请输入结束时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
        else:DLOExtendService.CommandLineInterface(self)
        try:
            time.strptime(GetStartTime, "%Y-%m-%d")
            time.strptime(GetEndTime, "%Y-%m-%d")
            StartTime = time.mktime(time.strptime(GetStartTime, "%Y-%m-%d"))
            EndTime = time.mktime(time.strptime(GetEndTime, "%Y-%m-%d"))
            if EndTime < StartTime:
                print("DLOSCS:开始时间大于结束时间,请重试.")
                DLOExtendService.CommandLineInterface(self)
        except:
            print("DLOSCS:输入的格式错误,请重试.")
            DLOExtendService.CommandLineInterface(self)
        ConformInfo = input('''请确认设定:\n目标文件夹及所有子文件夹:<<<%s>>>>\n开始时间:<<<%s>>>>\n结束时间:<<<%s>>>>\n输入"conform"开始文件清除进程\nAdmin: ''' % (GetTargetPath, GetStartTime, GetEndTime))
        if ConformInfo == ("conform"):
            pass
        else:
            print("DLOSCS:输入错误,请重试.")
            DLOExtendService.CommandLineInterface(self)
        RootPath = GetTargetPath
        StartTime = time.mktime(time.strptime(GetStartTime, "%Y-%m-%d"))
        EndTime = time.mktime(time.strptime(GetEndTime, "%Y-%m-%d"))
        NumberOfDeletedFiles = 0
        print("=======================Start=======================")
        DLOExtendService.FileFilter(self, RootPath, StartTime, EndTime)
        print("+++++++++++++++++++++++Done++++++++++++++++++++++++")
        print(NumberOfDeletedFiles)

        # # ########################Shortcut For Dev########################
        # start_time_source ='2017-01-01'
        # StartTime = time.mktime(time.strptime(start_time_source,"%Y-%m-%d"))
        # end_time_source ='2017-10-25'
        # EndTime = time.mktime(time.strptime(end_time_source,"%Y-%m-%d"))
        # # RootPath = 'E:\Resources\视频'
        # RootPath = 'E:\Resources'
        # NumberOfDeletedFiles = 0
        # DLOExtendService.FileFilterKeepLatestVersion(self, RootPath, StartTime, EndTime)
        # print(NumberOfDeletedFiles)
        # # ########################Shortcut For Dev########################

    def FileFilter(self, RootPath, StartDate, EndDate):
        global NumberOfDeletedFiles,LoadAllFileInFolder,GroupFiles
        ExtensionList = DLOExtendService.ExtensionListDataSource(self)
        LoadAllFileInFolder = []
        GroupFiles = []
        for Object in os.listdir(RootPath):
            FilePath = os.path.join(RootPath, Object)
            if os.path.isdir(FilePath):
                DLOExtendService.FileFilter(self, FilePath, StartDate, EndDate)
            elif os.path.isfile(FilePath):
                # del DedupeFilePathContain[:]
                CreateTime = os.path.getctime(FilePath)
                if (os.path.splitext(FilePath)[1] in ExtensionList) and (StartDate < CreateTime < EndDate):
                    Compare = Object.split("]")
                    del Compare[0]
                    if len(Compare) < 1:pass
                    else:
                        Compare = reduce(lambda x, y: x + y, Compare)
                        RawPackage = (Compare,CreateTime,FilePath)
                        LoadAllFileInFolder.append(RawPackage)
                else:pass
        for EachFile in sorted(LoadAllFileInFolder, key=lambda FileName: FileName[0]):
            if len(GroupFiles) < 1:GroupFiles.append(EachFile)
            else:
                if EachFile[0] == GroupFiles[0][0]:GroupFiles.append(EachFile)
                else:
                    if len(GroupFiles) < 1: pass
                    else:
                        SortByTime = sorted(GroupFiles, key=lambda FileCreateTime: FileCreateTime[1])
                        del SortByTime[-1]
                        for TargetFile in SortByTime:
                            DLOExtendService.DeleteExpiredFile(self,TargetFile[-1])
                            NumberOfDeletedFiles += 1
                    del GroupFiles[:]
                    GroupFiles.append(EachFile)
        if len(GroupFiles) < 1: pass
        else:
            SortByTime = sorted(GroupFiles, key=lambda FileCreateTime: FileCreateTime[1])
            del SortByTime[-1]
            for TargetFile in SortByTime:
                DLOExtendService.DeleteExpiredFile(self,TargetFile[-1])
                NumberOfDeletedFiles += 1

    def DeleteExpiredFile(self, FilePath):
        print('--File deleted-->>>', FilePath)
        # try:
        #     os.remove(file_path)
        #     print("Deleting",file_path)
        # except Exception as e:
        #     log.writelog(e,'CRITICAL')

    def ReadDataBase(self, SQL):
        ConnectDataBase = sqlite3.connect(DataBasePath)
        CursorDataBase = ConnectDataBase.cursor()
        SQL = CursorDataBase.execute(SQL)
        return SQL.fetchall()

    def WriteDataBase(self, DataBaseSQL, Data):
        ConnectDataBase = sqlite3.connect(DataBasePath)
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

if __name__ == '__main__':
    DLOExtendService.CommandLineInterface(object)


