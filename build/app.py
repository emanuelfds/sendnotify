# #--- v:1.0
# from flask import Flask, request, jsonify
# import requests
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Usuários e senhas de exemplo
# users = {
#     "admin": generate_password_hash("secret"),
#     "user": generate_password_hash("password")
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# @auth.error_handler
# def unauthorized():
#     # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
#     return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

# @app.route('/send_message', methods=['POST'])
# @auth.login_required
# def send_message():
#     message = request.json.get('message')  # Obtenha a mensagem do corpo da solicitação JSON
#     webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA5jfnDqU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MtkYzCpxmUHoQLMoy3Uu1F9c0P79P2QebGJxFcggKak'  # Substitua isso pelo seu URL do webhook

#     if message:
#         payload = {
#             "text": message
#         }

#         headers = {
#             "Content-Type": "application/json; charset=utf-8"
#         }

#         response = requests.post(webhook_url, json=payload, headers=headers)

#         if response.status_code == 200:
#             return "Mensagem enviada com sucesso para o Google Chat!"
#         else:
#             return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
#     else:
#         return jsonify({"error": "A mensagem está ausente no corpo da solicitação JSON"}), 400

# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')

#-- v:2.0 - mais log
# import logging
# from flask import Flask, request, jsonify
# import requests
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Usuários e senhas de exemplo
# users = {
#     "admin": generate_password_hash("secret"),
#     "user": generate_password_hash("password")
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# @auth.error_handler
# def unauthorized():
#     # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
#     return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

# @app.route('/send_message', methods=['POST'])
# @auth.login_required
# def send_message():
#     message = request.json.get('message')  # Obtenha a mensagem do corpo da solicitação JSON
#     webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA5jfnDqU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MtkYzCpxmUHoQLMoy3Uu1F9c0P79P2QebGJxFcggKak'  # Substitua isso pelo seu URL do webhook

#     if message:
#         payload = {
#             "text": message
#         }

#         headers = {
#             "Content-Type": "application/json; charset=utf-8"
#         }

#         response = requests.post(webhook_url, json=payload, headers=headers)

#         if response.status_code == 200:
#             app.logger.debug("Mensagem enviada com sucesso para o Google Chat!")
#             return "Mensagem enviada com sucesso para o Google Chat!"
#         else:
#             app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. Código de status: {response.status_code}")
#             return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
#     else:
#         app.logger.error("A mensagem está ausente no corpo da solicitação JSON")
#         return jsonify({"error": "A mensagem está ausente no corpo da solicitação JSON"}), 400

# if __name__ == '__main__':
#     # Configure o logger para exibir mensagens de debug
#     logging.basicConfig(level=logging.DEBUG)
#     app.run(debug=True, host='0.0.0.0')


# v:2.0.2 -> Funcionou a subscrição
# import logging
# from flask import Flask, request, jsonify
# import requests
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Usuários e senhas de exemplo
# users = {
#     "admin": generate_password_hash("secret"),
#     "user": generate_password_hash("password")
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# @auth.error_handler
# def unauthorized():
#     # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
#     return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

# @app.route('/subscription', methods=['POST'])
# @auth.login_required
# def subscription():
#     if not request.is_json:
#         app.logger.error("Recebido JSON inválido")
#         return jsonify({"error": "Invalid JSON"}), 400

#     data = request.get_json()

#     if 'ConfirmationURL' in data:
#         confirmation_url = data['ConfirmationURL']
#         app.logger.debug(f"ConfirmationURL recebido: {confirmation_url}")

#         try:
#             response = requests.get(confirmation_url)
#             response.raise_for_status()  # Verifique se a resposta foi bem-sucedida
#             return jsonify({"message": "Subscription confirmed"}), 200
#         except requests.RequestException as e:
#             app.logger.error(f"Erro ao confirmar a assinatura: {str(e)}")
#             return jsonify({"error": str(e)}), 500
#     elif 'message' in data:
#         message = data['message']
#         webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA5jfnDqU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MtkYzCpxmUHoQLMoy3Uu1F9c0P79P2QebGJxFcggKak'  # Substitua isso pelo seu URL do webhook

#         if message:
#             payload = {
#                 "text": message
#             }

#             headers = {
#                 "Content-Type": "application/json; charset=utf-8"
#             }

#             response = requests.post(webhook_url, json=payload, headers=headers)

#             if response.status_code == 200:
#                 app.logger.debug("Mensagem enviada com sucesso para o Google Chat!")
#                 return "Mensagem enviada com sucesso para o Google Chat!"
#             else:
#                 app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. Código de status: {response.status_code}")
#                 return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
#         else:
#             app.logger.error("A mensagem está ausente no corpo da solicitação JSON")
#             return jsonify({"error": "A mensagem está ausente no corpo da solicitação JSON"}), 400
#     else:
#         app.logger.error("Campos obrigatórios ausentes no corpo da solicitação JSON")
#         return jsonify({"error": "Campos obrigatórios ausentes no corpo da solicitação JSON"}), 400

# if __name__ == '__main__':
#     # Configure o logger para exibir mensagens de debug
#     logging.basicConfig(level=logging.DEBUG)
#     app.run(debug=True, host='0.0.0.0')

# v:2.0.6 -> Trocando o campo 'key'
# import logging
# from flask import Flask, request, jsonify
# import requests
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Usuários e senhas de exemplo
# users = {
#     "admin": generate_password_hash("secret"),
#     "user": generate_password_hash("password")
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# @auth.error_handler
# def unauthorized():
#     # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
#     return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

# @app.route('/subscription', methods=['POST'])
# @auth.login_required
# def subscription():
#     if not request.is_json:
#         app.logger.error("Recebido JSON inválido")
#         return jsonify({"error": "Invalid JSON"}), 400

#     data = request.get_json()

#     if 'ConfirmationURL' in data:
#         confirmation_url = data['ConfirmationURL']
#         app.logger.debug(f"ConfirmationURL recebido: {confirmation_url}")

#         try:
#             response = requests.get(confirmation_url)
#             response.raise_for_status()  # Verifique se a resposta foi bem-sucedida
#             return jsonify({"message": "Subscription confirmed"}), 200
#         except requests.RequestException as e:
#             app.logger.error(f"Erro ao confirmar a assinatura: {str(e)}")
#             return jsonify({"error": str(e)}), 500
#     elif 'title' in data:
#         title = data['title']
#         webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA5jfnDqU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MtkYzCpxmUHoQLMoy3Uu1F9c0P79P2QebGJxFcggKak'  # Substitua isso pelo seu URL do webhook

#         if title:
#             payload = {
#                 "text": title
#             }

#             headers = {
#                 "Content-Type": "application/json; charset=utf-8"
#             }

#             response = requests.post(webhook_url, json=payload, headers=headers)

#             if response.status_code == 200:
#                 app.logger.debug("Mensagem enviada com sucesso para o Google Chat!")
#                 return "Mensagem enviada com sucesso para o Google Chat!"
#             else:
#                 app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. Código de status: {response.status_code}")
#                 return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
#         else:
#             app.logger.error("O título está ausente no corpo da solicitação JSON")
#             return jsonify({"error": "O título está ausente no corpo da solicitação JSON"}), 400
#     else:
#         app.logger.error("Campos obrigatórios ausentes no corpo da solicitação JSON")
#         return jsonify({"error": "Campos obrigatórios ausentes no corpo da solicitação JSON"}), 400

# if __name__ == '__main__':
#     # Configure o logger para exibir mensagens de debug
#     logging.basicConfig(level=logging.DEBUG)
#     app.run(debug=True, host='0.0.0.0')

# v 2.0.7
# import logging
# from flask import Flask, request, jsonify
# import requests
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Usuários e senhas de exemplo
# users = {
#     "admin": generate_password_hash("secret"),
#     "user": generate_password_hash("password")
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# @auth.error_handler
# def unauthorized():
#     # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
#     return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

# @app.route('/subscription', methods=['POST'])
# @auth.login_required
# def subscription():
#     if not request.is_json:
#         app.logger.error("Recebido JSON inválido")
#         return jsonify({"error": "Invalid JSON"}), 400

#     data = request.get_json()

#     if 'ConfirmationURL' in data:
#         confirmation_url = data['ConfirmationURL']
#         app.logger.debug(f"ConfirmationURL recebido: {confirmation_url}")

#         try:
#             response = requests.get(confirmation_url)
#             response.raise_for_status()  # Verifique se a resposta foi bem-sucedida
#             return jsonify({"message": "Subscription confirmed"}), 200
#         except requests.RequestException as e:
#             app.logger.error(f"Erro ao confirmar a assinatura: {str(e)}")
#             return jsonify({"error": str(e)}), 500
#     elif 'title' in data:
#         title = data['title']
#         webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA5jfnDqU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MtkYzCpxmUHoQLMoy3Uu1F9c0P79P2QebGJxFcggKak'  # Substitua isso pelo seu URL do webhook

#         if title:
#             payload = {
#                 "text": title
#             }

#             headers = {
#                 "Content-Type": "application/json; charset=utf-8"
#             }

#             response = requests.post(webhook_url, json=payload, headers=headers)

#             if response.status_code == 200:
#                 app.logger.debug("Mensagem enviada com sucesso para o Google Chat!")
#                 return jsonify({"message": "Mensagem enviada com sucesso para o Google Chat!"}), 200
#             else:
#                 app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. Código de status: {response.status_code}")
#                 return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
#         else:
#             app.logger.error("O título está ausente no corpo da solicitação JSON")
#             return jsonify({"error": "O título está ausente no corpo da solicitação JSON"}), 400
#     else:
#         app.logger.error("Campos obrigatórios ausentes no corpo da solicitação JSON")
#         return jsonify({"error": "Campos obrigatórios ausentes no corpo da solicitação JSON"}), 400

# if __name__ == '__main__':
#     # Configure o logger para exibir mensagens de debug
#     logging.basicConfig(level=logging.DEBUG)
#     app.run(debug=True, host='0.0.0.0')

# v2.0.8
# import logging
# from flask import Flask, request, jsonify
# import requests
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Usuários e senhas de exemplo
# users = {
#     "admin": generate_password_hash("secret"),
#     "user": generate_password_hash("password")
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# @auth.error_handler
# def unauthorized():
#     # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
#     return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

# @app.route('/subscription', methods=['POST'])
# @auth.login_required
# def subscription():
#     if not request.is_json:
#         app.logger.error("Recebido JSON inválido")
#         return jsonify({"error": "Invalid JSON"}), 400

#     data = request.get_json()

#     if 'ConfirmationURL' in data:
#         confirmation_url = data['ConfirmationURL']
#         app.logger.debug(f"ConfirmationURL recebido: {confirmation_url}")

#         try:
#             response = requests.get(confirmation_url)
#             response.raise_for_status()  # Verifique se a resposta foi bem-sucedida
#             return jsonify({"message": "Subscription confirmed"}), 200
#         except requests.RequestException as e:
#             app.logger.error(f"Erro ao confirmar a assinatura: {str(e)}")
#             return jsonify({"error": str(e)}), 500
#     elif 'title' in data:
#         title = data['title']
#         body = data.get('body', '')
#         severity = data.get('severity', '')
#         alarm_metadata = data.get('alarmMetaData', [])
        
#         message = f"Title: {title}\nBody: {body}\nSeverity: {severity}"
        
#         if alarm_metadata:
#             alarm = alarm_metadata[0]
#             status = alarm.get('status', '')
#             namespace = alarm.get('namespace', '')
#             query = alarm.get('query', '')
#             alarm_summary = alarm.get('alarmSummary', '')
#             metric_values = alarm.get('metricValues', [])

#             message += f"\nStatus: {status}\nNamespace: {namespace}\nQuery: {query}\nSummary: {alarm_summary}"
#             if metric_values:
#                 message += f"\nMetric Values: {metric_values}"

#         webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA5jfnDqU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MtkYzCpxmUHoQLMoy3Uu1F9c0P79P2QebGJxFcggKak'  # Substitua isso pelo seu URL do webhook

#         payload = {
#             "text": message
#         }

#         headers = {
#             "Content-Type": "application/json; charset=utf-8"
#         }

#         response = requests.post(webhook_url, json=payload, headers=headers)

#         if response.status_code == 200:
#             app.logger.debug("Mensagem enviada com sucesso para o Google Chat!")
#             return jsonify({"message": "Mensagem enviada com sucesso para o Google Chat!"}), 200
#         else:
#             app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. Código de status: {response.status_code}")
#             return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
#     else:
#         app.logger.error("Campos obrigatórios ausentes no corpo da solicitação JSON")
#         return jsonify({"error": "Campos obrigatórios ausentes no corpo da solicitação JSON"}), 400

# if __name__ == '__main__':
#     # Configure o logger para exibir mensagens de debug
#     logging.basicConfig(level=logging.DEBUG)
#     app.run(debug=True, host='0.0.0.0')

# v 2.0.9 -- Deu certo \O/
import logging
from flask import Flask, request, jsonify
import requests
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

# Usuários e senhas de exemplo
users = {
    "admin": generate_password_hash("secret"),
    "user": generate_password_hash("password")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None

@auth.error_handler
def unauthorized():
    # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
    return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

@app.before_request
def log_request_info():
    app.logger.debug(f"Headers: {request.headers}")
    app.logger.debug(f"Body: {request.get_data()}")

@app.route('/subscription', methods=['POST'])
@auth.login_required
def subscription():
    if not request.is_json:
        app.logger.error("Recebido JSON inválido")
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()

    if 'ConfirmationURL' in data:
        confirmation_url = data['ConfirmationURL']
        app.logger.debug(f"ConfirmationURL recebido: {confirmation_url}")

        try:
            response = requests.get(confirmation_url)
            response.raise_for_status()  # Verifique se a resposta foi bem-sucedida
            return jsonify({"message": "Subscription confirmed"}), 200
        except requests.RequestException as e:
            app.logger.error(f"Erro ao confirmar a assinatura: {str(e)}")
            return jsonify({"error": str(e)}), 500
    elif 'title' in data:
        title = data['title']
        body = data.get('body', '')
        severity = data.get('severity', '')
        alarm_metadata = data.get('alarmMetaData', [])
        
        message = f"Title: {title}\nBody: {body}\nSeverity: {severity}"
        
        if alarm_metadata:
            alarm = alarm_metadata[0]
            status = alarm.get('status', '')
            namespace = alarm.get('namespace', '')
            query = alarm.get('query', '')
            alarm_summary = alarm.get('alarmSummary', '')
            metric_values = alarm.get('metricValues', [])

            message += f"\nStatus: {status}\nNamespace: {namespace}\nQuery: {query}\nSummary: {alarm_summary}"
            if metric_values:
                message += f"\nMetric Values: {metric_values}"

        webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAA5jfnDqU/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=MtkYzCpxmUHoQLMoy3Uu1F9c0P79P2QebGJxFcggKak'  # Substitua isso pelo seu URL do webhook

        payload = {
            "text": message
        }

        headers = {
            "Content-Type": "application/json; charset=utf-8"
        }

        response = requests.post(webhook_url, json=payload, headers=headers)

        if response.status_code == 200:
            app.logger.debug("Mensagem enviada com sucesso para o Google Chat!")
            return jsonify({"message": "Mensagem enviada com sucesso para o Google Chat!"}), 200
        else:
            app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. Código de status: {response.status_code}")
            return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
    else:
        app.logger.error("Campos obrigatórios ausentes no corpo da solicitação JSON")
        return jsonify({"error": "Campos obrigatórios ausentes no corpo da solicitação JSON"}), 400

if __name__ == '__main__':
    # Configure o logger para exibir mensagens de debug
    logging.basicConfig(level=logging.DEBUG)
    app.run(debug=True, host='0.0.0.0')


# v 2.0.10
# import logging
# import os
# from flask import Flask, request, jsonify
# import requests
# from flask_httpauth import HTTPBasicAuth
# from werkzeug.security import generate_password_hash, check_password_hash

# app = Flask(__name__)
# auth = HTTPBasicAuth()

# # Usuários e senhas de exemplo
# users = {
#     "admin": generate_password_hash("secret"),
#     "user": generate_password_hash("password")
# }

# @auth.verify_password
# def verify_password(username, password):
#     if username in users and check_password_hash(users.get(username), password):
#         return username
#     return None

# @auth.error_handler
# def unauthorized():
#     # Retorna uma resposta 401 Unauthorized com o cabeçalho WWW-Authenticate
#     return jsonify({"error": "Unauthorized access"}), 401, {'WWW-Authenticate': 'Basic realm="Login Required"'}

# @app.before_request
# def log_request_info():
#     app.logger.debug(f"Headers: {request.headers}")
#     app.logger.debug(f"Body: {request.get_data()}")

# @app.route('/subscription', methods=['POST'])
# @auth.login_required
# def subscription():
#     if not request.is_json:
#         app.logger.error("Recebido JSON inválido")
#         return jsonify({"error": "Invalid JSON"}), 400

#     data = request.get_json()

#     if 'ConfirmationURL' in data:
#         confirmation_url = data['ConfirmationURL']
#         app.logger.debug(f"ConfirmationURL recebido: {confirmation_url}")

#         try:
#             response = requests.get(confirmation_url)
#             response.raise_for_status()  # Verifique se a resposta foi bem-sucedida
#             return jsonify({"message": "Subscription confirmed"}), 200
#         except requests.RequestException as e:
#             app.logger.error(f"Erro ao confirmar a assinatura: {str(e)}")
#             return jsonify({"error": str(e)}), 500
#     elif 'title' in data:
#         title = data['title']
#         body = data.get('body', '')
#         severity = data.get('severity', '')
#         alarm_metadata = data.get('alarmMetaData', [])
        
#         message = f"Title: {title}\nBody: {body}\nSeverity: {severity}"
        
#         if alarm_metadata:
#             alarm = alarm_metadata[0]
#             status = alarm.get('status', '')
#             namespace = alarm.get('namespace', '')
#             query = alarm.get('query', '')
#             alarm_summary = alarm.get('alarmSummary', '')
#             metric_values = alarm.get('metricValues', [])

#             message += f"\nStatus: {status}\nNamespace: {namespace}\nQuery: {query}\nSummary: {alarm_summary}"
#             if metric_values:
#                 message += f"\nMetric Values: {metric_values}"

#         webhook_url =  str(os.environ.get('WEBHOOK'))

#         payload = {
#             "text": message
#         }

#         headers = {
#             "Content-Type": "application/json; charset=utf-8"
#         }

#         response = requests.post(webhook_url, json=payload, headers=headers)

#         if response.status_code == 200:
#             app.logger.debug("Mensagem enviada com sucesso para o Google Chat!")
#             return jsonify({"message": "Mensagem enviada com sucesso para o Google Chat!"}), 200
#         else:
#             app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. Código de status: {response.status_code}")
#             return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": response.status_code}), 500
#     else:
#         app.logger.error("Campos obrigatórios ausentes no corpo da solicitação JSON")
#         return jsonify({"error": "Campos obrigatórios ausentes no corpo da solicitação JSON"}), 400

# if __name__ == '__main__':
#     # Configure o logger para exibir mensagens de debug
#     logging.basicConfig(level=logging.DEBUG)
#     app.run(debug=True, host='0.0.0.0')