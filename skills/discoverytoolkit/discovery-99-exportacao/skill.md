---
name: discovery-99-exportacao
description: Roteador de skills do grupo discovery-99-exportacao. Permite executar qualquer uma das funções do grupo (exportação HTML, exportação NotebookLM) individualmente ou ambas em sequência.
---

# Skill Router — discovery-99-exportacao

Este roteador permite:
- Executar **qualquer** das funções do grupo:
  - Exportação HTML (`discovery-99-html-export`)
  - Exportação NotebookLM (`discovery-notebooklm-export`)
- Executar **todas** as funções em sequência (pipeline): HTML → NotebookLM.

## Como usar

- Para rodar uma função específica, chame pelo nome da skill desejada.
- Para rodar ambas em sequência, use o comando:

```
Rode o pipeline discovery-99-exportacao completo
```

## Skills disponíveis

| Skill                        | Descrição resumida                                      |
|------------------------------|--------------------------------------------------------|
| discovery-99-html-export     | Exporta toda a documentação de discovery para HTML      |
| discovery-notebooklm-export  | Gera pacote concatenado por tema em discovery/notebooklm |

## Pipeline sugerido

1. **Exportação HTML**: Gera discovery/html/ com todos os arquivos convertidos
2. **Exportação NotebookLM**: Gera discovery/notebooklm/ com 5 arquivos temáticos concatenados + índice

---

> Consulte cada skill individual para detalhes de uso, parâmetros e restrições.
