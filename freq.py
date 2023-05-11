from flask import Blueprint, request, jsonify
import requests
from datetime import datetime
import pandas as pd
import os

freq = Blueprint('freq', __name__)

API_ROUTE = "http://45.56.120.227/api/v1/json"

def get_students_json(api_route):
    headers = {'Accept': 'application/json'}
    request_json = requests.get(api_route, headers=headers)
    return request_json.json()

def get_today_info():
    today = datetime.now().strftime("%A")
    time = datetime.now().strftime("%H:%M")
    date = datetime.now().strftime("%d/%m/%Y")
    return today, time, date

PATH_DATA = './data/today.csv'

@freq.route('/frequencia', methods=['GET'])
def get_data():
    rfid_hash = request.args.get('cardData')

    translated_hash = bytes.fromhex(rfid_hash).decode('utf-8')
    students = get_students_json(API_ROUTE)
    student = students.get(translated_hash)
    if student != None:
        df_today = pd.read_csv(PATH_DATA, sep=';')

        key_mat = list(student.keys())[0]
        student_id_person = student[key_mat]['idPerson']
        student_name = student[key_mat]['nome']
        student_name = student_name.split(' ')
        student_name = student_name[0] + ' ' + student_name[-1]
        today, time, date = get_today_info()
        for studant_class in student[key_mat]['horarios'].get(today):
            class_id = studant_class['idClass']
            class_name = studant_class['subjectName']
            start = studant_class['hourStart']
            end = studant_class['hourEnd']
            if start <= time and end >= time:
                if df_today[(df_today['idPerson'] == student_id_person) & (df_today['idClass'] == class_id)].empty:
                    print(4)
                    status = 0
                    df_today = df_today._append({'date':date, 'weekday':today, 'idPerson':student_id_person, 'idClass':class_id,'start':start, 'end':end, 'startTime':time, 'status':status}, ignore_index=True)
                    break
                else:
                    print(5)
                    df_today.loc[df_today['idPerson'] == student_id_person, 'endTime'] = time
                    break
        class_name = class_name if class_name != None else 'disciplina nao identificada'
        print(df_today)
        df_today.to_csv(PATH_DATA, sep=';', index=False)
        return jsonify([1, class_name, student_name, translated_hash])
    class_name = class_name if class_name != None else 'disciplina nao identificada'
    student_name = student_name if student_name != None else 'aluno nao identificado'
    return jsonify([0, class_name, student_name, translated_hash])

