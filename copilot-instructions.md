# Instruções do Copilot

Este arquivo define instruções e obrigatoriedades para o uso do Copilot e das skills dentro deste workspace.

## Regras obrigatórias

- É obrigatório o uso da **skill `documentacao-de-software`** para documentação de requisitos.
- É obrigatório o uso da **skill `redmine-implementation`** para obter os chamados presentes no Redmine.
- É obrigatório o uso da **skill `copilot-planning`** para planejamento de tarefas.

## Código e arquitetura

- Para código deve ser utilizado o princípio de **clean code**.
- O projeto deve seguir o princípio da **programação orientada a objetos** para evitar repetição de código.
- Deve usar as melhores práticas da linguagem e versão do projeto.
- Deve ser criada documentação XML para os métodos públicos. Se for necessário detalhar algo, use a tag `<remarks>`.
- Toda alteração deve garantir que o **build da aplicação ocorra sem erros**.

## Testes e Qualidade

- Todo código criado ou alterado deve ter **testes unitários** com cenários exploratórios (testar casos limites, erros esperados e fluxo feliz).
