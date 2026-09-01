# n8n Automations

Coleção de automações e agentes de IA construídos em **n8n**, aplicados em projetos
reais de atendimento, vendas e operações comerciais.

Todos os workflows deste repositório foram **sanitizados**: credenciais, dados de
execução e identificadores de infraestrutura foram substituídos por placeholders
(veja [`tools/sanitize.py`](tools/sanitize.py)).

---

## Stack

| Camada | Tecnologias |
|---|---|
| Orquestração | n8n (self-hosted) |
| IA / LLM | OpenAI GPT-4.1 e GPT-5, LangChain nodes, MCP (Model Context Protocol) |
| RAG / Vetores | Supabase `pgvector`, embeddings OpenAI |
| Memória | Redis (buffer + chat memory), Memory Manager |
| Dados | PostgreSQL, MySQL, Supabase, Airtable, Google Sheets |
| Mensageria | WhatsApp Cloud API, Z-API, Chatwoot, Twilio |
| Integrações | GPTMaker, Power CRM, Hinova, 4Medic |

---

## Destaques

### 🤖 [Agentes de IA](agents/) — atendimento conversacional multimodal

Agentes de WhatsApp com pipeline completo: recepção multimodal (texto, áudio,
imagem e PDF), buffer de mensagens em Redis para consolidar mensagens picotadas,
RAG sobre base de conhecimento, tools de CRM e humanização da resposta.

| Workflow | Nós | O que demonstra |
|---|---|---|
| [Agente Vendedor](agents/agente-vendedor/) | 92 | 4 agentes encadeados, CRM em Airtable com 8 tools, follow-up autônomo agendado |
| [Agente SDR](agents/agente-sdr/) | 80 | **MCP Server + MCP Client**, agendamento via Google Calendar |
| [Agente Atendimento/Suporte](agents/agente-atendimento-suporte/) | 66 | Roteamento de intenção e escalonamento para humano |

### 🔍 [RAG](rag/) — busca semântica sobre dados de negócio

| Workflow | Nós | O que demonstra |
|---|---|---|
| [ArtPel — Consulta de Estoque](rag/artpel-consulta-estoque/) | 25 | Pipeline de ingestão incremental + agente consultando estoque em tempo real |
| [Chat RAG](rag/chat-rag/) | 10 | Implementação mínima de RAG com tratamento de erro via Discord |

### ⚙️ [Pipelines](pipelines/) — operações em lote

| Workflow | Nós | O que demonstra |
|---|---|---|
| [Disparo de Boleto](pipelines/executive-disparo-boleto/) | 39 | Régua de cobrança D+7/D+15 com paginação e rate limiting |
| [Cadência de Follow-up](pipelines/cadencia-follow-up/) | 4 workflows | Arquitetura modular com sub-workflows reutilizáveis |
| [Disparo Ativo WhatsApp](pipelines/disparo-ativo-whatsapp/) | 12 | Campanhas via WhatsApp Cloud API com controle de status |
| [Sync Sheets → Supabase](pipelines/artpel-sync-supabase/) | 4 | Upsert em lote agendado |

### 🔌 [Integrações](integrations/)

| Workflow | Nós | O que demonstra |
|---|---|---|
| [VITALE — 4Medic](integrations/vitale-4medic/) | 22 | API de agendamento médico exposta como tool para agente de IA |

### 🧰 [Utils](utils/)

Workflows curtos de apoio: consulta de cliente, histórico de conversas,
notificação por SMS e sincronizações pontuais de CRM.

---

## Como usar

1. No n8n: **Workflows → Import from File** e selecione o `.json` desejado.
2. Recrie as credenciais (elas foram removidas — cada nó indica o tipo esperado).
3. Defina as variáveis de ambiente referenciadas como `{{ $env.NOME }}`.
4. Substitua os placeholders `YOUR_*` e `GOOGLE_SHEET_ID` pelos seus próprios.

> Os workflows foram construídos para contextos de clientes específicos. Trate-os
> como referência de arquitetura, não como solução plug-and-play.

## Licença

[MIT](LICENSE)
