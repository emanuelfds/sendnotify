# Testes & Qualidade — SendNotify

## Como rodar os testes

```bash
python build/tests/test_providers.py
```

## Estrutura

```
build/tests/
├── test_providers.py      # Testes de detect + normalize
├── samples/
│   ├── oci-confirmation.json
│   ├── oci-firing.json
│   ├── oci-resolved.json
│   ├── aws-confirmation.json
│   ├── aws-firing.json
│   ├── aws-resolved.json
│   ├── azure-firing.json
│   └── azure-resolved.json
└── README.md
```

## O que os testes cobrem

| Teste               | Descrição                                                      |
| ------------------- | -------------------------------------------------------------- |
| `test_detect()`     | Verifica se cada payload é detectado como o provider correto   |
| `test_normalize()`  | Verifica se `status` e `confirmation_url` são extraídos corretamente |
| `test_unknown()`    | Garante que payloads desconhecidos retornam `None`             |

## Lint & Type Check (manual)

```bash
black build/ --check     # formatação
ruff check build/        # estilo + imports
mypy build/              # tipos
```

## Pre-commit (automático)

O repositório usa [pre-commit](https://pre-commit.com/) para rodar checks automaticamente antes de cada `git commit`.

### Hooks configurados

| Hook               | O que faz                                      |
| ------------------ | ---------------------------------------------- |
| `ruff`             | Lint + auto-fix (`--fix`)                       |
| `black`            | Formatação de código                            |
| `mypy`             | Type checking (usa config do `pyproject.toml`)  |
| `trailing-whitespace` | Remove espaços em branco no final das linhas |
| `end-of-file-fixer`   | Garante newline no final do arquivo           |

### Instalação

```bash
# Instalar o hook no .git/hooks/pre-commit
pre-commit install
```

### Uso

```bash
# Rodar em todos os arquivos (sem precisar commitar)
pre-commit run --all-files

# Rodar apenas nos arquivos staged (automático no commit)
git add .
git commit -m "sua mensagem"
```

### Config

- Todos os hooks de Python estão limitados a `^build/` (ignora arquivos fora do projeto)
- MyPy usa `additional_dependencies` para encontrar `requests`, `flask`, etc.
- Config detalhada está em `pyproject.toml` (Black, Ruff, MyPy)
