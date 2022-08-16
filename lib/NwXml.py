import datetime
import logging.config
import xml.etree.ElementTree as et

import lib.JobMapping as job
import lib.SVMapping as sv

class NwXml:

    def __init__(self) -> None:
        # ログの取得
        try:
            logging.config.fileConfig("logging.conf")
            self.logger = logging.getLogger()
        except Exception as ex:
            print(f'Error at logging.getLogger():{ex}')

        pass

    def load(self, filename):
        try:
            self.filename = filename
            self.tree = et.ElementTree(file=filename)

            root = self.tree.getroot()
            elem = root.find("CRI/Extension")
            if elem == None:
                self.logger.error(f'Extension is not exists. {filename}')
                return False
            self.extension = elem.text
            elem = root.find("CRI/AgentPBXID")
            if elem == None:
                self.logger.error(f'AgentPBXID is not exists. {filename}')
                return False
            self.agentPBXID = elem.text

            self.direction = None
            elem = root.find("CRI/Direction")
            if elem is not None:
                self.direction = elem.text

            self.dnis = None
            elem = root.find("CRI/DNIS")
            if elem is not None:
                self.dnis = elem.text

            LocalStartTime = None
            elem = root.find("CRI/LocalStartTime")
            if elem is not None:
                try:
                    LocalStartTime = datetime.datetime.strptime(elem.text, "%Y-%m-%dT%H:%M:%S.%f0+0900")
                except Exception as ex:
                    self.logger.error(f'LocalStartTime format error. {elem.text}')

            # LocalEndTime = None
            # elem = root.find("CRI/LocalEndTime")
            # if elem is not None:
            #     try:
            #         LocalEndTime = datetime.datetime.strptime(elem.text, "%Y-%m-%dT%H:%M:%S.%f0+0900")
            #     except Exception as ex:
            #         self.logger.error(f'LocalEndTime format error. {elem.text}')

            self.wavdate = None
            if LocalStartTime is not None:
                self.wavdate = LocalStartTime.date()

            # self.wavtime = 0
            # if LocalStartTime is not None and LocalEndTime is not None:
            #     self.wavtime = (LocalEndTime - LocalStartTime).total_seconds()

            self.wavtime = 0
            elem = root.find("CRI/Duration")
            if elem is not None:
                try:
                    self.wavtime = int(elem.text)
                except Exception as ex:
                    self.logger.error(f'Duration format error.')

        except Exception as ex:
            self.logger.error(f'Error at NwXml.load("{filename}"):{ex}')
            return False

        return True

    def get_extension(self):
        return self.extention

    def get_agentPBXID(self):
        return self.agentPBXID

    def get_direction(self):
        return self.direction

    def get_dnis(self):
        return self.dnis

    def get_wavdate(self):
        return self.wavdate

    def get_wavtime(self):
        return self.wavtime

    def change(self, jRow, svRow):
        try:
            root = self.tree.getroot()

            root.attrib['xmlns:xsd'] ="http://www.w3.org/2001/XMLSchema"
            root.attrib['xmlns:xsi'] ="http://www.w3.org/2001/XMLSchema-instance"

            elem = root.find("CRI")
            # AgentID
            elem.find('AgentID').text = svRow[sv.IDX_AGENTID]
            # AgentName
            root.find("Agent/Name").text = svRow[sv.IDX_AGENTNAME]
            # JobName
            et.SubElement(elem,'Jobs').text = jRow[job.IDX_JOB_NAME]
            # SuperVisorName
            et.SubElement(elem,'Supervisor').text = svRow[sv.IDX_SUPERVISORNAME]
            # ClientCode
            et.SubElement(elem,'ClientCode').text = jRow[job.IDX_CLIENTCODE]
            # SubJob
            et.SubElement(elem,'SubJob').text = jRow[job.IDX_SUBJOB]
            # AreaCode
            et.SubElement(elem,'AreaCode').text = jRow[job.IDX_AREACODE]
            # AreaName
            et.SubElement(elem,'AreaName').text = jRow[job.IDX_AREANAME]
            # CenterCode
            et.SubElement(elem,'CenterCode').text = jRow[job.IDX_CEMTERCODE]
            # CenterName
            et.SubElement(elem,'CenterName').text = jRow[job.IDX_CENTERNAME]

            #ANI
            elem.find('ANI').text = "0"
            #selem = et.SubElement(elem,'ANI').text = "0"
            #if elem is not None:
            #DNIS
            elem.find('DNIS').text = "0"
            #et.SubElement(elem,'DNIS').text = "0"
            #if elem is not None:

            self.tree.write(self.filename, encoding='utf-8', xml_declaration=True)

        except Exception as ex:
            self.logger.error(f'Error at NwXml.change("{jRow}, {svRow}"): {ex}')
            return False

        return True