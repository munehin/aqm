import logging.config

P_C_CTIPATH = 0
P_C_WAVPATH = 1
P_C_LOADLOG_ID = 2

# ログ設定の取得
try:
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
except Exception as ex:
    print("Error at logging.getLogger():", ex)

def create(conn, param):
    query = "INSERT INTO sendlogs(changed, ctipath, ctifile, wavpath, status, uploadlog_id, created)" \
        + " VALUES (NOW(), %s, %s, %s, 0, %s, NOW())"

    try:
        curs = conn.cursor()
        curs.execute(query, param)

    except Exception as ex:
        logger.error(f'Error at SendLog.create({param}), {ex}')
        return False

    finally:
        curs.close()
 
    return True

def removeOld(conn, ctipath):
    query = "UPDATE sendlogs" \
        + " SET status = 99" \
        + ", modified = NOW()" \
        + " WHERE ctipath = %s" \
        + " AND status = 0"

    try:
        curs = conn.cursor()
        curs.execute(query, (ctipath,))

    except Exception as ex:
        logger.error(f'Error at SendLog.removeOld({ctipath}), {ex}')
        return False

    finally:
        curs.close()
 
    return True

def report(conn, param):
    query = "UPDATE sendlogs" \
        + " SET status = %s" \
        + ", calldatetime = %s" \
        + ", processedondate = %s" \
        + ", disposition = %s" \
        + ", modified = NOW()" \
        + " WHERE ctifile = %s" \
        + " AND status = 0"

    try:
        curs = conn.cursor()
        curs.execute(query, param)

    except Exception as ex:
        logger.error(f'Error at SendLog.report({param}), {ex}')
        return False

    finally:
        curs.close()
 
    return True
