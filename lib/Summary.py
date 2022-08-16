import logging.config

# ログ設定の取得
try:
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger()
except Exception as ex:
    print("Error at logging.getLogger():", ex)

def create(conn, param):
    query = "INSERT INTO summaries(uploaded, total, ok, ng, wavsize, name, created)" \
        + " VALUES (CURDATE(), %s, %s, %s, %s, %s, NOW())"

    try:
        curs = conn.cursor()
        curs.execute(query, param)

    except Exception as ex:
        logger.error(f'Error at Summary.create({param}), {ex}')
        return False

    finally:
        curs.close()
 
    return True


