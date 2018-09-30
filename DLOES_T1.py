import os,hashlib,time,sqlite3,difflib,re,datetime
import string as s
from functools import reduce

def file_md5(filepath):
    f = open(filepath, 'rb')
    md5obj = hashlib.md5()
    md5obj.update(f.read())
    hash = md5obj.hexdigest()
    return hash

def file_dedup(dirpath):
    hashpool = []
    print(hashpool)
    print ("dedup files in", dirpath)
    filelist = os.listdir(dirpath)  # list all files and dirs in the dir
    for efile in filelist:
        print (efile, "check!!!")
        filepath = os.path.join(dirpath, efile)  # file's absolute path
        if os.path.isdir(filepath):  # if file is a dir
            print (filepath, "is a dir")
            continue
        else:
            filehash = file_md5(filepath)
            if filehash in hashpool:
                print ("exist! delete")
                os.remove(filepath)
            else:
                print ("new file")
                hashpool.append(filehash)

def iden_by_Extention(path):
    f_list = os.listdir(path)
    # print f_list
    for i in f_list:
        # os.path.splitext():分离文件名与扩展名
        list = ['.txt']
        if os.path.splitext(i)[1] in list:
            print (i)

def Test1(rootDir):
    list_dirs = os.walk(rootDir)
    for root, dirs, files in list_dirs:
        for d in dirs:
            print (os.path.join(root, d))
        for f in files:
            print (os.path.join(root, f))

class dloscs(object):

    def extention_list(self):
        raw_data = dloscs.DLOSCS_DB_read(self=None,sql_data_r="SELECT * FROM extension")
        extention_list = []
        for data in raw_data:
            extention_list.append(data[0])
        return extention_list

    def DLOSCS_DB_read(self, sql_data_r):
        get_old_path = os.getcwd()
        connect_db = sqlite3.connect("%s\DLOSCS_Data.db" % get_old_path)
        # connect_db = sqlite3.connect('/Users/xiayanzheng/Onedriver/OneDrive/Lib-Sandbox/cimt.db')
        cursor_db = connect_db.cursor()
        sql = cursor_db.execute(sql_data_r)
        fetchall_sql = sql.fetchall()
        return fetchall_sql

    def DLOSCS_DB_write(self, db_sql, db_data):
        get_old_path = os.getcwd()
        connect_db = sqlite3.connect("%s\DLOSCS_DB.db" % get_old_path)
        # connect_db = sqlite3.connect('/Users/xiayanzheng/Onedriver/OneDrive/Lib-Sandbox/cimt.db')
        c = connect_db.cursor()
        # Create table
        # c.execute('''Create TABLE if not exists sql_target_table("NA")''')
        # Insert links into table
        c.execute(db_sql, db_data)
        connect_db.commit()

    def DLOSCS_DB_get_last_column(self, data):
        list = []
        for traversal in data:
            list.append(traversal)
        result = (list[-1])[0]
        return result

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
    #                 # dloscs.DeleteExpiredFile(objpath)
    #                 print(objpath,"exist! delete")
    #             else:
    #                 hashpool.append(filehash)
    #                 print(objpath, "Save")
    #         elif os.path.isdir(objpath):
    #             dloscs.iter_all_file(objpath,start_time)

def time_checker(input):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(input, "%Y-%m-%d")
        print("Y")
        return True
    except:
        print("N")
        return False

    # print(re.search(r'\d{4}-\d{2}-\d{2}', 'xxxx1990-12-20xxxx').group(0))
    # print(re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}', 'xxxx2005-06-04T18:37:11xxxx').group(0))
    # print(re.search(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}', 'xxxx2005-06-04T18:37:11.111xxxx').group(0))
    # pattern = re.compile(r'(\d{4}-\d{2}-\d{2})((T\d{2}:\d{2}:\d{2}|))((.\d{3})|)')
    # print(pattern.search('xxxx2005-06-04T18:37:11.111xxxx').group(0))

def lop():

    paths = "[0WDdwwdwdwd00006w0]07-]Sw]in]g]-安D]W装]手]"
    qu = paths.split("]")
    print(qu)
    del qu[0]
    qu = reduce(lambda x, y: x + y, qu)
    print(qu)

def rop():
    list = ['wdawd','wadwda']
    print(list[0]+list[1])

def jwkj_get_filePath_fileName_fileExt(filename):
    (filepath,tempfilename) = os.path.split(filename);
    (shotname,extension) = os.path.splitext(tempfilename);
    return filepath,shotname,extension

# if __name__ == '__main__':
#     CurrentPath = os.getcwd()
#     CurrentTime = time.time()
#     N = ("%s\Logs\[%s]Log"%(CurrentPath, CurrentTime))
#     print(N)
#     # path = 'D:\Python.DLOES'
#     # Test1(path)
#     # # iden_by_Extention(path)
#     # # file_dedup(path)
#     # input = input("LL")
#     # time_checker(input)
#     # lop()
#     # rop()
#     # filename = "[0WDdwwdwdwd00006w0]07-Swing-安DW装手"
#
#     # print(jwkj_get_filePath_fileName_fileExt(filename))
n = []
l = ['.webm', '.vob', '.gif', '.avi', '.yuv', '.asf', '.mpg',
     '.mkv', '.ogv', '.gifv', '.mov', '.rm', '.amv', '.flv',
     '.drc', '.mng', '.wmv', '.rmvb', '.mp4', '.moeg', '.mpeg',
     '.m2v', '.mpe', '.m4v', '.3g2', '.nsv', '.f4p', '.mp2',
     '.mpv', '.qt', '.svi', '.mxf', '.f4a', '.m4p', '.ogg',
     '.3gp', '.roq', '.f4v', '.f4b', '.aa', '.act', '.ape',
     '.dct', '.flac', '.ivs', '.aac', '.aiff', '.au', '.dss',
     '.gsm', '.m4a', '.mmf', '.aax', '.amr', '.awb', '.dvf',
     '.iklax', '.m4b', '.mp3', '.mpc', '.mogg', '.raw', '.vox',
     '.wv', '.msv', '.opus', '.sln', '.wav', '.8svx','.oga',
     '.ra', '.tta', '.wma']


for x in l:
    if len(n) < 5:
        n.append(x)
    else:
        print(n)
        n.clear()