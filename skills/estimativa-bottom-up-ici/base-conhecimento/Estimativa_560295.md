# Estimativa Bottom-Up: Requisição 560295

## Identificação da Estimativa

| Campo | Valor |
|-------|-------|
| **Cliente** | PMC |
| **Sistema** | Sigesguarda Pro |
| **Órgão** | SMDT |
| **Requisição/Ofício** | 560295 |
| **Identificador SGC** | 2076 |
| **Analista Responsável** | Matheus Campos |
| **Tecnologia** | DotNet |
| **Data da Estimativa** | 25/8/2025 |

---

## Escopo da Estimativa

Esta solicitação tem como objetivo implementar um controle de acesso diferenciado no Sigesguarda Pro, abrangendo a tela de monitoramento de ocorrências e demais módulos do sistema. Será criado o grupo SETRAN OPERADORES, com permissões semelhantes ao grupo Rádio Operadores, porém restrito ao tratamento de protocolos e ocorrências relacionadas a trânsito.
O sistema passará a filtrar automaticamente os acessos conforme o perfil do usuário: agentes da SETRAN visualizarão e tratarão apenas ocorrências do tipo TR, enquanto os agentes da GM terão acesso às ocorrências dos tipos GM e DC, incluindo também os protocolos de trânsito quando necessário. Supervisores da SETRAN terão permissões equivalentes aos Supervisores GM, mas limitados aos assuntos de sua área.
As regras de acesso serão aplicadas de forma unificada em todas as telas do sistema, incluindo relatórios, cadastros, controle de materiais, uniformes e escalas, garantindo segregação de responsabilidades. Administradores manterão acesso total sem restrições. A solução contemplará ajustes no backend, frontend e banco de dados, bem como testes de validação com usuários-chave.

---

## Tabela de Requisitos Funcionais

| Funcionalidade | Requisito | Tipo | Descrição da Funcionalidade | Eng. Requisitos (40%) | Arquitetura (40%) | Implementação (75%) | Teste (20%) | Cientista de Dados (10%) | **Total Horas** |
|---|---|---|---|---|---|---|---|---|---|
| Definir as permissões de acesso | - | Novo | Definir as permissões de acesso para usuários SETRAN, GM e Supervisores | 2:00 | 0:00 | 0:00 | 0:00 | 0:00 | **2:00** |
| Criação de perfis | - | Novo | Criação de grupos e permissões para os usuários | 0:00 | 0:00 | 2:00 | 0:00 | 0:00 | **2:00** |
| Regras de visualização dos protocolos 156 | - | Melhoria | Implementar lógica de filtragem dos protocolos (TR, GM, DC) de acordo com o perfil | 0:00 | 0:00 | 8:00 | 2:00 | 0:00 | **10:00** |
| Controle de ocorrências por tipo | - | Melhoria | Restringir abertura/edição/encerramento de ocorrências por perfil (TR, GM, DC) | 0:00 | 0:00 | 10:00 | 2:00 | 0:00 | **12:00** |
| Ajustar relatórios | - | Melhoria | Alterar todos os relatórios do sistema para passar a considerar a exibição por perfil. | 0:00 | 0:00 | 24:00 | 6:00 | 0:00 | **30:00** |
| Módulo de escalas | - | Melhoria | Implementar restrição no módulo de escalas | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de cursos | - | Melhoria | Implementar restrição no módulo de cursos | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de porte de armas | - | Melhoria | Implementar restrição no módulo de porte de armas | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de veículos | - | Melhoria | Implementar restrição no módulo de veículos | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de equipamentos | - | Melhoria | Implementar restrição no módulo de equipamentos | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de romaneio | - | Melhoria | Implementar restrição no módulo de romaneio | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de cautela | - | Melhoria | Implementar restrição no módulo de cautela | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de uniformes | - | Melhoria | Implementar restrição no módulo de uniformes | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de atividades | - | Melhoria | Implementar restrição no módulo de atividades | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de equipes | - | Melhoria | Implementar restrição no módulo de equipes | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de rádio comunicação | - | Melhoria | Implementar restrição no módulo de rádio comunicação | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de identidade funcional | - | Melhoria | Implementar restrição no módulo de identidade funcional | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de vistoria | - | Melhoria | Implementar restrição no módulo de vistoria | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de saturação | - | Melhoria | Implementar restrição no módulo de saturação | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |
| Módulo de visitantes | - | Melhoria | Implementar restrição no módulo de visitantes | 0:00 | 0:00 | 5:00 | 1:00 | 0:00 | **6:00** |

---

## Resumo de Horas

| Atividade | Total Horas | Distribuição |
|-----------|-------------|--------------|
| Eng. Requisitos (40%) | 2:00 | 1,37% |
| Arquitetura (40%) | 0:00 | 0,00% |
| Implementação (75%) | 119:00 | 81,51% |
| Teste (20%) | 25:00 | 17,12% |
| Cientista de Dados (10%) | 0:00 | 0,00% |
| **TOTAL ESTIMADO** | **146:00** | **100,00%** |
