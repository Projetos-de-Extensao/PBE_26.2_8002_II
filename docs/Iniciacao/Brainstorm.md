---
id: brainstorm
title: Brainstorm
---

## Introdução

O brainstorm é uma técnica de elicitação de requisitos utilizada para levantar ideias, necessidades e possibilidades antes da definição formal do sistema. Nesta etapa, a equipe é incentivada a explorar diferentes alternativas para o problema, sem transformar toda ideia em requisito obrigatório.

Este documento registra as ideias iniciais para um sistema de gestão de uma academia de futebol de alta performance voltada para crianças de 7 a 12 anos. O sistema deverá apoiar a rotina dos responsáveis, profissionais e administradores, com atenção especial à segurança dos menores, à organização dos treinamentos e ao controle das regras de negócio.

## Metodologia

A equipe analisou os problemas identificados no Design Thinking e no 5W2H e organizou uma sessão de levantamento orientada por perguntas. As ideias foram agrupadas por tema para facilitar a futura modelagem do backend em Python/Django.

Durante o brainstorm, foram considerados os seguintes perfis:

- **Responsável**: cria e gerencia sua conta, cadastra dependentes e realiza agendamentos.
- **Profissional**: consulta sua agenda, acompanha as turmas e registra informações do treinamento.
- **Administrador ou recepção**: gerencia cadastros, horários, profissionais, campos, turmas e conflitos operacionais.

As ideias abaixo são hipóteses iniciais. Elas ainda deverão ser refinadas, validadas com os usuários e priorizadas antes de serem convertidas em requisitos, casos de uso e regras de negócio definitivos.

## Brainstorm

### Versão 1.0

## Perguntas e ideias levantadas

### 1. Qual é o objetivo principal da aplicação?

- Centralizar a gestão diária da academia em uma única aplicação.
- Permitir o controle de responsáveis, alunos, profissionais, campos, turmas e treinamentos.
- Reduzir o uso de planilhas, mensagens dispersas e controles manuais.
- Evitar conflitos de horário entre aluno, profissional, turma e campo.
- Aplicar automaticamente regras como faixa etária, capacidade máxima e disponibilidade.
- Oferecer uma experiência simples e segura para os responsáveis, sem retirar da administração o controle operacional.
- Apoiar o acompanhamento da frequência e da evolução física e técnica dos atletas.

### 2. Como será criado o acesso de um usuário?

- O responsável poderá criar uma conta informando dados pessoais, contato e credenciais de acesso.
- O cadastro deverá exigir confirmação de dados e aceite dos termos de uso e da política de privacidade.
- O usuário poderá entrar e sair do sistema com segurança e solicitar a recuperação de senha.
- A administração poderá cadastrar ou ativar contas de profissionais e conceder permissões conforme o perfil.
- O sistema deverá separar as permissões de administradores, profissionais e responsáveis.
- Um responsável deverá visualizar apenas seus próprios dados e os dados dos dependentes vinculados a ele.
- A aplicação deverá registrar alterações relevantes, como criação, edição e cancelamento de agendamentos.

### 3. Como será cadastrado um aluno?

- O responsável poderá cadastrar um ou mais dependentes, como irmãos, em sua própria conta.
- O cadastro deverá conter nome, data de nascimento, informações de contato e dados necessários para atendimento.
- O aluno deverá estar obrigatoriamente vinculado a pelo menos um responsável legal.
- A idade deverá ser validada automaticamente para confirmar a compatibilidade com o público da academia, de 7 a 12 anos.
- Poderão ser registradas informações de saúde, restrições e autorizações necessárias para a prática esportiva, com acesso restrito.
- A administração poderá alterar a situação do aluno, como ativo, afastado ou inativo.
- O responsável poderá solicitar a atualização de dados, enquanto a administração poderá revisar informações sensíveis.

### 4. Como serão cadastrados profissionais, campos e turmas?

- A administração poderá cadastrar profissionais, especialidades e formas de contato institucionais.
- Cada profissional poderá informar ou receber uma grade de disponibilidade.
- A administração poderá cadastrar campos, salas ou espaços de treinamento e suas capacidades.
- Cada turma poderá possuir modalidade, faixa etária, duração, capacidade máxima, local e profissional responsável.
- O sistema deverá impedir a criação de horários incompatíveis para o mesmo profissional ou espaço.
- Poderão existir turmas específicas, como iniciação, técnica, goleiro, preparação física e treinamento tático.
- A administração poderá suspender um profissional, espaço ou turma sem apagar o histórico de treinamentos realizados.

### 5. Como funcionará o agendamento de um treinamento?

- O responsável selecionará o aluno, a data, o horário e uma turma ou profissional disponível.
- O sistema deverá exibir somente opções compatíveis com a idade do aluno e sua situação cadastral.
- Antes de confirmar, a aplicação deverá verificar a disponibilidade do aluno, do profissional, do espaço e da turma.
- O sistema deverá bloquear novos agendamentos quando a turma atingir sua capacidade máxima.
- A confirmação deverá apresentar ao responsável os dados do treinamento, incluindo data, horário, local e profissional.
- O agendamento poderá ser realizado pelo responsável ou pela recepção, respeitando as mesmas regras de validação.
- O sistema deverá evitar registros duplicados para o mesmo aluno no mesmo horário.
- O responsável deverá consultar uma agenda dos próximos treinamentos de cada dependente.

### 6. Como serão tratados cancelamentos e reagendamentos?

- O responsável poderá cancelar um agendamento dentro do prazo definido pela academia.
- O sistema deverá informar claramente o prazo limite para cancelamento.
- Cancelamentos próximos ao horário do treino poderão ser bloqueados ou exigir autorização da administração.
- Quando um agendamento for cancelado, a vaga deverá ser liberada para a turma.
- O responsável poderá solicitar ou realizar um reagendamento para outro horário disponível.
- A administração poderá cancelar um treinamento por motivos operacionais, como ausência do profissional ou indisponibilidade do campo.
- Em caso de cancelamento pela academia, os usuários afetados deverão ser identificados para posterior comunicação.
- O histórico deverá manter o status do agendamento e o responsável pela alteração.

### 7. Que informações estarão disponíveis para cada perfil?

| Perfil        | Informações e ações possíveis                                                                                     |
| ------------- | ----------------------------------------------------------------------------------------------------------------- |
| Responsável   | Dados dos dependentes, agenda, status dos agendamentos, regras de cancelamento e comunicados da academia.         |
| Profissional  | Agenda individual, turmas atribuídas, lista de alunos, presença e avaliações permitidas.                          |
| Administração | Cadastros, ocupação das turmas, disponibilidade dos profissionais, campos, conflitos, cancelamentos e relatórios. |

O sistema deverá aplicar o princípio do menor privilégio: cada perfil acessa somente as informações necessárias para sua função. Dados de menores, informações de saúde e histórico de evolução deverão receber proteção adicional.

### 8. Como será o acompanhamento dos treinamentos?

- O profissional poderá visualizar a lista de alunos esperados em cada treinamento.
- Poderá ser registrada a presença, ausência ou justificativa do aluno.
- O profissional poderá registrar observações e avaliações físicas ou técnicas autorizadas.
- O responsável poderá consultar a evolução de seus dependentes, sem acessar dados de outras crianças.
- A administração poderá consultar históricos para acompanhar a operação e apoiar decisões.
- O sistema deverá preservar versões ou registros das alterações importantes para garantir rastreabilidade.

### 9. Como será feita a comunicação?

- O responsável deverá receber uma confirmação após a criação ou alteração de um agendamento.
- O profissional deverá ser avisado quando houver inclusão ou remoção de aluno em sua turma.
- A administração poderá publicar comunicados para uma turma, um grupo de usuários ou toda a academia.
- Cancelamentos de treinamentos deverão gerar avisos para os responsáveis e profissionais afetados.
- A primeira versão poderá utilizar notificações internas; e-mail ou SMS poderão ser avaliados em versões futuras.

### 10. Quais informações seriam úteis para a administração?

- Quantidade de vagas ocupadas e disponíveis por turma.
- Agenda diária dos campos e profissionais.
- Lista de treinamentos do dia e alunos esperados.
- Indicadores de faltas, cancelamentos e reagendamentos.
- Alertas para conflitos, turmas lotadas e profissionais sem disponibilidade.
- Visão de alunos ativos, afastados e inativos.
- Relatórios básicos para apoiar a gestão, sem transformar o brainstorm em uma definição fechada de escopo.

## Organização inicial das ideias

As ideias levantadas foram agrupadas nos seguintes módulos para orientar a próxima etapa de análise:

```text
Sistema de Gestão da Academia
|
|-- Autenticação e permissões
|   |-- Contas e recuperação de senha
|   |-- Perfis de acesso
|   `-- Privacidade e auditoria
|
|-- Cadastros
|   |-- Responsáveis
|   |-- Alunos e dependentes
|   |-- Profissionais
|   |-- Campos e espaços
|   `-- Turmas
|
|-- Operação
|   |-- Disponibilidade
|   |-- Agendamentos
|   |-- Validação de idade e capacidade
|   |-- Cancelamentos e reagendamentos
|   `-- Lista de espera
|
|-- Acompanhamento
|   |-- Presença
|   |-- Avaliações físicas e técnicas
|   `-- Histórico do atleta
|
`-- Comunicação e gestão
   |-- Notificações
   |-- Dashboard operacional
   `-- Relatórios
```

## Priorização inicial

Esta priorização é uma hipótese para o MVP e deverá ser revisada após a análise de viabilidade e a definição dos requisitos.

| Prioridade | Critério                                  | Funcionalidades sugeridas                                                                                                                                                                                    |
| ---------- | ----------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Alta**   | Essencial para validar o problema central | Criar conta e autenticar; cadastrar responsável e aluno; vincular dependentes; cadastrar turmas e profissionais; agendar com validação de idade, disponibilidade e vagas; consultar e cancelar agendamentos. |
| **Média**  | Melhora a operação e agrega valor         | Cadastro de campos; agenda do profissional; lista de presença; reagendamento; notificações internas; dashboard de lotação; histórico básico do atleta.                                                       |
| **Baixa**  | Complementar ou dependente de integrações | Fila de espera automática; integração financeira; bloqueio por inadimplência; notificações por e-mail ou SMS; relatórios avançados e indicadores de desempenho.                                              |

## Possíveis regras de negócio para validação futura

As regras abaixo foram identificadas durante o levantamento, mas ainda precisam ser detalhadas:

- Um aluno deve possuir pelo menos um responsável vinculado.
- Somente alunos dentro da faixa etária definida poderão ser associados às turmas correspondentes.
- Um treinamento não poderá ultrapassar a capacidade máxima do espaço ou da turma.
- Um profissional não poderá possuir dois treinamentos conflitantes.
- Um aluno não poderá possuir dois agendamentos no mesmo horário.
- O cancelamento deverá respeitar o prazo definido pela academia.
- Alterações relevantes deverão manter histórico e identificar o usuário responsável.
- Cada perfil deverá acessar apenas os dados autorizados para sua função.

## Conclusão

O brainstorm ampliou e organizou as possibilidades para o sistema de gestão da academia, partindo das principais dores identificadas: controles manuais, conflitos de agenda, superlotação, falhas de comunicação e proteção de dados de menores.

O levantamento indica que o núcleo do sistema está no vínculo entre responsável e aluno e no agendamento validado de treinamentos. As demais ideias poderão ser desenvolvidas de forma incremental, conforme a prioridade, a capacidade da equipe e a validação com os usuários. Na próxima etapa, as possibilidades deverão ser refinadas em requisitos funcionais e não funcionais, casos de uso e regras de negócio.

## Referências bibliográficas

- BARBOSA, S. D. J.; DA SILVA, B. S. _Interação humano-computador_. Elsevier, 2010.
- Documentos do projeto: [Design Thinking](design_thinking.md) e [5W2H](5w2h.md).

## Autores

| Data       | Versão | Descrição                                                                            | Autores                                                        |
| ---------- | ------ | ------------------------------------------------------------------------------------ | -------------------------------------------------------------- |
| 10/09/2026 | 1.0    | Substituição do modelo e consolidação do brainstorm da academia de futebol infantil. | Luiz Fernando, Giovanna Sales, Victor Coutinho e Ricardo Costa |
