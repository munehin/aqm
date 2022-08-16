import logging.config

IDX_ID = 0
IDX_AGENTPBXID = 1
IDX_AGENTNAME = 2
IDX_SUPERVISORNAME = 3
IDX_AGENTID = 4
IDX_JOB_ID = 5
IDX_JOB_NAME = 6
IDX_CREATED = 7
IDX_MODIFIED = 8

# ログ設定の取得
try:
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
except Exception as ex:
    print(f'Error at logging.getLogger():{ex}')

def findByAgentpbxid(conn, agentPbxId):
    query = "SELECT sv.id, sv.agentpbxid, sv.agentname, sv.supervisorname, sv.agentid, sv.job_id, j.name job_name, sv.created, sv.modified" \
        + " FROM svmappings AS sv" \
        + " JOIN jobs AS j" \
        + " ON (sv.job_id = j.id)" \
        + " WHERE sv.agentpbxid = %s"

    try:
        curs = conn.cursor()
        curs.execute(query, (agentPbxId,))
        rows = curs.fetchall()

    except Exception as ex:
        logger.error(f'Error at SVMapping.find("{agentPbxId}"): {ex}')
        return None

    finally:
        curs.close()

    return rows
