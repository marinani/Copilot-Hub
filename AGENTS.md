# AGENTS

Este arquivo serve como o manual de instruções mestre para todos os agentes de IA que operam neste repositório. O objetivo é garantir consistência, rastreabilidade e alta performance no desenvolvimento.

## Workflow Obrigatório 🚦

Além das diretrizes anteriores, o agente deve cumprir **obrigatoriamente** a seguinte sequência toda vez que for acionado por uma demanda:

1. **Leia a documentação inicial**: abra e estude o `README.md`, `copilot-instructions.md` e qualquer outro documento referenciado ou citado nesses arquivos.
2. **Entenda a demanda**: analise cuidadosamente o pedido do usuário. Se houver ambiguidade ou falta de informações, solicite esclarecimentos antes de prosseguir.
3. **Planeje o trabalho**: defina lotes, ondas e separação (ou transição para waveless) conforme necessário.
   * **Obrigatório**: sempre que disponível, utilize a **skill `copilot-planning`** para criar e validar o plano de execução.
4. **Documente o plano**: crie a documentação de requisitos, classe, fluxo, etc... dentro de `documentacao/`.
   * **Obrigatório**: sempre que disponível, utilize a **skill `documentacao-de-software`** para gerar, revisar ou atualizar qualquer documentação.
5. **Execute e valide**: assegure que todos os itens do checklist sejam executados.
6. **Compile sem erros**: garanta que a aplicação realiza **build completo sem falhas**. É inaceitável deixar a solução num estado que não compile.
7. **Resuma as operações**: ao finalizar, apresente um resumo claro das ações realizadas e dos resultados obtidos.

## 1. Diretrizes de Início e Contexto

* **Leitura Obrigatória do README:** Antes de iniciar qualquer tarefa, o agente deve ler o arquivo README.md na raiz para entender o contexto do projeto, a arquitetura e as tecnologias utilizadas.

* **Colaboração entre Agentes:** Deve haver colaboração total entre todos os agentes disponíveis no workspace. Agentes especialistas (ex: @test-agent, @lint-agent) devem ser acionados conforme sua função para garantir a qualidade da entrega.

* **Documentação de Requisitos:** A criação ou atualização de qualquer documento de requisitos (especialmente no diretório docs/requisitos) é exclusiva do agente writer.
  * **Obrigatório**: quando for para documentar requisito, deve-se utilizar a **skill `documentacao-de-software`** (se disponível).
  * Outros agentes podem ler e referenciar esses documentos, mas não devem editá-los diretamente.

## 2. Comunicação e Esclarecimento de Dúvidas

Para evitar erros por suposições incorretas, o agente deve seguir este protocolo:

* **Questionamento Progressivo:** Se uma demanda for ambígua ou faltarem informações, o agente deve pedir esclarecimentos ao usuário.

* **Uma por vez:** As perguntas devem ser feitas de forma individual e progressiva. O agente deve aguardar a resposta do usuário antes de formular a pergunta seguinte.

## 3. Resolução de Conflitos e Precedência

* **Regra de Proximidade:** Em casos de instruções conflitantes, o arquivo AGENTS.md mais próximo do arquivo que está sendo editado na estrutura de pastas tem precedência.
* **Soberania do Usuário:** Instruções diretas via chat pelo usuário anulam e sobrepõem qualquer diretriz contida neste arquivo ou no README.

## 5. Validação Técnica

Ao concluir um checklist, o agente deve:

* Executar comandos de validação (ex: npm test, pytest)
* Investigar a aplicação para garantir que todas as alterações funcionam conforme o esperado antes de declarar o lote como finalizado
