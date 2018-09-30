#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sqlite3,time,sys,io
from functools import reduce
from prettytable import PrettyTable
global DataBasePath,CurrentPath,CurrentTime
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
DataBaseFile = "Python.DLOES.db"
DataBasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataBaseFile)
CurrentPath = os.getcwd()
CurrentTime = time.time()

class DLOExtendService():

    def DatabaseAdapter(self, SQL, Data):
        try:
            ConnectDataBase = sqlite3.connect(DataBasePath)
            CursorDataBase = ConnectDataBase.cursor()
            if Data == None:
                SQL = CursorDataBase.execute(SQL)
                RawData = SQL.fetchall()
                return RawData
            else:
                CursorDataBase.execute(SQL, (Data,),)
                ConnectDataBase.commit()
                return True
        except:
            return False

    def GetExtensionList(self):
        try:
            ExtensionList = []
            for Data in DLOExtendService.DatabaseAdapter(self, SQL="SELECT * FROM EXTENSION", Data=None):
                ExtensionList.append(Data[0])
            return ExtensionList
        except:
            print("数据库连接失败")

    def UpdateExtension(self):
        AddOrDelExtension = input("Python.DLOES:当前目标扩展名为%s\n      按<1>添加扩展名\n      按<2>删除扩展名\n      或按任意键继续\nAdmin:"%DLOExtendService.GetExtensionList(self))
        if AddOrDelExtension == ("1"):
            DLOExtendService.AddExtension(self)
        elif AddOrDelExtension == ("2"):
            DLOExtendService.DelExtension(self)
        else:pass

    def AddExtension(self):
        ContinueOrQuite = input("Python.DLOES:按<1>回到上级菜单\n      或按任意键添加扩展名\nAdmin:")
        while ContinueOrQuite == ("1"):
            DLOExtendService.UpdateExtension(self)
        else:
            print('当前目标扩展名为:', DLOExtendService.GetExtensionList(self))
            NewExtension = input("Python.DLOES:请输入需要添加的扩展名\nAdmin:")
            if DLOExtendService.DatabaseAdapter(self, SQL="INSERT INTO EXTENSION(LIST) VALUES(?)",Data=NewExtension) == True:
                print("Python.DLOES:扩展名添加成功")
                DLOExtendService.AddExtension(self)
            else:
                print("Python.DLOES:扩展名添加失败")
                DLOExtendService.AddExtension(self)

    def DelExtension(self):
        ContinueOrQuite = input("Python.DLOES:按<1>回到上级菜单\n      或按任意键删除扩展名\nAdmin:")
        while ContinueOrQuite == ("1"):
            DLOExtendService.UpdateExtension(self)
        else:
            print(DLOExtendService.GetExtensionList(self))
            TargetExtension = input("Python.DLOES:请输入需要删除的扩展名\nAdmin:")
            if DLOExtendService.DatabaseAdapter(self, SQL="DELETE FROM EXTENSION WHERE LIST = (?)", Data=TargetExtension) == True:
                print("Python.DLOES:扩展名删除成功")
                DLOExtendService.DelExtension(self)
            else:print("Python.DLOES:扩展名删除失败")
            DLOExtendService.DelExtension(self)

    def GetTargetPath(self):
        GetPath = input("Python.DLOES:按<1>使用回到主菜单\n      按<2>自定义路径\n      或按任意键使用默认路径继续\nAdmin:")
        if GetPath == "1":
            DLOExtendService.CommandLineInterface(self)
        elif GetPath == "2":
            GetPath = input("Python.DLOES:请输入自定义路径\nAdmin:")
            if os.path.exists(GetPath) != False:
                return GetPath
            else:
                print("Python.DLOES:路径不存在或无法访问,请重试.")
                DLOExtendService.CommandLineInterface(self)
        else:
            if len(DLOExtendService.DatabaseAdapter(self, SQL="SELECT * FROM FILELOCATION", Data=None)) == 0:
                SetDefultPath = input("Python.DLOES:未找到默认路径,请设定默认路径\nAdmin:")
                if os.path.exists(SetDefultPath) != False:
                    if DLOExtendService.DatabaseAdapter(self,SQL="INSERT INTO FILELOCATION(PATH) VALUES(?)",Data=SetDefultPath) == True:
                        print("Python.DLOES:默认路径添加成功")
                        return SetDefultPath
                    else:
                        print("Python.DLOES:默认路径添加失败")
                        DLOExtendService.CommandLineInterface(self)
                else:
                    print("Python.DLOES:路径不存在或无法访问,请重试.")
                    DLOExtendService.CommandLineInterface(self)
            else:
               PathList = []
               for Data in DLOExtendService.DatabaseAdapter(self, SQL="SELECT * FROM FILELOCATION", Data=None):
                    PathList.append(Data[0])
               return PathList[-1]

    def GetLastRunTime(self):
        List = []
        for Data in DLOExtendService.DatabaseAdapter(self,SQL="SELECT * FROM LOGS",Data=None):
            List.append(Data[0])
        return List

    def GetTime(self):
        global ShowStartTime,ShowEndTime
        LastRunTime = DLOExtendService.GetLastRunTime(self)[-1]
        ChoiceForTime= input("Python.DLOES:按<1>回到主菜单\n      或按任意键设定开始与结束时间\nAdmin:")
        if ChoiceForTime == ('1'):DLOExtendService.CommandLineInterface(self)
        else:
            if input("Python.DLOES:上一次运行时间为%s是否使用此时间作为删除开始时间?(Y/N)\nAdmin:" % time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(LastRunTime))) in ['y', 'Y']:
                GetStartTime = LastRunTime
                FormatStartTime = time.strftime("%Y-%m-%d", time.localtime(LastRunTime))
                ShowStartTime = time.mktime(time.strptime(FormatStartTime, "%Y-%m-%d"))
            else:
                GetStartTime = input("Python.DLOES:请输入开始时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
                ShowStartTime = time.mktime(time.strptime(GetStartTime, "%Y-%m-%d"))
                try:
                    time.strptime(GetStartTime, "%Y-%m-%d")
                except:
                    print("Python.DLOES:PP输入的格式错误,请重试.")
                    DLOExtendService.CommandLineInterface(self)
            GetEndTime = input("Python.DLOES:请输入结束时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
            try:
                time.strptime(GetEndTime, "%Y-%m-%d")
                ShowEndTime = time.mktime(time.strptime(GetEndTime, "%Y-%m-%d"))
            except:
                print("Python.DLOES:LL输入的格式错误,请重试.")
                DLOExtendService.CommandLineInterface(self)
            if len(DLOExtendService.GetLastRunTime(self))<1:
                return [ShowStartTime, ShowEndTime, GetStartTime, GetEndTime]
            else:
                if ShowEndTime < ShowStartTime:
                    print("Python.DLOES:开始时间大于结束时间,请重试.")
                    DLOExtendService.GetTime(self)
                else:
                    if ShowStartTime or ShowEndTime < LastRunTime:
                        OverWriteExitesTime = input("Python.DLOES:开始时间或结束时间小于最后运行时间,是否仍然使用自定义时间?(Y/N)\nAdmin:")
                        if OverWriteExitesTime in ["y","Y"]:
                            return [ShowStartTime, ShowEndTime, GetStartTime, GetEndTime]
                        else:
                            print("Python.DLOES:请重试\nAdmin:")
                            DLOExtendService.GetTime(self)
                    else:return [ShowStartTime, ShowEndTime, GetStartTime, GetEndTime]

    def FunctionSelector(self):
        Choice = input("Python.DLOES:按<1>选择保留时间段内每个文件最后一个版本\n      按<2>选择删除时间段内所有版本\nAdmin:")
        if Choice == ("1"):
            return ['KLO',"保留时间段内每个文件最后一个版本"]
        elif Choice == ("2"):
            return ['DA',"删除时间段内所有版本"]
        else:DLOExtendService.CommandLineInterface(self)

    def CommandLineInterface(self):
        global NumberOfDeletedFiles,SizeOfDeletedFiles,Log
        NumberOfDeletedFiles = 0
        SizeOfDeletedFiles = 0
        LogTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
        LogPath = ("%s\Logs\[%s]Log.txt" % (CurrentPath, LogTime))
        Log = open(LogPath, 'w', encoding='utf-8')
        os.system('cls')
        if input("Python.DLOES:按<1>结束进程\n      或按任意键继续\nAdmin:") == "1":exit()
        else:pass
        SelectFunction = DLOExtendService.FunctionSelector(self)
        DLOExtendService.UpdateExtension(self)
        TargetPath = DLOExtendService.GetTargetPath(self)
        GetTime = DLOExtendService.GetTime(self)
        GetExtensionList = DLOExtendService.GetExtensionList(self)
        StartProcessTime = GetTime[0]
        EndProcessTime = GetTime[1]
        ShowStartTime = GetTime[2]
        ShowEndTime = GetTime[3]
        LogsPath = ("%s\Logs"%CurrentPath)
        DLOExtendService.LogMaintain(self,LogsPath)
        os.system('cls')
        ConformInfo = input('''Python.DLOES:请确认设定:
        \n      此操作将%s
        \n      目标文件夹及所有子文件夹:<<<%s>>>>
        \n      开始时间:<<<%s>>>>
        \n      结束时间:<<<%s>>>>
        \n      目标扩展名:<<<%s>>>
        \n      输入"conform"开始文件清除进程
        \n      或按任意键回到主菜单
        \nAdmin: ''' % (SelectFunction[1],TargetPath,ShowStartTime, ShowEndTime,GetExtensionList))
        if ConformInfo == ("conform"):pass
        else:DLOExtendService.CommandLineInterface(self)
        print("=======================Start=======================")
        # LogPath = (os.path.join(os.path.dirname(os.path.abspath(__file__)),'TempLog.txt'))
        if SelectFunction[0] == 'KLO':
            DLOExtendService.FileFilterKeepLatestVersion(self, TargetPath, StartProcessTime, EndProcessTime,GetExtensionList)
        elif SelectFunction[0] == 'DA':
            DLOExtendService.FileFilterDiscardAll(self, TargetPath, StartProcessTime, EndProcessTime,GetExtensionList)
        print(('''\n+++++++++++++++++++++++++++++++++++++++
		\n共删除%s个文件
		\n已释放%sMB磁盘空间
		\n%s
		\n+++++++++++++++++++++++++++++++++++++++
                ''' % (NumberOfDeletedFiles, int(SizeOfDeletedFiles / 1024 / 1024),DLOExtendService.LogRunTime(self))))
        Log.close()
        print("+++++++++++++++++++++++Done++++++++++++++++++++++++")
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

    def FileFilterKeepLatestVersion(self, RootPath, StartDate, EndDate,ExtensionList):
        global NumberOfDeletedFiles,AllFileInFolder,FilesGroup,SizeOfDeletedFiles
        AllFileInFolder = []
        FilesGroup = []
        for Object in os.listdir(RootPath):
            FilePath = os.path.join(RootPath, Object)
            if os.path.isdir(FilePath):
                DLOExtendService.FileFilterKeepLatestVersion(self, FilePath, StartDate, EndDate,ExtensionList)
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
                        AllFileInFolder.append(RawPackage)
                else:pass
        for EachFile in sorted(AllFileInFolder, key=lambda FileName: FileName[0]):
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

    def FileFilterDiscardAll(self, RootPath, StartDate, EndDate,ExtensionList):
        for Obeject in os.listdir(RootPath):
            FilePath = os.path.join(RootPath, Obeject)
            if os.path.isfile(FilePath):
                if (os.path.splitext(FilePath)[1] in ExtensionList) and\
                        (StartDate < int(os.path.getctime(FilePath)) < EndDate):
                    DLOExtendService.DeleteExpiredFile(self,FilePath)
                else:pass
            elif os.path.isdir(FilePath):
                DLOExtendService.FileFilterDiscardAll(self, FilePath, StartDate, EndDate,ExtensionList)

    def DeleteExpiredFile(self, FilePath):
        global NumberOfDeletedFiles,SizeOfDeletedFiles
        NumberOfDeletedFiles += 1
        try:
            os.path.getsize(FilePath)
            FileSize = os.path.getsize(FilePath)
            SizeOfDeletedFiles += FileSize
            print('--File deleted-->>>', FilePath)
            Log.write(FilePath)
            Log.write("\n")
            # try:
            #     os.remove(FilePath)
            #     print("--File deleted-->>>", FilePath)
            # except:
            #     print("File Cant Be Removed")
        except:pass

    def LogRunTime(self):
        try:
            if DLOExtendService.DatabaseAdapter(self, SQL="INSERT INTO LOGS(LASTRUNTIME) VALUES(?)", Data=CurrentTime) == True:
                return ("运行时间更新成功")
        except:
            return ("运行时间更新失败")

    def LogMaintain(self,FilePath,FolderSize=0):
        for Root, Dirs, Files in os.walk(FilePath):
            for File in Files:
                FolderSize += os.path.getsize(os.path.join(Root, File))
        if FolderSize > 10240:
            Choice = input("Python.DLOES:日志文件大小依超过10MB,是否进行日志清除?(Y/N)\nAdmin:")
            if Choice in ["y","Y"]:
                StartTime = 1459175064.0
                EndTime = time.time()
                ExtensionList = ['.txt']
                DLOExtendService.FileFilterDiscardAll(self,FilePath,StartTime,EndTime,ExtensionList)
            else:pass
        else:pass

if __name__ == '__main__':
    DLOExtendService.CommandLineInterface(object)


