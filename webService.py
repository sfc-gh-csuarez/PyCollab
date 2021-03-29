
import json
import Config
import sys
import datetime
import time 
import requests

from tqdm import tqdm 

from controladores import AuthControlador
from controladores import JotControlador
from controladores import SesionControlador
from controladores import MoodleControlador

class WebService():
    
    def __init__(self):
        self.KEY = Config.credenciales['learn_rest_key']
        self.SECRET = Config.credenciales['learn_rest_secret']
        self.DOMAIN = Config.credenciales['learn_rest_fqdn']
        self.KEY_C = Config.credenciales['collab_key']
        self.SECRET_C = Config.credenciales['collab_secret']
        self.DOMAIN_C = Config.credenciales['collab_base_url']
        if Config.credenciales["verify_certs"] == 'True':
            self.CERT = True
        else:
            self.CERT = False

        self.sesion = None
        self.jsesion = None

    def getToken(self):
         self.sesion = AuthControlador.AuthControlador(self.DOMAIN,self.KEY, self.SECRET)
         self.sesion.setToken()
         return(self.sesion.getToken())


    def getJot(self):
        self.jsesion = JotControlador.JotControlador(self.DOMAIN_C,self.KEY_C, self.SECRET_C,self.CERT)
        self.jsesion.setJot()
        return self.jsesion.getJot() 



    def getUser(self, userId):
        userURL =  '/learn/api/public/v1/users/userName:' + userId
        getURL = 'https://' + self.DOMAIN + userURL
        credencial = {'Authorization' : 'Bearer ' + self.getToken()}
        r = requests.get(getURL,headers=credencial)
        print(r)
        
    

    def getCourseInfo(self,courseId):
        url = 'https://' + self.DOMAIN+ '/learn/api/public/v1/courses/courseId:' + courseId 
        token = self.getToken()
        credencial = {
            'Authorization': 'Bearer ' + token
        }
        r = requests.get(url,headers=credencial)
        if r.status_code == 200:
            jsonInfo = json.loads(r.text)
            courseInfo = {'course_id': courseId, 'couse_name': jsonInfo['name'], 'course_uuid':jsonInfo['uuid'],'data_source':jsonInfo['dataSourceId']}
        else:
            courseInfo = {'course_id': courseId + ' not found', 'couse_name': 'Invalid', 'course_uuid':'Invalid','data_source':'Invalid'}
        return courseInfo





    def getUUID(self,course_id):
        courseURL = '/learn/api/public/v1/courses/courseId:' + course_id 
        getURL = 'https://' + self.DOMAIN + courseURL
        token = self.getToken()
        credencial = {'Authorization' : 'Bearer ' + token}
        r = requests.get(getURL,headers=credencial)
        if r.status_code == 200: 
            parsed_json = json.loads(r.text)
            return parsed_json['uuid']   
        elif r.status_code == 404:
            return course_id + " course not found"
        else:
            print("Error GetUUID", str(r))
            return "not found"

    
    def getGrabaciones(self,cursoUUID,tiempo):
        sesionCollab = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        grabaciones = sesionCollab.getGrabaciones(cursoUUID,tiempo)
        return(grabaciones)
    

    def get_recording_data(self,recording_id):
        sessions = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        recordingid = sessions.get_recording_data(recording_id)
        return recordingid


    def get_recording_data_4url(self,recording_id):
        sessions = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        recordingid = sessions.get_recording_data_4url(recording_id)
        return recordingid



    def getRecordingURL(self,recording_id):
        sessions = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        recording_url = sessions.getRecordingURL(recording_id)
        return recording_url



    def get_grabaciones_uuid(self,recording_id):
        sessionCollab = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        grabacion = sessionCollab.getGrabacionUUID(recording_id)
        return(grabacion)

    def get_grabacion_uuid_data(self,recording_id):
        sessions = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        recordingid = sessions.get_grabacion_UUID_data(recording_id)
        return recordingid

    def delete_recording(self,recording_id):
        sessions = SesionControlador.SesionControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        delete_info = sessions.delete_recording(recording_id)
        return delete_info



    def get_moodle_sesion_name(self,sesionId):
        moodle = MoodleControlador.MoodleControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        nombreMoodleSesion = moodle.moodleSesionName(sesionId)
        return nombreMoodleSesion

    def get_moodle_lista_sesiones(self,criteria):
        moodle = MoodleControlador.MoodleControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        listaCompleta = moodle.listaCompletaSessiones(criteria)
        return listaCompleta

    
    def get_moodle_lista_grabaciones(self,sname):
        moodle = MoodleControlador.MoodleControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        listaGrabacionesMoodle = moodle.listaMoodleGrabaciones(sname)
        return listaGrabacionesMoodle

    def get_moodle_lista_completa_grbaciones(self):
        moodle = MoodleControlador.MoodleControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        listaCompleta = moodle.listaCompletaMoodleGrabaciones()
        return listaCompleta

    def get_moodle_grabaciones_contexto(self,contexto_id,tiempo):
        moodle = MoodleControlador.MoodleControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        listaCompleta = moodle.getGrabacionesMoodleContextoLTI(contexto_id,tiempo)
        return listaCompleta
    
    def get_moodle_grabaciones_id(self,context_id):
        moodle = MoodleControlador.MoodleControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        listaCompleta = moodle.grabacionesMoodleLTI(context_id)
        return listaCompleta

    def get_moodle_grabacion_data(self,recording_id):
        moodle = MoodleControlador.MoodleControlador(self.DOMAIN_C,self.getJot(),self.CERT)
        jsonInfo = moodle.get_moodleLTI_recording_data(recording_id)
        return jsonInfo

        

        






    
    

