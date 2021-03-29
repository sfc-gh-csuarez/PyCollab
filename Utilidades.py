import datetime
import requests
from tqdm import tqdm 
from tqdm import trange
from webService import WebService
import csv
import sys,getopt
import json
from time import sleep

webService = WebService()

def listaGrabaciones(recordings):
        recordinglist = []
        x=0
        try:
          number_of_recordings = (len(recordings['results']))
          if number_of_recordings <= 0:
             return None
          while x < number_of_recordings:
            recording_id = recordings['results'][x]['id']
            rec_data = webService.get_recording_data(recording_id)
            if rec_data != None:
                if 'mediaDownloadUrl' in rec_data:  
                    size = recording_storageSize(rec_data['mediaDownloadUrl'])
                elif 'storageSize' in recordings['results'][x]:
                    size = recordings['results'][x]['storageSize']
                else:
                    size = recording_storageSize(rec_data['extStreams'][0]['streamUrl'])
                recordinglist.append({"recording_id" : recordings['results'][x]['id'], "recording_name" : recordings['results'][x]['name'], "duration":recordings['results'][x]['duration'], "storageSize":size,"created": recordings['results'][x]['created']})
            else:
                recordinglist.append({"recording_id" : recordings['results'][x]['id'],"recording_name" : recordings['results'][x]['name'],'msg':403})
            x += 1
          return recordinglist
        except TypeError:
            return None



def listaGrabacionesOnlyData(recordings):
        recordinglist = []
        x=0
        try:
          number_of_recordings = (len(recordings['results']))
          if number_of_recordings <= 0:
             return None
          while x < number_of_recordings:
            recording_id = recordings['results'][x]['id']
            rec_data = webService.get_recording_data_4url(recording_id)
            if rec_data != None:
                if 'mediaDownloadUrl' in rec_data:  
                    size = recording_storageSize(rec_data['mediaDownloadUrl'])
                elif 'storageSize' in recordings['results'][x]:
                    size = recordings['results'][x]['storageSize']
                else:
                    size = recording_storageSize(rec_data['extStreams'][0]['streamUrl'])
                recordinglist.append({"recording_id" : recordings['results'][x]['id'], "recording_name" : recordings['results'][x]['name'], "duration":recordings['results'][x]['duration'], "storageSize":size,"created": recordings['results'][x]['created']})
            else:
                recordinglist.append({"recording_id" : recordings['results'][x]['id'],"recording_name" : recordings['results'][x]['name'],'msg':403})
            x += 1
          return recordinglist
        except TypeError:
            return None



def listaGrabacion(recording_info):
    if recording_info == None:
        return None
    else:
        if 'storageSize' in recording_info and 'created' in recording_info:
            recording_data = {"recording_id" : recording_info['id'], "recording_name" : recording_info['name'], "duration":recording_info['duration'], "storageSize":recording_info['storageSize'],"created": recording_info['created']}
        else:
            rec_data = webService.get_recording_data(recording_info['results'][0]['id'])
            if 'mediaDownloadUrl' in rec_data:  
                size = recording_storageSize(rec_data['mediaDownloadUrl'])
            else:
                size = recording_storageSize(rec_data['extStreams'][0]['streamUrl'])
            recording_data = {"recording_id" : recording_info['id'], "recording_name" : recording_info['name'], "duration":recording_info['duration'], "storageSize":size,"created": recording_info['created']}
        return recording_data

        


def listaGrabacionCollabData(recording_info):
    if recording_info == None:
        return None
    else:
        if 'mediaDownloadUrl' in recording_info:
            size = recording_storageSize(recording_info['mediaDownloadUrl'])
            chats = recording_info['chats']
            downloadUrl = None
            if len(chats) > 0:
                chat = recording_info['chats'][0]['url']
            else:
                chat = None
            recording_data = {'downloadUrl':recording_info['mediaDownloadUrl'], 'recording_name':recording_info['name'],'duration':recording_info['duration'],'created':recording_info['created'],'size':size, 'chat':chat}
        else:
            try:
                downloadUrl = recording_info['extStreams'][0]['streamUrl']
                size = recording_storageSize(downloadUrl)
                try:
                    chats = recording_info['chats']
                    if len(chats) > 0:
                        chat = recording_info['chats'][0]['url']
                    else:
                        chat = None
                except KeyError:
                    chat = None
            except KeyError:
                size : 0 
            if downloadUrl != None:
                recording_data = {'downloadUrl':downloadUrl, 'recording_name':recording_info['name'],'duration':recording_info['duration'],'created':recording_info['created'],'size':size,'chat':chat}
            else:
                recording_data = {'downloadUrl': None, 'recording_name':recording_info['name'],'duration':recording_info['duration'],'created':recording_info['created'],'size':size,'chat':chat}
            
    return recording_data



def recording_id(url:str):
    splitedURL = url.split('/')
    ultimo = splitedURL[len(splitedURL)-1]
    return ultimo


def readCollabReport(fileName:str):
    recording_ids = []
    with open(fileName,encoding='utf-8') as f:
        columnas = f.readline()
    if 'RecordingLink' in columnas:
        with open(fileName, newline='', encoding='utf-8') as nline:
            registers = csv.DictReader(nline)
            for register in registers:
                recording = recording_id(register['RecordingLink'])
                sessionOwner = register['SessionOwner']
                sessionName = register['SessionName']
                sessionIdentifier = register['SessionIdentifier']
                recName = register['RecordingName']
                recording_ids.append({'recording':recording, 'sessionOwner':sessionOwner,'recName':recName,'sessionName':sessionName, 'sessionId':sessionIdentifier})
            return recording_ids
        nline.close()
    else:
        return None



def recording_storageSize(url:str):
    r = requests.get(url, stream=True,headers={'Accept-Encoding': None})
    size = int(r.headers.get('content-length',0))
    return size




def descargarGrabacion(url:str, fname:str):
    resp = requests.get(url,stream=True)
    total = int(resp.headers.get('content-length',0))
    progress_bar = tqdm(total=total, unit='iB', unit_scale=True,unit_divisor=1024)
    with open(fname,'wb') as file:
            for data in resp.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
    progress_bar.close()



def crearArchivoChat(url:str,fname:str):
    chatFile = requests.get(url, stream=True)
    if chatFile.status_code == 200:
        try:
            jsonInfo = json.loads(chatFile.text)
            #CSV
            filename =  fname + '.csv'
            header = ["Participant id", "Student Name", "Message"]
            try:
                file = open(filename, 'w', encoding="utf-8")
                writer = csv.writer(file)
                writer.writerow(header)  
                for jsonRow in jsonInfo:
                    writer.writerow([jsonRow['id'],jsonRow['userName'], jsonRow['body']])
                file.close()
            except OSError as oserror:
                if oserror.errno == 36:
                    print("Long file name")
                    pass
            total = int(chatFile.headers.get('content-length',0))
            with tqdm(total=total) as progress_bar:
                for size in trange(total):
                    progress_bar.update(size)
            progress_bar.close()
        except json.decoder.JSONDecodeError:
            print('Chat file is empty')
            pass
    else:
        print("Chat URL is not valid:", str(chatFile))
    
    

             

def downloadrecording(recording_list, name, course_uuid):
      for recording in recording_list:
        recording_data = webService.get_recording_data(recording['recording_id'])
        if recording_data != None:
            filename = course_uuid + '-' + recording['recording_id'] + '-' + checkLongFilenameVideo(' ', recording['recording_name'])
            chatFileName = 'Chat-' + course_uuid +  '-' + recording['recording_id'] + '-' + checkLongFilenameChat(' ',recording['recording_name'])
            fullpath = './downloads/'
            print(fullpath + filename)
            descargarGrabacion(recording_data['extStreams'][0]['streamUrl'],fullpath + filename)
            
            if len(recording_data['chats']) == 0:
                print("No chat on the recording")
            else:
                print("Downloaling chat")
                downloadChats(recording_data['chats'][0],fullpath + chatFileName)
        
            


def downloadOneRecording(recording, course_id):
    if recording != 403:
        recording_data = webService.get_recording_data(recording['recording_id'])
        if recording_data != None:
            filename = course_id + '-' + recording['recording_id'] + '-' +  checkLongFilenameVideo(course_id, recording['recording_name'])
            chatFileName = 'Chat-' + course_id + '-' + recording['recording_id'] + '-' + checkLongFilenameChat(course_id,recording['recording_name'])
            fullpath = './downloads/'
            print(fullpath + filename)
            descargarGrabacion(recording_data['extStreams'][0]['streamUrl'],fullpath + filename)
            if len(recording_data['chats']) == 0:
                print("No chat on the recording")
            else:
                print("Downloaling chat")
                downloadChats(recording_data['chats'][0],fullpath + chatFileName)
            return True
        else:
            return None


def downloadOneRecordingURL(recording,recording_url, course_id):
        recording_data = webService.get_recording_data_4url(recording['recording_id'])
        if recording_data != None:
            filename = course_id + '-' + recording['recording_id'] + '-' +  checkLongFilenameVideo(course_id, recording['recording_name'])
            #chatFileName = 'Chat-' + course_id + '-' + recording['recording_id'] + '-' + checkLongFilenameChat(course_id,recording['recording_name'])
            fullpath = './downloads/'
            print(fullpath + filename)
            descargarGrabacion(recording_url,fullpath + filename)
            '''
            if len(recording_data['chats']) == 0:
                print("No chat on the recording")
            else:
                print("Downloaling chat")
                downloadChats(recording_data['chats'][0],fullpath + chatFileName)
            '''
            return True
        else:
            return None
           
     

def downloadOneRecordingOnly(recording):
    recording_data = webService.get_recording_data(recording['recording_id'])
    if recording_data != None:
        filename =  recording['recording_id'] + '-' +  checkLongFilenameVideo(' ', recording['recording_name'])
        chatFileName = 'Chat-' + recording['recording_id'] + '-' + checkLongFilenameChat(' ',recording['recording_name'])
        fullpath = './downloads/'
        print(fullpath + filename)
        descargarGrabacion(recording_data['extStreams'][0]['streamUrl'],fullpath + filename)
        if len(recording_data['chats']) == 0:
            print("No chat on the recording")
        else:
            print("Downloaling chat")
            downloadChats(recording_data['chats'][0],fullpath + chatFileName)
        return True
    else:
        return None




def downloadRecordingsUUID(recording_lista):
    if recording_lista != None:
        if 'recordingId' in recording_lista:
            filename =  recording_lista['recordingId'] + '-' +  checkLongFilenameVideo('', recording_lista['recording_name'])
        else:
            filename = checkLongFilenameVideo(recording_lista['recordingId'], recording_lista['recording_name'])
        chatFileName = 'Chat-' + filename
        fullpath = './downloads/'
        print(fullpath + filename)
        descargarGrabacion(recording_lista['downloadUrl'],fullpath + filename)
        if recording_lista['chat'] == None:
            print("No chat on the recording")
        else:
            print("Downloaling chat")
            downloadChatsFromURL(recording_lista['chat'],fullpath + chatFileName)
    else:
        print("No data from Recording ID on Collaborate")


def downloadFromURL(recording_id):
    url = webService.getRecordingURL(recording_id)
    return url



def downloadChats(chat_data,name):
    chat_url = chat_data['url']
    crearArchivoChat(chat_url,name)

def downloadChatsFromURL(chat_url,name):
    crearArchivoChat(chat_url,name)



def deleteRecording(recording_id):
    delete_info = webService.delete_recording(recording_id)
    if delete_info != None:
        return True
    else:
        return delete_info



def checkLongFilenameVideo(courseId:str, fname:str):
    filename = fname.replace(':', ' ').replace('/', ' ').replace('”', '').replace('“', '').replace(',', '').replace('?', '').replace('|', '').replace('"', '') + '.mp4'
    if len(filename) > 160:
        return courseId + '.mp4'
    else:
        return filename

def checkLongFilenameChat(courseId:str, fname:str):
    filename = fname.replace(':', ' ').replace('/', ' ').replace('”', '').replace('“', '').replace(',', '').replace('?', '').replace('|', '').replace('"', '') 
    if len(filename) > 160:
        return " "
    else:
        return filename



def crearReporte(reporte):
   filename = './reports/Collab_Download_RecordingReport.csv'
   header = ["sessionOwner","Recording ID", "Recording Name", "Duration", "Storage Size (MB)", "Created Date"]
   file = open(filename, 'w',newline='', encoding='utf-8')
   writer = csv.writer(file)
   writer.writerow(header)
   for x in range(len(reporte)):
      registro = reporte[x]
      sessionOwner = registro[0]
      recording_id = registro[1]
      recording_name = registro[2]
      duration = calcularTiempo(int(registro[3]/1000))
      storage = str(round(float(registro[4])/1000000, 2))
      created = convertirFecha(registro[5])
      writer.writerow([sessionOwner,recording_id,recording_name,duration,storage,created])
   file.close()
   return "Report: Collab_Download_RecordingReport.csv created!"



def crearReporteMoodle(reporte):
   filename = './reports/Collab_Moodle_Session_RecordingReport.csv'
   header = ["Recording ID", "Recording Name", "Duration", "Storage Size (MB)", "Created Date"]
   file = open(filename, 'w',newline='', encoding='utf-8')
   writer = csv.writer(file)
   writer.writerow(header)
   for x in range(len(reporte)):
      registro = reporte[x]
      recording_id = registro[0]
      recording_name = registro[1]
      duration = calcularTiempo(int(registro[2]/1000))
      storage = str(round(float(registro[3])/1000000, 2))
      created = convertirFecha(registro[4])
      writer.writerow([recording_id,recording_name,duration,storage,created])
   file.close()
   return "Report: Collab_Moodle_Session_RecordingReport.csv created!"



def crearReporteCollabDownload(reporte):
   filename = './reports/Collab_Download_RecordingReport.csv'
   header = ["Course ID/UUID","Recording ID", "Recording Name", "Duration", "Storage Size (MB)", "Created Date"]
   file = open(filename, 'w',newline='', encoding='utf-8')
   writer = csv.writer(file)
   writer.writerow(header)
   for x in range(len(reporte)):
      registro = reporte[x]
      course_id = registro[0]
      recording_id = registro[1]
      recording_name = registro[2]
      duration = calcularTiempo(int(registro[3]/1000))
      storage = str(round(float(registro[4])/1000000, 2))
      created = convertirFecha(registro[5])
      writer.writerow([course_id,recording_id,recording_name,duration,storage,created])
   file.close()
   return "Report: Collab_Download_RecordingReport.csv created!"


def crearReporteCollabRecIdDownload(reporte):
   filename = './reports/Collab_Download_RecordingsId_Report.csv'
   header = ["Recording ID", "Recording Name", "Duration", "Storage Size (MB)", "Created Date"]
   file = open(filename, 'w',newline='', encoding='utf-8')
   writer = csv.writer(file)
   writer.writerow(header)
   for x in range(len(reporte)):
      registro = reporte[x]
      
      recording_id = registro[0]
      recording_name = registro[1]
      duration = calcularTiempo(int(registro[2]/1000))
      storage = str(round(float(registro[3])/1000000, 2))
      created = convertirFecha(registro[4])
      writer.writerow([recording_id,recording_name,duration,storage,created])
   file.close()
   return "Report: Collab_Download_RecordingsId_Report.csv created!"


def crearReporte_403(reporte):
   filename = './reports/Collab_Download_RecordingReport_403.csv'
   header = ["Course ID","Recording ID", "Recording Name", "Detail"]
   file = open(filename, 'w',newline='', encoding='utf-8')
   writer = csv.writer(file)
   writer.writerow(header)
   for x in range(len(reporte)):
      registro = reporte[x]
      course_id = registro[0]
      recording_id = registro[1]
      recording_name = registro[2]
      detail = registro[3]
      writer.writerow([course_id,recording_id,recording_name,detail])
   file.close()
   return "Report: Collab_Download_RecordingReport_403.csv created!"
   


def crearReporteCollab(reporte):
    filename = './reports/Collab_Report_from_Course.csv'
    headers = [ 'Course ID', 'Course Name','Course UUID', 'Recording ID', 'Recording Name','Duration', 'Storage Size (MB)', 'Created Date']
    file = open(filename, 'w', newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(headers)
    for x in range(len(reporte)):
        registro = reporte[x]
        course_id = registro[0]
        couse_name = registro[1]
        course_uuid = registro[2]
        recording_id = registro[3]
        recording_name = registro[4]
        duration = calcularTiempo(int(registro[5]/1000))
        storageSize = str(round(float(registro[6])/1000000, 2))
        if registro[7]== 'not defined':
            created = 'not defined'
        else:
            created = convertirFecha(registro[7])
        writer.writerow([course_id,couse_name,course_uuid,recording_id,recording_name,duration,storageSize,created])
    file.close()
    return "Report: Collab_Report_from_Course.csv created!"



def crearReporteCollabRecordings(reporte):
    filename = './reports/Collab_Report_Recordings.csv'
    headers = ['sessionOwner','Recording ID', 'Recording Name','Duration', 'Storage Size (MB)', 'Created Date']
    file = open(filename, 'w',newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(headers)
    for x in range(len(reporte)):
        registro = reporte[x]
        session_ownner = registro[0]
        recording_id = registro[1]
        recording_name = registro[2]
        duration = calcularTiempo(int(registro[3]/1000))
        storageSize = str(round(float(registro[4])/1000000, 2))
        created = convertirFecha(registro[5])
        writer.writerow([session_ownner,recording_id,recording_name,duration,storageSize,created])
    file.close()








def crearReporteCollab_403(reporte):
    filename = './reports/Collab_Report_from_Course_error.csv'
    headers = [ 'Course ID', 'Course Name','Course UUID', 'Recording ID', 'Recording Name','Detail']
    file = open(filename, 'w',newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(headers)
    for x in range(len(reporte)):
        registro = reporte[x]
        course_id = registro[0]
        couse_name = registro[1]
        course_uuid = registro[2]
        recording_id = registro[3]
        recording_name = registro[4]
        detail = registro[5]
        writer.writerow([course_id,couse_name,course_uuid,recording_id,recording_name,detail])
    file.close()
    return "Report: Collab_Report_from_Course_error.csv created!"



def crearReporte_Recordings_403(reporte):
    filename = './reports/Collab_Report_Recordings_error.csv'
    headers = [ 'OwnerSession', 'Session Name','Session ID', 'Recording ID', 'Recording Name','Detail']
    file = open(filename, 'w',newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(headers)
    for x in range(len(reporte)):
        registro = reporte[x]
        course_id = registro[0]
        couse_name = registro[1]
        course_uuid = registro[2]
        recording_id = registro[3]
        recording_name = registro[4]
        detail = registro[5]
        writer.writerow([course_id,couse_name,course_uuid,recording_id,recording_name,detail])
    file.close()
    return "Report: Collab_Download_RecordingReport_error.csv created!"


def crearReporteDelete(reporte):
    filename = './reports/Collab_Delete_Recordings.csv'
    headers = [ 'Recording Id', 'Status']
    file = open(filename, 'w',newline='', encoding='utf-8')
    writer = csv.writer(file)
    writer.writerow(headers)
    for x in range(len(reporte)):
        registro = reporte[x]
        recording_id = registro[0]
        status = registro[1]
        writer.writerow([recording_id,status])
    file.close()
    return "Report: Collab_Delete_Recordings.csv created!"




def leerCursos(filename):
   cursos = []
   with open(filename,encoding='utf-8') as reader:
      for linea in reader:
         contenido = linea.rstrip()
         cursos.append(str(contenido))
   reader.close()
   return cursos


def leerUUID(filename):
   uuids = []
   with open(filename,encoding='utf-8') as reader:
      for linea in reader:
         contenido = linea.rstrip()
         uuids.append(str(contenido))
   reader.close()
   return uuids

def leerRecUUID(filename):
   uuids = []
   with open(filename,encoding='utf-8') as reader:
      for linea in reader:
         contenido = linea.rstrip()
         uuids.append(str(contenido))
   reader.close()
   return uuids





def main(argv):
    archivoCursos = ''
    archivoUUID = ''
    semanas = 0
    try:
        opts,args = getopt.getopt(argv,"hf:e:w:", ["cfile=","ext=","weeks="])
    except getopt.GetoptError:
        print('Collab.py -f <LearnFileName_COURSE_ID.txt> -w <numberOfWeekBehindToSearch>')
        print('Collab.py -e <LearnFileName_COURSE_UUID> -w <numberOfWeekBehindToSearch>')
        
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('Collab.py -f <LearnFileName_COURSE_ID.txt> -w <numberOfWeekBehindToSearch>')
            print('Collab.py -e <LearnFileName_COURSE_UUID> -w <numberOfWeekBehindToSearch>')

            sys.exit()
        elif opt in ('-f', '--cfile'):
            archivoCursos = arg
        elif opt in ('-w', '--weeks'):
            semanas = int(arg)
        elif opt in ('-e', '--ext'):
            archivoUUID = arg
    return [archivoCursos, archivoUUID, semanas]



def mainMoodle(argv):
    moodleSessionID = ''
    moodleLTI = ''
    semanas = 0
    try:
        opts,args = getopt.getopt(argv,"hs:l:w:", ["session=","lti=","weeks="])
    except getopt.GetoptError:
        print("The correct params are:")
        print('CollabMoodle.py -s <MoodlePlugInFileName_SESSION_ID.txt> -w <numberOfWeekBehindToSearch>')
        print('CollabMoodle.py -l <MoodleFileName_LTI.txt> -w <numberOfWeekBehindToSearch>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabMoodle.py -s <MoodlePlugInFileName_SESSION_ID.txt> -w <numberOfWeekBehindToSearch>')
            print('CollabMoodle.py -l <MoodleFileName_LTI.txt> -w <numberOfWeekBehindToSearch>')
            sys.exit()
        elif opt in ('-s', '--session'):
            moodleSessionID = arg
        elif opt in ('-l', '--lti'):
            moodleLTI = arg
        elif opt in ('-w', '--weeks'):
            semanas = int(arg)
    return [moodleSessionID, moodleLTI, semanas]



def mainReport(argv):
    archivoCursos = ''
    semanas = 0
    try:
        opts,args = getopt.getopt(argv,"hf:w:", ["cfile=","weeks="])
    except getopt.GetoptError:
        print('CollabReport.py -f <LearnFileName_COURSE_ID.txt> -w <numberOfWeekBehindToSearch>')
        
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabReport.py -f <LearnFileName_COURSE_ID.txt> -w <numberOfWeekBehindToSearch>')
            sys.exit()
        elif opt in ('-f', '--cfile'):
            archivoCursos = arg
        elif opt in ('-w', '--weeks'):
            semanas = int(arg)
    return [archivoCursos, semanas]




def mainRecordings(argv):
    recordingsFile = ''
    try:
        opts,args = getopt.getopt(argv,"hf:", ["recordings="])
    except getopt.GetoptError:
        print("The correct params are:")
        print('CollabRecordings.py -f <RecordingsReport.csv>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabRecordings.py -f <RecordingsReport.csv>')
            sys.exit()
        elif opt in ('-f', '--recordings'):
            recordingsFile = arg
    return [recordingsFile]


def mainMinutes(argv):
    attendanceFile = ''
    try:
        opts,args = getopt.getopt(argv,"hf:", ["attendance="])
    except getopt.GetoptError:
        print("The correct params are:")
        print('CollabMinutes.py -t <AttendaceReport.csv>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabMinutes.py -t <AttendaceReport.csv>')
            sys.exit()
        elif opt in ('-f', '--attendance'):
            attendanceFile = arg
    return [attendanceFile]




def mainStorage(argv):
    recordingFile = ''
    try:
        opts,args = getopt.getopt(argv,"hf:", ["recordings="])
    except getopt.GetoptError:
        print("The correct params are:")
        print('CollabStorage.py -t <RecordingReport.csv>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabStorage.py -t <RecordingReport.csv>')
            sys.exit()
        elif opt in ('-f', '--recordings'):
            recordingFile = arg
    return [recordingFile]


def mainRecfromid(argv):
    attendanceFile = ''
    try:
        opts,args = getopt.getopt(argv,"hf:", ["list="])
    except getopt.GetoptError:
        print("The correct params are:")
        print('CollabRecfromid.py -f <recodidingids_list.txt>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabRecfromid.py -f <recodidingids_list.txt>')
            sys.exit()
        elif opt in ('-f', '--list'):
            attendanceFile = arg
    return [attendanceFile]


def mainDelete(argv):
    attendanceFile = ''
    try:
        opts,args = getopt.getopt(argv,"hf:", ["list="])
    except getopt.GetoptError:
        print("The correct params are:")
        print('CollabDeleteRecordings.py -f <recodidingids_list.txt>')
        sys.exit(2)
    for opt,arg in opts:
        if opt == '-h':
            print('CollabDeleteRecordings.py -f <recodidingids_list.txt>')
            sys.exit()
        elif opt in ('-f', '--list'):
            attendanceFile = arg
    return [attendanceFile]


def calcularTiempo(s):
   m, s = divmod(s,60)
   h,m = divmod(m,60)
   d, h = divmod(h,24)
   tiempoEnSesion =  datetime.time(h,m,s)
   return tiempoEnSesion.strftime('%H:%M:%S')


def convertirFecha(fecha):
   objetoFecha = datetime.datetime.strptime(fecha,'%Y-%m-%dT%H:%M:%S.%fZ')
   return objetoFecha.strftime('%b %d,%Y')


def semanasAtiempo(weeks):
    tiempo = datetime.datetime.now() - datetime.timedelta(weeks=int(weeks))
    tiempo = tiempo.strftime('%Y-%m-%dT%H:%M:%SZ')
    return tiempo


def collabTimeToMinutes(stime:str):
    #ctime = datetime.datetime.strptime(stime,'%H:%M:%S').time()
    ctime = stime.split(':')
    hours = float(ctime[0])*60
    minutes = float(ctime[1])
    seconds = float(ctime[2])/60
    return round(hours + minutes + seconds)
    

def collabMinutes(fileName:str):
    minutes = 0
    with open(fileName, encoding='utf-8') as f:
        columnas = f.readline()
    if 'AttendeeTotalTimeInSession' in columnas:
        with open(fileName, newline='', encoding='utf-8') as nline:
            registers = csv.DictReader(nline)
            for register in registers:
                minutes += collabTimeToMinutes(register['AttendeeTotalTimeInSession'])
            fminutes = round(minutes)
            return '{:,}'.format(fminutes)
        nline.close()
    else:
        return None
    f.close 


def collabMinutesLoginGroups(fileName:str,login_gropus):
    minutesByLoginGroup = convertList2Dic(login_gropus)
    with open(fileName, newline='', encoding='utf-8') as nline:
        registers = csv.DictReader(nline)
        for register in registers:
            if register['SessionOwner'] in login_gropus:
                data = str2Minutes(register['RecordingDuration'])
                if data != None:
                    minutesByLoginGroup[register['SessionOwner']] += data
                #minutesByLoginGroup[register['SessionOwner']] += 1   
    nline.close()
    return minutesByLoginGroup


def convertList2Dic(aList):
    fDict = {aList[idx]:0 for idx in range(0,len(aList))}
    return fDict    

def str2Minutes(t):
    s = str(t)
    total = 0
    times = s.split(':')
    if len(times) == 1 and times[0] == '':
        pass 
    else:
        horas2min = float(times[0]) * 60
        mins = float(times[1])
        seg2min = float(times[2]) / 60
        total = round(horas2min + mins + seg2min)
    return total
    
    


def collabLoginGroup(fileName:str):
    loginGroup = []
    sessionOwners = []
    with open(fileName, encoding='utf-8') as f:
        columnas = f.readline()
    if 'SessionOwner' in columnas:
        with open(fileName, newline='', encoding='utf-8') as nline:
            registers = csv.DictReader(nline)
            for register in registers:
                sessionOwners.append(register['SessionOwner'])
            loginGroup = list(set(sessionOwners))
            return loginGroup
        nline.close()
    else:
        return None
    f.close 






def collabStorage(fileName:str, ltiAccount:str):
    storage = 0.0
    with open(fileName, encoding='utf-8') as f:
        columnas = f.readline()
    if 'RecordingDuration' in columnas:
        with open(fileName, newline='', encoding='utf-8') as nline:
            registros = csv.DictReader(nline)
            for registro in registros:
                #minutes += collabTimeToMinutes(registro['StorageUsageGigabytes'])
                if registro['SessionOwner'] == ltiAccount:
                    storage += float(registro['StorageUsageGigabytes'])
            fstorage = round(storage)
            return '{:,}'.format(storage)
        nline.close()
    else:
        return None
    f.close 



def listRecordingids(filename):
    recids = []
    with open(filename,encoding='utf-8') as reader:
        for linea in reader:
            contenido = linea.rstrip()
            recids.append(str(contenido))
    reader.close()
    return recids


