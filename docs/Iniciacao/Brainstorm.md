---
id: brainstorm
title: Brainstorm
---

## Introdução

O brainstorm é uma técnica de elicitação de requisitos utilizada para levantar ideias, necessidades e possibilidades antes da definição formal do sistema. Nesta etapa, a equipe é incentivada a explorar diferentes alternativas para o problema, sem transformar toda ideia em requisito obrigatório.

Este documento registra as ideias iniciais para um sistema de gestão de uma academia de alta performance voltada para crianças de 7 a 12 anos. O sistema deverá apoiar a rotina dos responsáveis e profissionais, com atenção especial à segurança dos menores, à organização dos agendamentos e ao controle das regras de negócio.

## Metodologia

A equipe analisou os problemas identificados no Design Thinking e no 5W2H e organizou uma sessão de levantamento orientada por perguntas. As ideias foram agrupadas por tema para facilitar a futura modelagem do backend em Python/Django.

Durante o brainstorm, foram considerados os seguintes perfis:

- **Responsável**: cria e gerencia sua conta, cadastra dependentes e realiza agendamentos.
- **Profissional**: consulta sua agenda e registra o resultado do treinamento (presença, observações e avaliações).

As ideias abaixo foram refinadas e várias delas já foram implementadas na API do projeto. Cada seção indica o que foi concretizado.

## Brainstorm

### Versão 2.0

## Perguntas e ideias levantadas

### 1. Qual é o objetivo principal da aplicação?

- Centralizar a gestão diária da academia em uma única aplicação. **(Implementado)**
- Permitir o controle de responsáveis, alunos, profissionais, serviços, salas e treinamentos. **(Implementado)**
- Evitar conflitos de horário e superlotação das salas. **(Implementado via capacidade da sala)**
- Aplicar automaticamente regras como faixa etária (7 a 12 anos) e disponibilidade. **(Implementado)**
- Oferecer uma experiência simples e segura para os responsáveis. **(Implementado)**

### 2. Como será criado o acesso de um usuário?

- O usuário cria a conta informando username, e-mail e senha (mínimo de 8 caracteres). **(Implementado — `POST /api/auth/register/`)**
- O usuário entra com autenticação por token e encerra a sessão invalidando o token. **(Implementado — `POST /api/auth/token/` e `POST /api/auth/logout/`)**
- Um responsável visualiza apenas seus próprios dados e os dados dos dependentes vinculados a ele. **(Implementado — filtragem por `perfil_responsavel`)**

### 3. Como será cadastrado um aluno?

- O responsável cadastra um ou mais dependentes em sua própria conta. **(Implementado)**
- O cadastro contém nome, data de nascimento e o responsável é atribuído automaticamente. **(Implementado)**
- A idade é validada automaticamente: a academia atende exclusivamente crianças de 7 a 12 anos. **(Implementado — `clean()` do modelo `Aluno`)**
- Cada aluno recebe uma matrícula única gerada automaticamente, no formato `ALU-<ano>-<código>`. **(Implementado)**
- O aluno possui situação cadastral: ativo ou inativo. **(Implementado)**

### 4. Como serão cadastrados profissionais, serviços e salas?

- O profissional se cadastra informando nome e ocupação (o tipo de serviço que oferece), e o sistema valida que ele não possui cadastro duplicado. **(Implementado)**
- Cada profissional recebe um código único gerado automaticamente, no formato `PRO-<ano>-<código>`. **(Implementado)**
- A disponibilidade do profissional é registrada como "disponível" ou "indisponível". **(Implementado)**
- O administrador cadastra as salas com nome e capacidade; as salas previstas são: Área de Treinamento Funcional e Gramado Sintético, Laboratório de Avaliação Física, Consultório de Nutrição Esportiva e Espaço de Fisioterapia e Recovery. **(Implementado)**
- Os serviços (Nutrição Esportiva, Fisioterapia, Recuperação Muscular, Preparação Física, Treinamento Funcional e Avaliação de Performance) são gerenciados pela administração e cada serviço define em qual sala acontece. **(Implementado — consulta via API; escrita pelo Django Admin)**

> Nota: a versão anterior deste documento previa o cadastro de **turmas** (modalidade, faixa etária, capacidade). Essa abordagem foi descartada: o sistema atual trabalha com **agendamentos individuais** de aluno por serviço, e o limite de pessoas é controlado pela **capacidade da sala**.

### 5. Como funcionará o agendamento de um treinamento?

- O responsável seleciona o aluno, o serviço, o profissional, a sala e a data/hora. **(Implementado)**
- O sistema verifica se a capacidade da sala no horário escolhido já foi atingida. **(Implementado)**
- Se a sala já estiver na capacidade máxima, o agendamento entra automaticamente em **fila de espera**, com posição calculada. **(Implementado — status `fila_espera` e campo `posicao_fila`)**
- O sistema só confirma o agendamento quando a sala tem vagas (status "ativo"). **(Implementado)**
- O responsável consulta a agenda dos próximos treinamentos de cada dependente. **(Implementado)**
- O agendamento só pode ser criado pelo responsável dos alunos envolvidos. **(Implementado — validação de permissão)**

### 6. Como serão tratados cancelamentos e reagendamentos?

- O responsável pode cancelar um agendamento, o que libera a vaga da sala. **(Implementado via alteração de status)**
- O histórico mantém a data de criação e o status atual do agendamento. **(Implementado — `criado_em` e `status`)**

### 7. Que informações estão disponíveis para cada perfil?

| Perfil       | Informações e ações possíveis                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Responsável  | Cadastro e consulta dos dependentes, criação e cancelamento de agendamentos, consulta da fila de espera e dos registros dos treinos dos próprios alunos. |
| Profissional | Cadastro próprio, consulta dos próprios serviços e agendamentos, criação de registros de treinamento dos seus agendamentos. |
| Administrador (staff) | Escrita sobre profissionais, salas, serviços e consulta de todos os dados (qualquer usuário autenticado pode consultar salas e serviços). |

O sistema aplica o princípio do menor privilégio: consulta é liberada para qualquer usuário autenticado, mas escrita é restrita ao dono do recurso ou ao administrador.

### 8. Como será o acompanhamento dos treinamentos?

- O profissional registra, para cada agendamento, a presença do aluno, observações e avaliações físicas e técnicas. **(Implementado — `RegistroTreinamento`, 1:1 com o agendamento)**
- O responsável consulta os registros de treinamento apenas dos seus dependentes. **(Implementado)**
- Apenas profissionais autenticados podem criar registros. **(Implementado — permissão dedicada)**

### 9. Como será feita a comunicação?

- A comunicação foi considerada fora do escopo do MVP atual. Notificações internas, e-mail e SMS ficam como evolução futura.

### 10. Quais informações seriam úteis para a administração?

- Quantidade de agendamentos ativos e em fila de espera por sala e horário. **(Possível via consulta da API)**
- Agenda diária dos profissionais.
- Indicadores de faltas e cancelamentos.
- Relatórios básicos para apoiar a gestão.

### 11. Pagamento

- A integração de pagamentos foi descartada do escopo do projeto. O sistema atual não cobrança, não registra transações e não consome API financeira.

## Organização das ideias (estado atual)

```text
Sistema de Gestão da Academia
|
|-- Autenticação e permissões
|   |-- Registro e login por token
|   |-- Logout com invalidação do token
|   `-- Controle por perfil (responsável, profissional, staff)
|
|-- Cadastros
|   |-- Responsáveis
|   |-- Alunos (matrícula automática, idade 7 a 12)
|   |-- Profissionais (código automático, ocupação, disponibilidade)
|   |-- Salas (nome e capacidade)
|   `-- Serviços (catálogo fixo, duração, sala correspondente)
|
|-- Operação
|   |-- Agendamentos (aluno, profissional, serviço, sala, data/hora)
|   |-- Validação de capacidade da sala
|   `-- Fila de espera automática com posição
|
`-- Acompanhamento
    |-- Registro de presença
    |-- Observações do treinador
    `-- Avaliações física e técnica
```

## Priorização

| Prioridade | Critério                                  | Funcionalidades                                                                                                                    |
| ---------- | ----------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Alta**   | Essencial para validar o problema central | Criar conta e autenticar; cadastrar responsável, aluno, profissional; agendar com validação de capacidade da sala; fila de espera. |
| **Média**  | Melhora a operação                        | Catálogo de serviços e salas pela administração; registros de treinamento com presença e avaliações.                                |
| **Baixa**  | Evolução futura                           | Notificações internas, relatórios avançados, dashboard operacional, pagamentos.                                                     |

## Regras de negócio implementadas

- Um aluno deve possuir um responsável vinculado.
- A academia atende exclusivamente alunos entre 7 e 12 anos.
- Matrícula do aluno e código do profissional são gerados automaticamente e são únicos.
- Um profissional não pode se cadastrar duas vezes com a mesma conta.
- Um agendamento deve estar vinculado obrigatoriamente a um serviço.
- Quando a capacidade da sala no horário é atingida, o agendamento entra em fila de espera em vez de ser recusado.
- Cada perfil acessa apenas os dados autorizados para sua função.

## Conclusão

O brainstorm ampliou e organizou as possibilidades para o sistema de gestão da academia, partindo das principais dores identificadas: controles manuais, conflitos de agenda e superlotação. Na versão atual, o núcleo implementado é o vínculo entre responsável e aluno, o agendamento individual por serviço com validação de capacidade da sala e a fila de espera automática. Evoluções como notificações, dashboard e integração financeira ficam para iterações futuras.

## Referências bibliográficas

- BARBOSA, S. D. J.; DA SILVA, B. S. _Interação humano-computador_. Elsevier, 2010.
- Documentos do projeto: [Design Thinking](design_thinking.md) e [5W2H](5w2h.md).

## Autores

| Data       | Versão | Descrição                                                                       | Autores                                                        |
| ---------- | ------ | ------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 10/09/2026 | 1.0    | Criação do brainstorm da academia de alta performance infantil.                 | Luiz Fernando, Giovanna Sales, Victor Coutinho e Ricardo Costa |
| 13/11/2026 | 2.0    | Reescrita para refletir o código implementado (agendamentos individuais, sem turmas e sem pagamentos). | Ricardo Costa                                    |
