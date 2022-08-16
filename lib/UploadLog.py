import logging.config

P_C_CTIPATH = 0
P_C_CTIFILE = 1
P_C_WAVFILE = 2
P_C_CLIENTCODE = 3
P_C_EXTENSION = 4
P_C_JOB_NAME = 5
P_C_AGENTNAME = 6
P_C_AGENTPBXID = 7

IDX_ID = 0
IDX_UPLOADED = 1
IDX_CTIPATH = 2
IDX_CTIFILE = 3
IDX_WAVFILE = 4
IDX_CLIENTCODE = 5
IDX_EXTENSION = 6
IDX_JOB_ID = 7
IDX_JOB_NAME = 8
IDX_AGENTNAME = 9
IDX_AGENTPBXID = 10
IDX_STATUS = 11
IDX_NOTSEND = 12
IDX_CREATED = 13
IDX_MODIFIED = 14
IDX_WAVTIME = 15

# ログ設定の取得
try:
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
except Exception as ex:
    print("Error at logging.getLogger():", ex)

def create(conn, param):
    query = "INSERT INTO uploadlogs(uploaded, ctipath, ctifile, wavfile, wavsize, wavdate, wavtime, clientcode, extension, job_id, agentname, agentpbxid, status, created)" \
        + " VALUES (NOW(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 0, NOW())"

    try:
        curs = conn.cursor()
        curs.execute(query, param)

    except Exception as ex:
        logger.error(f'Error at UploadLog.create({param}), {ex}')
        return False

    finally:
        curs.close()
 
    return True

def createError(conn, param):
    query = "INSERT INTO uploadlogs(uploaded, ctifile, status, created)" \
        + " VALUES (NOW(), %s, 97, NOW())"

    try:
        curs = conn.cursor()
        curs.execute(query, param)

    except Exception as ex:
        logger.error(f'Error at UploadLog.createError({param}), {ex}')
        return False

    finally:
        curs.close()
 
    return True

def load(conn, id):
    query = "SELECT * FROM uploadlogs WHERE id = ?"

    try:
        curs = conn.cursor()
        curs.execute(query, (id))
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at UploadLog.load({id}):{ex}')
        return None

    finally:
        curs.close()

    return rows

def removeOld(conn, ctipath):
    query = "UPDATE uploadlogs" \
        + " SET status = 99" \
        + ", modified = NOW()" \
        + " WHERE ctipath = %s" \
        + " AND status = 0"

    try:
        curs = conn.cursor()
        curs.execute(query, (ctipath,))

    except Exception as ex:
        logger.error(f'Error at UploadLog.removeOld({ctipath}), {ex}')
        return False

    finally:
        curs.close()
 
    return True

def getSendList(conn):
    query = "SELECT u.id, u.uploaded, u.ctipath, u.ctifile, u.wavfile, u.clientcode, u.extension, u.job_id, j.name job_name, u.agentname, u.agentpbxid, u.status, u.notsend, u.created, u.modified" \
        + " FROM uploadlogs u" \
	    + " JOIN jobs j" \
	    + " ON (u.job_id = j.id)" \
        + " WHERE u.status = 0" \
        + " AND u.notsend = false" \
        + " AND u.wavsize >= IFNULL(j.wavmin, 0)" \
        + " AND u.wavsize <= IFNULL(j.wavmax, 2147483647)"

    try:
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at UploadLog.getSendList():{ex}')
        return None

    finally:
        curs.close()

    return rows

def send(conn, id):
    query = "UPDATE uploadlogs" \
        + " SET status = 1" \
        + ", modified = NOW()" \
        + " WHERE id = %s" \
        + " AND status = 0"

    try:
        curs = conn.cursor()
        curs.execute(query, (id,))

    except Exception as ex:
        logger.error(f'Error at UploadLog.send({id}), {ex}')
        return False

    finally:
        curs.close()
 
    return True

def removeFilesize(conn):
    query = "UPDATE uploadlogs u, jobs j" \
        + " SET u.status = 98" \
        + ", u.modified = NOW()" \
        + " WHERE u.job_id = j.id" \
        + " AND u.status = 0" \
        + " AND (u.wavsize < IFNULL(j.wavmin, 0)" \
        + " OR u.wavsize > IFNULL(j.wavmax, 2147483647))"

    try:
        curs = conn.cursor()
        curs.execute(query)

    except Exception as ex:
        logger.error(f'Error at UploadLog.moveFilesize(), {ex}')
        return False

    finally:
        curs.close()
 
    return True

def getSendListM(conn):
    query = "SELECT id, uploaded, ctipath, ctifile, wavfile, clientcode, extension, job_id, job_name, agentname, agentpbxid, status, notsend, created, modified" \
        + " FROM (" \
        + " SELECT ROW_NUMBER() OVER (PARTITION BY u.job_id, u.agentpbxid ORDER BY ABS(u.wavtime - m.wavtime)) rownum, u.id, u.uploaded, u.ctipath, u.ctifile, u.wavfile, u.clientcode, u.extension, u.job_id, j.name job_name, u.agentname, u.agentpbxid, u.status, u.notsend, u.created, u.modified, j.sendmax" \
        + " FROM uploadlogs u" \
        + " JOIN jobs j" \
        + " ON (u.job_id = j.id)" \
        + " JOIN tmp_medians m" \
        + " ON (u.job_id = m.job_id AND u.wavdate = m.wavdate)" \
        + " WHERE u.status = 0" \
        + " AND u.notsend = false" \
        + " ORDER BY u.job_id, u.agentpbxid, ABS(u.wavtime - m.wavtime)" \
        + " ) t" \
        + " WHERE rownum <= IFNULL(sendmax, 2147483647)"

    try:
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at UploadLog.getSendListM():{ex}')
        return None

    finally:
        curs.close()

    return rows

def getMinSendList(conn):
    query = "SELECT u.id, u.uploaded, u.ctipath, u.ctifile, u.wavfile, u.clientcode, u.extension, u.job_id, j.name job_name, u.agentname, u.agentpbxid, u.status, u.notsend, u.created, u.modified, u.wavtime" \
        + " FROM uploadlogs u" \
        + " JOIN jobs j" \
        + " ON (u.job_id = j.id)" \
        + " JOIN tmp_min_uploadlogs mu" \
        + " ON (u.id = mu.id)"

    try:
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at UploadLog.getMinSendList():{ex}')
        return None

    finally:
        curs.close()

    return rows

def getMaxSendList(conn):
    query = "SELECT u.id, u.uploaded, u.ctipath, u.ctifile, u.wavfile, u.clientcode, u.extension, u.job_id, j.name job_name, u.agentname, u.agentpbxid, u.status, u.notsend, u.created, u.modified, u.wavtime" \
        + " FROM uploadlogs u" \
        + " JOIN jobs j" \
        + " ON (u.job_id = j.id)" \
        + " JOIN tmp_max_uploadlogs mu" \
        + " ON (u.id = mu.id)" \
        + " ORDER BY mu.rownum, mu.gap"

    try:
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at UploadLog.getMaxSendList():{ex}')
        return None

    finally:
        curs.close()

    return rows

def removeStatus0(conn):
    query = "UPDATE uploadlogs u" \
        + " SET u.status = 98" \
        + ", u.modified = NOW()" \
        + " WHERE u.status = 0"

    try:
        curs = conn.cursor()
        curs.execute(query)

    except Exception as ex:
        logger.error(f'Error at UploadLog.moveStatus0, {ex}')
        return False

    finally:
        curs.close()
 
    return True

def getFilesizeList(conn):
    query = "SELECT u.id, u.ctipath, j.name" \
        + " FROM uploadlogs u" \
        + " JOIN jobs j" \
        + " ON (u.job_id = j.id)" \
        + " WHERE u.status = 0" \
        + " AND (u.wavsize < IFNULL(j.wavmin, 0)" \
        + " OR u.wavsize > IFNULL(j.wavmax, 2147483647))" \
        + " ORDER BY u.id"

    try:
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at UploadLog.getFilesizeList():{ex}')
        return None

    finally:
        curs.close()

    return rows

def getStatus0List(conn):
    query = "SELECT u.id, u.ctipath, j.name" \
        + " FROM uploadlogs u" \
        + " JOIN jobs j" \
        + " ON (u.job_id = j.id)" \
        + " WHERE u.status = 0" \
        + " ORDER BY u.id"

    try:
        curs = conn.cursor()
        curs.execute(query)
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at UploadLog.getStatus0List():{ex}')
        return None

    finally:
        curs.close()

    return rows

def updateStatus98(conn, id):
    query = "UPDATE uploadlogs" \
        + " SET status = 98" \
        + ", modified = NOW()" \
        + " WHERE id = %s" \
        + " AND status = 0"

    try:
        curs = conn.cursor()
        curs.execute(query, (id,))

    except Exception as ex:
        logger.error(f'Error at UploadLog.updateStatus98, {ex}')
        return False

    finally:
        curs.close()
 
    return True

