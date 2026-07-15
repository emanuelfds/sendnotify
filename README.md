<div align="center">

![SendNotify](images/sendnotify.png)

</div>

[![Python](https://img.shields.io/badge/Python-3.12+-blue?logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-blue?logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![Docker](https://img.shields.io/badge/Docker-Alpine-0db7ed?logo=docker&logoColor=white)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.28+-326CE5?logo=kubernetes&logoColor=white)](https://kubernetes.io)
[![OCI](https://img.shields.io/badge/OCI-F80000?logo=oracle&logoColor=white)](https://oracle.com/cloud)
[![AWS](https://img.shields.io/badge/AWS-FF9900?logo=amazonaws&logoColor=white)](https://aws.amazon.com)
[![Azure](https://img.shields.io/badge/Azure-0078D4?logo=microsoftazure&logoColor=white)](https://azure.microsoft.com)
[![Google Chat](https://img.shields.io/badge/Google_Chat-34A853?logo=googlechat&logoColor=white)](https://chat.google.com)
[![License](https://img.shields.io/badge/License-MIT-green?logo=opensourceinitiative&logoColor=white)](LICENSE)
[![Build](https://github.com/emanuelfds/sendnotify/actions/workflows/deploy.yaml/badge.svg)](https://github.com/emanuelfds/sendnotify/actions/workflows/deploy.yaml)
[![Release](https://img.shields.io/github/v/release/emanuelfds/sendnotify)](https://github.com/emanuelfds/sendnotify/releases/latest)
[![Trivy Scanning](https://img.shields.io/badge/Trivy-Scanning-brightgreen?logo=trivy&logoColor=white)](https://github.com/aquasecurity/trivy)
[![Bandit](https://img.shields.io/badge/Bandit-SAST-yellow?logo=python&logoColor=white)](https://bandit.readthedocs.io)
[![Gitleaks](https://img.shields.io/badge/Gitleaks-Secrets-orange?logo=gitguardian&logoColor=white)](https://github.com/gitleaks/gitleaks)
[![Hadolint](https://img.shields.io/badge/Hadolint-Dockerfile-blue?logo=docker&logoColor=white)](https://github.com/hadolint/hadolint)

# 📨 SendNotify

## Why SendNotify?

- **Multi-cloud em um único endpoint** — integra OCI, AWS e Azure no mesmo webhook, sem manter 3 integrações separadas
- **Auto-detection** — detecta o provedor automaticamente pelo payload, sem configuração
- **Normalização** — payloads diferentes → formato único para Google Chat
- **Zero vendor lock-in** — não depende de ferramentas proprietárias de cada cloud

---

**SendNotify** é um webhook bridge **multi-cloud** que recebe alertas de **OCI Monitoring**, **AWS CloudWatch** e **Azure Monitor** e os encaminha para o **Google Chat**.

A aplicação **detecta automaticamente** qual nuvem enviou o alerta, normaliza o payload e formata a mensagem com emojis e estrutura adequada para cada status (`FIRING` / `RESOLVED`).

---

## Sumário

- [🎯 Visão Geral](#-visão-geral)
- [⚙️ Funcionalidades](#️-funcionalidades)
- [🛡️ Segurança](#️-segurança)
- [🏗️ Fluxo](#️-fluxo)
- [📁 Estrutura do Projeto](#-estrutura-do-projeto)
- [💻 Pré-requisitos](#-pré-requisitos)
- [🚀 Testar Localmente (passo a passo)](#-testar-localmente-passo-a-passo)
- [☁️ Providers](#️-providers)
  - [OCI Monitoring](#oci-monitoring)
  - [AWS CloudWatch](#aws-cloudwatch)
  - [Azure Monitor](#azure-monitor)
- [🐳 Testar com Docker](#-testar-com-docker)
- [☸️ Deploy no Kubernetes](#️-deploy-no-kubernetes)
- [🧪 Testar com Mocks](#-testar-com-mocks)
- [📦 Instalar via pip](#-instalar-via-pip)
- [🌐 Testar via Ingress (URL pública)](#-testar-via-ingress-url-pública)
- [🛠️ Troubleshooting](#️-troubleshooting)
- [📬 Endpoints](#-endpoints)
- [🤝 Contribuindo](#-contribuindo)

---

## 🎯 Visão Geral

**Send Notify** é um webhook bridge **multi-cloud** que recebe alertas de **OCI Monitoring**, **AWS CloudWatch** e **Azure Monitor** e os encaminha para o **Google Chat**.

A aplicação **detecta automaticamente** qual nuvem enviou o alerta, normaliza o payload e formata a mensagem com emojis e estrutura adequada para cada status (`FIRING` / `RESOLVED`).

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## ⚙️ Funcionalidades

| Funcionalidade | Status |
|---|---|
| Suporte OCI Monitoring | ✅ |
| Suporte AWS CloudWatch (via SNS) | ✅ |
| Suporte Azure Monitor | ✅ |
| Auto-detect do provider pelo payload | ✅ |
| Confirmação automática de subscription | ✅ |
| Autenticação Basic Auth no /send | ✅ |
| Health check (/health) | ✅ |
| Endpoint de teste (/send) | ✅ |
| Probes Kubernetes (liveness + readiness) | ✅ |
| Node affinity para nós monitoring | ✅ |
| Security hardening (runAsNonRoot, seccompProfile, capabilities drop) | ✅ |
| CI/CD Pipeline (Trivy, Black, Ruff, MyPy, Slack notification) | ✅ |
| SAST (Bandit) | ✅ |
| Secret Scanning (Gitleaks) | ✅ |
| Dockerfile Lint (Hadolint) | ✅ |
| Dependency Audit (pip-audit) | ✅ |
| Testes offline com mocks | ✅ |
| Pronto para Docker | ✅ |

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🛡️ Segurança

O pipeline de CI/CD utiliza múltiplas ferramentas de segurança:

| Ferramenta | Tipo | O que detecta |
|---|---|---|
| **Trivy** | Vulnerability Scanning | CVEs em dependências, imagens Docker, manifests K8s |
| **Bandit** | SAST (Python) | `eval()`, `exec()`, SQL injection, hardcoded passwords |
| **Gitleaks** | Secret Scanning | Chaves, tokens, senhas no histórico git |
| **Hadolint** | Dockerfile Lint | Boas práticas de segurança em Dockerfiles |
| **pip-audit** | Dependency Audit | CVEs known em pacotes Python |
| **SBOM** | Software Bill of Materials | Lista completa de dependências |
| **Cosign** | Image Signing | Assinatura criptográfica da imagem Docker |

### Configuração no pipeline

```
Jobs:
  security     → Trivy (repo, app, k8s)
  sast         → Bandit + Gitleaks + Hadolint
  ci           → Ruff, Black, Mypy, Pytest, pip-audit
  build-and-push → Build, Trivy image, SBOM, Cosign
  deploy-argocd → Deploy ArgoCD (environment: production)
```

### Como rodar as ferramentas localmente

```bash
# Bandit (SAST)
pip install bandit
bandit -r build/ -ll --skip B101

# Gitleaks (Secret Scanning)
# Requer gitleaks CLI: https://github.com/gitleaks/gitleaks
gitleaks detect --source .

# Hadolint (Dockerfile Lint)
# Requer hadolint CLI: https://github.com/hadolint/hadolint
hadolint build/Dockerfile

# pip-audit (Dependency Audit)
pip install pip-audit
pip-audit -r build/requirements.txt
```

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🏗️ Fluxo

```
┌──────────────────┐     ┌──────────┐     ┌────────────────────┐     ┌──────────────┐
│  OCI / AWS       │ ──▶ │  Tópico  │ ──▶ │  Ingress (nginx)   │ ──▶ │  Google Chat │
│  / Azure         │     │ (SNS)    │     │  Subscription      │     │  (Webhook)   │
│                  │     │          │     │  HTTP → SendNotify │     │              │
└──────────────────┘     └──────────┘     └────────┬───────────┘     └──────────────┘
                                                    │
                                              ┌─────┴──────┐
                                              │ Basic Auth │ ← AUTH_USER / AUTH_PASS
                                              ├────────────┤
                                              │  detect()  │ ← identifica OCI / AWS / Azure
                                              ├────────────┤
                                              │  normalize │ ← traduz para formato único
                                              └─────┬──────┘
                                                    │
                                         ┌──────────┴──────────┐
                                         │                     │
                                  ┌──────┴───────┐   envia para Google Chat
                                  │ confirmation │
                                  │    _url?     │
                                  ├──────────────┤
                                  │  SIM → GET   │ → "Subscription confirmed"
                                  │  NÃO ↓       │
                                  └──────────────┘
```

**Detecção automática do provider:**

| Provider | Identificado por |
|----------|-----------------|
| OCI Monitoring | Campo `alarmMetaData` |
| AWS CloudWatch | Campo `Type` + `Message` (SNS) |
| Azure Monitor | Campo `data.essentials` |

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 📁 Estrutura do Projeto

```
sendnotify/
│
├── build/                          # Código fonte e imagem
│   ├── __init__.py             # Pacote raiz (importável via pip install -e .)
│   ├── main.py                     # App Flask (endpoints /subscription, /send, /health)
│   ├── wsgi.py                     # Entrypoint para gunicorn
│   ├── requirements.txt            # Dependências
│   ├── Dockerfile                  # Imagem Docker (python:3.12-alpine)
│   │
│   ├── providers/                  # Normalizadores multi-cloud
│   │   ├── __init__.py             # Registry + auto-detect
│   │   ├── oci.py                  # OCI Monitoring
│   │   ├── aws.py                  # AWS CloudWatch via SNS
│   │   └── azure.py                # Azure Monitor
│   │
│   └── tests/                      # Testes com mocks offline
│       ├── conftest.py             # sys.path para pytest imports
│       ├── test_providers.py       # Testes pytest (detect + normalize)
│       ├── README.md               # Documentação dos testes
│       └── samples/                # 8 payloads mock de exemplo
│
├── artifacts/                      # Manifestos Kubernetes
│   ├── 01-sendnotify-rbac.yaml       # ServiceAccount + ClusterRole + Binding
│   ├── 02-sendnotify-configmap.yaml  # TZ, CLOUD, CLOUDID
│   ├── 03-sendnotify-secret.yaml     # Template da Secret (NÃO commit com creds reais)
│   ├── 04-sendnotify-service.yaml    # Service (headless)
│   ├── 05-sendnotify-deployment.yaml # Deployment com probes + affinity
│   └── 06-sendnotify-ingress.yaml    # Ingress HTTP
│
├── .github/
│   ├── workflows/
│   │   ├── deploy.yaml              # CI/CD: lint, test, build, push, Trivy, Slack
│   │   └── release-please.yaml      # Release automático via conventional commits
│   └── actions/
│       └── notificar-slack/
│           ├── action.yaml           # Composite action para Slack
│           └── notify.sh             # Script de notificação
│
├── images/
│   └── sendnotify.png               # Logo do projeto
│
├── .dockerignore                    # Exclusões do Docker build
├── .gitignore
├── .pre-commit-config.yaml          # Hooks: ruff, black, mypy, whitespace
├── pyproject.toml                   # Config de Black, Ruff, MyPy
├── CONTRIBUTING.md                  # Guia de commits e releases
├── CHANGELOG.md                     # Changelog automático (release-please)
├── .release-please-manifest.json    # Versão atual (release-please)
├── release-please-config.json       # Config do release-please
└── README.md
```

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 💻 Pré-requisitos

- **Python 3.12+**
- **curl**
- **Docker** (opcional, para teste com container)
- **kubectl** (opcional, para deploy no Kubernetes)
- Um **webhook do Google Chat** ([como criar](https://developers.google.com/chat/how-tos/webhooks))

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🚀 Testar Localmente (passo a passo)

> Instruções para quem nunca usou Python.

### 1. Clone o repositório

```bash
cd /caminho/do/sendnotify
```

### 2. Crie o ambiente virtual

Instale as dependências do projeto:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Você verá `(.venv)` no início do terminal.

### 3. Instale as dependências

```bash
pip install -r build/requirements.txt
```

> **Ou**, se preferir instalar como pacote (com ferramentas de dev):
>
> ```bash
> pip install -e ".[dev]"
> ```

### 4. Configure as variáveis de ambiente

```bash
export AUTH_USER=admin
export AUTH_PASS=secret
export WEBHOOK='https://chat.googleapis.com/v1/spaces/SEU_SPACE/messages?key=SEU_KEY&token=SEU_TOKEN'
```

> 💡 **Dica**: crie um arquivo `.env` (não versionado) para não digitar toda vez:
>
> ```bash
> cat > .env << 'EOF'
> export AUTH_USER=admin
> export AUTH_PASS=secret
> export WEBHOOK='URL_DO_WEBHOOK'
> EOF
> source .env
> ```

### 5. Inicie a aplicação

```bash
python build/main.py
```

Saída esperada:

```
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
```

**Deixe este terminal aberto.** Abra outro para os testes.

### 6. Teste o health check

```bash
curl http://localhost:8080/health
```

```json
{"status": "ok"}
```

### 7. Envie uma mensagem de teste

```bash
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"text":"🧪 Teste via /send"}' \
  http://localhost:8080/send
```

```json
{
  "chat_message_id": "spaces/SEU_SPACE/messages/ID_UNICO",
  "message": "enviado"
}
```

### 8. Pare a aplicação

Pressione `Ctrl + C` no terminal da app.

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## ☁️ Providers

> **Nota:** Todos os exemplos abaixo utilizam `-u <user>:<password>` para autenticação. Substitua pelas credenciais da Secret `s-sendnotify`.

### OCI Monitoring

<details>
<summary>📋 Confirmação de subscription</summary>

```bash
curl -X POST -u <user>:<password> -H "Content-Type: application/json" \
  -d '{"ConfirmationURL": "https://httpbin.org/get"}' \
  http://localhost:8080/subscription
```
</details>

<details>
<summary>🔥 Alarme FIRING</summary>

```bash
curl -X POST -u <user>:<password> -H "Content-Type: application/json" \
  -d '{
    "title": "CPU Alta",
    "severity": "CRITICAL",
    "alarmMetaData": [{
      "status": "FIRING",
      "namespace": "oci_computeagent",
      "query": "CpuUtilization > 90",
      "alarmSummary": "CPU acima de 90%",
      "metricValues": [95.2]
    }]
  }' \
  http://localhost:8080/subscription
```
</details>

<details>
<summary>✅ Alarme RESOLVED</summary>

```bash
curl -X POST -u <user>:<password> -H "Content-Type: application/json" \
  -d '{
    "title": "CPU Alta",
    "severity": "CRITICAL",
    "alarmMetaData": [{
      "status": "OK",
      "namespace": "oci_computeagent",
      "query": "CpuUtilization > 90",
      "alarmSummary": "CPU normalizada",
      "metricValues": [45.0]
    }]
  }' \
  http://localhost:8080/subscription
```
</details>

### AWS CloudWatch

<details>
<summary>📋 Confirmação de subscription</summary>

```bash
curl -X POST -u <user>:<password> -H "Content-Type: application/json" \
  -d '{
    "Type": "SubscriptionConfirmation",
    "SubscribeURL": "https://sns.us-east-1.amazonaws.com/confirm?Token=abc"
  }' \
  http://localhost:8080/subscription
```
</details>

<details>
<summary>🔥 Alarme disparando (ALARM → FIRING)</summary>

```bash
curl -X POST -u <user>:<password> -H "Content-Type: application/json" \
  -d '{
    "Type": "Notification",
    "Message": "{\"AlarmName\":\"CPU Alta\",\"NewStateValue\":\"ALARM\",\"Region\":\"us-east-1\",\"AWSAccountId\":\"123456\",\"NewStateReason\":\"Threshold Crossed\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"Threshold\":90}}"
  }' \
  http://localhost:8080/subscription
```
</details>

<details>
<summary>✅ Alarme resolvido (OK → RESOLVED)</summary>

```bash
curl -X POST -u <user>:<password> -H "Content-Type: application/json" \
  -d '{
    "Type": "Notification",
    "Message": "{\"AlarmName\":\"CPU Alta\",\"NewStateValue\":\"OK\",\"Region\":\"us-east-1\",\"AWSAccountId\":\"123456\",\"NewStateReason\":\"Threshold OK\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"Threshold\":90}}"
  }' \
  http://localhost:8080/subscription
```
</details>

### Azure Monitor

<details>
<summary>🔥 Alarme disparando (Fired → FIRING)</summary>

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "data": {
      "essentials": {
        "alertRule": "CPU Alta",
        "severity": "Sev2",
        "monitorCondition": "Fired",
        "monitoringService": "Platform",
        "description": "CPU acima de 90%",
        "alertTargetIDs": ["/subscriptions/sub/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/vm01"]
      },
      "alertContext": {
        "condition": {"metricName": "Percentage CPU", "metricValue": "95.3"}
      }
    }
  }' \
  http://localhost:8080/subscription
```
</details>

<details>
<summary>✅ Alarme resolvido (Resolved → RESOLVED)</summary>

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{
    "data": {
      "essentials": {
        "alertRule": "CPU Alta",
        "severity": "Sev2",
        "monitorCondition": "Resolved",
        "monitoringService": "Platform",
        "description": "CPU normalizada",
        "alertTargetIDs": ["/subscriptions/sub/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/vm01"]
      },
      "alertContext": {
        "condition": {"metricName": "Percentage CPU", "metricValue": "45.0"}
      }
    }
  }' \
  http://localhost:8080/subscription
```
</details>

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 📦 Payloads de Exemplo

Como os payloads dos provedores são normalizados para o formato do Google Chat.

<details>
<summary><b>🔴 OCI Monitoring (FIRING)</b></summary>

**Input** (enviado pelo OCI Monitoring):

```json
{
  "title": "CPU > 90%",
  "severity": "CRITICAL",
  "body": "Alerta de CPU alta",
  "alarmMetaData": [
    {
      "status": "FIRING",
      "namespace": "oci_computeagent",
      "query": "CpuUtilization[5m] > 90",
      "alarmSummary": "CPU acima de 90% nos últimos 5 minutos",
      "metricValues": ["95.3"]
    }
  ]
}
```

**Output** (normalizado para Google Chat):

```
🔥 FIRING 🔥

*Alarm*: CPU > 90%
*Severity*: CRITICAL
*Namespace*: oci_computeagent
*Query*: CpuUtilization[5m] > 90
*Summary*: CPU acima de 90% nos últimos 5 minutos
*Metric Values*: ['95.3']
*Body*: Alerta de CPU alta
```

</details>

<details>
<summary><b>🟢 OCI Monitoring (RESOLVED)</b></summary>

**Input**:

```json
{
  "title": "CPU > 90%",
  "severity": "CRITICAL",
  "alarmMetaData": [
    {
      "status": "OK",
      "namespace": "oci_computeagent",
      "query": "CpuUtilization[5m] > 90",
      "alarmSummary": "CPU normalizada"
    }
  ]
}
```

**Output**:

```
✅ RESOLVED ✅

*Alarm*: CPU > 90%
*Severity*: CRITICAL
*Namespace*: oci_computeagent
*Query*: CpuUtilization[5m] > 90
*Summary*: CPU normalizada
```

</details>

<details>
<summary><b>🟠 AWS CloudWatch / SNS (FIRING)</b></summary>

**Input** (enviado pelo SNS):

```json
{
  "Type": "Notification",
  "Message": "{\"AlarmName\":\"High-CPU-Prod\",\"NewStateValue\":\"ALARM\",\"OldStateValue\":\"OK\",\"NewStateReason\":\"Threshold Crossed: 1 out of the last 1 datapoints [95.2 (13/07/26 18:00)] was greater than the threshold (90.0)\",\"Region\":\"sa-east-1\",\"AWSAccountId\":\"123456789012\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"Namespace\":\"AWS/EC2\",\"Threshold\":90}}"
}
```

> O campo `Message` é um JSON **stringificado** dentro do payload. O normalizer faz o `json.loads()` automaticamente.

**Output**:

```
🔥 FIRING 🔥

*Alarm*: High-CPU-Prod
*Account*: 123456789012
*Region*: sa-east-1
*State*: OK → ALARM
*Reason*: Threshold Crossed: 1 out of the last 1 datapoints [95.2 (13/07/26 18:00)] was greater than the threshold (90.0)
*Metric*: CPUUtilization
*Threshold*: 90
*Severity*: CRITICAL
*Namespace*: AWS/EC2
*Query*: CPUUtilization
*Summary*: Threshold Crossed: 1 out of the last 1 datapoints [95.2 (13/07/26 18:00)] was greater than the threshold (90.0)
*Metric Values*: [90]
*Body*: Account: 123456789012
Region: sa-east-1
State: OK → ALARM
Reason: Threshold Crossed: 1 out of the last 1 datapoints [95.2 (13/07/26 18:00)] was greater than the threshold (90.0)
Metric: CPUUtilization
Threshold: 90
```

</details>

<details>
<summary><b>🔵 Azure Monitor (FIRING)</b></summary>

**Input** (enviado pelo Action Group):

```json
{
  "data": {
    "essentials": {
      "alertRule": "High-CPU-Alert",
      "monitorCondition": "Fired",
      "severity": "Sev2",
      "description": "CPU acima de 90% no namespace principal",
      "signalType": "Metric",
      "monitoringService": "Azure Monitor",
      "alertTargetIDs": [
        "/subscriptions/aaa-bbb-ccc/resourceGroups/myRG/providers/Microsoft.Compute/virtualMachines/myVM"
      ]
    },
    "alertContext": {
      "condition": {
        "metricName": "Percentage CPU",
        "metricValue": "95.2"
      }
    }
  }
}
```

**Output**:

```
🔥 FIRING 🔥

*Alarm*: High-CPU-Alert
*Signal*: Metric
*Service*: Azure Monitor
*Condition*: Fired
*Description*: CPU acima de 90% no namespace principal
*Metric*: Percentage CPU = 95.2
*Resource*: myVM
*Severity*: WARNING
*Namespace*: Azure Monitor
*Query*: Percentage CPU
*Summary*: CPU acima de 90% no namespace principal
*Metric Values*: ['95.2']
*Body*: Signal: Metric
Service: Azure Monitor
Condition: Fired
Description: CPU acima de 90% no namespace principal
Metric: Percentage CPU = 95.2
Resource: myVM
```

</details>

<details>
<summary><b>📋 Tabela de Mapeamento de Severidade</b></summary>

| OCI | AWS | Azure | SendNotify |
|-----|-----|-------|------------|
| `CRITICAL` | `ALARM` | `Sev0`, `Sev1` | `CRITICAL` |
| — | `INSUFFICIENT_DATA` | `Sev2`, `Sev3` | `WARNING` |
| — | `OK` | `Sev4`, `Sev5` | `INFO` |

| OCI | AWS | Azure | SendNotify |
|-----|-----|-------|------------|
| `FIRING` | `ALARM` | `Fired` | `FIRING` |
| `OK` | `OK` | `Resolved` | `RESOLVED` |

</details>

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🐳 Testar com Docker

```bash
# Build
docker build -t send-notify build/

# Run
docker run --rm -p 8080:8080 \
  -e AUTH_USER=admin \
  -e AUTH_PASS=secret \
  -e WEBHOOK='URL_DO_WEBHOOK' \
  send-notify
```

```bash
# Testar (em outro terminal)
curl -X POST -u admin:secret \
  -H "Content-Type: application/json" \
  -d '{"text":"🧪 Teste via Docker"}' \
  http://localhost:8080/send
```

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## ☸️ Deploy no Kubernetes

### 1. Crie a Secret

```bash
kubectl create secret generic s-sendnotify \
  --from-literal=AUTH_USER=<seu_usuario> \
  --from-literal=AUTH_PASS=<sua_senha> \
  --from-literal=WEBHOOK='URL_DO_WEBHOOK' \
  --namespace=observability
```

> ⚠️ O arquivo `03-sendnotify-secret.yaml` é um **template**. Nunca commitar com credenciais reais.

### 2. Aplique os manifestos

```bash
kubectl apply -f artifacts/01-sendnotify-rbac.yaml
kubectl apply -f artifacts/02-sendnotify-configmap.yaml
kubectl apply -f artifacts/04-sendnotify-service.yaml
kubectl apply -f artifacts/05-sendnotify-deployment.yaml
kubectl apply -f artifacts/06-sendnotify-ingress.yaml
```

### 3. Verifique

```bash
kubectl get pods -n observability -l app=sendnotify
kubectl logs -n observability -l app=sendnotify --tail=50
```

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🧪 Testar com Mocks

Valida todos os normalizadores **sem precisar de webhook ou servidor rodando**:

```bash
pytest -v
```

Saída esperada:

```
build/tests/test_providers.py::test_detect[oci-confirmation.json] PASSED
build/tests/test_providers.py::test_detect[oci-firing.json] PASSED
build/tests/test_providers.py::test_detect[oci-resolved.json] PASSED
build/tests/test_providers.py::test_detect[aws-confirmation.json] PASSED
build/tests/test_providers.py::test_detect[aws-firing.json] PASSED
build/tests/test_providers.py::test_detect[aws-resolved.json] PASSED
build/tests/test_providers.py::test_detect[azure-firing.json] PASSED
build/tests/test_providers.py::test_detect[azure-resolved.json] PASSED
build/tests/test_providers.py::test_normalize[oci-confirmation.json] PASSED
build/tests/test_providers.py::test_normalize[oci-firing.json] PASSED
build/tests/test_providers.py::test_normalize[oci-resolved.json] PASSED
build/tests/test_providers.py::test_normalize[aws-confirmation.json] PASSED
build/tests/test_providers.py::test_normalize[aws-firing.json] PASSED
build/tests/test_providers.py::test_normalize[aws-resolved.json] PASSED
build/tests/test_providers.py::test_normalize[azure-firing.json] PASSED
build/tests/test_providers.py::test_normalize[azure-resolved.json] PASSED
build/tests/test_providers.py::test_unknown_payload PASSED

============================== 17 passed in 0.03s ==============================
```

Payloads de exemplo disponíveis em `build/tests/samples/`:

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

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 📦 Instalar via pip

O projeto é um pacote Python. Você pode instalar com `pip` para usar os normalizadores
fora do Docker ou para desenvolvimento local.

### Instalação para desenvolvimento

```bash
# Criar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar em modo editável (com dependências de dev)
pip install -e ".[dev]"

# Rodar testes
pytest -v

# Lint & format
ruff check .
black --check .
mypy .
```

### Instalação apenas dependências

```bash
pip install -e .
```

### Como funciona

O `pyproject.toml` define o pacote `sendnotify` com todas as dependências
em `dependencies`. Ao rodar `pip install -e .`, o pip:

1. Instala o pacote em **modo editável** (alterações refletem imediatamente)
2. Instala todas as dependências automaticamente
3. Torna `providers` importável de qualquer diretório

### Usar os normalizadores como biblioteca

```python
from providers import detect, normalize

payload = {
    "title": "CPU Alta",
    "severity": "CRITICAL",
    "alarmMetaData": [{
        "status": "FIRING",
        "namespace": "oci_computeagent",
        "query": "CpuUtilization > 90",
        "alarmSummary": "CPU acima de 90%",
        "metricValues": [95.2]
    }]
}

provider = detect(payload)   # "oci"
message  = normalize(payload) # dict com campos normalizados
```

### Docker

O Dockerfile continua usando `requirements.txt` para manter a imagem leve
(sem ferramentas de dev como pytest, black, ruff).

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🌐 Testar via Ingress (URL pública)

Após aplicar os manifestos do Kubernetes, teste os endpoints pelo hostname configurado no Ingress.

> **Nota:** Ambos os endpoints `/subscription` e `/send` exigem Basic Auth. As credenciais são definidas na Secret `s-sendnotify` (`AUTH_USER` / `AUTH_PASS`).

### 1. Verifique o Ingress

```bash
kubectl get ingress -n observability in-sendnotify
```

Copie o IP da coluna `ADDRESS`.

### 2. Teste o health check

```bash
curl http://sendnotify.emanuelfds.com.br/health
```

```json
{"status": "ok"}
```

### 3. Teste envio de mensagem (com Basic Auth)

```bash
curl -X POST -u <user>:<password> \
  -H "Content-Type: application/json" \
  -d '{"text":"Teste via URL pública"}' \
  http://sendnotify.emanuelfds.com.br/send
```

### 4. Teste confirmação de subscription (simula OCI)

Quando o OCI Monitoring cria um alarme com webhook, ele envia um POST com `ConfirmationURL`. A aplicação faz GET nessa URL para confirmar a subscription automaticamente.

```bash
curl -X POST -u <user>:<password> \
  -H "Content-Type: application/json" \
  -d '{"ConfirmationURL": "https://httpbin.org/get"}' \
  http://sendnotify.emanuelfds.com.br/subscription
```

```json
{"message": "Subscription confirmed"}
```

> Verifique os logs para confirmar: `kubectl logs -n observability -l app=sendnotify --tail=10`

### 5. Teste alarme OCI

```bash
curl -X POST -u <user>:<password> \
  -H "Content-Type: application/json" \
  -d '{
    "title": "CPU Alta",
    "severity": "CRITICAL",
    "alarmMetaData": [{
      "status": "FIRING",
      "namespace": "oci_computeagent",
      "query": "CpuUtilization > 90",
      "alarmSummary": "CPU acima de 90%",
      "metricValues": [95.2]
    }]
  }' \
  http://sendnotify.emanuelfds.com.br/subscription
```

### 6. Teste alarme AWS

```bash
curl -X POST -u <user>:<password> \
  -H "Content-Type: application/json" \
  -d '{
    "Type": "Notification",
    "Message": "{\"AlarmName\":\"CPU Alta\",\"NewStateValue\":\"ALARM\",\"Region\":\"us-east-1\",\"AWSAccountId\":\"123456\",\"NewStateReason\":\"Threshold Crossed\",\"Trigger\":{\"MetricName\":\"CPUUtilization\",\"Threshold\":90}}"
  }' \
  http://sendnotify.emanuelfds.com.br/subscription
```

### 7. Teste alarme Azure

```bash
curl -X POST -u <user>:<password> \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "essentials": {
        "alertRule": "CPU Alta",
        "severity": "Sev2",
        "monitorCondition": "Fired",
        "monitoringService": "Platform",
        "description": "CPU acima de 90%",
        "alertTargetIDs": ["/subscriptions/sub/resourceGroups/rg/providers/Microsoft.Compute/virtualMachines/vm01"]
      },
      "alertContext": {
        "condition": {"metricName": "Percentage CPU", "metricValue": "95.3"}
      }
    }
  }' \
  http://sendnotify.emanuelfds.com.br/subscription
```

### Resolução DNS (se necessário)

Se o hostname ainda não resolver, adicione no `/etc/hosts`:

```bash
echo "<IP_DO_INGRESS> sendnotify.emanuelfds.com.br" | sudo tee -a /etc/hosts
```

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🛠️ Troubleshooting

### App retorna 200 mas mensagem não aparece no Google Chat

1. Teste o webhook direto (sem a app):
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"text":"teste"}' '$WEBHOOK'
   ```
   Se falhar, o webhook está inválido ou expirado.

2. Confira se o `spaces/ID` no webhook é o espaço correto.

3. Verifique os logs:
   ```bash
   tail -f /tmp/sendnotify.log
   ```
   Procure por `HTTP 200` na linha do Google Chat.

### Provider não detectado

Execute o script de mocks para validar o payload:

```bash
pytest -v
```

Se o payload for de uma nuvem não suportada, será necessário [adicionar um novo provider](#-visão-geral).

### Pod no Kubernetes não inicia

```bash
kubectl describe pod -n observability -l app=sendnotify
kubectl logs -n observability -l app=sendnotify
```

Verifique se a Secret `s-sendnotify` existe:

```bash
kubectl get secret -n observability s-sendnotify
```

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 📬 Endpoints

| Método | Rota | Autenticação | Descrição |
|---|---|---|---|
| `GET` | `/health` | ❌ | Health check para probes |
| `POST` | `/subscription` | ✅ Basic Auth | Webhook de providers (OCI/AWS/Azure) |
| `POST` | `/send` | ✅ Basic Auth | Envio de texto livre |

<div align="right">

**[🔼 Voltar ao topo](#-sendnotify)**

</div>

---

## 🤝 Contribuindo

Consulte o [CONTRIBUTING.md](CONTRIBUTING.md) para guia de commits convencionais, fluxo de release e configuração de pre-commit.

---

<div align="center">

Feito com ☕ para simplificar alertas multi-cloud no Google Chat

</div>
