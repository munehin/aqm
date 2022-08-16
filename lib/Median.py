import logging.config

# ログ設定の取得
try:
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
except Exception as ex:
    print(f'Error at logging.getLogger(): {ex}')

def createTable(conn):
    query1 = "DROP TABLE IF EXISTS tmp_medians"

    #query = "CREATE TEMPORARY TABLE tmp_medians (" \
    query2 = "CREATE TABLE tmp_medians (" \
        + " job_id INT," \
        + " wavdate DATE," \
        + " wavtime FLOAT," \
        + " created DATETIME)"

    try:
        curs = conn.cursor()
        curs.execute(query1)
        curs.execute(query2)

    except Exception as ex:
        logger.error(f'Error at Median.createTable():{ex}')
        return False

    finally:
        curs.close()

    return True

def create(conn):
    query = "INSERT INTO tmp_medians (job_id, wavdate, wavtime, created)" \
        + " SELECT t1.job_id, t1.wavdate, AVG(t1.wavtime) wavtime, NOW()" \
        + " FROM" \
        + " (SELECT ROW_NUMBER() OVER (PARTITION BY job_id, wavdate ORDER BY wavtime) rownum, job_id, wavdate, wavtime" \
        + " FROM uploadlogs" \
        + " WHERE status = 0" \
        + " ORDER BY job_id, wavdate, wavtime) t1" \
        + " JOIN" \
        + " (SELECT job_id, wavdate, COUNT(*) count" \
        + " FROM uploadlogs" \
        + " WHERE status = 0" \
        + " GROUP BY job_id, wavdate) t2" \
        + " ON" \
        + " (t1.job_id = t2.job_id AND t1.wavdate = t2.wavdate)" \
        + " WHERE t1.rownum in (CEIL(t2.count / 2), CEIL((t2.count + 1) / 2))" \
        + " GROUP BY t1.job_id, t1.wavdate" \
        + " ORDER BY t1.job_id, t1.wavdate"

    try:
        curs = conn.cursor()
        curs.execute(query)

    except Exception as ex:
        logger.error(f'Error at Median.create():{ex}')
        return False

    finally:
        curs.close()

    return True
