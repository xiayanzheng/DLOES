import os,sys,sqlite3


# def ReadDataBase(SQL):
#     db_file = "dloes.db"
#     GetCurrentPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_file)
#     ConnectDataBase = sqlite3.connect( GetCurrentPath)
#     CursorDataBase = ConnectDataBase.cursor()
#     SQL = CursorDataBase.execute(SQL)
#     return SQL.fetchall()
#
# print(ReadDataBase(SQL="SELECT * FROM extension"))


TheFileName = "E:\Resources\Documents\PD\Sandbox\DLOME\DLOES_V9.py"
TheFileSize = os.path.getsize(TheFileName)
print(TheFileSize / 1024)


