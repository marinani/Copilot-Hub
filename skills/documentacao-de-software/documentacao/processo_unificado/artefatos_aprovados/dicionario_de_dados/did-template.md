# Dicionário de Dados Template

## Metadados

- **Código do documento:** `did-template`
- **Título:** Template de Dicionário de Dados
- **Data de criação:** DD/MM/AAAA
- **Última atualização:** DD/MM/AAAA
- **Autor:** Nome do autor
- **Versão:** 1.0.0
- **Status:** Rascunho | Em revisão | Aprovado

## Objetivo

Catalogar campos, tipos, domínios e regras de dados relevantes para a funcionalidade.

## Escopo

- Tabelas/objetos cobertos:
- Limites do documento:

## Artefatos relacionados

### Documentos/requisitos que impactam este artefato

- `req-...`
- `der-...`

### Documentos/requisitos impactados por este artefato

- `api-...`
- `min-...`

### Componentes técnicos relacionados

- Tabelas/colunas:
- Views:
- Procedures/functions:
- Campos de frontend:

## Dicionário de campos

| Objeto | Campo | Tipo | Tamanho | Obrigatório | Regra/Domínio | Origem/Uso |
| ------ | ----- | ---- | ------- | ----------- | ------------- | ---------- |
|        |       |      |         | Sim/Não     |               |            |

## Regras complementares

- Valores default:
- Regras de consistência:
- Máscaras e formatações:
- Sensibilidade/LGPD: toda coluna documentada deve indicar obrigatoriamente `LGPD: dado sensível` ou `LGPD: dado não sensível` no campo `Comentário`. Exemplo: `Nome do usuário. LGPD: dado sensível`. Esta classificação é **obrigatória e bloqueante** — coluna sem classificação LGPD impede a finalização do documento (ver regra 36.a da skill `documentacao-de-software`).

## Validações realizadas para esta documentação

- [ ] Estrutura de banco verificada
- [ ] Campos usados em API/frontend confirmados
- [ ] Regras de domínio registradas
- [ ] Documentações relacionadas revisadas

## Histórico de alterações

| Data       | Autor | Versão | Alteração            |
| ---------- | ----- | ------ | -------------------- |
| DD/MM/AAAA | Nome  | 1.0.0  | Criação do documento |

## Esclarecimentos

- Premissas consideradas:
- Dúvidas pendentes:
- Decisões tomadas:
