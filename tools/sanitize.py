#!/usr/bin/env python3
"""
Sanitiza exports de workflows do n8n antes de versioná-los.

Remove credenciais, dados pinados (que costumam conter dados reais de clientes),
identificadores de infraestrutura e PII, substituindo por placeholders ou por
expressões `$env` — que é a forma recomendada de referenciar segredos no n8n.

Uso:
    python3 tools/sanitize.py origem.json destino.json
"""
import json
import re
import sys
from pathlib import Path

# Segredos literais conhecidos, carregados de um arquivo externo NÃO versionado
# (`tools/secrets.local.json`, no formato {"valor_literal": "NOME_DA_VAR"}).
# Este script nunca deve conter um segredo em texto claro — ele mesmo seria o
# vazamento. Sem o arquivo, a sanitização recai nos padrões genéricos abaixo.
def load_known_secrets() -> dict:
    try:
        with open(Path(__file__).parent / "secrets.local.json", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        return {}


SECRETS = load_known_secrets()

# Padrões genéricos: qualquer coisa com cara de token vira placeholder.
TOKEN_PATTERNS = [
    (re.compile(r"Bearer\s+[A-Za-z0-9._\-]{15,}"), "Bearer {{ $env.API_TOKEN }}"),
    (re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}"), "{{ $env.OPENAI_API_KEY }}"),
    (re.compile(r"\bsb_secret_[A-Za-z0-9_\-]+"), "{{ $env.SUPABASE_SERVICE_KEY }}"),
    (re.compile(r"\bEAA[A-Za-z0-9]{40,}"), "{{ $env.META_WHATSAPP_TOKEN }}"),
    (re.compile(r"eyJfcmFpbHM[A-Za-z0-9._\-]+"), "REDACTED_ATTACHMENT_TOKEN"),
    (re.compile(r"\beyJ[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]{20,}\.[A-Za-z0-9_\-]+"),
     "{{ $env.API_TOKEN }}"),
]

# Hosts de instâncias privadas -> placeholder. APIs públicas de fornecedores
# (gptmaker, 4medic, powercrm, hinova, z-api) são preservadas: elas documentam
# a integração e não expõem nada.
PRIVATE_HOSTS = [
    (re.compile(r"https://[a-z0-9\-]+\.supabase\.co"), "https://YOUR_PROJECT.supabase.co"),
    (re.compile(r"https://[a-z0-9.\-]*leomarques\.com\.br"), "https://YOUR_CHATWOOT_HOST"),
    (re.compile(r"https://[a-z0-9.\-]*topia-n8n\.com\.br"), "https://YOUR_N8N_HOST"),
    (re.compile(r"https://[a-z0-9.\-]*topiaagencia\.com\.br"), "https://YOUR_CLIENT_HOST"),
]

PII_PATTERNS = [
    (re.compile(r"[\w.+\-]+@[\w\-]+\.[\w.]{2,}"), "user@example.com"),
    (re.compile(r"\b55\d{10,11}\b"), "5500000000000"),
    (re.compile(r"\b\d{3}\.\d{3}\.\d{3}-\d{2}\b"), "000.000.000-00"),  # CPF
]

# Chaves cujo valor é sempre substituído, onde quer que apareçam.
REDACT_KEYS = {
    "documentId": "GOOGLE_SHEET_ID",
    "baseId": "AIRTABLE_BASE_ID",
    "cachedResultUrl": "",
    "webhookId": "",
    "instanceId": "",
}


def scrub_text(value: str) -> str:
    for literal, env_var in SECRETS.items():
        value = value.replace(literal, "{{ $env.%s }}" % env_var)
    for pattern, replacement in TOKEN_PATTERNS + PRIVATE_HOSTS + PII_PATTERNS:
        value = pattern.sub(replacement, value)
    return value


def scrub(node, key=None):
    if isinstance(node, dict):
        # Credenciais: preserva só o tipo, para documentar o que o workflow usa.
        if key == "credentials":
            return {k: {"name": f"<{k}>"} for k in node}
        out = {}
        for k, v in node.items():
            if k in REDACT_KEYS:
                placeholder = REDACT_KEYS[k]
                out[k] = placeholder if placeholder else ""
                continue
            out[k] = scrub(v, k)
        return out
    if isinstance(node, list):
        return [scrub(v, key) for v in node]
    if isinstance(node, str):
        return scrub_text(node)
    return node


def main() -> int:
    src, dst = sys.argv[1], sys.argv[2]
    with open(src, encoding="utf-8") as fh:
        data = json.load(fh)

    # pinData guarda amostras de execuções reais — sempre descartado.
    data.pop("pinData", None)
    for meta_key in ("id", "versionId", "meta", "shared", "tags"):
        data.pop(meta_key, None)

    clean = scrub(data)
    with open(dst, "w", encoding="utf-8") as fh:
        json.dump(clean, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
