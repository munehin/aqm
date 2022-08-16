import csv
import datetime
import logging.config
import os
import MySQLdb

import lib.NwConfig as nwConfig
import lib.SendLog as send

# ログ設定の取得
try:
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
except Exception as ex:
    print(f'Error at logging.getLogger():{ex}')

logger.info("start")

# 設定ファイルの取得
config = nwConfig.NwConfig()
config.load()
if config.check() == False:
    exit()

# 作業日の取得
dt = datetime.datetime.today()  
ymd = f'{dt.year}{dt.month:02d}{dt.day:02d}'

logger.info(f'ymd is {ymd}')

# ファイル一覧の取得
repfiles = []

for root, dirs, files in os.walk(config.report):
    if root.find(ymd) == -1:
        continue
    for file in files:
        if file.lower().startswith("CallIngestReport".lower()):
            repfiles.append(os.path.join(root, file))

logger.info(f'total {len(repfiles)} file.')

try: 
    # 接続する
    if len(config.passwd) == 0:
        conn = MySQLdb.connect(user=config.user, host=config.host, db=config.db)
    else:
        conn = MySQLdb.connect(user=config.user, passwd=config.passwd, host=config.host, db=config.db)

    logger.info(f'connected MySQL.')

    for repfile in repfiles:

        logger.debug(f'read start. {repfile}')

        fp = open(repfile, "rt", encoding='utf-8')
        
        lines = csv.reader(fp, quotechar='"')
        
        i = 0
        for line in lines:
           
            if i == 0:
                i += 1
                continue

            filename = line[1]
            calldatetime = line[2]
            processedondate = line[3]
            disposition = line[4]
            status = 1 if disposition == "Ingested" else 2

            param = (status, calldatetime, processedondate, disposition, filename)
            send.report(conn, param)

            conn.commit()

            i += 1

        fp.close()            

        logger.info(f'{repfile} read {i} line.')

except Exception as ex:
    logger.error(f'Error at main.:{ex}')
    if "conn" in locals():
        conn.rollback()

finally:
    if "conn" in locals():
        conn.close()

logger.info("end")