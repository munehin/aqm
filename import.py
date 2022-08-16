import datetime
import logging.config
import MySQLdb
import os
import time

import lib.NwConfig as nwConfig
import lib.NwXml as nwXml
import lib.NwUtility as nwUtility
import lib.JobMapping as job
import lib.Summary as summary
import lib.SVMapping as sv
import lib.UploadLog as upload

JOB_JLIS = 'Ｊ－Ｌｉｓ'
#JOB_JLIS = 'USEN'

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

time_list = 0
time_str = time.perf_counter()
# ファイル一覧の取得
xmlfiles = []
wavfiles = []

for root, dirs, files in os.walk(config.bs0):
    for file in files:
        if file.lower().endswith(".xml"):
            xmlfiles.append(os.path.join(root, file))
        elif file.lower().endswith(f".{config.wavext}"):
            wavfiles.append(os.path.join(root, file))

time_end = time.perf_counter()
time_list = time_end - time_str

logger.info(f'total {len(xmlfiles)} file.')

# DNISファイルの取得
lstDnis = []

if len(config.dnis) > 0:
    fp = open(config.dnis, "rt", encoding="utf-8")
    lines = fp.readlines()
    for line in lines:
        line = line.replace("\n", "")
        if len(line) > 0:
            lstDnis.append(line)
    fp.close()          

try:
    # 接続する
    if len(config.passwd) == 0:
        conn = MySQLdb.connect(user=config.user, host=config.host, db=config.db)
    else:
        conn = MySQLdb.connect(user=config.user, passwd=config.passwd, host=config.host, db=config.db)
    
    logger.debug(f'connected MySQL.')

    #conn.autocommit(True)

    coOK = 0
    coNG = 0
    sumSize = 0

    time_wav = 0
    time_xml = 0
    time_jobm = 0
    time_svm = 0
    time_move = 0
    time_remove = 0
    time_create = 0

    for xmlfile in xmlfiles:

        logger.debug(f'check start. {xmlfile}')

        # ctiファイル名の確認
        wavpath = nwUtility.getWavpath(xmlfile, config.wavdir, config.wavext)
        if len(wavpath) == 0:
            logger.warning(f'cti file name is wrong. {xmlfile}')
            nwUtility.remove(xmlfile)
            upload.createError(conn, (os.path.basename(xmlfile),))
            conn.commit()
            coNG += 1
            continue

        time_str = time.perf_counter()
        # wavファイルは存在するか
        if nwUtility.isExist(wavpath, wavfiles) == False:
            logger.warning(f'wav file is not exist. {wavpath}')
            coNG += 1
            continue

        time_end = time.perf_counter()
        time_wav += time_end - time_str

        time_str = time.perf_counter()
        # xmlファイルのチェック
        xml = nwXml.NwXml()
        if xml.load(xmlfile) == False:
            nwUtility.remove2(xmlfile, config.wavdir, config.wavext)
            upload.createError(conn, (os.path.basename(xmlfile),))
            conn.commit()
            coNG += 1
            continue

        time_end = time.perf_counter()
        time_xml += time_end - time_str

        # 内部通話の削除
        if xml.direction == "0":
            logger.warning(f'direction is 0.')
            nwUtility.remove2(xmlfile, config.wavdir, config.wavext)
            upload.createError(conn, (os.path.basename(xmlfile),))
            conn.commit()
            coNG += 1
            continue

        # DNISの確認
        if len(lstDnis) > 0:
            if xml.dnis not in lstDnis:
                logger.warning(f'dnis is not exist.')
                nwUtility.remove2(xmlfile, config.wavdir, config.wavext)
                upload.createError(conn, (os.path.basename(xmlfile),))
                conn.commit()
                coNG += 1
                continue

        time_str = time.perf_counter()
        # JobMappingの取得
        jRows = job.findByExtension(conn, xml.extension)
        if jRows is None or len(jRows) != 1:
            logger.warning(f'JobMapping Error extension = "{xml.extension}"')
            nwUtility.remove2(xmlfile, config.wavdir, config.wavext)
            upload.createError(conn, (os.path.basename(xmlfile),))
            conn.commit()
            coNG += 1
            continue

        time_end = time.perf_counter()
        time_jobm += time_end - time_str

        time_str = time.perf_counter()
        # SVMappingの取得
        sRows = sv.findByAgentpbxid(conn, xml.agentPBXID)
        if sRows is None or len(sRows) != 1:
            logger.warning(f'SVMapping Error agentpbxid = "{xml.agentPBXID}"')
            nwUtility.remove2(xmlfile, config.wavdir, config.wavext)
            upload.createError(conn, (os.path.basename(xmlfile),))
            conn.commit()
            coNG += 1
            continue

        time_end = time.perf_counter()
        time_svm += time_end - time_str

        #JLIS and direction = 2
        if jRows[0][job.IDX_JOB_NAME] == JOB_JLIS and xml.direction == "2":
            logger.warning(f'JLIS and direction = 2')
            nwUtility.remove2(xmlfile, config.wavdir, config.wavext)
            upload.createError(conn, (os.path.basename(xmlfile),))
            conn.commit()
            coNG += 1
            continue

        # ファイルサイズ、時間の取得
        filesize = os.path.getsize(wavpath)
        filedate = xml.get_wavdate()
        filetime = xml.get_wavtime()

        logger.debug(f'move start. {xmlfile}')

        time_str = time.perf_counter()
        # XML, wavの移動
        #ret = nwUtility.move2bs1(xmlfile[0], config.bs1, jRows[0][job.IDX_JOB_NAME], ymd, xml.extension)
        ret = nwUtility.move2bs1(xmlfile, config.bs1, ymd, config.wavdir, config.wavext)
        if ret == False:
            coNG += 1
            continue

        logger.debug(f'moved. {xmlfile}')
        time_end = time.perf_counter()
        time_move += time_end - time_str

        # uploadLogの登録
        bs1xmlfile = nwUtility.getBs1path(xmlfile, config.bs1, ymd, config.wavdir, config.wavext)
        wavfile = nwUtility.getWavpath(xmlfile, config.wavdir, config.wavext)

        param = (bs1xmlfile, os.path.basename(xmlfile), os.path.basename(wavfile), filesize, filedate, filetime \
            , jRows[0][job.IDX_CLIENTCODE], xml.extension, jRows[0][job.IDX_JOB_ID], sRows[0][sv.IDX_AGENTNAME], xml.agentPBXID)

        time_str = time.perf_counter()
        upload.removeOld(conn, bs1xmlfile)
        time_end = time.perf_counter()
        time_remove += time_end - time_str

        time_str = time.perf_counter()
        upload.create(conn, param)

        conn.commit()

        time_end = time.perf_counter()
        time_create += time_end - time_str

        logger.debug(f'{xmlfile} is imported. new path is {bs1xmlfile}')
        coOK += 1
        sumSize += filesize

    summary.create(conn, (len(xmlfiles), coOK, coNG, sumSize, config.name))
    conn.commit()

    logger.info(f'imported {coOK} file.')
    logger.info(f'error {coNG} file.')

    logger.debug(f'ファイル一覧の取得 {time_list}秒.')
    logger.debug(f'wavファイルの存在確認 {time_wav}秒.')
    logger.debug(f'xmlファイルのチェック {time_xml}秒.')
    logger.debug(f'JobMappingの取得 {time_jobm}秒.')
    logger.debug(f'SVMappingの取得 {time_svm}秒.')
    logger.debug(f'XML, wavの移動 {time_move}秒.')
    logger.debug(f'古いuploadLogの更新 {time_remove}秒.')
    logger.debug(f'uploadLogの登録 {time_create}秒.')

except Exception as ex:
    logger.error(f'Error at main.:{ex}')
    if "conn" in locals():
        conn.rollback()

finally:
    if "conn" in locals():
        conn.close()

logger.info("end")