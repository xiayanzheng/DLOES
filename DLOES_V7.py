#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sqlite3,time
from functools import reduce
from prettytable import PrettyTable
global DataBasePath,UnRemovableFileLog
DataBaseFile = "dloes.db"
DataBasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataBaseFile)
UnRemovableFileLog = 'Log.txt'
UnRemovableFileLogPath = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), UnRemovableFileLog), 'w')

class DLOExtendService():

    def CommandLineInterface(self):
        global GetStartTime,GetEndTime,NumberOfDeletedFiles,SizeOfDeletedFiles
        ContinueOrQuite = input("Python.DLOES:按<1>结束进程\n      或按任意键继续\nAdmin:")
        if ContinueOrQuite == "1":exit()
        else:pass
        print('当前目标扩展名为:', DLOExtendService.GetExtensionList(self))
        AddOrDelExtension = input("Python.DLOES:按<1>添加扩展名\n      按<2>删除扩展名\n      或按任意键继续\nAdmin:")
        if AddOrDelExtension == ("1"):
            DLOExtendService.AddExtension(self)
        elif AddOrDelExtension == ("2"):
            DLOExtendService.DelExtension(self)
        else:pass
        GetTargetPath = input("Python.DLOES:按<1>使用默认路径\n      按<2>自定义路径\n      或按任意键继续\nAdmin:")
        if GetTargetPath == "1":GetTargetPath = "E:\Resources\视频"
        elif GetTargetPath == "2":
            GetTargetPath = input("Python.DLOES:请输入自定义路径\nAdmin:")
            if os.path.exists(GetTargetPath) != False:
                GetTargetPathInput = GetTargetPath
            else:
                print("Python.DLOES:路径不存在或无法访问,请重试.")
                DLOExtendService.CommandLineInterface(self)
        else:pass
        ChoiceForTime= input("Python.DLOES:按<1>回到主菜单\n      或按任意键设定开始与结束时间\nAdmin:")
        if ChoiceForTime == ('1'):DLOExtendService.CommandLineInterface(self)
        else:
            GetStartTime = input("Python.DLOES:请输入开始时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
            GetEndTime = input("Python.DLOES:请输入结束时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
        try:
            time.strptime(GetStartTime, "%Y-%m-%d")
            time.strptime(GetEndTime, "%Y-%m-%d")
            StartTime = time.mktime(time.strptime(GetStartTime, "%Y-%m-%d"))
            EndTime = time.mktime(time.strptime(GetEndTime, "%Y-%m-%d"))
            if len(DLOExtendService.GetLastRunTime(self))<1:pass
            else:
                if StartTime or EndTime < DLOExtendService.GetLastRunTime(self)[-1]:
                    print("Python.DLOES:开始时间或结束时间小于最后运行时间.")
                    DLOExtendService.CommandLineInterface(self)
                elif EndTime < StartTime:
                    print("Python.DLOES:开始时间大于结束时间,请重试.")
                    DLOExtendService.CommandLineInterface(self)
        except:
            print("Python.DLOES:输入的格式错误,请重试.")
            DLOExtendService.CommandLineInterface(self)
        os.system('cls')
        ConformInfo = input('''Python.DLOES:请确认设定:
        \n      目标文件夹及所有子文件夹:<<<%s>>>>
        \n      开始时间:<<<%s>>>>
        \n      结束时间:<<<%s>>>>
        \n      输入"conform"开始文件清除进程
        \n      或按任意键回到主菜单
        \nAdmin: ''' % (GetTargetPath, GetStartTime, GetEndTime))
        if ConformInfo == ("conform"):
            pass
        else:
            print("Python.DLOES:输入错误,请重试.")
            DLOExtendService.CommandLineInterface(self)
        RootPath = GetTargetPath
        StartTime = time.mktime(time.strptime(GetStartTime, "%Y-%m-%d"))
        EndTime = time.mktime(time.strptime(GetEndTime, "%Y-%m-%d"))
        NumberOfDeletedFiles = 0
        print("=======================Start=======================")
        DLOExtendService.FileFilterKeepLatestVersion(self, RootPath, StartTime, EndTime)
        print("+++++++++++++++++++++++Done++++++++++++++++++++++++")
        NumberOfDeletedFiles = 0
        SizeOfDeletedFiles = 0
        Result = (''''
                +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                                          共删除%s个文件
                                        已释放%sMB磁盘空间
                                              %s
                +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                ''' % (NumberOfDeletedFiles, int(SizeOfDeletedFiles / 1024 / 1024),DLOExtendService.LogRunTime(self)))
        print(Result)
        os.system('pause')

        # # ########################Shortcut For Dev########################
        # start_time_source ='2017-01-01'
        # StartTime = time.mktime(time.strptime(start_time_source,"%Y-%m-%d"))
        # end_time_source ='2017-10-25'
        # EndTime = time.mktime(time.strptime(end_time_source,"%Y-%m-%d"))
        # RootPath = 'E:\Resources\视频'
        # # RootPath = 'E:\Resources'
        # NumberOfDeletedFiles = 0
        # SizeOfDeletedFiles = 0
        # DLOExtendService.FileFilterKeepLatestVersion(self, RootPath, StartTime, EndTime)
        # Result = ('''
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                          共删除%s个文件
        #                        已释放%sMB磁盘空间
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ''' % (NumberOfDeletedFiles,int(SizeOfDeletedFiles / 1024 / 1024)))
        # print(Result)
        # # ########################Shortcut For Dev########################

    def FileFilterKeepLatestVersion(self, RootPath, StartDate, EndDate):
        global NumberOfDeletedFiles,LoadAllFileInFolder,FilesGroup,SizeOfDeletedFiles
        ExtensionList = DLOExtendService.GetExtensionList(self)
        LoadAllFileInFolder = []
        FilesGroup = []
        for Object in os.listdir(RootPath):
            FilePath = os.path.join(RootPath, Object)
            if os.path.isdir(FilePath):
                DLOExtendService.FileFilterKeepLatestVersion(self, FilePath, StartDate, EndDate)
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
            if len(FilesGroup) < 1:FilesGroup.append(EachFile)
            else:
                if EachFile[0] == FilesGroup[0][0]:FilesGroup.append(EachFile)
                else:
                    if len(FilesGroup) < 1: pass
                    else:
                        SortByTime = sorted(FilesGroup, key=lambda FileCreateTime: FileCreateTime[1])
                        del SortByTime[-1]
                        for TargetFile in SortByTime:
                            DLOExtendService.DeleteExpiredFile(self,TargetFile[-1])
                    del FilesGroup[:]
                    FilesGroup.append(EachFile)
        if len(FilesGroup) < 1: pass
        else:
            SortByTime = sorted(FilesGroup, key=lambda FileCreateTime: FileCreateTime[1])
            del SortByTime[-1]
            for TargetFile in SortByTime:
                DLOExtendService.DeleteExpiredFile(self,TargetFile[-1])

    def FileFilterDiscardAll(self, RootPath, StartDate, EndDate):
        ExtensionList = DLOExtendService.GetExtensionList(self)
        for Obeject in os.listdir(RootPath):
            FilePath = os.path.join(RootPath, Obeject)
            if os.path.isfile(FilePath):
                if (os.path.splitext(FilePath)[1] in ExtensionList) and\
                        (StartDate < int(os.path.getctime(FilePath)) < EndDate):
                    DLOExtendService.DeleteExpiredFile(self,FilePath)
                else:pass
            elif os.path.isdir(FilePath):
                DLOExtendService.FileFilterDiscardAll(self, FilePath, StartDate, EndDate)

    def DeleteExpiredFile(self, FilePath):
        global NumberOfDeletedFiles,SizeOfDeletedFiles
        NumberOfDeletedFiles += 1
        FileSize = os.path.getsize(FilePath)
        SizeOfDeletedFiles += FileSize
        print('--File deleted-->>>', FilePath)
        # try:
        #     os.remove(FilePath)
        #     print("Deleting",FilePath)
        # except Exception as e:
        #     UnRemovableFileLogPath.write(e,'CRITICAL')

    def GetLastRunTime(self):
        ConnectDataBase = sqlite3.connect(DataBasePath)
        CursorDataBase = ConnectDataBase.cursor()
        SQL = CursorDataBase.execute("SELECT * FROM LOGS")
        RawData = SQL.fetchall()
        List = []
        for Data in RawData:
            List.append(Data[0])
        return List

    def LogRunTime(self):
        try:
            CurrentTime = time.time()
            ConnectDataBase = sqlite3.connect(DataBasePath)
            CursorDataBase = ConnectDataBase.cursor()
            # Create table
            # c.execute('''Create TABLE if not exists sql_target_table("NA")''')
            # Insert links into table
            CursorDataBase.execute("INSERT INTO LOGS(LASTRUNTIME) VALUES(?)", (CurrentTime,), )
            ConnectDataBase.commit()
            Result = ("运行时间更新成功")
            return Result
        except:
            Result = ("运行时间更新失败")
            return Result

    def GetExtensionList(self):
        try:
            ConnectDataBase = sqlite3.connect(DataBasePath)
            CursorDataBase = ConnectDataBase.cursor()
            SQL = CursorDataBase.execute("SELECT * FROM extension")
            RawData = SQL.fetchall()
            ExtensionList = []
            for Data in RawData:
                ExtensionList.append(Data[0])
            return ExtensionList
        except:
            print("数据库连接失败")

    def AddExtension(self):
        ConformExtension = input("Python.DLOES:按<1>更新扩展名列表\n      按任意键继续\nAdmin:")
        if ConformExtension == '1':
            ContinueOrQuite = input("Python.DLOES:按<1>开始添加扩展名\n      或按任意键继续\nAdmin:")
            while ContinueOrQuite == ("1"):
                print('当前目标扩展名为:', DLOExtendService.GetExtensionList(self))
                NewExtension = input("Python.DLOES:请输入需要添加的扩展名\nAdmin:")
                try:
                    ConnectDataBase = sqlite3.connect(DataBasePath)
                    CursorDataBase = ConnectDataBase.cursor()
                    # Create table
                    # c.execute('''Create TABLE if not exists sql_target_table("NA")''')
                    # Insert links into table
                    CursorDataBase.execute("INSERT INTO EXTENSION(LIST) VALUES(?)", (NewExtension,), )
                    ConnectDataBase.commit()
                    print("Python.DLOES:更新成功")
                    DLOExtendService.AddExtension(self)
                except:
                    print("Python.DLOES:更新失败")
        else:DLOExtendService.CommandLineInterface(self)

    def DelExtension(self):
        ConformExtension = input("Python.DLOES:按<1>更新扩展名列表\n      按任意键继续\nAdmin:")
        if ConformExtension == '1':
            ContinueOrQuite = input("Python.DLOES:按<1>开始删除扩展名\n      或按任意键继续\nAdmin:")
            while ContinueOrQuite == ("1"):
                print(DLOExtendService.GetExtensionList(self))
                TargetExtension = input("Python.DLOES:请输入需要删除的扩展名\nAdmin:")
                try:
                    ConnectDataBase = sqlite3.connect(DataBasePath)
                    CursorDataBase = ConnectDataBase.cursor()
                    CursorDataBase.execute("DELETE FROM EXTENSION WHERE LIST = (?)", (TargetExtension,), )
                    ConnectDataBase.commit()
                    print("Python.DLOES:更新成功")
                    DLOExtendService.DelExtension(self)
                except:
                    print("Python.DLOES:更新失败")
        else:DLOExtendService.CommandLineInterface(self)


if __name__ == '__main__':
    DLOExtendService.CommandLineInterface(object)


