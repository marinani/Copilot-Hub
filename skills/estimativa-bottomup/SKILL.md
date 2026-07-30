---
name: Estimativa de Alteração de Requisito (Bottom-Up) v2
description: "Gerar estimativa técnica para um ou mais requisitos, com validação de percentuais, suporte a múltiplos formatos de hora e geração de arquivo markdown."
---

# Skill: Estimativa de Alteração de Requisito (Bottom-Up) v2

## Objetivo

Gerar uma estimativa técnica para **um ou mais requisitos funcionais**, respeitando as regras da planilha `Estimativa-Bottom-Up-1.3.xlsx`, com validação de percentuais, suporte a múltiplos formatos de hora e geração de arquivo markdown.

## Formatos de Hora Suportados

- `hh:mm` → ex: `03:30` (3 horas e 30 minutos)
- `h` decimal → ex: `3.5`
- `X days, hh:mm` → ex: `2 days, 02:00` (50 horas)

## Estrutura do Arquivo Markdown

Deve ser utilizado o template `template.md` como estrutura obrigatória para a geração do arquivo de estimativa, preenchendo as seções conforme as informações fornecidas.

## Regras de Validação Automática

1. **Por requisito:** `Total Horas = EngRequisitos + Implementacao + Teste + Cientista`
2. **Por atividade (agregado):** `%Atividade = TotalHorasAtividade / TotalHorasRequisitos * 100`
3. **Limites:**
   - Engenharia Requisitos ≤ 40%
   - Implementação ≤ 75%
   - Teste ≤ 20%
   - Cientista Dados ≤ 10%
4. **Homologação e Implantação:** calculadas separadamente, aplicadas sobre o total de requisitos ou sobre valor informado explicitamente
5. **Se tipo = MELHORIA:** sugerir pesos menores para engenharia de requisitos (ex: 20% em vez de 40%)

## Comportamento Esperado

- **Múltiplos requisitos:** permite adicionar N linhas na tabela
- **Cálculo automático:** soma todas as linhas e gera os totais
- **Alerta visual:** `⚠️` quando percentual excede limite
- **Conversão automática:** converte `2 days, 02:00` para `50:00`
- **Geração do arquivo:** `estimativa-YYYY-MM-DD.md`

## Exemplo de Uso Avançado

> "Crie uma estimativa com 2 requisitos:
>
> 1. REQ001 - Manter Usuário (Melhoria) - 3h engenharia, 12h implementação, 3.5h teste
> 2. REQ012 - API Endereço (Novo) - 7h engenharia, 2 days, 2:00 implementação, 15h teste
>    Cliente: ABC, Sistema: Portal, Tecnologia: DotNet"

O skill deve:

- Converter `2 days, 02:00` para `50:00`
- Somar os dois requisitos
- Validar percentuais
- Gerar o markdown com duas linhas na tabela

```

---

## Resumo das Melhorias Propostas

| Lacuna                               | Melhoria                                |
|--------------------------------------|-----------------------------------------|
| Apenas um requisito                  | Suporte a múltiplos requisitos          |
| Homologação/implantação misturadas   | Seção separada com limites específicos  |
| Sem comparação com limites           | Coluna "Status" com ✅/⚠️              |
| Formato `2 days, 2:00:00`            | Conversão automática para horas         |
| Sem regras por tipo                  | Regras diferentes para MELHORIA vs NOVO |
| Sem validação de soma                | Validação por linha e total             |
| Faltava cientista de dados explícito | Coluna dedicada na tabela               |

---
```
