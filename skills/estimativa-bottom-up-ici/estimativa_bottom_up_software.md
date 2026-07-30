# Estimativa de Software Bottom-Up

## Conceito Central

A estimativa Bottom-Up é uma técnica de estimativa de software baseada na decomposição progressiva do trabalho em unidades pequenas e mensuráveis, estimando cada item individualmente e depois agregando tudo em uma estimativa consolidada.

Ela é amplamente utilizada em metodologias como:

- PMBOK/WBS
- Scrum em projetos complexos
- Engenharia de software tradicional
- Contratos de fábrica de software
- Planejamento de roadmap técnico
- Planejamento de sprint com alto nível de precisão

---

# Conceito central

A lógica do Bottom-Up é:

> “Quanto menor e mais concreta a unidade de trabalho, maior a precisão da estimativa.”

Ao invés de estimar:

- “Sistema de biblioteca digital → 3 meses”

Você decompõe:

- Autenticação JWT
- CRUD de documentos
- Upload de PDF
- Extração de metadados
- Controle de acesso
- Busca textual
- Integração PostgreSQL
- Testes
- Deploy
- Observabilidade
- etc.

E estima cada item individualmente.

Depois:
- soma
- aplica fatores de risco
- adiciona overhead
- gera cronograma/custo

---

# Estrutura técnica do Bottom-Up

A estrutura normalmente possui:

```text
Projeto
 └── Épicos
      └── Features
           └── User Stories
                └── Tasks Técnicas
                     └── Subtasks
```

O nível ideal de estimativa Bottom-Up geralmente é:
- task técnica
- ou subtask

Porque:
- É concreta
- Possui escopo claro
- Tem baixa variabilidade

---

# Fluxo completo da estimativa

## 1. Levantamento de requisitos

Primeiro ocorre:
- descoberta funcional
- descoberta técnica
- identificação de integrações
- restrições arquiteturais
- requisitos não funcionais

Exemplo:

Sistema:
- Biblioteca digital da guarda municipal

Requisitos:
- Upload PDF
- OCR
- Busca textual
- Controle por perfil
- Auditoria
- Consulta pública
- Extração de metadados
- Edição de anexos
- Versionamento

---

# 2. Criação da WBS (Work Breakdown Structure)

A WBS é a espinha dorsal do Bottom-Up.

Ela divide o projeto em componentes hierárquicos.

Exemplo simplificado:

```text
1. Infraestrutura
   1.1 PostgreSQL
   1.2 Docker
   1.3 CI/CD

2. Backend
   2.1 Autenticação
   2.2 Autorização
   2.3 Documentos
   2.4 Busca

3. Frontend
   3.1 Tela de login
   3.2 Consulta pública
   3.3 Upload

4. OCR
   4.1 Pipeline OCR
   4.2 Indexação

5. Testes
   5.1 Unitários
   5.2 Integração
```

---

# 3. Decomposição até unidades estimáveis

Cada item precisa ser:
- pequeno
- verificável
- implementável
- testável
- independente

Regra prática:
- task ideal = entre 2h e 16h
- acima disso → decompor novamente

---

# Exemplo REAL de decomposição técnica

## Feature: Upload de PDF

### Tasks

| Task | Horas |
|---|---|
| Criar endpoint upload | 3h |
| Validar MIME type | 1h |
| Salvar em storage | 2h |
| Persistir metadados | 2h |
| Implementar hash SHA256 | 1h |
| Criar DTOs | 1h |
| Criar migration | 1h |
| Tratar exceptions | 2h |
| Logging estruturado | 1h |
| Testes unitários | 3h |
| Testes integração | 4h |

Subtotal:
```text
21h
```

---

# 4. Definição da unidade de estimativa

Pode ser:

| Unidade | Uso |
|---|---|
| Horas | Mais comum |
| Dias ideais | Consultorias |
| Story points | Scrum |
| T-shirt sizing | Pré-venda |
| Complexidade relativa | Discovery |

Bottom-Up clássico geralmente usa:
- horas ideais
- homem-hora

---

# 5. Técnicas usadas dentro do Bottom-Up

## Analogous Estimation

Comparar com tarefa semelhante.

---

## Three Point Estimation (PERT)

Estimativa:
- otimista
- provável
- pessimista

Fórmula:

```math
E = (O + 4M + P) / 6
```

Onde:
- O = Optimistic
- M = Most Likely
- P = Pessimistic

Exemplo:

| Tipo | Horas |
|---|---|
| O | 4 |
| M | 8 |
| P | 20 |

Resultado:

```math
E = (4 + 4(8) + 20) / 6 = 9.33
```

---

## Planning Poker

Muito usado em Scrum.

Cada desenvolvedor:
- estima individualmente
- discute divergências
- converge

---

## Wideband Delphi

Versão mais formal do Planning Poker.

Muito usada em:
- engenharia
- contratos
- enterprise

---

# 6. Aplicação de fatores técnicos

A soma bruta raramente é usada diretamente.

São adicionados multiplicadores.

## Fatores comuns

| Fator | Impacto |
|---|---|
| Complexidade técnica | +10% a +50% |
| Débito técnico | +15% |
| Integrações externas | +20% |
| Dependência de terceiros | +10% |
| Curva de aprendizado | +15% |
| Requisitos instáveis | +30% |
| Equipe júnior | +25% |
| Ambiente legado | +40% |

---

# 7. Overhead operacional

Software não é apenas codar.

## Overheads típicos

| Item | Percentual |
|---|---|
| Reuniões | 10% |
| Code review | 10% |
| QA | 15% |
| DevOps | 5% |
| Refinamento | 5% |
| Gestão | 10% |

---

# 8. Contingência

Estimativa madura SEMPRE possui contingência.

## Contingência técnica

Normalmente:
- 10% a 30%

Projetos enterprise:
- até 50%

---

# Fórmula consolidada

```math
T = (Σ Tasks) × F_complexidade × F_overhead + Contingencia
```

---

# Exemplo completo

## Soma das tasks

```text
420h
```

## Complexidade

```text
+20%
```

Resultado:
```text
504h
```

## Overhead operacional

```text
+15%
```

Resultado:
```text
579.6h
```

## Contingência

```text
+20%
```

Resultado final:
```text
~700 horas
```

---

# Conversão para prazo

## Fórmula

```math
Prazo = HorasTotais / CapacidadeDaEquipe
```

## Exemplo

Equipe:
- 2 devs
- 6h úteis reais/dia

Capacidade:
```text
12h/dia
```

Prazo:
```text
700 / 12 = 58 dias úteis
```

---

# Capacidade real da equipe

Erro clássico:
usar 8h/dia.

Na prática:

| Tipo | Horas reais |
|---|---|
| Senior | 5h–6h |
| Pleno | 4h–5h |
| Júnior | 3h–4h |

Restante:
- reuniões
- contexto
- suporte
- interrupções

---

# Bottom-Up em Scrum

No Scrum normalmente ocorre:

```text
Epic
 → Story
    → Tasks
```

As stories recebem:
- story points

As tasks:
- horas

---

# Relação com Velocity

Exemplo:

Velocity média:
```text
40 pontos/sprint
```

Projeto:
```text
200 pontos
```

Resultado:
```text
5 sprints
```

---

# Bottom-Up híbrido

Empresas maduras usam:

| Fase | Técnica |
|---|---|
| Pré-venda | Top-down |
| Discovery | T-shirt |
| Planejamento | Bottom-Up |
| Sprint | Planning Poker |

---

# Precisão do Bottom-Up

## Vantagens

| Benefício | Motivo |
|---|---|
| Alta precisão | Granularidade |
| Melhor controle | Visibilidade |
| Melhor rastreabilidade | Tasks explícitas |
| Melhor gestão de risco | Dependências claras |
| Melhor orçamento | Custos detalhados |

---

## Desvantagens

| Problema | Motivo |
|---|---|
| Muito caro | Alto esforço |
| Demorado | Exige decomposição |
| Pode gerar falsa precisão | Horas parecem exatas |
| Requer maturidade técnica | Precisa conhecer arquitetura |
| Sofre com requisitos instáveis | Reestimativas constantes |

---

# Erros clássicos

## Não decompor suficiente

Ruim:
```text
“Implementar backend” → 80h
```

Bom:
```text
JWT → 6h
Refresh Token → 4h
RBAC → 8h
```

---

## Ignorar testes

Teste frequentemente representa:
- 20% a 40% do esforço

---

## Ignorar bugs

Projetos reais sempre possuem:
- retrabalho
- estabilização
- correções

---

## Não considerar integração

Integração costuma ser:
- altamente imprevisível

---

# Como empresas maduras fazem

Grandes empresas normalmente possuem:
- histórico de produtividade
- baseline histórica
- métricas DORA
- throughput
- lead time
- cycle time
- coeficientes por stack

Exemplo:

```text
CRUD simples .NET + PostgreSQL:
~6h por endpoint
```

---

# Bottom-Up em contratos de software

Muito usado em:
- licitações
- fábrica de software
- escopo fechado

Porque permite:
- rastreabilidade
- auditoria
- justificativa de custo

---

# Ferramentas usadas

## Gestão

- Jira
- Azure DevOps
- ClickUp
- Linear

---

## Estimativa

- Planning Poker
- Monte Carlo
- PERT
- WSJF
- Story Mapping

---

# Bottom-Up vs Top-Down

| Aspecto | Bottom-Up | Top-Down |
|---|---|---|
| Precisão | Alta | Média |
| Velocidade | Baixa | Alta |
| Custo da estimativa | Alto | Baixo |
| Necessita detalhes | Sim | Não |
| Bom para | Execução | Pré-venda |
| Risco | Menor | Maior |

---

# Bottom-Up moderno com IA

Hoje algumas empresas usam IA para:
- decomposição automática
- previsão por histórico
- análise de backlog
- detecção de risco
- previsão probabilística
- geração automática de WBS

Mas ainda existe forte dependência de:
- contexto arquitetural
- experiência humana
- conhecimento do domínio

Porque o principal problema da estimativa não é matemática:
é incerteza de requisitos.
