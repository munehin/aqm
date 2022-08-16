import logging.config
import os
import re
import shutil

# ログ設定の取得
try:
    logging.config.fileConfig("logging.conf")
    logger = logging.getLogger()
except Exception as ex:
    print(f'Error at logging.getLogger():{ex}')

def remove(path):
    try:
        # ctiファイル
        os.remove(path)

    except Exception as ex:
        logger.error(f'Error at remove({path}): {ex}')
        return False
    
    return True

def remove2(path, wavdir, wavext):
    try:
        wavpath = getWavpath(path, wavdir, wavext)

        # ctiファイル
        os.remove(path)
        # wavファイル
        os.remove(wavpath)

    except Exception as ex:
        logger.error(f'Error at remove2({path}): {ex}')
        return False
    
    return True

def isExist(file1, file2List):
    # for file2 in file2List:
    #     if file1.lower() == file2.lower():
    #         return True
    # return False
    return os.path.exists(file1)

#def move2bs1(path, bs1, jobname, ymd, extension):
def move2bs1(path, bs1, ymd, wavdir, wavext):
    try:
        #xmlfile = getXmlfile(path)
        #wavfile = getWavfile(path)
        wavpath = getWavpath(path, wavdir, wavext)
        if len(wavpath) == 0:
            logger.error(f'Wavpathの取得に失敗しました。({path}, {wavdir}, {wavext})')
            return False
        newxml = getBs1path(path, bs1, ymd, wavdir, wavext)
        if len(newxml) == 0:
            logger.error(f'Bs1pathの取得に失敗しました。({path}, {bs1}, {ymd}, {wavdir}, {wavext})')
            return False
        newwav = getBs1path(wavpath, bs1, ymd, wavdir, wavext)
        if len(newwav) == 0:
            logger.error(f'Bs1pathの取得に失敗しました。({wavpath}, {bs1}, {ymd}, {wavdir}, {wavext})')
            return False

        # ctiファイル
        #target = f'{bs1}\\{jobname}\\{ymd}\\{extension}\\IDX'
        newdir = os.path.dirname(newxml)
        # Pathの確認
        if os.path.exists(newdir) == False:
            os.makedirs(newdir)
        #xmlファイルの移動
        shutil.move(path, newxml)

        # wavファイル
        #target = f'{bs1}\\{jobname}\\{ymd}\\{extension}\\WAV'
        newdir = os.path.dirname(newwav)
        # Pathの確認
        if os.path.exists(newdir) == False:
            os.makedirs(newdir)
        #wavファイルの移動
        shutil.move(wavpath, newwav)

    except Exception as ex:
        logger.error(f'Error at move2bs1({path}, {bs1}, {ymd}): {ex}')
        return False
    
    return True

# def getXmlfile(path):
#     rt = re.match('^.*\\\\IDX\\\\([^\\\\]*\.xml)$', path, re.IGNORECASE) 
#     if rt != None:
#         buf = rt.group(1)
#         return buf
#     return ""

def getWavpath(path, wavdir, wavext):
    rt = re.match('^(.*)\\\\IDX\\\\([^\\\\]*)\.xml$', path, re.IGNORECASE) 
    if rt != None:
        buf = f'{rt.group(1)}\\{wavdir}\\{rt.group(2)}.{wavext}'
        return buf
    return ""

# def getWavfile(path):
#     rt = re.match('^.*\\\\IDX\\\\([^\\\\]*)\.xml$', path, re.IGNORECASE) 
#     if rt != None:
#         buf = f'{rt.group(1)}.wav'
#         return buf
#     return ""

#def getBs1path(path, bs1, jobname, ymd, extension):
    # xmlfile = getXmlfile(path)
    # target = f'{bs1}\\{jobname}\\{ymd}\\{extension}\\IDX'
    # return os.path.join(target, xmlfile)
def getBs1path(path, bs1, ymd, wavdir, wavext):
    #rt = re.match(f'^.*\\\\([^\\\\]*)\\\\([^\\\\]*\\\\(IDX|{wavdir})\\\\[^\\\\]*\.(xml|{wavext}))$', path, re.IGNORECASE) 
    rt = re.match(f'^.*\\\\([^\\\\]*)\\\\([^\\\\]*\\\\[^\\\\]*\\\\(IDX|{wavdir})\\\\[^\\\\]*\.(xml|{wavext}))$', path, re.IGNORECASE) 
    if rt != None:
        buf = f'{bs1}\\{rt.group(1)}\\{ymd}\\{rt.group(2)}'
        return buf
    return ""

def move2bs2(path, bs2, jobname, ymd, extension, agentPBXID, wavdir, wavext):
    try:
        newfile = getNewfile(os.path.basename(path), extension, agentPBXID)
        if len(newfile) == 0:
            logger.error(f'Newfileの取得に失敗しました。({os.path.basename(path)}, {extension}, {agentPBXID})')
            return False
        wavpath = getWavpath(path, wavdir, wavext)
        if len(wavpath) == 0:
            logger.error(f'Wavpathの取得に失敗しました。({path}, {wavdir}, {wavext})')
            return False
        newwav = getNewfile(os.path.basename(wavpath), extension, agentPBXID)
        if len(newwav) == 0:
            logger.error(f'Newfile({os.path.basename(wavpath)}, {extension}, {agentPBXID})')
            return False
 
        newdir = f'{bs2}\\{jobname}\\{ymd}'

        # Pathの確認
        if os.path.exists(newdir) == False:
            os.makedirs(newdir)
        #xmlファイルの移動
        shutil.move(path, os.path.join(newdir, newfile))
        #wavファイルの移動
        shutil.move(wavpath, os.path.join(newdir, newwav))

    except Exception as ex:
        logger.error(f'Error at move2bs2({path}, {bs2}, {jobname}, {ymd}, {extension}, {agentPBXID}): {ex}')
        return False
    
    return True

def getNewfile(file, extension, agentPBXID):
    rt = re.match('^(\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})_sid_\d{8}_dbsid_\d{3}.((xml|wav|mp3))$', file, re.IGNORECASE) 
    if rt != None:
        buf = f'{rt.group(1)}_{extension}_{agentPBXID}_sid_dbsid.{rt.group(2)}'
        return buf
   
    return ""

# def getNewwav(file, extension, agentPBXID):
#     rt = re.match('^(\d{2}-\d{2}-\d{4}_\d{2}-\d{2}-\d{2})(_sid_\d{8}_dbsid_\d{3}.wav)$', file, re.IGNORECASE) 
#     if rt != None:
#         buf = f'{rt.group(1)}_{extension}_{agentPBXID}_sid_dbsid.wav'
#         return buf
#     return ""
