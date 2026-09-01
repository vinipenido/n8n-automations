# Utils

Workflows curtos de apoio, usados como blocos de outros fluxos ou como endpoints
pontuais.

| Arquivo | Função | Nós |
|---|---|---|
| [`checa-cliente.json`](checa-cliente.json) | Webhook que consulta cadastro no MySQL e responde | 4 |
| [`busca-historico.json`](busca-historico.json) | Webhook que recupera histórico de conversas no MySQL | 4 |
| [`notificacao-sms.json`](notificacao-sms.json) | Webhook → SMS via Twilio | 2 |
| [`executive-ids-marcas.json`](executive-ids-marcas.json) | Coleta IDs de marcas via API paginada para o Sheets | 6 |
| [`executive-power-crm.json`](executive-power-crm.json) | Atualiza lista de contatos no Power CRM | 10 |

São implementações diretas, sem arquitetura relevante — estão aqui pela
completude do portfólio.
