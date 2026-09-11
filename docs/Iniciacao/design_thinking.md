---
id: dt
title: Design Thinking
---

# Design Thinking

## 1. Capa

- **Título do projeto:** Sistema de Gestão para Academia de Futebol Infantil
- **Equipe:** Grupo 2 - Luiz Fernando, Giovanna Sales, Victor Coutinho, Ricardo Rocha

## 2. Introdução

### 2.1 Contexto do projeto

O projeto busca compreender as necessidades e dificuldades das pessoas envolvidas na rotina de uma academia de futebol de alta performance. A solução deverá considerar os diferentes perfis que participam da gestão, do agendamento e da realização dos treinamentos para crianças de 7 a 12 anos.

### 2.2 Objetivo

Espera-se que o sistema ofereça uma experiência simples, organizada e segura. A solução deverá reduzir os atritos na comunicação entre os responsáveis e a academia, automatizar regras de negócio, como idade e quantidade de vagas, e permitir que os treinadores se concentrem na evolução dos atletas.

### 2.3 Público-alvo

- Profissionais da academia;
- Responsáveis pelos alunos;
- Alunos e atletas;
- Equipe administrativa e de recepção.

### 2.4 Escopo inicial

O sistema deverá apoiar o cadastro de usuários, alunos e profissionais, o gerenciamento de turmas e espaços, o agendamento de treinamentos, o controle de disponibilidade, os cancelamentos e o acompanhamento básico dos atletas.

## 3. Fases do Design Thinking

### 3.1 Empatia

#### 3.1.1 Necessidades identificadas

Durante a análise do contexto, foram identificadas as seguintes necessidades:

- Centralizar as informações e o histórico dos atletas;
- Organizar os treinamentos com validação da faixa etária de 7 a 12 anos;
- Controlar a disponibilidade dos profissionais e o limite de vagas dos espaços;
- Facilitar o agendamento e o cancelamento por meio de autoatendimento para os responsáveis;
- Permitir uma consulta rápida das informações de evolução física e técnica;
- Reduzir erros operacionais, como a superlotação de turmas;
- Controlar adequadamente os acessos, garantindo que os responsáveis visualizem apenas seus dependentes e que os treinadores acessem apenas suas turmas;
- Proteger os dados pessoais e sensíveis de menores de idade.

#### 3.1.2 Principais dificuldades

- **Cancelamentos de última hora:** prejudicam o planejamento dos exercícios, pois o treinador organiza o treino para uma quantidade de atletas diferente da quantidade presente.
- **Agendamentos incorretos:** podem colocar uma criança de 7 anos em uma turma avançada destinada a atletas de 11 ou 12 anos.
- **Falhas de comunicação:** o profissional pode não ser avisado a tempo quando um aluno é adicionado ou removido de sua turma.
- **Dependência de processos manuais:** planilhas e mensagens descentralizadas dificultam a atualização das informações.
- **Acesso inadequado a dados:** informações pessoais, médicas ou financeiras podem ser visualizadas por pessoas sem autorização.

#### 3.1.3 Expectativas dos usuários

Espera-se que o sistema ofereça uma experiência simples, organizada e segura. A solução deverá reduzir o atrito na comunicação com a academia, automatizar as regras de idade e de vagas e fornecer aos treinadores informações confiáveis para o planejamento dos treinamentos.

### 3.2 Definição

#### 3.2.1 Problema identificado

A academia necessita de uma forma centralizada e confiável para administrar os processos relacionados a jovens atletas, responsáveis, treinadores e treinamentos. A dependência de controles manuais aumenta a possibilidade de conflitos de agenda, falhas de comunicação e erros que afetam a qualidade do serviço.

#### 3.2.2 Problema central

Como oferecer à academia de futebol uma gestão centralizada, segura e eficiente, garantindo que regras de negócio, como limite de vagas, adequação da faixa etária e prazo para cancelamento, sejam aplicadas automaticamente pelo sistema?

#### 3.2.3 Necessidades prioritárias

A solução deverá considerar principalmente:

- Gestão de alunos com vínculo obrigatório a um ou mais responsáveis;
- Controle de disponibilidade e lotação dos espaços de treinamento;
- Agendamento de treinamentos com validação das regras de negócio;
- Cancelamento e reagendamento com prazos definidos;
- Relatórios de evolução técnica e física;
- Indicadores operacionais e financeiros, quando aplicável;
- Proteção rigorosa dos dados pessoais e sensíveis.

#### 3.2.4 Objetivo da solução

Desenvolver um backend em Python e Django capaz de centralizar e organizar as principais operações da academia, proporcionando maior controle, segurança e eficiência. O sistema deverá funcionar como fonte confiável de informações para a operação diária.

### 3.3 Ideação

#### 3.3.1 Objetivo da ideação

Gerar e organizar possíveis soluções para os problemas identificados, traduzindo as necessidades dos usuários em módulos e funcionalidades que possam ser analisados e desenvolvidos posteriormente.

#### 3.3.2 Possíveis soluções

##### Gestão de usuários e segurança

- Utilizar a autenticação e a autorização nativas do Django;
- Organizar permissões por grupos, como administradores, treinadores e responsáveis;
- Proteger dados pessoais e sensíveis, considerando a aplicação da LGPD a menores de idade;
- Registrar alterações relevantes para manter uma trilha de auditoria.

##### Gestão de alunos e atletas

- Cadastrar o atleta infantil com validação da data de nascimento;
- Vincular cada aluno a um ou mais responsáveis legais;
- Controlar a situação do aluno, como ativo, afastado ou inativo;
- Registrar informações de evolução física e técnica;
- Consultar o histórico de treinamentos e a frequência do atleta.

##### Gestão de profissionais

- Cadastrar treinadores e suas especialidades;
- Controlar a disponibilidade e a grade de horários dos profissionais;
- Disponibilizar uma agenda individual para cada treinador;
- Associar profissionais às turmas e aos treinamentos correspondentes.

##### Gestão de treinamentos

- Permitir o agendamento de treinos com validação automática da faixa etária;
- Controlar o limite de vagas de cada turma ou espaço;
- Impedir conflitos de horário entre aluno, profissional e espaço;
- Permitir o cancelamento pelo responsável dentro do prazo estabelecido;
- Liberar a vaga quando um agendamento for cancelado;
- Enviar notificações sobre alterações no treinamento ou na turma;
- Avaliar a criação de uma fila de espera para turmas lotadas.

##### Administração

- Disponibilizar um dashboard com a lotação das turmas e a ocupação dos espaços;
- Gerenciar usuários, alunos, responsáveis, profissionais, espaços e turmas;
- Acompanhar cancelamentos, faltas e conflitos de agenda;
- Avaliar o controle de mensalidades e de inadimplência em uma etapa posterior.

#### 3.3.3 Priorização inicial

As funcionalidades prioritárias deverão começar pelo núcleo do negócio: cadastro de dependentes e agendamento com validação de idade, disponibilidade e vagas. Esse conjunto concentra os principais problemas operacionais identificados na academia e representa a base do MVP.

### 3.4 Prototipagem

Esta etapa será desenvolvida nas próximas iterações do projeto.

#### 3.4.1 Descrição do protótipo

Deverá ser descrito como as ideias serão transformadas em um protótipo, que poderá incluir fluxos de navegação, wireframes, telas da aplicação ou modelos de interação entre os perfis de usuário.

#### 3.4.2 Materiais utilizados

Deverão ser registrados os recursos utilizados para criar o protótipo, como ferramentas de prototipação, diagramas, modelos de dados e documentação dos fluxos.

#### 3.4.3 Testes realizados

Deverão ser descritos os cenários utilizados para avaliar o protótipo, especialmente cadastro de aluno, criação de agendamento, validação de vagas e cancelamento de treinamento.

### 3.5 Teste

Esta etapa será preenchida após a avaliação do protótipo com os usuários ou com representantes dos perfis identificados.

#### 3.5.1 Feedback dos usuários

Registrar as percepções dos responsáveis, profissionais e administradores sobre a clareza, a facilidade de uso e a adequação da solução.

#### 3.5.2 Ajustes realizados

Documentar as mudanças feitas com base nos problemas e nas sugestões identificados durante os testes.

#### 3.5.3 Resultados finais

Apresentar os resultados obtidos após os testes e indicar quais funcionalidades foram validadas, ajustadas ou adiadas.

## 4. Conclusão

### 4.1 Resultados obtidos

Até o momento, o Design Thinking permitiu identificar os principais usuários, necessidades, dificuldades e oportunidades de melhoria na rotina da academia.

### 4.2 Próximos passos

- Validar as ideias com os usuários e representantes da academia;
- Refinar os requisitos funcionais e não funcionais;
- Definir as regras de negócio do agendamento;
- Elaborar os protótipos das principais telas e fluxos;
- Modelar as entidades e os relacionamentos do sistema;
- Planejar a implementação do backend em Python e Django.

### 4.3 Aprendizados

O levantamento mostrou a importância de compreender os diferentes pontos de vista envolvidos na operação. Também evidenciou que regras como faixa etária, limite de vagas, disponibilidade e permissões de acesso devem ser consideradas desde o início para reduzir falhas e garantir a segurança dos usuários.

## 5. Anexos

Podem ser incluídos nesta seção:

- Mapas de empatia;
- Jornadas dos usuários;
- Fluxos de navegação;
- Esboços e protótipos;
- Registros de entrevistas ou reuniões;
- Tabelas, gráficos e outras evidências da pesquisa.

## 6. Orientações para evolução do documento

- Utilizar linguagem clara e objetiva;
- Manter a numeração das seções conforme a hierarquia do documento;
- Registrar as decisões e alterações realizadas a cada iteração;
- Diferenciar ideias levantadas, requisitos validados e funcionalidades implementadas;
- Incluir visualizações que ajudem a explicar os usuários, os processos e os fluxos do sistema;
- Atualizar o documento conforme o projeto avance pelas fases de prototipagem e teste.

Este documento poderá ser ajustado conforme as necessidades do projeto e da equipe. O mais importante é que ele registre o processo colaborativo e iterativo de compreensão do problema e construção da solução.
