import logging
import os

import providers
import requests
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {}


def load_users():
    user = os.environ.get("AUTH_USER")
    password = os.environ.get("AUTH_PASS")
    if user and password:
        users[user] = generate_password_hash(password)


load_users()


@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username
    return None


@auth.error_handler
def unauthorized():
    return jsonify({"error": "Unauthorized access"}), 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}


@app.before_request
def log_request_info():
    app.logger.debug(f"Headers: {request.headers}")
    app.logger.debug(f"Body: {request.get_data()}")


@app.route("/subscription", methods=["POST"])
@auth.login_required
def subscription():
    if not request.is_json:
        app.logger.error("Recebido JSON inválido")
        return jsonify({"error": "Invalid JSON"}), 400

    data = request.get_json()
    alert = providers.normalize(data)

    if not alert:
        return jsonify({"error": "Unknown payload format"}), 400

    app.logger.info(f"Alert from provider={alert['provider']} status={alert['status']}")

    if alert["confirmation_url"]:
        url = alert["confirmation_url"]
        app.logger.info(f"Confirming subscription: {url}")
        try:
            response = requests.get(url, verify=False, timeout=30)
            app.logger.info(f"Confirmation status: {response.status_code}")
            response.raise_for_status()
            return jsonify({"message": "Subscription confirmed"}), 200
        except requests.RequestException as e:
            app.logger.error(f"Erro ao confirmar a assinatura: {str(e)}")
            return jsonify({"error": str(e)}), 500

    if not alert["title"]:
        app.logger.error("Campos obrigatórios ausentes no payload")
        return jsonify({"error": "Campos obrigatórios ausentes"}), 400

    lines = [alert["title"]]

    if alert["severity"]:
        lines.append(f"*Severity*: {alert['severity']}")

    d = alert["details"]
    if d.get("namespace") or d.get("query"):
        lines.append(f"*Namespace*: {d.get('namespace', '')}\n" f"*Query*: {d.get('query', '')}")
    if d.get("summary"):
        lines.append(f"*Summary*: {d['summary']}")
    if d.get("metric_values"):
        lines.append(f"*Metric Values*: {d['metric_values']}")

    if alert["body"]:
        lines.append(f"*Body*: {alert['body']}")

    message = "\n".join(lines)
    webhook_url = os.environ.get("WEBHOOK")

    payload = {"text": message}
    headers = {"Content-Type": "application/json; charset=utf-8"}

    try:
        r = requests.post(webhook_url, json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        app.logger.error(f"Erro ao enviar para o Google Chat: {str(e)}")
        return jsonify({"error": str(e)}), 500

    chat_response = r.json() if r.text else {}
    msg_id = chat_response.get("name", "")

    if r.status_code == 200:
        app.logger.info(f"Mensagem enviada! ID: {msg_id}")
        return (
            jsonify(
                {
                    "message": "Mensagem enviada com sucesso para o Google Chat!",
                    "chat_message_id": msg_id,
                }
            ),
            200,
        )

    app.logger.error(f"Falha ao enviar a mensagem para o Google Chat. " f"Código de status: {r.status_code}")
    return jsonify({"error": "Falha ao enviar a mensagem para o Google Chat.", "status_code": r.status_code}), 500


@app.route("/send", methods=["POST"])
@auth.login_required
def send():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    webhook_url = os.environ.get("WEBHOOK")
    payload = {"text": data["text"]}
    headers = {"Content-Type": "application/json; charset=utf-8"}

    try:
        r = requests.post(webhook_url, json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        app.logger.error(f"Erro ao enviar: {str(e)}")
        return jsonify({"error": str(e)}), 500

    chat_response = r.json() if r.text else {}
    msg_id = chat_response.get("name", "")

    if r.status_code == 200:
        return jsonify({"message": "enviado", "chat_message_id": msg_id}), 200

    return jsonify({"error": "falha", "status_code": r.status_code}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    app.run(port=8080, debug=True, host="0.0.0.0")
