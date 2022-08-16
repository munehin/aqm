import configparser
import logging.config
import os

class NwConfig():

    def __init__(self) -> None:
        # ログの取得
        try:
            logging.config.fileConfig("logging.conf")
            self.logger = logging.getLogger()
        except Exception as ex:
            print(f'Error at logging.getLogger():{ex}')

        pass

    def load(self):
        try:
            self.cfg = configparser.ConfigParser()
            self.cfg.read("settings.cfg")
        except Exception as ex:
            self.logger.error(f'Error at configparser.ConfigParser():{ex}')

    def check(self):
        try:
            self.bs0 = self.cfg["path"]["bs0"]
            self.bs1 = self.cfg["path"]["bs1"]
            self.bs2 = self.cfg["path"]["bs2"]
            self.report = self.cfg["path"]["report"]

            self.dnis = self.cfg["path"]["dnis"]

            #self.dsn = self.cfg["database"]["dsn"]
            self.user = self.cfg["database"]["user"]
            self.passwd = self.cfg["database"]["passwd"]
            self.host = self.cfg["database"]["host"]
            self.db = self.cfg["database"]["db"]

            try:
                self.maxwavtime = int(self.cfg["common"]["maxwavtime"]) 
            except Exception as ex:
                self.maxwavtime = 2147483647

            self.name = self.cfg["common"]["name"]
            self.wavdir = self.cfg["path"]["wavdir"]
            self.wavext = self.cfg["path"]["wavext"]

            # Pathの確認
            #if inputPath.endswith("\\") == False:
            #    inputPath += "\\"
            if os.path.exists(self.bs0) == False:
                self.logger.error(f'Check bs0. {self.bs0}')
                return False

            if os.path.exists(self.bs1) == False:
                self.logger.error(f'Check bs1. {self.bs1}')
                return False

            if os.path.exists(self.bs2) == False:
                self.logger.error(f'Check bs2. {self.bs2}')
                return False

            if os.path.exists(self.report) == False:
                self.logger.error(f'Check report. {self.report}')
                return False

            if len(self.dnis) > 0: 
                if os.path.exists(self.dnis) == False:
                    self.logger.error(f'Check dnis. {self.dnis}')
                    return False

            #     connect= pyodbc.connect(dsn)
            #     connect.close()

        except Exception as ex:
            self.logger.error(f'Check Path or dsn. {ex}')
            return False
        
        return True

    def get_bs0(self):
        return self.bs0

    def get_bs1(self):
        return self.bs1

    def get_bs2(self):
        return self.bs2

    def get_report(self):
        return self.report

    def get_dnis(self):
        return self.dnis

    def get_dsn(self):
        return self.dsn

    def get_user(self):
        return self.user

    def get_passwd(self):
        return self.passwd

    def get_host(self):
        return self.host    

    def get_db(self):
        return self.db

    def get_maxwavtime(self):
        return self.maxwavtime

    def get_name(self):
        return self.name

    def get_wavdir(self):
        return self.wavdir

    def get_wavext(self):
        return self.wavext
