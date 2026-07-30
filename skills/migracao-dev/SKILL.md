---
name: migracao-dev
description: Skill para planejar e executar migração de aplicações entre tecnologias, preservando regras de negócio, experiência do usuário e qualidade. Use quando houver migração de framework, linguagem, plataforma, arquitetura ou stack. Esta skill pode ser invoca utilizando as palavras como 'migre a pagina', ' migra a funcionalidade', 'migração' e combinações semelhantes.
---

# migracao-dev

Esta skill orienta migrações de software de uma tecnologia para outra com foco em previsibilidade, baixo risco e rastreabilidade.

## Quando usar

Use esta skill quando a solicitação envolver:

- migração de framework (ex.: Blazor para Angular, AngularJS para Angular, jQuery para React);
- migração de linguagem/runtime (ex.: .NET Framework para .NET 8, Node 14 para Node 20);
- migração de arquitetura (monólito para modular/microserviços, SSR para SPA);
- atualização tecnológica com impacto funcional, visual ou de integração.

Palavras-chave úteis: `migração`, `portabilidade`, `modernização`, `reescrita`, `paridade funcional`, `legado`, `upgrade de stack`.

## Objetivo

Garantir que a aplicação migrada mantenha:

1. 100% de fidelidade funcional com o sistema legado;
2. 100% de fidelidade visual/comportamental quando aplicável;
3. segurança, acessibilidade e performance mínimas aceitáveis;
4. documentação de requisitos, decisões e validações.

## Fluxo recomendado

1. **Inventário do legado**
   - mapear telas, fluxos, regras de negócio, integrações e contratos.
2. **Definição de escopo da onda**
   - selecionar funcionalidades por prioridade e risco.
3. **Critérios de equivalência**
   - definir critérios objetivos de “migrado com sucesso” (UI, comportamento, APIs, erros, auditoria).
4. **Plano técnico de migração**
   - decidir estratégia (incremental, estrangulamento, big-bang controlado, dual-run).
5. **Implementação orientada a testes**
   - criar/ajustar testes unitários e E2E para validar paridade.
6. **Validação e evidências**
   - executar validações funcionais, visuais e não-funcionais; registrar evidências.
7. **Documentação e handoff**
   - registrar requisitos, decisões técnicas, riscos, pendências e próximos passos.

## Regras de execução

- Não alterar sistema legado fora do escopo permitido.
- Evitar refatorações “extra” que não contribuam para a migração da onda.
- Manter rastreabilidade entre requisito, implementação e teste.
- Em caso de ambiguidade, priorizar a interpretação mais simples e aderente ao legado.
- Ao migrar uma página, realizar investigação prévia completa do original e manter fielmente: itens de tela, componentes, redirecionamentos, validações, formatos, máscaras e posicionamento.
- A expectativa desta skill é 100% de fidelidade do item migrado; qualquer diferença só é aceita quando expressamente requisitada pelo usuário.
- Sempre utilizar as mesmas cores do sistema original. Em caso de divergência, questionar o usuário antes de implementar a mudança.
- Quando houver ajuste visual aprovado, atualizar também o arquivo de design e os artefatos de padrão visual aplicáveis.
- Toda interação com o usuário durante a execução da migração deve ocorrer por meio de handoff.
- Quando necessário para contemplar a demanda com qualidade, utilizar skills e agents auxiliares apropriados.

## Checklist de conclusão da onda

- [ ] Funcionalidade migrada com paridade comprovada.
- [ ] Funcionalidade migrada com 100% de fidelidade comprovada em relação ao original.
- [ ] Investigação da página original concluída e registrada antes da implementação.
- [ ] Itens, componentes, redirecionamentos, validações, formatos, máscaras e posicionamento mantidos fiéis ao original.
- [ ] Cores validadas com o original; divergências tratadas com questionamento explícito ao usuário.
- [ ] Arquivos de design e padrão visual atualizados quando necessário.
- [ ] Skills e agents auxiliares utilizados quando necessário para garantir completude e qualidade da entrega.
- [ ] Testes automatizados relevantes passando.
- [ ] Diferenças intencionais documentadas e aprovadas.
- [ ] Qualquer diferença aplicada foi expressamente requisitada pelo usuário e devidamente registrada.
- [ ] Riscos residuais registrados com plano de mitigação.
- [ ] Documentação da onda atualizada nos artefatos oficiais.
- [ ] Handoffs realizados e registrados nas interações com o usuário.

## Exemplo de uso

**Entrada:** “Migrar tela de cadastro de usuários de Blazor para Angular.”

**Saída esperada com esta skill:**

- mapeamento da tela e regras do legado;
- implementação equivalente na nova stack;
- testes unitários e E2E de paridade;
- documentação técnica e funcional da onda.
