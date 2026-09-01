# Executive — Régua de Cobrança via WhatsApp

Automação de cobrança que consulta boletos por janela de vencimento e dispara a
mensagem com o link de pagamento pelo WhatsApp.

**39 nós** · Z-API · Google Sheets · 3 schedules

## Régua

O workflow trata cinco janelas de vencimento — `D+2`, `D+3`, `D+4`, `D+7` e
`D+15` — cada uma com sua consulta à API e sua mensagem. Três schedules
independentes (**9h**, **10h** e **11h**) distribuem as ondas ao longo da manhã,
em vez de concentrar tudo em um pico.

```mermaid
flowchart TD
    S9[Schedule 9h] --> L7[Listar boletos D+7]
    S10[Schedule 10h] --> L2[Listar boletos D+2]
    S11[Schedule 11h] --> L15[Listar boletos D+15]

    L7 --> SO7[Split Out] --> LP[Loop Over Items]
    L2 --> SO2[Split Out] --> LP
    L15 --> SO15[Split Out] --> LP

    LP --> IF{Elegível?}
    IF -->|não| NOP[Pula]
    IF -->|sim| WT[Wait — intervalo]
    WT --> BL[Busca link do boleto]
    BL --> MSG[Envia mensagem<br/>Z-API]
    MSG --> OK[Registra envio<br/>Google Sheets]
    OK --> LP
```

## Pontos de engenharia

**Link buscado por item, não em lote.** O link do boleto é gerado sob demanda
imediatamente antes do envio — links pré-gerados expiram e o cliente recebe uma
URL morta.

**Registro duplo na planilha.** Cada envio grava em duas abas (controle
operacional e histórico), permitindo auditar a régua sem consultar a API.

**Rate limiting explícito.** Nós `Wait` entre envios mantêm a cadência dentro do
limite da Z-API.

**Trigger manual preservado.** Além dos schedules, o fluxo tem gatilho manual para
reprocessamento pontual sem esperar a próxima janela.

## Dependências

Z-API (WhatsApp) · Google Sheets (OAuth2) · API de boletos com Bearer token

> Os tokens foram substituídos por `{{ $env.ZAPI_TOKEN }}` e `{{ $env.API_TOKEN }}`.
