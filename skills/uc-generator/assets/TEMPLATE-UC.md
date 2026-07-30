# UC-XXX — Nome do User Case

**Módulo:** (ex: Configuração de Processos / Atendimento / Tramitação)  
**Status:** Rascunho  
**Autor:** (nome do analista/responsável)  
**Fonte:** (ex: Transcrição de reunião — DD/MM/AAAA / Documento escrito — DD/MM/AAAA)  
**Complementa:** (opcional — ex: UC-XXX)

---

## 1. Contexto de Negócio (To-Be)

> Descreva o que o sistema **novo** deve fazer neste contexto. Foque no comportamento esperado pelo usuário, sem referências ao legado.

---

## 2. Regras de Negócio Globais

| ID        | Regra |
| --------- | ----- |
| RN-XXX-01 | ...   |

---

# 3. Estrutura UX e Navegação

> Descreve a organização funcional da experiência do usuário para permitir entendimento operacional e geração de requisitos derivados.

---

## 3.1 Jornada operacional do usuário

| Etapa | Ação do usuário       | Resultado esperado       |
| ----- | --------------------- | ------------------------ |
| 1     | Usuário acessa menu X | Sistema apresenta tela Y |

---

## 3.2 Estrutura de menus e navegação

```
- Menu (pai)
  -- Submenu (filho do menu)
     --- Item 1 (filho do submenu)
     --- Item 2
  -- Submenu 2
     --- Item 1
```

| Nível   | Menu (pai)  | Submenu      | Item             | Rótulo exibido no menu |
| ------- | ----------- | ------------ | ---------------- | ---------------------- |
| Menu    | Atendimento | —            | —                | Atendimento            |
| Submenu | Atendimento | Solicitações | —                | Solicitações           |
| Item    | Atendimento | Solicitações | Nova Solicitação | Nova Solicitação       |

---

## 3.3 Telas envolvidas

| Tela                     | Objetivo funcional         | Tipo |
| ------------------------ | -------------------------- | ---- |
| Consulta de Solicitações | Permitir busca operacional | Nova |
| Detalhamento             | Visualizar dados completos | Nova |

---

### Campos relevantes da tela

| Campo              | Tipo  | Obrigatório | Observação      |
| ------------------ | ----- | ----------- | --------------- |
| Número Solicitação | Texto | Sim         | Busca principal |

---

## 3.4 Componentes e comportamento funcional

| Elemento | Comportamento esperado    |
| -------- | ------------------------- |
| Tabela   | Paginação server-side     |
| Modal    | Exigir confirmação        |
| Filtro   | Persistir última pesquisa |

---

## 3.5 Estados, feedbacks e exceções

| Cenário                 | Comportamento esperado    |
| ----------------------- | ------------------------- |
| Sem resultados          | Exibir mensagem amigável  |
| Erro integração         | Exibir alerta operacional |
| Processamento concluído | Exibir confirmação        |

---

# 4. Critérios de Aceite Macro

| ID    | Critério                                      |
| ----- | --------------------------------------------- |
| CA-01 | Usuário consegue concluir o fluxo operacional |
| CA-02 | Sistema valida regras obrigatórias            |
| CA-03 | Fluxo respeita permissões                     |
| CA-04 | A navegação segue estrutura definida          |

---

# 5. Rastreabilidade

## UCs relacionados

| UC              | Relação                            |
| --------------- | ---------------------------------- |
| UC-XXX — Nome   | Complementa / Depende de / Precede |

---

## Requisitos derivados

| Requisito          | Status                             |
| ------------------ | ---------------------------------- |
| `req-XXXX-nome.md` | A criar / Em elaboração / Aprovado |

---

## Módulos do novo sistema impactados

| Módulo                     | Caminho (codebase)         | Impacto esperado                      |
| -------------------------- | -------------------------- | ------------------------------------- |
| `gprev-api` — NomeService  | `gprev-api/src/.../`       | Novo endpoint / Novo domínio / Ajuste |
| `gprev-admin` — NomeModule | `gprev-admin/src/app/.../` | Nova tela / Ajuste de componente      |

---

# 6. Dúvidas e Checklist de Validação

- [ ]