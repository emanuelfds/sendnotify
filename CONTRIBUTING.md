# Contribuindo — SendNotify

## Conventional Commits

O projeto usa [Conventional Commits](https://www.conventionalcommits.org/) para gerar changelogs e versionamento automático via **release-please**.

### Formato

```
<tipo>(<escopo>): <descrição>

[corpo opcional]

[footer opcional]
```

### Tipos de commit

| Tipo     | Quando usar                          | Version bump |
| -------- | ------------------------------------ | ------------ |
| `feat`   | Nova funcionalidade                  | minor        |
| `fix`    | Correção de bug                      | patch        |
| `docs`   | Apenas documentação                  | nenhum       |
| `chore`  | Manutenção, dependências, CI/CD      | nenhum       |
| `refactor` | Reestruturação sem mudar behavior  | nenhum       |
| `test`   | Adição/correção de testes            | nenhum       |
| `ci`     | Mudanças no pipeline (GitHub Actions)| nenhum       |
| `style`  | Formatação, whitespace               | nenhum       |

### Exemplos

```bash
# Feature → bump minor (1.0.0 → 1.1.0)
git commit -m "feat: suporte a Datadog como provider"

# Fix → bump patch (1.0.0 → 1.0.1)
git commit -m "fix: correlation_id ausente no payload OCI"

# Chore → sem bump
git commit -m "chore: adiciona pre-commit hooks"

# Docs → sem bump
git commit -m "docs: atualiza README com seção de providers"

# CI → sem bump
git commit -m "ci: adiciona job de lint no deploy.yaml"

# Breaking change → bump major (1.0.0 → 2.0.0)
git commit -m "feat!: muda formato do payload de entrada

BREAKING CHANGE: o campo 'text' agora é obrigatório"
```

### Regras

- Usar **inglês** nas mensagens
- Descrição em **minúscula**, sem ponto final
- Máximo de **72 caracteres** na primeira linha
- Usar `feat!:` ou `BREAKING CHANGE:` no footer para mudanças que quebram compatibilidade

## Fluxo de release

```
branch fix/feat/chore ──commit──► PR p/ main ──► merge ──► release-please cria Release PR ──► merge PR ──► tag v* ──► deploy
```

1. Faça commits em branches auxiliares (`feat/*`, `fix/*`, `chore/*`) com mensagens convencionais
2. Abra um PR para `main`
3. Após o merge, o **release-please** cria/atualiza um Release PR automaticamente
4. Ao merge do Release PR:
   - Gera o `CHANGELOG.md`
   - Cria a tag `v*`
   - Dispara o workflow de deploy (build + push imagem)

## Branch Protection

A branch `main` possui proteções obrigatórias:

- **PR review**: todo PR precisa de pelo menos 1 approval
- **Status checks**: CI (lint + test) e Trivy devem passar antes do merge
- **Signed commits** (recomendado): usar `git commit -S`
- **Force push**: desabilitado na branch `main`

### Regras

- Nunca faça push direto para `main`
- Use branches auxiliares (`feat/*`, `fix/*`, `chore/*`)
- Squash merge para manter histórico limpo

## Pré-commit

Hooks rodam automaticamente antes de cada `git commit`:

```bash
# Instalar (uma vez)
pre-commit install

# Rodar manualmente em todos os arquivos
pre-commit run --all-files
```

Hooks: `ruff` (lint), `black` (format), `mypy` (types), `trailing-whitespace`, `end-of-file-fixer`.
