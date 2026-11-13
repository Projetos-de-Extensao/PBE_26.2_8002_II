---
id: pesquisa
title: Pesquisa
---

# Pesquisa

## 1. Analisar Aplicações de Alocação de Eventos

### 1.1. Descrição

Núcleo central do sistema que gerencia a alocação de recursos (sala, profissional, aluno) em horários específicos, garantindo o respeito à capacidade das salas e às regras de negócio da academia.

### 1.2. Requisitos Funcionais

| ID     | Descrição                                                                                       | Prioridade |
| ------ | ----------------------------------------------------------------------------------------------- | ---------- |
| ALO-01 | Validar a capacidade da sala no horário desejado antes de confirmar o agendamento               | Must       |
| ALO-02 | Encaminhar automaticamente para fila de espera quando a sala atingir a capacidade no horário    | Must       |
| ALO-03 | Impedir que um responsável agende para aluno que não é seu dependente                           | Must       |
| ALO-04 | Liberar a capacidade da sala instantaneamente em caso de cancelamento                           | Must       |
| ALO-05 | Registrar a posição do aluno na fila de espera conforme a ordem de criação do agendamento       | Should     |
| ALO-06 | Sugerir os próximos horários livres cruzando a idade do aluno e o serviço                       | Could      |

### 1.3. Regras de Negócio Específicas

- **Controle por capacidade da sala:** o sistema conta os agendamentos ativos para a mesma sala e horário. Se a quantidade atingir a capacidade cadastrada da sala, o novo agendamento não é recusado: entra automaticamente em fila de espera.
- **Obrigatório vincular a um serviço:** todo agendamento deve indicar o serviço praticado; a associação serviço-sala orienta onde o treino acontece.
- **Idade do aluno:** o cadastro do aluno só é aceito entre 7 e 12 anos, validado automaticamente.

### 1.4. Estrutura de Dados e Relacionamentos

Cada agendamento conecta: **Aluno**, **Profissional**, **Serviço** e **Sala**, com data e hora e status (`ativo` ou `fila_espera`). O agendamento é criado pelo responsável do aluno e pode gerar no máximo um **Registro de Treinamento**.

## 2. Funcionalidades do Sistema

### 2.1 Calendário

#### 2.1.1 Descrição

Componente para visualização e manipulação dos agendamentos por data e hora, com operações de criação, consulta e cancelamento.

#### 2.1.2 Requisitos Funcionais

| ID     | Descrição                                                        | Prioridade |
| ------ | ---------------------------------------------------------------- | ---------- |
| CAL-01 | Visualizar a agenda dos dependentes por aluno                    | Must       |
| CAL-02 | Filtrar agendamentos por aluno, profissional, sala ou serviço    | Should     |
| CAL-03 | Criar e cancelar agendamentos                                    | Must       |
| CAL-04 | Consultar a posição na fila de espera do agendamento             | Should     |
| CAL-05 | Receber notificações (e-mail, push) sobre agendamentos           | Could      |

#### 2.1.3 Regras de Negócio Específicas

- Somente usuários autenticados podem operar a API (autenticação por token).
- Somente o responsável do aluno pode criar ou cancelar agendamentos dele.
- Cada responsável visualiza somente os agendamentos dos seus dependentes.

### 2.2 Salas (Espaços Físicos)

#### 2.2.1 Descrição

Gerenciamento dos espaços físicos da academia para controlar capacidade e disponibilidade.

#### 2.2.2 Requisitos Funcionais

| ID     | Descrição                                                                       | Prioridade |
| ------ | -------------------------------------------------------------------------------- | ---------- |
| SAL-01 | Cadastro de salas com nome e capacidade (executado pela administração)           | Must       |
| SAL-02 | Catálogo fixo de quatro espaços: treinamento funcional/gramado, laboratório de avaliação, consultório de nutrição e espaço de fisioterapia/recovery | Must |
| SAL-03 | Consulta das salas por qualquer usuário autenticado                              | Must       |
| SAL-04 | Relatório de ocupação de salas por período                                       | Could      |

#### 2.2.3 Regras de Negócio Específicas

- A capacidade da sala limita a quantidade de agendamentos ativos no mesmo horário.
- O excedente vai para a fila de espera vinculada à mesma sala e horário.
- Cada serviço do catálogo está associado à sala em que acontece.

### 2.3 Profissionais

#### 2.3.1 Descrição

Gestão de preparadores físicos, fisioterapeutas, nutricionistas e avaliadores, garantindo que cada criança seja atendida pelo profissional adequado ao serviço escolhido.

#### 2.3.2 Requisitos Funcionais

| ID     | Descrição                                                                           | Prioridade |
| ------ | ------------------------------------------------------------------------------------ | ---------- |
| PRF-01 | Cadastrar profissional com nome e ocupação (tipo de serviço)                          | Must       |
| PRF-02 | Gerar código profissional único automaticamente (`PRO-<ano>-<código>`)                | Must       |
| PRF-03 | Registrar disponibilidade do profissional (disponível/indisponível)                   | Must       |
| PRF-04 | Associar profissionais aos serviços que ministram                                     | Should     |
| PRF-05 | Restringir a um profissional a criação de registros apenas dos seus agendamentos      | Must       |

#### 2.3.3 Regras de Negócio Específicas

- A ocupação do profissional deve ser um dos seis serviços do catálogo.
- Cada conta de usuário pode possuir apenas um perfil de profissional.
- O profissional registra presença e avaliações somente nos seus agendamentos.

## 3. Aplicativos Similares

### 3.1 Comparativo de Plataformas

| Sistema        | Foco Principal                                                      | Pontos Fortes                                                                      | Limitações para o Nosso Cenário                                                                                   | Site Oficial                                        |
| :------------- | :------------------------------------------------------------------ | :--------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| **Tecnofit**   | Gestão completa de academias tradicionais e centros de treinamento. | Controle eficiente de turmas, gestão de capacidade de salas e controle financeiro. | Focado no adulto autônomo; não separa claramente a conta do "responsável" da ficha de evolução da "criança".      | [tecnofit.com.br](https://www.tecnofit.com.br/)     |
| **Evo**        | Gestão de academias com foco na jornada e retenção do aluno.        | Interface muito amigável para reserva de aulas e controle de check-in.             | A estrutura assume como padrão que o usuário que agenda pelo aplicativo é o mesmo que realiza a atividade física. | [evo.com.br](https://evo.com.br/)                   |
| **Calendly**   | Agendamento genérico de horários e compromissos.                    | Fluxo de reserva de tempo extremamente limpo, direto e fácil de usar.              | Não gerencia recursos físicos (limitações de espaço de salas ou equipamentos disponíveis) de forma nativa.        | [calendly.com](https://calendly.com/)               |
| **Doctoralia** | Agendamento de consultas com especialistas de saúde e bem-estar.    | Ótimo fluxo de escolha de profissionais focado nas especialidades de cada um.      | Modelo engessado em atendimentos estritamente individuais (1:1), sem suporte nativo ideal para treinos em grupo.  | [doctoralia.com.br](https://www.doctoralia.com.br/) |

### 3.2 Funcionalidades Essenciais Extraídas

- **Visões de Usuário Distintas:** interfaces separadas para responsável (agendador) e profissional (executor/avaliador).
- **Gestão de Dependentes:** conta principal gerenciando múltiplos perfis secundários (ex.: pai com 2 filhos).
- **Filtros Cruzados:** busca simultânea por data, serviço e profissional.
- **Registro de Evolução:** espaço para o profissional registrar desempenho físico e técnico pós-treino.
- **Fila de Espera:** quando o recurso está cheio, o interesse é registrado em ordem de chegada.

## 4. Integrações avaliadas e descartadas

Durante a pesquisa, avaliou-se a integração com uma API de pagamentos fornecida por uma equipe parceira. A integração foi **descartada do escopo atual**: o sistema não cobrança, não registra transações financeiras e não consome serviços externos. Caso retomada no futuro, os requisitos seriam: registrar identificador externo, valor, status e data da tentativa, e confirmar o agendamento somente após pagamento aprovado, sem armazenar dados sensíveis do meio de pagamento.
