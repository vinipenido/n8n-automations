# Segurança

## Sanitização

Nenhum workflow deste repositório contém credenciais. Antes de qualquer commit,
os exports passam por [`tools/sanitize.py`](tools/sanitize.py), que remove:

| Item | Tratamento |
|---|---|
| Tokens de API, Bearer, JWT, service keys | Substituídos por `{{ $env.NOME }}` |
| Objetos `credentials` dos nós | Reduzidos ao tipo da credencial |
| `pinData` | Removido — guarda amostras de execuções reais |
| E-mails, telefones, CPFs | Substituídos por valores fictícios |
| IDs de planilhas e bases Airtable | Substituídos por placeholders |
| Hosts de instâncias privadas | Substituídos por `YOUR_*` |
| `webhookId`, `instanceId`, `versionId` | Removidos |

APIs públicas de fornecedores são preservadas propositalmente — elas documentam a
integração e não expõem nada.

## Uso

```bash
python3 tools/sanitize.py export-cru.json destino/workflow.json
```

Exports crus não devem ser versionados: o `.gitignore` cobre `raw/`,
`*.local.json` e qualquer arquivo de backup da instância.

## Reportando um problema

Se encontrar algum dado sensível que tenha escapado da sanitização, abra uma
issue **sem incluir o valor encontrado** e ele será removido e rotacionado.
