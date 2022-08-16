import logging.config

# ログ設定の取得
try:
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
except Exception as ex:
    print(f'Error at logging.getLogger(): {ex}')

def createTable(conn):
    query1 = "DROP TABLE IF EXISTS tmp_min_uploadlogs"

    #query = "CREATE TEMPORARY TABLE tmp_min_uploadlogs (" \
    query2 = "CREATE TABLE tmp_min_uploadlogs (" \
        + " job_id INT," \
        + " agentpbxid VARCHAR(16)," \
        + " wavdate DATE," \
        + " rownum INT," \
        + " id INT," \
        + " gap INT," \
        + " created DATETIME)"

    try:
        curs = conn.cursor()
        curs.execute(query1)
        curs.execute(query2)

    except Exception as ex:
        logger.error(f'Error at MinUploadLog.createTable():{ex}')
        return False

    finally:
        curs.close()

    return True

def create(conn):
    query = "INSERT INTO tmp_min_uploadlogs (job_id, agentpbxid, wavdate, rownum, id, gap, created)" \
        + " SELECT job_id, agentpbxid, wavdate, rownum, id, gap, NOW()" \
        + " FROM (" \
        + " SELECT ROW_NUMBER() OVER (PARTITION BY u.job_id, u.agentpbxid, u.wavdate ORDER BY ABS(u.wavtime - m.wavtime)) rownum," \
        + " u.id, u.wavdate, u.job_id, u.agentpbxid, ABS(u.wavtime - m.wavtime) gap, j.sendmin" \
        + " FROM uploadlogs u" \
        + " JOIN jobs j" \
        + " ON (u.job_id = j.id)" \
        + " JOIN tmp_medians m" \
        + " ON (u.job_id = m.job_id AND u.wavdate = m.wavdate)" \
        + " WHERE u.status = 0" \
        + " AND u.notsend = false" \
        + " ORDER BY u.job_id, u.agentpbxid, u.wavdate, ABS(u.wavtime - m.wavtime)" \
        + " ) t" \
        + " WHERE rownum <= IFNULL(sendmin, 0)"

    try:
        curs = conn.cursor()
        curs.execute(query)

    except Exception as ex:
        logger.error(f'Error at MinUploadLog.create():{ex}')
        return False

    finally:
        curs.close()

    return True
