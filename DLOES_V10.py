#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os,sqlite3,time,sys,io
from functools import reduce
from prettytable import PrettyTable
global DataBasePath
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gb18030')
DataBaseFile = "Python.DLOES.db"
DataBasePath = os.path.join(os.path.dirname(os.path.abspath(__file__)), DataBaseFile)
CurrentPath = os.getcwd()

class DLOExtendService(object):
    NumberOfDeletedFiles = 0
    SizeOfDeletedFiles = 0
    LogTime = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    LogPath = ("%s\Logs\{%s}Log.txt" % (CurrentPath, LogTime))
    Log = open(LogPath, 'w', encoding='utf-8')
    TimeList = []

    def __init__(self, NumberOfDeletedFiles, SizeOfDeletedFiles, Log,TimeList):
        self.NumberOfDeletedFiles = NumberOfDeletedFiles
        self.SizeOfDeletedFiles = SizeOfDeletedFiles
        self.Log = Log
        self.TimeList = TimeList

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

    def Get(self,Mode):
        if Mode == ("ExtensionList"):
            try:
                ExtensionList = []
                for Data in DLOExtendService.DatabaseAdapter(self, SQL="SELECT * FROM EXTENSION", Data=None):
                    ExtensionList.append(Data[0])
                return ExtensionList
            except:
                print("数据库连接失败")
        if Mode == ("TargetPath"):
            if len(DLOExtendService.DatabaseAdapter(self, SQL="SELECT * FROM FILELOCATION", Data=None)) == 0:
                SetDefultPath = input("Python.DLOES:未找到默认路径,请设定默认路径\nAdmin:")
                if os.path.exists(SetDefultPath) != False:
                    if DLOExtendService.DatabaseAdapter(self, SQL="INSERT INTO FILELOCATION(PATH) VALUES(?)",
                                                        Data=SetDefultPath) == True:
                        print("Python.DLOES:默认路径添加成功")
                        DLOExtendService.Get(self,"TargetPath")
                    else:
                        print("Python.DLOES:默认路径添加失败")
                        DLOExtendService.Flow(self)
                else:
                    print("Python.DLOES:路径不存在或无法访问,请重试.")
                    DLOExtendService.Get(self, "TargetPath")
            else:
                PathList = []
                for Data in DLOExtendService.DatabaseAdapter(self, SQL="SELECT * FROM FILELOCATION", Data=None):
                    PathList.append(Data[0])
            GetPath = input("Python.DLOES:当前默认路径为<<%s>>\n      "
                            "按<1>使用回到主菜单\n      "
                            "按<2>自定义路径\n      "
                            "按<3>更新默认路径\n      "
                            "或按任意键使用默认路径继续\nAdmin:"% PathList[-1])
            if GetPath == "1":DLOExtendService.Flow(self)
            elif GetPath == "2":
                GetPath = input("Python.DLOES:请输入自定义路径\nAdmin:")
                if os.path.exists(GetPath) != False:
                    return GetPath
                else:
                    print("Python.DLOES:路径不存在或无法访问,请重试.")
                    DLOExtendService.Flow(self)
            elif GetPath == "3":
                UpdateDefaultPath = input("Python.DLOES:请输入新默认路径\nAdmin:")
                if os.path.exists(UpdateDefaultPath) != False:
                    if DLOExtendService.DatabaseAdapter(self, SQL="UPDATE FILELOCATION SET PATH = (?)",
                                                        Data=UpdateDefaultPath) == True:
                        print("Python.DLOES:默认路径更新成功")
                        DLOExtendService.Get(self,"TargetPath")
                    else:
                        print("Python.DLOES:默认路径更新失败")
                        DLOExtendService.Flow(self)
                else:
                    print("Python.DLOES:路径不存在或无法访问,请重试.")
                    DLOExtendService.Get(self, "TargetPath")

            else:return PathList[-1]
        if Mode == ("LastRunTime"):
            List = []
            for Data in DLOExtendService.DatabaseAdapter(self, SQL="SELECT * FROM LOGS", Data=None):
                List.append(Data[0])
            return List
        if Mode == ("Mode"):
            Choice = input("Python.DLOES:按<1>选择保留时间段内每个文件最后一个版本\n      按<2>选择删除时间段内所有版本\nAdmin:")
            if Choice == ("1"):
                return ['KLO', "保留时间段内每个文件最后一个版本"]
            elif Choice == ("2"):
                return ['DA', "删除时间段内所有版本"]
            else:
                print("Python.DLOES:未知选择项")
                DLOExtendService.Get(self,"Mode")
        if Mode == ("Time"):
            # global IntStartTime,IntEndTime,StrStartTime,StrEndTime,LastRunTime
            if input("Python.DLOES:按<1>回到主菜单\n      或按任意键设定开始与结束时间\nAdmin:") == ('1'):
                DLOExtendService.Flow(self)
            else:
                try:
                    LastRunTime = DLOExtendService.Get(self, "LastRunTime")[-1]
                    if input("Python.DLOES:上一次运行时间为%s是否使用此时间作为删除开始时间?(Y/N)\nAdmin:" % LastRunTime) in ['y', 'Y']:
                        # ShowStartTime = time.strftime("%Y-%m-%d", time.localtime(LastRunTime))
                        DLOExtendService.TimeList.append(time.mktime(time.strptime(LastRunTime, "%Y-%m-%d")))
                    else:
                        StrStartTime = input("Python.DLOES:请输入开始时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
                        try:
                            DLOExtendService.TimeList.append(time.mktime(time.strptime(StrStartTime, "%Y-%m-%d")))
                        except:
                            print("Python.DLOES:开始时间输入的格式错误,请重试.")
                            DLOExtendService.Get(self,"Time")
                except:pass
                if input("Python.DLOES:是否使用当前时间作为结束时间?(Y/N)\nAdmin:") in  ['y', 'Y']:
                    DLOExtendService.TimeList.append(time.time())
                else:
                    StrEndTime = input("Python.DLOES:请输入结束时间【!格式必须为YYYY-MM-DD!】\nAdmin:")
                    try:
                        DLOExtendService.TimeList.append(time.mktime(time.strptime(StrEndTime, "%Y-%m-%d")))
                    except:
                        print("Python.DLOES:结束时间输入的格式错误,请重试.")
                        DLOExtendService.Get(self, "Time")
                if DLOExtendService.TimeList[0] > DLOExtendService.TimeList[1]:
                    print("Python.DLOES:开始时间大于结束时间,请重试.")
                    DLOExtendService.Get(self, "Time")
                else:
                    try:
                        LastRunTime = DLOExtendService.Get(self, "LastRunTime")[-1]
                        if DLOExtendService.TimeList[0] or DLOExtendService.TimeList[1] < LastRunTime:
                            OverWriteExitesTime = input("Python.DLOES:开始时间或结束时间小于最后运行时间,是否仍然使用自定义时间?(Y/N)\nAdmin:")
                            if OverWriteExitesTime in ["y", "Y"]:
                                return [DLOExtendService.TimeList[0],DLOExtendService.TimeList[1],
                                        time.strftime("%Y-%m-%d", time.localtime(DLOExtendService.TimeList[0])),
                                        time.strftime("%Y-%m-%d", time.localtime(DLOExtendService.TimeList[1]))]
                            else:
                                print("Python.DLOES:请重试\nAdmin:")
                                DLOExtendService.Get(self, "Time")
                    except:
                        return [DLOExtendService.TimeList[0], DLOExtendService.TimeList[1],
                                time.strftime("%Y-%m-%d", time.localtime(DLOExtendService.TimeList[0])),
                                time.strftime("%Y-%m-%d", time.localtime(DLOExtendService.TimeList[1]))]

    def UpdateExtension(self,Selection):
        if Selection == "Add":
            ContinueOrQuite = input("Python.DLOES:按<1>回到上级菜单\n      或按任意键添加扩展名\nAdmin:")
            while ContinueOrQuite == ("1"):
                DLOExtendService.UpdateExtension(self,"Add")
            else:
                print('当前目标扩展名为:', DLOExtendService.Get(self,("ExtensionList")))
                NewExtension = input("Python.DLOES:请输入需要添加的扩展名\nAdmin:")
                if DLOExtendService.DatabaseAdapter(self, SQL="INSERT INTO EXTENSION(LIST) VALUES(?)",
                                                    Data=NewExtension) == True:
                    print("Python.DLOES:扩展名添加成功")
                    DLOExtendService.UpdateExtension(self,"Add")
                else:
                    print("Python.DLOES:扩展名添加失败")
                    DLOExtendService.UpdateExtension(self,("Add"))
        elif Selection == "Del":
            ContinueOrQuite = input("Python.DLOES:按<1>回到上级菜单\n      或按任意键删除扩展名\nAdmin:")
            while ContinueOrQuite == ("1"):
                DLOExtendService.UpdateExtension(self,input("Python.DLOES:当前目标扩展名为%s\n      按<1>添加扩展名"
                                                            "\n      按<2>删除扩展名\n      或按任意键继续"
                                                            "\nAdmin:"%DLOExtendService.Get(self,"ExtensionList")))
            else:
                print(DLOExtendService.UpdateExtension(self,("Del")))
                TargetExtension = input("Python.DLOES:请输入需要删除的扩展名\nAdmin:")
                if DLOExtendService.DatabaseAdapter(self, SQL="DELETE FROM EXTENSION WHERE LIST = (?)",
                                                    Data=TargetExtension) == True:
                    print("Python.DLOES:扩展名删除成功")
                    DLOExtendService.UpdateExtension(self,("Del"))
                else:
                    print("Python.DLOES:扩展名删除失败")
                    DLOExtendService.UpdateExtension(self, ("Del"))
        else:pass

    def Flow(self):
        os.system('cls')
        if input("Python.DLOES:按<1>结束进程\n      或按任意键继续\nAdmin:") == "1":exit()
        else:pass
        SelectFunction = DLOExtendService.Get(self,"Mode")
        DLOExtendService.UpdateExtension(self,input("Python.DLOES:当前目标扩展名为%s\n      "
                                                    "按<1>添加扩展名\n      "
                                                    "按<2>删除扩展名\n      "
                                                    "或按任意键继续\nAdmin:"%DLOExtendService.Get(self,"ExtensionList")))
        TargetPath = DLOExtendService.Get(self,"TargetPath")
        GetTime = DLOExtendService.Get(self,"Time")
        GetExtensionList = DLOExtendService.Get(self,"ExtensionList")
        StartProcessTime = GetTime[0]
        EndProcessTime = GetTime[1]
        ShowStartTime = GetTime[2]
        ShowEndTime = GetTime[3]
        LogsPath = ("%s\Logs"%CurrentPath)
        DLOExtendService.Logger(self,("Maintain"),LogsPath,FolderSize=10)
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
        else:DLOExtendService.Flow(self)
        print("=======================Start=======================")
        # LogPath = (os.path.join(os.path.dirname(os.path.abspath(__file__)),'TempLog.txt'))
        if SelectFunction[0] == 'KLO':
            DLOExtendService.FileFilter(self, SelectFunction[0],TargetPath, StartProcessTime, EndProcessTime,GetExtensionList)
        elif SelectFunction[0] == 'DA':
            DLOExtendService.FileFilter(self, SelectFunction[0], TargetPath, StartProcessTime, EndProcessTime, GetExtensionList)
        print(('''\n+++++++++++++++++++++++++++++++++++++++
		\n共删除%s个文件
		\n已释放%sMB磁盘空间
		\n%s
		\n+++++++++++++++++++++++++++++++++++++++
                ''' % (DLOExtendService.NumberOfDeletedFiles, int(DLOExtendService.SizeOfDeletedFiles / 1024 / 1024),DLOExtendService.Logger(self,("LastRunTime"),None,None))))
        DLOExtendService.Log.close()
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
        # DLOExtendService.FileFilter(self, RootPath, StartTime, EndTime)
        # Result = ('''
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        #                          共删除%s个文件
        #                        已释放%sMB磁盘空间
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        # ''' % (NumberOfDeletedFiles,int(SizeOfDeletedFiles / 1024 / 1024)))
        # print(Result)
        # # ########################Shortcut For Dev########################

    def FileFilter(self, Mode, RootPath, StartDate, EndDate, ExtensionList):
        global MatchFilesGroup
        AllFileInFolder = []
        MatchFilesGroup = []
        for Object in os.listdir(RootPath):
            FilePath = os.path.join(RootPath, Object)
            if os.path.isdir(FilePath):
                DLOExtendService.FileFilter(self, Mode,FilePath, StartDate, EndDate,ExtensionList)
            elif os.path.isfile(FilePath):
                CreateTime = os.path.getctime(FilePath)
                if (os.path.splitext(FilePath)[1] in ExtensionList) and (StartDate < CreateTime < EndDate):
                    if Mode == "DA":
                        DLOExtendService.DeleteExpiredFile(self,FilePath)
                    else:pass
                    Compare = Object.split("]")
                    del Compare[0]
                    if len(Compare) < 1:print("--\n----")
                    else:
                        Compare = reduce(lambda x, y: x + y, Compare)
                        RawPackage = (Compare,CreateTime,FilePath)
                        AllFileInFolder.append(RawPackage)
                else:
                    print("--\n----")
        for EachFile in sorted(AllFileInFolder, key=lambda FileName: FileName[0]):
            if len(MatchFilesGroup) < 1:MatchFilesGroup.append(EachFile)
            else:
                if EachFile[0] == MatchFilesGroup[0][0]:MatchFilesGroup.append(EachFile)
                else:
                    if len(MatchFilesGroup) < 1: print("--\n----")
                    else:
                        SortMatchFilesGroupByTime = sorted(MatchFilesGroup, key=lambda FileCreateTime: FileCreateTime[1])
                        del SortMatchFilesGroupByTime[-1]
                        for TargetFile in SortMatchFilesGroupByTime:
                            DLOExtendService.DeleteExpiredFile(self,TargetFile[-1])
                    del MatchFilesGroup[:]
                    MatchFilesGroup.append(EachFile)
        if len(MatchFilesGroup) < 1:print("--\n----")
        else:
            SortMatchFilesGroupByTime = sorted(MatchFilesGroup, key=lambda FileCreateTime: FileCreateTime[1])
            del SortMatchFilesGroupByTime[-1]
            for TargetFile in SortMatchFilesGroupByTime:
                DLOExtendService.DeleteExpiredFile(self,TargetFile[-1])

    def DeleteExpiredFile(self, FilePath):
        try:
            DLOExtendService.SizeOfDeletedFiles += os.path.getsize(FilePath)
            print('--File deleted-->>>', FilePath)
            DLOExtendService.Log.write(FilePath)
            DLOExtendService.Log.write("\n")
            # try:
            #     os.remove(FilePath)
            #     print("--File deleted-->>>", FilePath)
            #     DLOExtendService.NumberOfDeletedFiles += 1
            # except:
            #     print("File Cant Be Removed")
        except:pass

    def Logger(self,Mode,FilePath,FolderSize):
        if Mode == ("LastRunTime"):
            try:
                if DLOExtendService.DatabaseAdapter(self, SQL="INSERT INTO LOGS(LASTRUNTIME) VALUES(?)",
                                                    Data=time.strftime("%Y-%m-%d", time.localtime(time.time()))) == True:
                    return ("运行时间更新成功")
            except:
                return ("运行时间更新失败")
        elif Mode == ("Maintain"):
            for Root, Dirs, Files in os.walk(FilePath):
                for File in Files:
                    FolderSize += os.path.getsize(os.path.join(Root, File))
            if FolderSize > 10240:
                Selection = input("Python.DLOES:日志文件大小依超过10MB,是否进行日志清除?(Y/N)\nAdmin:")
                if Selection in ["y","Y"]:
                    StartTime = 1459175064.0
                    EndTime = time.time()
                    ExtensionList = ['.txt']
                    DLOExtendService.FileFilter(self, ("DA"), FilePath, StartTime, EndTime, ExtensionList)
                else:pass
            else:pass

if __name__ == '__main__':
    DLOExtendService.Flow(object)


