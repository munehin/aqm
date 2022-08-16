import logging.config

IDX_ID = 0
IDX_EXTENSION = 1
IDX_CLIENTCODE = 2
IDX_SUBJOB = 3
IDX_AREACODE = 4
IDX_AREANAME = 5
IDX_CEMTERCODE = 6
IDX_CENTERNAME = 7 
IDX_JOB_ID = 8
IDX_JOB_NAME = 9
IDX_CREATED = 10
IDX_MODIFIED = 11

# ログ設定の取得
try:
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
except Exception as ex:
    print(f'Error at logging.getLogger(): {ex}')

def findByExtension(conn, extension):
    query = "SELECT jm.id, jm.extension, jm.clientcode, jm.subjob, jm.areacode, jm.areaname, jm.centercode, jm.centername, jm.job_id, j.name AS jobname, jm.created, jm.modified" \
        + " FROM jobmappings AS jm" \
        + " JOIN jobs AS j" \
        + " ON (jm.job_id = j.id)" \
        + " WHERE jm.extension = %s"

    try:
        curs = conn.cursor()
        curs.execute(query, (extension,))
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at JobMapping.findByExtension("{extension}"):{ex}')
        return None

    finally:
        curs.close()

    return rows
