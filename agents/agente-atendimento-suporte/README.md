# Agente de Atendimento e Suporte

Agente de suporte ao cliente no WhatsApp, com base de conhecimento em RAG,
coleta de NPS e escalonamento para atendimento humano.

**66 nós** · RAG · Supabase · Redis · Chatwoot


> **Nota de créditos:** a arquitetura de recepção (buffer Redis, entrada
> multimodal, humanizador, Chatwoot) parte de um template de curso de
> automação com n8n. As customizações próprias estão detalhadas em
> [Créditos e escopo do trabalho próprio](../README.md#créditos-e-escopo-do-trabalho-próprio).

## Objetivo

Resolver dúvidas recorrentes sem fila de espera, e — igualmente importante —
**reconhecer o que não deve responder** e passar para uma pessoa.

## Tools do agente

| Tool | Função |
|---|---|
| `treinamento` (vector store) | Busca semântica na base de conhecimento |
| `update_cadastro` | Atualiza dados do cliente no Supabase |
| `add_nps` | Registra a nota de satisfação ao fim do atendimento |
| `redirect_human` | Escala a conversa para um atendente no Chatwoot |
| `Think` | Raciocínio intermediário antes de responder |

## Escalonamento como tool

`redirect_human` é uma tool, não uma regra de negócio no fluxo. O agente decide
escalar a partir do conteúdo da conversa — pedido explícito de atendente,
reclamação grave, ou assunto fora da base de conhecimento. A decisão fica no
prompt, onde pode ser ajustada sem alterar a topologia do workflow.

## NPS no fim da conversa

Concluído o atendimento, o agente solicita a avaliação e grava via `add_nps`,
fechando o ciclo de qualidade sem intervenção humana.

## Fluxo

Mesma arquitetura de recepção dos demais agentes — ver
[README dos agentes](../README.md).

## Dependências

Redis · Supabase (`pgvector`) · Chatwoot · OpenAI
