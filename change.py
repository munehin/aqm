import datetime
import logging.config
import MySQLdb
import os
import time

import lib.MaxUploadLog as maxupload
import lib.Median as median
import lib.MinUploadLog as minupload
import lib.NwConfig as nwConfig
import lib.NwXml as nwXml
import lib.NwUtility as nwUtility
import lib.JobMapping as job
import lib.SVMapping as sv
import lib.SendLog as send
import lib.UploadLog as upload

JOB_ACCS = 'Nippon Insatsu'

WAV_DIR = "WAV" 
WAV_EXT = "wav"
MP3_DIR = "MP3" 
MW3_EXT = "mp3"

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

try:
    # 接続する
    if len(config.passwd) == 0:
        conn = MySQLdb.connect(user=config.user, host=config.host, db=config.db)
    else:
        conn = MySQLdb.connect(user=config.user, passwd=config.passwd, host=config.host, db=config.db)

    logger.debug(f'connected MySQL.')

    # wavファイルの容量
    #if upload.removeFilesize(conn) == False:
    #    exit()

    uRows = upload.getFilesizeList(conn)
    
    logger.debug(f'filesize list size is {len(uRows)}.')

    for uRow in uRows:
        if uRow[2] == JOB_ACCS:
            nwUtility.remove2(uRow[1], MP3_DIR, MW3_EXT)
        else:
            nwUtility.remove2(uRow[1], WAV_DIR, WAV_EXT)
        upload.updateStatus98(conn, uRow[0])
        conn.commit()

    logger.debug(f'filesize removed.')

    # 中央値の作成
    if median.createTable(conn) == False:
        exit()
    if median.create(conn) == False:
        exit()

    logger.debug(f'median created.')

    # 最低抽出件数の取得
    if minupload.createTable(conn) == False:
        exit()
    if minupload.create(conn) == False:
        exit()

    logger.debug(f'minupload created.')

    # 中央値に近いデータから取得
    if maxupload.createTable(conn) == False:
        exit()
    if maxupload.create(conn) == False:
        exit()

    logger.debug(f'maxupload created.')

    # ファイル一覧の取得
    #uRows = upload.getSendListM(conn)
    uRows = []
    uRows1 = upload.getMinSendList(conn)
    uRows2 = upload.getMaxSendList(conn)

    logger.debug(f'sendlist created.')

    # 合計時間
    wavtime = 0
    for uRow1 in uRows1:
        uRows.append(uRow1)
        wavtime += uRow1[upload.IDX_WAVTIME]

    if wavtime < config.maxwavtime:
        for uRow2 in uRows2:
            if wavtime + uRow2[upload.IDX_WAVTIME] < config.maxwavtime:
                uRows.append(uRow2)
                wavtime += uRow2[upload.IDX_WAVTIME]
            else:
                break

    logger.debug(f'sendlist marged.')

    # 変換開始
    coOK = 0
    coNG = 0

    time_jobm = 0
    time_svm = 0
    time_move = 0
    time_remove = 0
    time_create = 0
    time_update = 0

    for uRow in uRows:

        logger.debug(f'check start. {uRow[upload.IDX_CTIPATH]}')

        # xmlファイルのチェック
        xml = nwXml.NwXml()
        if xml.load(uRow[upload.IDX_CTIPATH]) == False:
            coNG += 1
            continue

        time_str = time.perf_counter()
        # JobMappingの取得
        jRows = job.findByExtension(conn, xml.extension)
        if jRows is None or len(jRows) != 1:
            logger.error(f'JobMapping Error extension = "{xml.extension}"')
            coNG += 1
            continue

        time_end = time.perf_counter()
        time_jobm += time_end - time_str

        time_str = time.perf_counter()
        # SVMappingの取得
        sRows = sv.findByAgentpbxid(conn, xml.agentPBXID)
        if sRows is None or len(sRows) != 1:
            logger.error(f'SVMapping Error agentpbxid = "{xml.agentPBXID}"')
            coNG += 1
            continue

        time_end = time.perf_counter()
        time_svm += time_end - time_str

        # xmlの変換
        logger.debug(f'change start. {uRow[upload.IDX_CTIPATH]}')

        xml.change(jRows[0], sRows[0])

        logger.debug(f'changed. {uRow[upload.IDX_CTIPATH]}')

        logger.debug(f'move start. {uRow[upload.IDX_CTIPATH]}')

        time_str = time.perf_counter()
        # XML, wavの移動
        if uRow[upload.IDX_JOB_NAME] == JOB_ACCS:
            ret = nwUtility.move2bs2(uRow[upload.IDX_CTIPATH], config.bs2, uRow[upload.IDX_JOB_NAME], ymd, uRow[upload.IDX_EXTENSION],
                                 uRow[upload.IDX_AGENTPBXID], MP3_DIR, MW3_EXT)
        else:
            ret = nwUtility.move2bs2(uRow[upload.IDX_CTIPATH], config.bs2, uRow[upload.IDX_JOB_NAME], ymd, uRow[upload.IDX_EXTENSION],
                                 uRow[upload.IDX_AGENTPBXID], WAV_DIR, WAV_EXT)

        if ret == False:
            coNG += 1
            continue

        logger.debug(f'moved. {uRow[upload.IDX_CTIPATH]}')
        time_end = time.perf_counter()
        time_move += time_end - time_str

        # sendLogの登録
        newfile = nwUtility.getNewfile(os.path.basename(uRow[upload.IDX_CTIPATH]), xml.extension, xml.agentPBXID)
        if uRow[upload.IDX_JOB_NAME] == JOB_ACCS:
            wavpath = nwUtility.getWavpath(uRow[upload.IDX_CTIPATH], MP3_DIR, MW3_EXT)
        else:
            wavpath = nwUtility.getWavpath(uRow[upload.IDX_CTIPATH], WAV_DIR, WAV_EXT)
        newwav = nwUtility.getNewfile(os.path.basename(wavpath), xml.extension, xml.agentPBXID)
 
        target = f'{config.bs2}\\{uRow[upload.IDX_JOB_NAME]}\\{ymd}'

        param = (os.path.join(target, newfile), newfile, os.path.join(target, newwav), uRow[upload.IDX_ID])

        time_str = time.perf_counter()
        send.removeOld(conn, os.path.join(target, newfile))
        time_end = time.perf_counter()
        time_remove += time_end - time_str

        time_str = time.perf_counter()
        send.create(conn, param)
        time_end = time.perf_counter()
        time_create += time_end - time_str

        time_str = time.perf_counter()
        # uploadLogの更新
        upload.send(conn, uRow[upload.IDX_ID])
        time_end = time.perf_counter()
        time_update += time_end - time_str

        conn.commit()

        logger.debug(f'{uRow[upload.IDX_CTIPATH]} is sended. new path is {os.path.join(target, newfile)}')
        coOK += 1

    logger.debug(f'changed.')

    logger.debug(f'start remove.')

    time_status = 0
    time_str = time.perf_counter()
    # 変換対象外のファイルの削除
    #upload.removeStatus0(conn)
    #
    #conn.commit()

    uRows = upload.getStatus0List(conn)

    logger.debug(f'status0 list size is {len(uRows)}.')

    for uRow in uRows:
        if uRow[2] == JOB_ACCS:
            nwUtility.remove2(uRow[1], MP3_DIR, MW3_EXT)
        else:
            nwUtility.remove2(uRow[1], WAV_DIR, WAV_EXT)
        upload.updateStatus98(conn, uRow[0])
        conn.commit()

    time_end = time.perf_counter()
    time_status += time_end - time_str

    logger.debug(f'removed.')

except Exception as ex:
    logger.error(f'Error at main.:{ex}')
    if "conn" in locals():
        conn.rollback()

finally:
    if "conn" in locals():
        conn.close()

logger.info(f'changed {coOK} file.')
logger.info(f'error {coNG} file.')
logger.info(f'wavtime {wavtime}')

logger.debug(f'JobMappingの取得 {time_jobm}秒.')
logger.debug(f'SVMappingの取得 {time_svm}秒.')
logger.debug(f'XML, wavの移動 {time_move}秒.')
logger.debug(f'古いsendLogの更新 {time_remove}秒.')
logger.debug(f'sendlogLogの登録 {time_create}秒.')
logger.debug(f'uploadLogの更新 {time_update}秒.')
logger.debug(f'変換対象外のファイルの削除 {time_status}秒.')

logger.info("end")