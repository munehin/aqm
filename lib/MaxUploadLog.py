import logging.config

# ログ設定の取得
try:
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
except Exception as ex:
    print(f'Error at logging.getLogger(): {ex}')

def createTable(conn):
    query1 = "DROP TABLE IF EXISTS tmp_max_uploadlogs"

    #query = "CREATE TEMPORARY TABLE tmp_max_uploadlogs (" \
    query2 = "CREATE TABLE tmp_max_uploadlogs (" \
        + " job_id INT," \
        + " agentpbxid VARCHAR(16)," \
        + " rownum INT," \
        + " id INT," \
        + " gap INT," \
        + " created DATETIME)"

    try:
        curs = conn.cursor()
        curs.execute(query1)
        curs.execute(query2)

    except Exception as ex:
        logger.error(f'Error at TuploadLog.createTable():{ex}')
        return False

    finally:
        curs.close()

    return True

def create(conn):
    query = "INSERT INTO tmp_max_uploadlogs (job_id, agentpbxid, rownum, id, gap, created)" \
        + " SELECT job_id, agentpbxid, rownum, id, gap, NOW()" \
        + " FROM (" \
        + " SELECT ROW_NUMBER() OVER (PARTITION BY job_id, agentpbxid ORDER BY ABS(u.wavtime - m.wavtime)) rownum," \
        + " u.id, u.job_id, u.agentpbxid, ABS(u.wavtime - m.wavtime) gap, j.sendmax, mu2.count" \
        + " FROM uploadlogs u" \
        + " JOIN jobs j" \
        + " ON (u.job_id = j.id)" \
        + " JOIN tmp_medians m" \
        + " ON (u.job_id = m.job_id AND u.wavdate = m.wavdate)" \
        + " LEFT JOIN tmp_min_uploadlogs mu1" \
        + " ON (u.id = mu1.id)" \
        + " LEFT JOIN (" \
        + " SELECT job_id, agentpbxid, count(*) count" \
        + " FROM tmp_min_uploadlogs" \
        + " GROUP BY job_id, agentpbxid" \
        + " ) mu2" \
        + " ON (u.job_id = mu2.job_id AND u.agentpbxid = mu2.agentpbxid)" \
        + " WHERE u.status = 0" \
        + " AND u.notsend = false" \
        + " AND mu1.id IS NULL" \
        + " ORDER BY u.job_id, u.agentpbxid, ABS(u.wavtime - m.wavtime)" \
        + " ) t" \
        + " WHERE rownum <= IFNULL(sendmax, 2147483647) - IFNULL(count, 0)"

    try:
        curs = conn.cursor()
        curs.execute(query)

    except Exception as ex:
        logger.error(f'Error at MaxUploadLog.create():{ex}')
        return False

    finally:
        curs.close()

    return True
