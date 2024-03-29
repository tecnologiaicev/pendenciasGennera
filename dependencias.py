import json, requests
from textwrap import indent
from sys import prefix
import datetime as dt
from datetime import datetime
from dateutil import parser, tz
from flask import Flask, redirect, jsonify, render_template, request
import json
from datetime import datetime, timedelta

app = Flask(__name__)

calendarios = [2528, 2965, 3315, 3224, 3629, 4400, 4283, 5041, 5190, 6460, 5992, 7073, 7394]

headers = {
    "x-access-token" : "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJuYW1lIjoiVGVjbm9sb2dpYSBpQ0VWIiwidXNlcm5hbWUiOiJ0ZWNub2xvZ2lhQHNvbW9zaWNldi5jb20iLCJoYXNoIjoiUGpMcFZJUlM5a0hkbGROWG1pS3Zqb1kzbDhHc3VQcU5zWHNKV0l2WiIsImlkVXNlciI6MTY2ODg5OSwiaWRDb3VudHJ5IjozMiwiaWRMYW5ndWFnZSI6MiwibGFuZ3VhZ2VDb2RlIjoicHQiLCJpZFRpbWV6b25lIjoxMTMsImlhdCI6MTYyNTYwOTI3OCwiaXNzIjoiaHR0cDovL2FwcHMuZ2VubmVyYS5jb20uYnIiLCJzdWIiOiJ0ZWNub2xvZ2lhQHNvbW9zaWNldi5jb20ifQ.jm_uCOeY_bNAv3rK0nIce-O3HmaLOap4kYgBMszz1EvVSxn558WR-_6xQG39O8TxT3pcTSZA89eAbtNTl3CF17Y1d0LNcJf3c6OJjQlt2hRR9Y0vLSfbPEm9KOxM-Opf58zQh2Y94zR42DopEsX_M1fmsVGC6yJCBz2jRq3zd3A6PSAiqnLOAKKVFEIXH2HoyGLCW9unvr0hWBcdA5Y0tVS6ZiKXwUQ_SQxuB5FPStskXnegV1VPWusPpMk9rJjpwg-ClLVsmAwHHRmeNxU2AncoWLmhkXh0MO3786tS1OlA3YuxVNzO20kIDOFGfPZt_NzEtOOHEF7CzIKFzrtOm5yW0jWCGt9duS3leY7OWpP56ogDgrDZSd0Pql6eUXrXZPryUHR4vMVDXEZsLzXinjm8lH6Kvy72LgJw3HlP0OCQi4WkkCgN-uDOcwyn8RJLv5nYSo0oqO2HAs6Aq3JUigg4QVMMX76j7NnDWBsyxYZ2mHwJnh0ylrXXkVL0zk9Dw3HewRJq4t3xehZr2eP-XnCp6TXbskLSB3wZAO1VnU_dZDYVKWuh_KZWcmZI8_quEV5SLCQ0A6LU_zbS5qmoa6sYxy6r1BC-ZJFeHiRVEMICbBL-dXQhZ4rH4f1DGhDoYDPAB7myT_D_Ylg-Wce1JltCZL1fk_gsOxveZNhZKOU"
}

DEBUG = True

class RegistrosAcademicos():
    def get(self):
        url_registros = f"https://api2.gennera.com.br/institutions/64/enrollmentRecords"
        try:
            lst_registros = json.loads(json.dumps(requests.get(url_registros, headers=headers).json()))
        except Exception as e:
            return e
        for ra in lst_registros:
            url_disc = f"https://api2.gennera.com.br/institutions/64/enrollmentRecords/{ra['idEnrollmentRecord']}/subjects"
            try:
                lst_disc = json.loads(json.dumps(requests.get(url_disc, headers=headers).json()))
            except Exception as e:
                lst_disc = []
            ra['disciplinas'] = lst_disc
        return lst_registros
    
    def getByCourse(self, course_name):
        url_registros = f"https://api2.gennera.com.br/institutions/64/enrollmentRecords"
        try:
            lst_registros = json.loads(json.dumps(requests.get(url_registros, headers=headers).json()))
        except Exception as e:
            return e
        return [c for c in lst_registros if c['courseName']==course_name]
    
    def getByPerson(self, person_id):
        url_registros = f"https://api2.gennera.com.br/institutions/64/persons/{person_id}/enrollmentRecords"
        try:
            lst_registros = json.loads(json.dumps(requests.get(url_registros, headers=headers).json()))
        except Exception as e:
            return e
        for ra in lst_registros:
            print(indent('Varrendo registros acadêmicos recuperados ...', prefix = '    ', predicate=None))
            url_disc = f"https://api2.gennera.com.br/institutions/64/enrollmentRecords/{ra['idEnrollmentRecord']}/subjects"
            try:
                lst_disc = json.loads(json.dumps(requests.get(url_disc, headers=headers).json()))
            except Exception as e:
                lst_disc = []
            ra['disciplinas'] = lst_disc
        
        return lst_registros
    


class Matriculas():
    def getDisciplinas(self, enrollment_id):
        url_disciplinas = f"https://api2.gennera.com.br/institutions/64/enrollments/{enrollment_id}/subjects"
        try:
            disciplinas = json.loads(json.dumps(requests.get(url_disciplinas, headers=headers).json()))
        except Exception as e:
            return e
        return disciplinas
    
    def get(self, enrollment_id):
        url_matricula = f"https://api2.gennera.com.br/institutions/64/enrollments/{enrollment_id}"
        try:
            matricula = json.loads(json.dumps(requests.get(url_matricula, headers=headers).json()))
        except Exception as e:
            return e
        return matricula
    
    def getByPerson(self, person_id):
        url_matriculas = f"https://api2.gennera.com.br/institutions/64/persons/{person_id}/enrollments"
        try:
            lst_matriculas = json.loads(json.dumps(requests.get(url_matriculas, headers=headers).json()))
        except Exception as e:
            return e
        for mat in lst_matriculas:
            mat['disciplinas'] = []
            url_disc = f"https://api2.gennera.com.br/institutions/64/enrollments/{mat['idEnrollment']}/subjects"
            try:
                lst_disc = json.loads(json.dumps(requests.get(url_disc, headers=headers).json()))
            except Exception as e:
                lst_disc = []
            mat['disciplinas'] = lst_disc
        return lst_matriculas
    
    def filterByCourse(self, matriculas, curso_nome):
        nova_lista = []
        for m in matriculas[0]:
            if 'courseName' in m and m['courseName'] == curso_nome:
                nova_lista.append(m)
        return nova_lista


class CurriculoByName():
    def get(self, course_id, curriculo_name):
        curric = Curriculo()
        lst_curriculos = curric.get(course_id)
        for c in lst_curriculos:
            if c['name'] == curriculo_name:
                return c
        return None

class Curso():
    def get(self, curso_id='', course_type = None):
        url_cursos = f"https://api2.gennera.com.br/institutions/64/courses/{curso_id}"
        try:
            lst_cursos = json.loads(json.dumps(requests.get(url_cursos, headers=headers).json()))
        except Exception as e:
            return e
        
        if course_type == None:
            return lst_cursos        
        else:
            lst_cursos_tipo = [c for c in lst_cursos if c['courseTypeName'] == course_type]
            return lst_cursos_tipo
    
    def getCursoByName(self, curso_name):
        lst_cursos = Curso().get()
        for c in lst_cursos:
            if c['name'] == curso_name:
                return c
        return None
    
    def getGraduacaoCurriculos(self):
        cursos = Curso().get('','Graduação')
        matrizes = {}
        for c in cursos:
            print(f"Currículos do curso {c['name']}")
            id_course = c['idCourse']
            courseName = c['name']
            # ras = RegistrosAcademicos().getByCourse(courseName)
            matrizes[id_course] = {'id_course': id_course, 'name': courseName, 'curriculos': Curriculo().get(id_course)}
        return matrizes
        

class Modulo():
    def get(self, curso_id, curriculo_id, modulo_id = ''):
        if modulo_id != '':
            url_modulos = f"https://api2.gennera.com.br/institutions/64/courses/{curso_id}/curriculums/{curriculo_id}/modules/{modulo_id}"
        else:
            url_modulos = f"https://api2.gennera.com.br/institutions/64/courses/{curso_id}/curriculums/{curriculo_id}/modules"

        try:
            lst_modulos = json.loads(json.dumps(requests.get(url_modulos, headers=headers).json()))
        except Exception as e:
            return e
        return lst_modulos

class Curriculo():
    def get(self, curso_id, curriculo_id=''):
        url_curriculos = f"https://api2.gennera.com.br/institutions/64/courses/{curso_id}/curriculums/{curriculo_id}"
        try:
            lst_curriculos = json.loads(json.dumps(requests.get(url_curriculos, headers=headers).json()))
        except Exception as e:
            return e
        if curriculo_id == '':
            for m in lst_curriculos:
                lst_periodos = Modulo().get(curso_id, m['idCurriculum'])
                lst_periodos = sorted(lst_periodos, key=lambda x: x['index'])
                m['modules'] = []
                for p in lst_periodos:
                    d = Disciplinas()
                    disc = d.get(curso_id,m['idCurriculum'],p['idModule'])
                    p['disciplinas'] = disc
                    m['modules'].append(p)
        else:
            lst_periodos = Modulo().get(curso_id, lst_curriculos['idCurriculum'])
            lst_periodos = sorted(lst_periodos, key=lambda x: x['index'])
            lst_curriculos['modules'] = []
            for p in lst_periodos:
                d = Disciplinas()
                disc = d.get(curso_id,lst_curriculos['idCurriculum'],p['idModule'])
                p['disciplinas'] = disc
                lst_curriculos['modules'].append(p)
            
        return lst_curriculos        

class Disciplinas():
    def get(self, curso_id, curriculo_id, modulo_id):
        url_disciplinas = f"https://api2.gennera.com.br/institutions/64/courses/{curso_id}/curriculums/{curriculo_id}/modules/{modulo_id}/subjects"
        try:
            lst_disciplinas = json.loads(json.dumps(requests.get(url_disciplinas, headers=headers).json()))
        except Exception as e:
            return e
        return lst_disciplinas

class Campanhas():
    def get(self, id_calendar):
        url_campanhas = f"https://api2.gennera.com.br/institutions/64/academicCalendars/{id_calendar}/campaigns"
        try:
            lst_campanhas = json.loads(json.dumps(requests.get(url_campanhas, headers=headers).json()))
        except Exception as e:
            return e
        return lst_campanhas
    
    def getCampanhaMatriculas(self, id_calendar):
        lst_campanhas = Campanhas().get(id_calendar)
        matriculas = []
        for c in lst_campanhas:
            url_matriculas = f"https://api2.gennera.com.br/institutions/64/campaigns/{c['idCampaign']}/enrollments"
            try:
                lst_matriculas = json.loads(json.dumps(requests.get(url_matriculas, headers=headers).json()))
            except Exception as e:
                return e
            # print(indent('Adicionando disciplinas das matrículas',prefix='  ', predicate=None))
            i = 1
            for m in lst_matriculas:
                if DEBUG:
                    if i > 20:
                        break
                # if m['courseName'] == '02 - Bacharelado em Administração':
                print(indent(f"Matrícula {i} de {len(lst_matriculas)}                   ",prefix='    ', predicate=None), end = '\r')
                if m['status'] == 'active':
                    if 'idEnrollment' in m:
                        m['disciplinas'] = Matriculas().getDisciplinas(m['idEnrollment'])
                        # j = 1
                        l_disc = []

                        for d in m['disciplinas']:
                            if d['status'] == 'active':
                                l_disc.append(d)
                            if ('complementName' in d) or ('equivalence' in d):
                                print('a') 
                        # print(indent(f"Registro {j} de {len(m['disciplinas'])}    ",prefix='      ', predicate=None), end='\r')
                        # j += 1
                        m['disciplinas'] = l_disc
                        matriculas = matriculas + [m]
                    else:
                        print(m)
                i += 1
                    
        
        return matriculas
    
    def filterByCourse(self, campanhas, curso_nome):
        nova_lista = [c for c in campanhas if 'courseName' in c and c['courseName'] == curso_nome]
        return nova_lista



class Alunos():
    def get(self):
        url_pessoas = f"https://api2.gennera.com.br/institutions/64/persons/"
        try:
            lst_pessoas = json.loads(json.dumps(requests.get(url_pessoas, headers=headers).json()))
        except Exception as e:
            return e
        lst_alunos = []
        for p in lst_pessoas:
            if len(p['profiles']) > 0:
                for prof in p['profiles']:
                    if prof['profile'] == 'Student':
                        lst_alunos.append(p)
                        break    
        return lst_alunos
    def getByCursos(self, curso_id):
        url_pessoas = f"https://api2.gennera.com.br/institutions/64/persons/"
        try:
            lst_pessoas = json.loads(json.dumps(requests.get(url_pessoas, headers=headers).json()))
        except Exception as e:
            return e
        lst_alunos = []
        for p in lst_pessoas:            
            if p['active'] == True:
                matriculas = Matriculas().getByPerson(p['idPerson'])
                if len(matriculas) > 0 and matriculas[0]['courseName'] == Curso().get(curso_id)['name']:
                    if len(p['profiles']) > 0:
                        for prof in p['profiles']:
                            if prof['profile'] == 'Student':
                                lst_alunos.append(p)
                                break    
    def filterByCourse(self, alunos, curso_id):
        nova_lista = [a for a in alunos if 'curso_id' in a and a['curso_id'] == curso_id]
        return nova_lista
    
    def buildDependencias(self, alunos, matrizes):
        # Initialize an empty dictionary to store the result
        result_json = {}
        i = 0
        # Iterate through each student in the 'alunos' JSON
        for student_id, student_info in alunos.items():
            i += 1
            print(f"Construindo dependências. Registro {i} de {len(alunos)}...            ", end='\r')
            # Initialize a dictionary for the current student
            student_data = {
                "idPerson": student_info["idPerson"],
                "name": student_info["name"],
                "course": student_info["nomeCurso"],
                "matriz":Curriculo().get(student_info['idCourse'], student_info['idCurriculumAtual']),
                "completed_subjects": [],
                "failed_subjects": [],
                "remaining_subjects": []
            }
            
            # Get the enrollment records for the current student
            enrollment_records = student_info.get("registros", [])
            
            # Monta a lista de disciplinas integralizadas
            for enrollment_record in enrollment_records:
                if 'disciplinas' in enrollment_record:
                    disciplinas = enrollment_record['disciplinas']
                    # Check if the enrollment status is "APPROVED"
                    for disciplina in disciplinas:    
                        if disciplina['status'] == "APPROVED":
                            # Add the subject to the list of completed subjects
                            completed_subject = {
                                "subjectName": disciplina["subjectName"],
                                "workload": disciplina["workload"],
                                "average": disciplina["average"]
                            }
                            student_data["completed_subjects"].append(completed_subject)
            
            # Monta a lista de disciplinas reprovadas e não cursadas
            for enrollment_record in enrollment_records:
                if 'disciplinas' in enrollment_record:
                    disciplinas = enrollment_record['disciplinas']
                    # Check if the enrollment status is "APPROVED"
                    for disciplina in disciplinas:    
                        if (disciplina['status'] == "FAILED") and \
                            disciplina['subjectName'] not in ([sub["subjectName"] for sub in student_data["completed_subjects"]]):
                            # Add the subject to the list of completed subjects
                                failed_subject = {
                                "subjectName": disciplina["subjectName"],
                                "workload": disciplina["workload"],
                                "average": disciplina["average"]
                            }
                                student_data["failed_subjects"].append(failed_subject)
            
            # Ajustar pegando o resultado da disciplina no diário
            enrollment_records = student_info.get("matriculas", [])
            
            for enrollment_record in enrollment_records:
                if 'disciplinas' in enrollment_record:
                    disciplinas = enrollment_record['disciplinas']
                    # Check if the enrollment status is "APPROVED"
                    for disciplina in disciplinas:    
                        if disciplina["status"] == "APPROVED":
                            # Add the subject to the list of completed subjects
                            completed_subject = {
                                "subjectName": disciplina["subjectName"],
                                "workload": disciplina["workload"],
                                "average": disciplina["average"]
                            }
                            student_data["completed_subjects"].append(completed_subject)
            
            for enrollment_record in enrollment_records:
                if 'disciplinas' in enrollment_record:
                    disciplinas = enrollment_record['disciplinas']
                    # Check if the enrollment status is "APPROVED"
                    for disciplina in disciplinas:    
                            if (disciplina['status'] == "FAILED") and \
                                    disciplina['subjectName'] not in ([sub["subjectName"] for sub in student_data["completed_subjects"]]):
                                failed_subject = {
                                "subjectName": disciplina["subjectName"],
                                "workload": disciplina["workload"],
                                "average": disciplina["average"]
                            }
                                student_data["failed_subjects"].append(failed_subject)                                
            # Get the curriculum for the current student's course
            student_info["idCourse"] = Curso().getCursoByName(student_info['nomeCurso'])['idCourse']
            curricula = matrizes.get(student_info["idCourse"], {}).get("curriculos", [])
            # verificar se existem 2 matrizes aqui e checar o preenchimento do idCurriculum anteriormente.
            curriculum = [c for c in curricula if c['idCurriculum'] == student_info['idCurriculumAtual']] 
            # curriculum = matrizes.get(student_info["nomeCurso"], {}).get("curriculos", [])
            
            # Iterate through each curriculum
            for curr in curriculum:
                # Iterate through each module in the curriculum
                for module in curr.get("modules", []):
                    # Iterate through each subject in the module
                    periodo = module['index'] + 1
                    if periodo <= student_info['periodo_esperado']:
                        for subject in module.get("disciplinas", []):
                            # Check if the subject is not completed
                            if (subject["name"] not in [sub["subjectName"] for sub in student_data["completed_subjects"]]) and \
                                    (subject["name"] not in [sub["subjectName"] for sub in student_data["failed_subjects"]]):
                                # Add the subject to the list of remaining subjects
                                remaining_subject = {
                                    "subjectName": subject["name"],
                                    "workload": subject["workload"]
                                }
                                student_data["remaining_subjects"].append(remaining_subject)
            student_data['remaining_subjects'] += student_data['failed_subjects']    
            # Add the student's data to the result JSON
            result_json[student_id] = student_data

        # Print the result JSON
        return result_json


def testeTOTVS():
    
    
    auth = ("ricardo.sekeff","Jfsb@102628")
    
    headers = {
        "Content-Type": "application/json"
    }
    
    url_registros = f"https://grupoeducacional127611.rm.cloudtotvs.com.br:8051/api/framework/v1/consultaSQLServer/RealizaConsulta/API.EDU.001/0/S/?parameters=CODCOLIGADA=4;ANO_LETIVO=2024.1;FILTRO=%"
    lst_registros = json.loads(json.dumps(requests.get(url_registros, headers=headers, auth=auth).json()))
    for r in lst_registros:
        print(f"{r['RA']} - {r['NOMEALUNO']}")
    return lst_registros
    

def testeTovs2():
    body = {'username':'00287283356',
'password':'123456',
'rememberUser':'false'}
    url = "https://grupoeducacional127611.rm.cloudtotvs.com.br/FrameHTML/web/app/Edu/PortalDoProfessor/aliasname.corporerm/api/connect/token"    
    try:
        token = json.loads(json.dumps(requests.post(url, data=body).json()))
    except Exception as e:
        print(e)
        return e
    return token
    
# @app.route('/')
# def get_token():
#     # Obtenha os dados do token
#     token_data =testeTovs2()

#     # Criar a estrutura desejada
#     token_info = {
#         'alias': 'Y29ycG9yZXJt',
#         'breadcrumbs': '',
#         'datelogin': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#         'expires_at': (datetime.now() + timedelta(seconds=token_data['expires_in'])).strftime("%Y-%m-%d %H:%M:%S"),
#         'expires_in': token_data['expires_in'],
#         'PO_DEFAULT_LANGUAGE': 'pt-BR',
#         'refresh_token': token_data['refresh_token'],
#         'user_access_token': token_data['access_token']
#     }

#     # Armazenar os dados no armazenamento local do navegador
#     session_data = json.dumps(token_info)
    
#     return render_template('index.html', token_info = token_info)
#     js_code = f'''
#         localStorage.setItem("x", {session_data});

#         var cookieValue = "odlzmadzhkh5cjd3fhx1cfo1";
#         var expirationDate = new Date();
#         expirationDate.setMinutes(expirationDate.getMinutes() + 30);  // Defina o tempo de expiração do cookie aqui
#         var cookieString = "ASP.Net_SessionId=" + cookieValue;
#         cookieString += "; Domain=grupoeducacional127611.rm.cloudtotvs.com.br";
#         cookieString += "; Expires=" + expirationDate.toUTCString();
#         cookieString += "; SameSite=Lax";
#         cookieString += "; HttpOnly";
#         cookieString += "; Secure";
#         document.cookie = cookieString;

#         window.location.replace("https://grupoeducacional127611.rm.cloudtotvs.com.br/FrameHTML/Web/App/Edu/PortalDoProfessor/#/portal/home");
#     '''
#     return f'<script>{js_code}</script>'
#     return f'<script>localStorage.setItem("token_info", {session_data}); window.location.replace("https://grupoeducacional127611.rm.cloudtotvs.com.br/FrameHTML/Web/App/Edu/PortalDoProfessor/#/portal/home");</script>'

    

def normalizarMatriculas(matriculas):
    alunos = {}
    i = 0
    total = len(matriculas)
    for m in matriculas:
        print(indent('Varrendo matrículas recuperadas...', prefix = '   ', predicate=None))
        if 'idEnrollment' in m:
#            if m['idPerson'] == 145768: 
            mc = Matriculas().get(m['idEnrollment'])
            if m['idPerson'] in alunos:
                alunos[m['idPerson']]['matriculas'].append(m)
                if m['courseName'] != alunos[m['idPerson']]['nomeCurso']:
                    ndia = [c['date'] for c in mc['statuses'] if c['status'] == 'active']
                    if len(ndia) > 0:
                        if ndia[0] > alunos[m['idPerson']]['dtmat']:
                            alunos[m['idPerson']]['dtmat'] = ndia[0]
                            alunos[m['idPerson']]['idCourse'] = Curso().getCursoByName(m['courseName'])['idCourse']
                            alunos[m['idPerson']]['nomeCurso'] = m['courseName']
                            alunos[m['idPerson']]['idCurriculumAtual'] = m['idCurriculum']
                            alunos[m['idPerson']]['curriculos'].append(m['idCurriculum'])
            else:
                dia = [c['date'] for c in mc['statuses'] if c['status'] == 'active']
                periodo_esperado = (24 - int(m['code'][0:2])) * 2
                alunos[m['idPerson']] = {'idPerson':m['idPerson'] ,'ra': m['code'], 'periodo_esperado':periodo_esperado, 'name': m['personName'],'idCourse': Curso().getCursoByName(m['courseName'])['idCourse'],'nomeCurso':m['courseName'], 'idCurriculumAtual': m['idCurriculum'], 'curriculos': [m['idCurriculum']], 'dtmat': dia[0] if len(dia) > 0 else ''}
                alunos[m['idPerson']]['matriculas'] = [m]
                
            i += 1
            print(indent(f"Matrícula {i} de {total}", prefix = '       ', predicate=None))
            if DEBUG:
                if i > 20:
                    break
        else:
            print(m)
    return alunos

# testeTovs2()
if DEBUG:
    calendarios = [2528, 2965, 3315, 5190]
    print('====== MODO DEBUG =====')
print('Recuperando matrículas das Campanhas...')
#calendarios = [1244,1498,3795,1847,1876,2248,2528,2965,3224,3629]
matriculas = []
i = 0
for c in calendarios:
    i += 1
    print(f"\nCalendário {i} de {len(calendarios)}                      ")
    matriculas = matriculas + Campanhas().getCampanhaMatriculas(c)
print('Recuperando matrizes dos cursos...')
matrizes = Curso().getGraduacaoCurriculos()

print('Vinculando matrículas aos alunos...')
alunos = normalizarMatriculas(matriculas)
# alunos = Alunos().get()
print('Recuperando registros acadêmicos dos alunos...')
i=1
tam = len(alunos)
# continua daqui
for aluno in alunos:
    alunos[aluno]['registros'] = RegistrosAcademicos().getByPerson(alunos[aluno]['idPerson'])
    print(f"{i} de {tam}" )
    i = i+1
    if DEBUG:
        if i>20:
            break

print('Construíndo a tabela de dependências finais...')    
alunos = Alunos().buildDependencias(alunos, matrizes)
print('Salvando resultado...')
file_path = "novoalunos.json"

# Open the file in write mode and write the JSON data
with open(file_path, "w") as json_file:
    json.dump(alunos, json_file, indent=4)

print("JSON data saved to:", file_path)

# if __name__ == '__main__':
#     app.run(debug=True)
