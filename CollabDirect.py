import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.main(sys.argv[1:])
    webService = WebService()
    report = []
    report_403 = []
    course_uuids = []
    if param[2]== 0:
        tiempo = ut.semanasAtiempo(12)
    else:
        tiempo = ut.semanasAtiempo(param[2])
    if  param[0] != '' and param[1] == '':
        print("Course Recordings from " + tiempo)
        cursos_id = ut.leerCursos(param[0])
        for curso in cursos_id:
            course_uuids.append([{'uuid':webService.getUUID(curso), 'cursoid':curso}])
        
        for elemento in course_uuids:
            cuuid = elemento[0]['uuid']
            cursoid = elemento[0]['cursoid']
            grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
            grabaciones = ut.listaGrabacionesOnlyData(grabacionesJson)
            if grabaciones is None:
                print("There's no recording for course: " + cuuid)
            else:
                for grabacion in grabaciones:
                        recording_url = ut.downloadFromURL(grabacion['recording_id'])
                        ut.downloadOneRecordingURL(grabacion,recording_url,cuuid)
                        report.append([cursoid,grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])     
        if len(report) > 0: 
            print(ut.crearReporteCollabDownload(report))
        else:
            print('No downloading was executed')
        if len(report_403) > 0:
            print(ut.crearReporte_403(report_403))
        else:
            print('No private recording was found')
        
    elif param[0] == '' and param[1] != '':
        print("Course Recordings from " + tiempo)
        course_uuids = ut.leerUUID(param[1])
        for cuuid in course_uuids:
            grabacionesJson = webService.getGrabaciones(cuuid,tiempo)
            grabaciones = ut.listaGrabaciones(grabacionesJson)
            if grabaciones is None:
                print("There's no recording: " + cuuid)
            else:
                for grabacion in grabaciones:
                    if 'msg' not in grabacion:
                        recording_url = ut.downloadFromURL(grabacion['recording_id'])
                        ut.downloadOneRecordingURL(grabacion,recording_url,cuuid)
                        report.append([cursoid,grabacion['recording_id'], grabacion['recording_name'],grabacion['duration'],grabacion['storageSize'],grabacion['created']])                     
        if len(report) > 0: 
            print(ut.crearReporteCollabDownload(report))
        else:
            print('No downloading was executed')
        if len(report_403) > 0:
            print(ut.crearReporte_403(report_403))
        else:
            print('No private recording was found')
        
