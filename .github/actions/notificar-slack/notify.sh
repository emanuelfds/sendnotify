#!/bin/bash
set -euo pipefail

for var in SLACK_WEBHOOK_URL VERSION IMAGE_NAME REPO SHA REF_NAME ACTOR TITLE; do
  if [ -z "${!var:-}" ]; then
    echo "::error::Variável obrigatória não definida: $var"
    exit 1
  fi
done

SHORT_SHA=$(echo "$SHA" | cut -c1-7)
TIMESTAMP=$(date +"%d/%m/%Y %H:%M")
COMMIT_URL="https://github.com/${REPO}/commit/${SHA}"
REPO_URL="https://github.com/${REPO}"

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST \
  -H 'Content-type: application/json' \
  --data "{
  \"blocks\": [
    {
      \"type\": \"header\",
      \"text\": {
        \"type\": \"plain_text\",
        \"text\": \"${TITLE}\",
        \"emoji\": true
      }
    },
    {
      \"type\": \"section\",
      \"fields\": [
        { \"type\": \"mrkdwn\", \"text\": \"*Aplicação:*\n${IMAGE_NAME}\" },
        { \"type\": \"mrkdwn\", \"text\": \"*Versão:*\n\`${VERSION}\`\" },
        { \"type\": \"mrkdwn\", \"text\": \"*Branch:*\n\`${REF_NAME}\`\" },
        { \"type\": \"mrkdwn\", \"text\": \"*Commit:*\n<${COMMIT_URL}|\`${SHORT_SHA}\`>\" },
        { \"type\": \"mrkdwn\", \"text\": \"*Autor:*\n@${ACTOR}\" },
        { \"type\": \"mrkdwn\", \"text\": \"*Data e Hora:*\n${TIMESTAMP}\" }
      ]
    },
    {
      \"type\": \"context\",
      \"elements\": [
        { \"type\": \"mrkdwn\", \"text\": \"<${REPO_URL}|Ver repositório>\" }
      ]
    }
  ]
}" "$SLACK_WEBHOOK_URL")

if [ "$HTTP_CODE" -ne 200 ]; then
  echo "::error::Falha ao enviar notificação Slack (HTTP $HTTP_CODE)"
  exit 1
fi

echo "✅ Notificação Slack enviada com sucesso"
