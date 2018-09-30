# from stat import S_ISREG, ST_CTIME, ST_MODE
# import os, sys, time
#
# # path to the directory (relative or absolute)
# dirpath = sys.argv[1] if len(sys.argv) == 2 else r'E:\Resources\视频'
#
# # get all entries in the directory w/ stats
# entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
# entries = ((os.stat(path), path) for path in entries)
#
# # leave only regular files, insert creation date
# entries = ((stat[ST_CTIME], path)
#            for stat, path in entries if S_ISREG(stat[ST_MODE]))
# #NOTE: on Windows `ST_CTIME` is a creation date
# #  but on Unix it could be something else
# #NOTE: use `ST_MTIME` to sort by a modification date
#
# for cdate, path in sorted(entries):
#     print (time.ctime(cdate), os.path.basename(path))

from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time

# path to the directory (relative or absolute)
dirpath = sys.argv[1] if len(sys.argv) == 2 else r'E:\Resources\视频'

# get all entries in the directory w/ stats
entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
entries = ((os.stat(path), path) for path in entries)

# leave only regular files, insert creation date
entries = ((stat[ST_CTIME], path)
           for stat, path in entries if S_ISREG(stat[ST_MODE]))
#NOTE: on Windows `ST_CTIME` is a creation date
#  but on Unix it could be something else
#NOTE: use `ST_MTIME` to sort by a modification date

# for cdate, path in sorted(entries):
#     print (path)
#
# import time
# print(time.strftime("%Y-%m-%d", time.localtime(time.time())))

# list = ['.xlsx', '.txt', '.pptx', '.docx', '.pdf', '.doc', '.log', '.lop', '.lpx']
# su = []
# gu = []
# for x in list:
#     if len(su) < 5:
#         su.append(x)
#     else:
#         gu.append(su)
#         del su[:]
#     print(gu)

# import datetime
# today = datetime.date.today()
# print(today.month,today.year)
# first = datetime.date(day=1, month=today.month, year=today.year)
# lastMonth = first - datetime.timedelta(days=1)
# print(lastMonth)

today = ("2017-10-23")
su = today.split("-")
print(su)