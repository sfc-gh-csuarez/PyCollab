import datetime
from webService import WebService
import Utilidades as ut
import sys


if __name__ == "__main__":
    param = ut.mainDelete(sys.argv[1:])
    webService = WebService()
    report = []
    if  param[0] != '':
        recodingsids = ut.listRecordingids(param[0])
        for recording in recodingsids:
            resp = ut.deleteRecording(recording)
            if resp == True:
                print(recording + ': Recording was deleted!')
                report.append([recording, 'deleted'])
            elif resp == '404':
                print(recording + ': Resource not found, Already deleted')
                report.append([recording, 'Resource not found, Already deleted'])
            
        if len(report) > 0: 
            print(ut.crearReporteDelete(report))
        else:
            print('No deletions was executed')
    else:
        print("Error, missing argument (list of recordings id file)")