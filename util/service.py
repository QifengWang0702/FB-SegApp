# -*- coding: UTF-8 -*-
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import A4
from PyCameraList.camera_device import list_video_devices
import pytesseract
import datetime
import subprocess
import psutil
import torch
import cv2
import re
import yaml
import shutil
import os
import sys
import util.database as database
from util.logger import logger
from util.createPdf import create
import dl.CSP_CV_seg as segment
import dl.SPIN_resolve as resolve
import dl.YOLOv8_keyPoint as keypoint

configs = ''
user = {}


def loadConfigs(configs_path):
    try:
        global configs
        with open(configs_path, 'r') as f:
            configs = yaml.load(f, Loader=yaml.Loader)
        logger.info(f'service - loadConfigs - load configs: {configs_path}')
    except Exception as e:
        logger.error(f'service - loadConfigs - {e}')
        return False


def getUserInfo():
    return user


def getConfigs():
    return configs


def getNowTime(mode=1):
    try:
        if mode:
            now = datetime.datetime.now()
            cur = now.strftime('%Y%m%d%H_%M%S%f')
        else:
            now = datetime.date.today()
            cur = now.strftime('%Y-%m-%d')
        logger.info(f'service - getNowTime - Get time: {cur}')
        return cur
    except Exception as e:
        logger.error(f'service - getNowTime - {e}')
        return ''


def saveFile(file, filename, saveClass, name=''):
    try:
        saveTime = getNowTime(0)
        save_dir = os.path.join(configs['save'][saveClass], saveTime)
        if saveClass == 'head':
            if name == '':
                logger.error(f'service - saveFile - save file name is empty!')
                return ''
            save_dir = os.path.join(configs['save'][saveClass], name)
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        if saveClass != 'report':
            cv2.imwrite(save_path, file)
        else:
            doc = SimpleDocTemplate(save_path, pagesize=A4)
            doc.build(file)
        return save_path
    except Exception as e:
        logger.error(f'service - saveFile - {e}')
        return ''


def deleteFile(path, table='', key=''):
    try:
        if isinstance(path, int):
            results, _ = database.find(table, [key], [path])
            if len(results) > 0:
                database.delete(table, key, path)
                logger.info(f'service - deleteFile - Delete {path} successfully!')
        else:
            if os.path.exists(path):
                if os.path.isdir(path):
                    os.rmdir(path)
                else:
                    os.remove(path)
                logger.info(f'service - deleteFile - Delete {path} successfully!')
    except Exception as e:
        logger.error(f'service - deleteFile - {e}')


def login(loginName, password):
    try:
        global user
        results, _ = database.find('doctor', ['loginName', 'password'], [loginName, password])
        if len(results):
            loginNumber = results[0].value(results[0].count() - 3) + 1
            lastTime = getNowTime(0)
            for i in range(results[0].count()):
                if i == results[0].count() - 3:
                    user[results[0].fieldName(i)] = loginNumber
                else:
                    user[results[0].fieldName(i)] = results[0].value(i)

            if not database.update('doctor', 'userId', results[0].value(0), ['loginNumber', 'lastTime'],
                                   [loginNumber, lastTime]):
                logger.error(f'service - login - {loginName} Login failed!')
                return False
            # userHeadPath = os.path.join(configs['save']['pic'], loginName)
            if not os.path.exists(os.path.join(configs['save']['head'], loginName, configs['picture']['head'])):
                head_path = os.path.join(configs['save']['pic'], configs['picture']['head'])
                userPath = changeUserHead(f'{head_path}', user['loginName'])
                if userPath == '':
                    logger.error(f'service - login - {loginName} login failed!')
            logger.info(f'service - login - {loginName} login successfully! login number: {loginNumber}')
            return True
        else:
            logger.error(f'service - login - {loginName} login failed!')
            return False
    except Exception as e:
        logger.error(f'service - login - {e}')
        return False


def getReportNum():
    try:
        results, _ = database.find('pregnant', [], [])
        logger.info(f'service - getReportNum - Get report number: {len(results)}')
        return len(results)
    except Exception as e:
        logger.error(f'service - getReportNum - {e}')
        return 0


def getLastLoginTime():
    try:
        if user['loginNumber'] > 1:
            logger.info(f'service - getLastLoginTime - Get last login time successfully!')
            return user['lastTime']
        elif 0 <= user['loginNumber'] < 2:
            logger.info(f'service - getLastLoginTime - Get last login time successfully!')
            return '2024-01-01'
        else:
            logger.error(f'service - getLastLoginTime - Get last login time failed!')
            return '2024-01-01'
    except Exception as e:
        logger.error(f'service - getLastLoginTime - {e}')
        return 'This is the first time login'


def getComputerStatus():
    try:
        gpu = 'None GPU'
        if torch.cuda.is_available():
            command = 'nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits'
            result = subprocess.check_output(command, shell=True)
            gpu = [int(x) for x in result.decode().strip().split('\n')]
        cpu = psutil.cpu_percent(interval=1)
        m = psutil.virtual_memory()
        memory = m.percent
        if gpu == 'None GPU':
            logger.info(f'service - getComputerStatus - Memory: {memory}%, CPU: {cpu}%, GPU: {gpu}')
        else:
            logger.info(f'service - getComputerStatus - Memory: {memory}%, CPU: {cpu}%, GPU: {gpu}%')
        return memory, cpu, gpu
    except Exception as e:
        logger.error(f'service - getComputerStatus - {e}')
        return -1, -1, 'None GPU'


def getCameraList():
    try:
        cameras = list_video_devices()
        camerasIds = []
        cameraNames = []
        for key, value in cameras:
            camerasIds.append(int(key))
            cameraNames.append(value)
        logger.info(f'service - getCameraList - Get cameras: {cameraNames}')
        return camerasIds
    except Exception as e:
        logger.error(f'service - getCameraList - {e}')


def isLegal(key, value, judge=False):
    try:
        tap = ''
        warn = ''
        if key in configs['update']['not_null'] and value == '':
            flag = False
            tap = f'The {key} can not be empty!'
        elif value == '':
            flag = True
        else:
            pattern = ''
            if key == 'reportId':
                pattern = r'^[1-9]\d*$'
                tap = 'The report id is wrong!'
                warn = 'The report id must be greater than 0!'
            if key == 'userId':
                pattern = r'^[1-9]\d*$'
                tap = 'The user id is wrong!'
                warn = 'The user id must be greater than 0!'
            if key == 'age':
                pattern = r'^((1[0-1])|[1-9])?\d$'
                tap = 'The age is wrong!'
                warn = 'The age must be greater than 0 and less than 120!'
            if key == 'name':
                pattern = r'^[A-Za-z\u4e00-\u9fa5]{1,64}$'
                tap = 'The name is not standardized!'
                warn = 'The name cannot be characters other than Chinese and English!'
            if key == 'pregweek':
                pattern = r'^(?:[1-9]|[1-3][0-9]|4[0-1])$'
                tap = 'The pregweek is wrong!'
                warn = 'The pregweek must be greater than 0 and less than 42!'
            if key == 'doctor':
                pattern = r'^(?![\u4e00-\u9fa5])[\w_-]{1,64}$'
                tap = 'The doctor name is not standardized!'
                warn = ('The doctor name cannot be characters other than the special character(_)(-), numbers and '
                        'English!')
            if key == 'result':
                pattern = r'^(normal|abnormal)$'
                tap = 'The result can only be normal or abnormal!'
            if key == 'loginName':
                pattern = r'^(?![\u4e00-\u9fa5])[\w_-]{1,64}$'
                tap = 'The login name is not standardized!'
                warn = ('The login name cannot be characters other than the special character(_)(-), numbers and '
                        'English!')
            if key == 'password':
                pattern = r'^(?=.*[A-Z]|.*[a-z]|.*\d|.*[@#$%^&*()_+\-=])[A-Za-z\d@#$%^&*()_+\-=]{6,32}$'
                tap = 'The password is not standardized!'
                warn = ('The password contains at least one of uppercase letters, lowercase letters, numbers, '
                        'and special characters, and is 8 to 32 characters in length. Special characters include (@), '
                        '(#), ($), (%), (^), (&), (*) (()), (_), (+), (-), (=) .')
            if key == 'identity':
                pattern = r'^(A|D)$'
                tap = 'The identity can only be A or D!'
            if key == 'cardId':
                pattern = r'^\d{17}[\dXx]$'
                tap = 'The card id is not standardized!'
                warn = 'The card id cannot contain characters other than numbers and X, and is 18 characters long.'
            if key == 'gender':
                pattern = r'^(M|F)$'
                tap = 'The gender can only be M or F!'
            if key == 'department':
                pattern = r'^[\w\\u4e00-\\u9fa5]{1,30}$'
                tap = 'The department is not standardized!'
                warn = 'The department cannot be characters other than numbers, Chinese and English!'
            flag = re.match(pattern, value) is not None
            if key == 'loginName' and judge:
                result, _ = database.find('doctor', [key], [value])
                flag = len(result) == 0
                tap = f'The login name {value} is exists!'
            if key == 'cardId' and judge:
                result, _ = database.find('doctor', [key], [value])
                flag = len(result) == 0
                tap = f'The card id {value} is exists!'
            if key == 'doctor' and judge:
                result, _ = database.find('doctor', ['loginName'], [value])
                flag = len(result) != 0
                tap = f'The doctor {value} is not exists!'
        if not flag:
            logger.error(f'service - isLegal - {key}: {value} - {tap}')
        else:
            logger.info(f'service - isLegal - {key}: {value} is legal!')
            tap = ''
            warn = ''
        return flag, tap, warn
    except Exception as e:
        logger.error(f'service - isLegal - {e}')
        return False, f'Error! Reason: {e}'


def getResolve(image_path):
    try:
        logger.info(f'service - getResolve - image_path: {image_path}')
        SPIN_path = os.path.join(configs['save']['configs'], configs['rebuild']['model']['SPIN_path'])
        FSRCNN_path = os.path.join(configs['save']['configs'], configs['rebuild']['model']['FSRCNN_path'])
        configs_path = os.path.join(configs['save']['configs'], configs['rebuild']['param'])
        image = cv2.imread(image_path)
        dst = resolve.SPIN_resolve(image_path, [SPIN_path, FSRCNN_path], configs_path)
        fileName = getNowTime()
        saveFile(image, fileName + '.jpg', 'import')
        visual_path = saveFile(dst, fileName + '.jpg', 'preprocess')
        return visual_path, fileName
    except Exception as e:
        logger.error(f'service - getResolve - {e}')
        return '', ''


def getCorrect(image_path):
    try:
        logger.info(f'service - getCorrect - image_path: {image_path}')
        YOLO_path = os.path.join(configs['save']['configs'], configs['correct']['model']['YOLO_path'])
        save_path = configs['save']['temp']
        reSize = list(configs['correct']['param']['reSize'])
        dstSize = list(configs['correct']['param']['dstSize'])
        image = cv2.imread(image_path)
        dst = keypoint.yolov8_keypoint(image_path, YOLO_path, save_path, reSize, dstSize)
        fileName = getNowTime()
        saveFile(image, fileName + '.jpg', 'capture')
        visual_path = saveFile(dst, fileName + '.jpg', 'preprocess')
        return visual_path, fileName
    except Exception as e:
        logger.error(f'service - getCorrect - {e}')
        return '', ''


def getSegCCC_CV(image_path, fileName=''):
    try:
        logger.info(f'service - getSegCCC_CV - image_path: {image_path}')
        CCC_path = os.path.join(configs['save']['configs'], configs['segmentation']['model']['CCC_path'])
        CV_path = os.path.join(configs['save']['configs'], configs['segmentation']['model']['CV_path'])
        net_type = configs['segmentation']['param']['net_type']
        in_chns = configs['segmentation']['param']['in_chns']
        class_num = configs['segmentation']['param']['class_num']
        size = configs['segmentation']['param']['size']
        lengthScale = configs['segmentation']['param']['lengthScale']
        areaScale = configs['segmentation']['param']['areaScale']

        CCC_pred = segment.inference(image_path, CCC_path, net_type, in_chns, class_num, size)
        CCC_pro, CCC_area, CCC_length = segment.compute(CCC_pred, lengthScale, areaScale)

        CV_pred = segment.inference(image_path, CV_path, net_type, in_chns, class_num, size)
        CV_pro, CV_area, CV_length = segment.compute(CV_pred, lengthScale, areaScale)

        image = cv2.imread(image_path)
        # image = cv2.imencode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        dst = segment.mix(image_path, CCC_pro, CV_pro, size)
        if fileName == '':
            fileName = getNowTime()
            saveFile(image, fileName + '.jpg', 'import')
            saveFile(image, fileName + '.jpg', 'preprocess')
        saveFile(CCC_pro, fileName + '.jpg', 'CCC')
        saveFile(CV_pro, fileName + '.jpg', 'CV')
        visual_path = saveFile(dst, fileName + '.jpg', 'visual')

        logger.info(f'service - getSegCCC_CV - Save visual to {visual_path}')
        logger.info(f'service - getSegCCC_CV - Get CCC&CV successfully!')
        return visual_path, fileName, round(CCC_area, 2), round(CV_area, 2), round(CCC_length, 2), round(CV_length, 2)
    except Exception as e:
        logger.error(f'service - getSegCCC_CV - {e}')
        return '', '', 0, 0, 0, 0


def getSegResult(CArea, CLength, VArea, VLength):
    try:
        CAreaScale = configs['segmentation']['normal']['CAreaScale']
        CLengthScale = configs['segmentation']['normal']['CLengthScale']
        VAreaScale = configs['segmentation']['normal']['VAreaScale']
        VLengthScale = configs['segmentation']['normal']['VLengthScale']
        if CArea < CAreaScale[0] or CArea > CAreaScale[1]:
            return False
        if CLength < CLengthScale[0] or CLength > CLengthScale[1]:
            return False
        if VArea < VAreaScale[0] or VArea > VAreaScale[1]:
            return False
        if VLength < VLengthScale[0] or VLength > VLengthScale[1]:
            return False
        return True
    except Exception as e:
        logger.error(f'service - getSegResult - {e}')
        return False


def getOcr(image_path):
    try:
        image = cv2.imread(image_path, 0)
        # image = cv2.imencode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        # image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, w = image.shape
        image_cut = image[0:80, 180:int(w / 3)]
        _, binary = cv2.threshold(image_cut, 128, 255, cv2.THRESH_BINARY)
        text = pytesseract.image_to_string(binary)
        pattern = r'\b(\d+)w'
        matches = re.findall(pattern, text)
        # print(text)
        if matches:
            logger.info(f'service - getOcr - get Text: {matches[0]}w')
            return matches[0] + 'w', ''
        else:
            logger.info(f'service - getOcr - get Text: none')
            return 'none', ''
    except Exception as e:
        logger.error(f'service - getOcr - {e}')
        return 'none', 'Get pregweek error! Please check your Tesseract-OCR environment path!'


def storeResult(name, date, result, report_path, pregweek='none', age=-1, doctor='', id=0, isSecond=False):
    try:
        if isSecond:
            os.path.join(configs['save']['report'], report_path + '.pdf')
            results, _ = database.find('pregnant', ['report'], [report_path])
            if len(results) > 0:
                id = results[0].value(0)
        keys = ['name', 'doctor', 'date', 'result', 'report']
        if doctor == '':
            doctor = user['loginName']
        values = [name, doctor, date, result, report_path]
        if pregweek != 'none':
            keys.append('pregweek')
            if len(pregweek) > 2:
                pregweek = pregweek[:-1]
            values.append(int(pregweek))
        if age != -1:
            keys.append('age')
            values.append(age)
        if id != 0:
            keys.append('reportId')
            values.append(id)
        flag = database.add('pregnant', keys, values)
        if flag:
            result, _ = database.find('pregnant', keys, values)
            # print(result[0].value(1))
            logger.info(f'service - storeResult - Store successfully! id: {result[0].value(0)}')
            return result[0].value(0)
        else:
            logger.error(f'service - storeResult - Store result error!')
            return -1
    except Exception as e:
        logger.error(f'service - storeResult - {e}')
        return -1


def setPDF(fileName, reportId, visual_path, CArea, CLength, VArea, VLength, name, pregweek, date, result, age=-1,
           docName='', department=''):
    try:
        if reportId == -1:
            logger.error(f'service - setPDF - Store report failed!')
            return False
        if docName == '' and department == '':
            docName = user['loginName']
            department = user['department']
        if age == -1:
            content = create(configs, reportId, visual_path, CArea, CLength, VArea, VLength, name, pregweek, docName,
                             date, result, 'none', department)
        else:
            content = create(configs, reportId, visual_path, CArea, CLength, VArea, VLength, name, pregweek, docName,
                             date, result, age, department)
        if not fileName.endswith('.pdf'):
            fileName = fileName + '.pdf'
        report_path = saveFile(content, fileName, 'report')

        if not database.update('pregnant', 'reportId', reportId, ['report'], [report_path]):
            logger.error(f'service - setPDF - report {reportId} Update failed!')
            return ''
        logger.info(f'service - setPDF - Store PDF successfully! id: {reportId}')
        return report_path
    except Exception as e:
        logger.error(f'service - setPDF - {e}')
        return ''


def getFieldName(table):
    try:
        _, model = database.find(table, [], [])
        headers = []
        for i in range(model.record().count()):
            headers.append(model.record().fieldName(i))
        logger.info(f'service - getFieldName - Get headers: {headers}')
        return headers
    except Exception as e:
        logger.error(f'service - getFieldName - {e}')


def getHistoryList(table, curPage=-1, pageCount=-1, key='', value='', headers=None):
    try:
        # if headers is not None and 'report' in headers:
        #     headers.remove('report')
        if key == '' and value == '':
            if curPage == -1 and pageCount == -1:
                _, model = database.find(table, [], [], queryKey=headers)
            else:
                _, model = database.find(table, [], [], curPage * pageCount, pageCount, headers)
            logger.info(f'service - getHistoryList - Get history list successfully!')
            return model
        elif key == '' and value != '':
            logger.error(f'service - getHistoryList - Key is NULL!')
            return None
        if curPage == -1 and pageCount == -1:
            _, model = database.find(table, [key], [value], queryKey=headers)
        else:
            _, model = database.find(table, [key], [value], curPage * pageCount, pageCount, headers)
        logger.info(f'service - getHistoryList - Get history list successfully!')
        return model
    except Exception as e:
        logger.error(f'service - getHistoryList - {e}')
        return None


def deleteRow(table, key, value, report='', userHead=''):
    try:
        if report != '':
            fileName = report
            if '/' in report:
                fileName = report.split('\\')[-2].split('/')[-1] + '\\' + report.split('\\')[-1].split('.')[0]
            deleteFile(os.path.join(configs['save']['preprocess'], fileName + '.jpg'))
            deleteFile(os.path.join(configs['save']['CCC'], fileName + '.jpg'))
            deleteFile(os.path.join(configs['save']['CV'], fileName + '.jpg'))
            deleteFile(os.path.join(configs['save']['visual'], fileName + '.jpg'))
            deleteFile(os.path.join(configs['save']['capture'], fileName + '.jpg'))
            deleteFile(os.path.join(configs['save']['import'], fileName + '.jpg'))
            deleteFile(report)
        if userHead != '':
            userDir = os.path.join(configs['save']['head'], userHead)
            deleteFile(os.path.join(userDir, configs['picture']['head']))
            deleteFile(userDir)
        return deleteFile(int(value), table, key)
    except Exception as e:
        logger.error(f'service - deleteRow - {e}')
        return False


def addRow(table, keys: list, values: list):
    try:
        keys.append('loginNumber')
        values.append(0)
        keys.append('lastTime')
        values.append(getNowTime(0))
        if not database.add(table, keys, values):
            logger.error(f'service - addRow - {values[0]} add failed!')
            return False
        if not os.path.exists(os.path.join(configs['save']['head'], values[0], configs['picture']['head'])):
            head_path = os.path.join(configs['save']['pic'], configs['picture']['head'])
            userPath = changeUserHead(head_path, values[0])
            if userPath == '':
                logger.error(f'service - addRow - {values[0]} add failed!')
                return False
        return True
    except Exception as e:
        logger.error(f'service - deleteRow - {e}')
        return False


def changeUserHead(changePath, name):
    try:
        image = cv2.imread(changePath)
        userPath = saveFile(image, configs['picture']['head'], 'head', name)
        if userPath != '':
            logger.info(f'service - changeUserHead - Change user head successfully!')
        else:
            logger.error(f'service - changeUserHead - Change user head failed!')
        return userPath
    except Exception as e:
        logger.error(f'service - changeUserHead - {e}')
        return ''


def getUpdateAble(table):
    try:
        infoList = []
        identity = user['identity']
        for key in configs['update'][f'{table}_{identity}']:
            infoList.append(key)
        logger.info(f'service - getUpdateAble - Get update list: {infoList}')
        return infoList
    except Exception as e:
        logger.error(f'service - getUpdateAble - {e}')


def updateInfo(table, id, keys, values, name='', report=''):
    try:
        if table == 'doctor':
            flag = database.update(table, 'userId', id, keys, values)
            results, _ = database.find(table, ['userId'], [id])
            if not flag or len(results) == 0:
                logger.error(f'service - updateInfo - Update info failed!')
                return False
            if name == '':
                identity = user['identity']
                name = user['loginName']
                for i in range(results[0].count()):
                    if results[0].fieldName(i) in configs['update'][f'{table}_{identity}']:
                        user[results[0].fieldName(i)] = results[0].value(i)
                    if 'loginName' in results[0].fieldName(i):
                        loginName = results[0].value(i)
            else:
                for i in range(results[0].count()):
                    if 'loginName' in results[0].fieldName(i):
                        loginName = results[0].value(i)
            if name != loginName:
                userPath = changeUserHead(os.path.join(configs['save']['head'], name, configs['picture']['head']), loginName)
                if userPath == '':
                    logger.error(f'service - updateInfo - {name} update failed!')
                shutil.rmtree(os.path.join(configs['save']['head'], name))
        elif report != ''and user['identity'] == 'A':
            results, _ = database.find('doctor', ['loginName'], [values[3]])
            if len(results) == 0:
                logger.error(f'service - updateInfo - There is no doctor {values[3]}!')
                return False
            fileName = report
            if '/' in report:
                fileName = report.split('\\')[-2].split('/')[-1] + '\\' + report.split('\\')[-1].split('.')[0]
            root_path = os.path.join(configs['save']['preprocess'], fileName + '.jpg')
            visual_path, file_name, CArea, VArea, CLength, VLength = getSegCCC_CV(root_path)
            deleteRow(table, 'reportId', id, report=report)
            date = getNowTime(0)
            if values[2] == '':
                values[2] = 'none'
            storeResult(values[0], date, values[4], file_name, values[2], values[1], values[3], id)
            report_path = setPDF(file_name, id, visual_path, CArea, CLength, VArea, VLength, values[0], values[2], date,
                                 values[4], values[1], values[3], results[0].value(6))
            if report_path == '':
                logger.error(f'service - updateInfo - Report path is none!')
                return False
        elif report != '' and user['identity'] != 'A':
            results, _ = database.find(table, ['reportId'], [id])
            print(report)
            fileName = report
            if '/' in report:
                fileName = report.split('\\')[-2].split('/')[-1] + '\\' + report.split('\\')[-1].split('.')[0]
            root_path = os.path.join(configs['save']['preprocess'], fileName + '.jpg')
            visual_path, file_name, CArea, VArea, CLength, VLength = getSegCCC_CV(root_path)
            deleteRow(table, 'reportId', id, report=report)
            date = getNowTime(0)
            if values[0] == '':
                values[0] = 'none'
            storeResult(results[0].value(1), date, values[1], file_name, values[0],
                                   results[0].value(2), user['loginName'], id)
            report_path = setPDF(file_name, id, visual_path, CArea, CLength, VArea, VLength, results[0].value(1),
                                 values[0], date, values[1], results[0].value(2),
                                 user['loginName'], user['department'])
            if report_path == '':
                logger.error(f'service - updateInfo - Report path is none!')
                return False
        else:
            logger.error(f'service - updateInfo - Update info failed!')
            return False
        logger.info(f'service - updateInfo - Update info successfully!')
        return True
    except Exception as e:
        logger.error(f'service - updateInfo - {e}')
        return False


def openDir(path):
    try:
        path = os.path.abspath(path)
        if not os.path.exists(path):
            logger.error(f'service - openDir - {path} not exists!')
            return False
        platform = sys.platform
        if platform == 'darwin':
            order = 'open ' + path
        elif 'linux' in platform:
            order = 'nautilus ' + path
        elif 'win' in platform:
            order = 'start ' + path
        else:
            logger.error(f'service - openDir - The IRSPUI does not currently support {platform}!')
            return False
        os.system(order)
        logger.info(f'service - openDir - {path} successfully opened!')
        return True
    except Exception as e:
        logger.error(f'service - openDir - {e}')
        return False
