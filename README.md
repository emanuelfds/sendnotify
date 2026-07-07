# OCI Send Notify

App que recebe alertas de várias nuvens (**OCI**, **AWS**, **Azure**) e envia para o **Google Chat**.

## Sumário

- [Como funciona](#como-funciona)
- [Pré-requisitos](#pré-requisitos)
- [Testar localmente (passo a passo)](#testar-localmente-passo-a-passo)
- [Provider OCI](#provider-oci)
- [Provider AWS](#provider-aws)
- [Provider Azure](#provider-azure)
- [Endpoint /send (teste rápido)](#endpoint-send-teste-rápido)
- [Testar com Docker](#testar-com-docker)
- [Deploy no Kubernetes](#deploy-no-kubernetes)
- [Arquitetura do código](#arquitetura-do-código)
- [Adicionar um novo provider](#adicionar-um-novo-provider)

---

## Como funciona

```
Alarme (OCI/AWS/Azure) → Tópico → Subscription HTTP → esta app → Google Chat
```

A app:
1. Recebe um POST no `/subscription`
2. **Detecta automaticamente** qual nuvem enviou (OCI, AWS ou Azure)
3. Normaliza o payload para um formato único
4. Monta a mensagem e envia para o Google Chat

### Suporte por nuvem

| Nuvem | Serviço | Confirmação subscription | Status FIRING | Status RESOLVED |
|---|---|---|---|---|
| **OCI** | Monitoring | `ConfirmationURL` | `FIRING` | `OK` → RESOLVED |
| **AWS** | CloudWatch via SNS | `SubscribeURL` | `ALARM` → FIRING | `OK` → RESOLVED |
| **Azure** | Monitor | — | `Fired` → FIRING | `Resolved` → RESOLVED |

---

## Pré-requisitos

- **Python 3.10+** instalado
- **curl** (para testar os endpoints)
- Um **webhook do Google Chat** (como criar: abra o Google Chat → espaço → Gerenciar webhooks)

---

## Testar localmente (passo a passo)

### 1. Baixe o projeto

```bash
cd /caminho/onde/baixou/oci-send-notify
```

### 2. Crie um ambiente virtual Python

Isola as dependências do projeto para não afetar o sistema:

```bash
python3 -m venv .venv
```

Ative o ambiente:

```bash
source .venv/bin/activate
```

Você deve ver `(.venv)` no início do terminal.

### 3. Instale as dependências

```bash
pip install -r build/requirements.txt
```

A saída deve mostrar a instalação dos pacotes: Flask, requests, gunicorn etc.

### 4. Configure as variáveis de ambiente

Defina as credenciais e o webhook. O `AUTH_admin` e `AUTH_user` são os usuários que vão autenticar no endpoint:

```bash
export AUTH_admin=secret
export AUTH_user=password
export WEBHOOK='URL_DO_SEU_WEBHOOK_DO_GOOGLE_CHAT'
export CLOUDID=MinhaEmpresa
```

> **Dica**: para não digitar toda vez, crie um arquivo `.env` (ele não será versionado):
> ```bash
> cat > .env << 'EOF'
> export AUTH_admin=secret
> export AUTH_user=password
> export WEBHOOK='https://chat.googleapis.com/v1/spaces/SEU_SPACE/messages?key=SEU_KEY&token=SEU_TOKEN'
> export CLOUDID=MinhaEmpresa
> EOF
> source .env
> ```

### 5. Inicie a aplicação

```bash
python build/main.py
```

Você deve ver algo como:

```
 * Serving Flask app 'main'
 * Debug mode: on
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
```

A aplicação está rodando em `http://localhost:8080`.

**Deixe este terminal aberto.** Abra outro terminal para os próximos passos.

### 6. Teste se a app está no ar

```bash
curl http://localhost:8080/health
```

Saída esperada:

```json
{
  "status": "ok"
}
```

### 7. Teste o webhook direto (sem a app)

Isola se o problema é no webhook ou na app:

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"text":"🧪 Teste direto do webhook"}' \
  '$WEBHOOK'
```

Saída esperada (com um ID único):

```json
{
  "name": "spaces/SEU_SPACE/messages/ID_UNICO",
  "text": "🧪 Teste direto do webhook"
}
```

Se falhar, o webhook está inválido ou expirado.

### 8. Teste o endpoint /send (mais fácil)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"text":"🧪 Teste via app"}' \
  http://localhost:8080/send
```

Saída esperada:

```json
{
  "chat_message_id": "spaces/SEU_SPACE/messages/ID_UNICO",
  "message": "enviado"
}
```

### 9. Pare a aplicação

No terminal onde a app está rodando, pressione `Ctrl + C`.

---

## Provider OCI

### Payload de confirmação (primeiro POST)

A OCI envia um `ConfirmationURL` para confirmar a subscription. A app faz um GET nessa URL automaticamente:

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"ConfirmationURL": "https://httpbin.org/get"}' \
  http://localhost:8080/subscription
```

### Payload de alarme disparando (FIRING)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CPU Alta",
    "severity": "CRITICAL",
    "alarmMetaData": [
      {
        "status": "FIRING",
        "namespace": "oci_computeagent",
        "query": "CpuUtilization > 90",
        "alarmSummary": "CPU acima de 90% por 5 minutos",
        "metricValues": [95.2]
      }
    ]
  }' \
  http://localhost:8080/subscription
```

### Payload de alarme resolvido (OK → RESOLVED)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CPU Alta",
    "severity": "CRITICAL",
    "alarmMetaData": [
      {
        "status": "OK",
        "namespace": "oci_computeagent",
        "query": "CpuUtilization > 90",
        "alarmSummary": "CPU abaixo do limiar",
        "metricValues": [45.0]
      }
    ]
  }' \
  http://localhost:8080/subscription
```

---

## Provider AWS

### Payload de confirmação

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{
    "Type": "SubscriptionConfirmation",
    "SubscribeURL": "https://sns.us-east-1.amazonaws.com/confirm?Token=abc123"
  }' \
  http://localhost:8080/subscription
```

### Payload de alarme disparando (ALARM → FIRING)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{
    "Type": "Notification",
    "Message": "{\"AlarmName\":\"CPU Alta\",\"NewStateValue\":\"ALARM\",\"Region\":\"us-east-1\",\"AWSAccountId\":\"123456\",\"NewStateReason\":\"Threshold Crossed\",\"OldStateValue\":\"OK\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"Namespace\":\"AWS/EC2\",\"Threshold\":90}}"
  }' \
  http://localhost:8080/subscription
```

### Payload de alarme resolvido (OK → RESOLVED)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{
    "Type": "Notification",
    "Message": "{\"AlarmName\":\"CPU Alta\",\"NewStateValue\":\"OK\",\"Region\":\"us-east-1\",\"AWSAccountId\":\"123456\",\"NewStateReason\":\"Threshold OK\",\"OldStateValue\":\"ALARM\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"Namespace\":\"AWS/EC2\",\"Threshold\":90}}"
  }' \
  http://localhost:8080/subscription
```

---

## Provider Azure

### Payload de alarme disparando (Fired → FIRING)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "essentials": {
        "alertRule": "CPU Alta",
        "severity": "Sev2",
        "signalType": "Metric",
        "monitorCondition": "Fired",
        "monitoringService": "Platform",
        "description": "CPU acima de 90%",
        "alertTargetIDs": ["/subscriptions/sub-123/resourceGroups/rg-prod/providers/Microsoft.Compute/virtualMachines/vm-app01"]
      },
      "alertContext": {
        "condition": {
          "metricName": "Percentage CPU",
          "metricValue": "95.3",
          "threshold": "90"
        }
      }
    }
  }' \
  http://localhost:8080/subscription
```

### Payload de alarme resolvido (Resolved → RESOLVED)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "essentials": {
        "alertRule": "CPU Alta",
        "severity": "Sev2",
        "signalType": "Metric",
        "monitorCondition": "Resolved",
        "monitoringService": "Platform",
        "description": "CPU normalizada",
        "alertTargetIDs": ["/subscriptions/sub-123/resourceGroups/rg-prod/providers/Microsoft.Compute/virtualMachines/vm-app01"]
      },
      "alertContext": {
        "condition": {
          "metricName": "Percentage CPU",
          "metricValue": "45.0",
          "threshold": "90"
        }
      }
    }
  }' \
  http://localhost:8080/subscription
```

---

## Endpoint /send (teste rápido)

Endpoint simples que envia qualquer texto direto para o Google Chat, sem normalização de provider:

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"text":"🧪 Mensagem de teste"}' \
  http://localhost:8080/send
```

Útil para testar se o webhook está funcionando sem precisar montar um payload de alarme.

---

## Testar sem instalar nada (usando Docker)

### 1. Construa a imagem

```bash
docker build -t send-notify build/
```

### 2. Execute o container

```bash
docker run --rm -p 8080:8080 \
  -e AUTH_admin=secret \
  -e AUTH_user=password \
  -e WEBHOOK='https://chat.googleapis.com/v1/spaces/SEU_SPACE/messages?key=SEU_KEY&token=SEU_TOKEN' \
  -e CLOUDID=MinhaEmpresa \
  send-notify
```

### 3. Teste (em outro terminal)

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"text":"🧪 Teste via Docker"}' \
  http://localhost:8080/send
```

---

## Deploy no Kubernetes

### 1. Crie a Secret (credenciais e webhook)

```bash
kubectl create secret generic auth-users \
  --from-literal=AUTH_admin=secret \
  --from-literal=AUTH_user=password \
  --from-literal=WEBHOOK='https://chat.googleapis.com/v1/spaces/SEU_SPACE/messages?key=SEU_KEY&token=SEU_TOKEN' \
  --namespace=monitoring
```

### 2. Aplique os manifestos

```bash
kubectl apply -f artifacts/02-clusterRole.yaml
kubectl apply -f artifacts/03-clusterRoleBinding.yaml
kubectl apply -f artifacts/06-serviceAccount.yaml
kubectl apply -f artifacts/04-deployment.yaml
kubectl apply -f artifacts/05-service.yaml
kubectl apply -f artifacts/07-ingress.yaml
```

### 3. Verifique

```bash
kubectl get pods -n monitoring -l app=sendnotify
kubectl logs -n monitoring -l app=sendnotify --tail=50
```

---

## Testar com mocks (validação offline)

Testa os normalizadores sem precisar de webhook ou servidor rodando:

```bash
python3 build/tests/test_providers.py
```

Saída esperada:

```
=== Detect ===
  ✓ oci-confirmation.json          → oci        (expected oci)
  ✓ oci-firing.json                → oci        (expected oci)
  ✓ oci-resolved.json              → oci        (expected oci)
  ✓ aws-confirmation.json          → aws        (expected aws)
  ✓ aws-firing.json                → aws        (expected aws)
  ✓ aws-resolved.json              → aws        (expected aws)
  ✓ azure-firing.json              → azure      (expected azure)
  ✓ azure-resolved.json            → azure      (expected azure)

=== Normalize ===
  ✓ oci-confirmation.json          → confirmation_url=...
  ✓ oci-firing.json                → status=FIRING
  ✓ oci-resolved.json              → status=RESOLVED
  ✓ aws-confirmation.json          → confirmation_url=...
  ✓ aws-firing.json                → status=FIRING
  ✓ aws-resolved.json              → status=RESOLVED
  ✓ azure-firing.json              → status=FIRING
  ✓ azure-resolved.json            → status=RESOLVED

=== Unknown ===
  ✓ unknown payload                → None (correct)

→ Todos os testes passaram!
```

Os payloads de exemplo ficam em `build/tests/samples/`:

| Arquivo | Provider | Cenário |
|---|---|---|
| `oci-confirmation.json` | OCI | Confirmação |
| `oci-firing.json` | OCI | Disparando |
| `oci-resolved.json` | OCI | Resolvido |
| `aws-confirmation.json` | AWS | Confirmação |
| `aws-firing.json` | AWS | Disparando |
| `aws-resolved.json` | AWS | Resolvido |
| `azure-firing.json` | Azure | Disparando |
| `azure-resolved.json` | Azure | Resolvido |

---

## Arquitetura do código

```
oci-send-notify/
├── build/
│   ├── main.py                 # App Flask (endpoints /subscription, /send, /health)
│   ├── wsgi.py                 # Entrypoint para gunicorn
│   ├── app.py                  # Atalho para rodar python app.py (igual main.py)
│   ├── requirements.txt        # Dependências Python
│   ├── Dockerfile              # Imagem Docker
│   ├── providers/
│   │   ├── __init__.py         # Registry + auto-detect do provider
│   │   ├── oci.py              # Normalizador OCI Monitoring
│   │   ├── aws.py              # Normalizador AWS CloudWatch (via SNS)
│   │   └── azure.py            # Normalizador Azure Monitor
│   └── tests/
│       ├── test_providers.py   # Script de validação dos normalizadores
│       └── samples/            # Payloads mock de cada nuvem (8 arquivos)
├── artifacts/
│   ├── 02-clusterRole.yaml
│   ├── 03-clusterRoleBinding.yaml
│   ├── 04-deployment.yaml
│   ├── 05-service.yaml
│   ├── 06-serviceAccount.yaml
│   ├── 07-ingress.yaml
│   └── 08-secret-auth.yaml     # Template da Secret
└── README.md
```

### Fluxo de uma requisição

```
POST /subscription
  │
  ├─ providers.detect(data)          ← identifica OCI / AWS / Azure
  │
  ├─ providers.normalize(data)       ← traduz para formato único:
  │                                     { title, body, severity, status,
  │                                       confirmation_url, details }
  │
  ├─ Se tem confirmation_url:
  │   └─ GET na URL para confirmar subscription
  │
  ├─ Se não tem título:
  │   └─ retorna 400
  │
  └─ Monta mensagem e envia para Google Chat via WEBHOOK
```

### Formato normalizado (unificado)

```python
{
    "provider": "oci" | "aws" | "azure",
    "confirmation_url": str | None,  # URL para GET de confirmação
    "title": str,                    # Título do alarme
    "body": str,                     # Descrição
    "severity": str,                 # "CRITICAL" | "WARNING" | "INFO"
    "status": "FIRING" | "RESOLVED", # Status normalizado
    "details": {
        "namespace": str,
        "query": str,
        "summary": str,
        "metric_values": list,
    }
}
```

---

## Adicionar um novo provider

### 1. Crie o arquivo do normalizador

`build/providers/sua_nuvem.py`:

```python
from . import register

@register('sua_nuvem')
def normalize(data):
    return {
        'confirmation_url': None,
        'title': data.get('nome_do_alarme', ''),
        'body': data.get('descricao', ''),
        'severity': data.get('severidade', ''),
        'status': 'FIRING' if data.get('state') == 'ALERT' else 'RESOLVED',
        'details': {
            'namespace': '',
            'query': '',
            'summary': '',
            'metric_values': [],
        },
    }
```

### 2. Adicione a detecção

Em `build/providers/__init__.py`, função `detect()`:

```python
def detect(data):
    if 'alarmMetaData' in data or 'ConfirmationURL' in data:
        return 'oci'
    if 'Type' in data and data.get('Type') in ('Notification', 'SubscriptionConfirmation'):
        return 'aws'
    if 'data' in data and 'essentials' in data.get('data', {}):
        return 'azure'
    if 'SEU_CAMPO_IDENTIFICADOR' in data:
        return 'sua_nuvem'
    return None
```

### 3. Teste com um payload mock

Crie `build/tests/samples/sua_nuvem-firing.json` e rode:

```bash
python3 build/tests/test_providers.py
```
