---
id: pesquisa
title: Pesquisa
---

# Pesquisa

## 1. Analisar Aplicações de Alocação de Eventos

### 1.1. Descrição

Núcleo central do sistema que gerencia a alocação de recursos (sala, professor, aluno) em horários específicos, garantindo a ausência de conflitos e o respeito às regras de negócio da academia.

### 1.2. Requisitos Funcionais

| ID     | Descrição                                                                        | Prioridade |
| ------ | -------------------------------------------------------------------------------- | ---------- |
| ALO-01 | Validar a disponibilidade simultânea da Sala e do Professor no horário desejado  | Must       |
| ALO-02 | Impedir agendamentos duplos durante requisições simultâneas                      | Must       |
| ALO-03 | Aplicar tempo de intervalo automaticamente entre atendimentos sequenciais        | Must       |
| ALO-04 | Liberar os recursos (sala/professor) instantaneamente em caso de cancelamento    | Must       |
| ALO-05 | Sugerir os próximos horários livres cruzando a idade do aluno e a atividade      | Should     |
| ALO-06 | Gerenciar fila de espera para atividades de grupo que atingiram a lotação máxima | Could      |

### 1.3. Regras de Negócio Específicas

- **Proteção contra Duplicidade:** O processo de reserva deve ocorrer de forma única e garantida. Se a sala estiver livre, mas o professor entrar em conflito de horário no mesmo instante, a operação inteira deve ser interrompida e não salva.
- **Cálculo de Janela Temporal:** O bloqueio na agenda considera o tempo efetivo da atividade somado ao tempo de reconfiguração e higienização dos equipamentos de alta performance.
- **Prioridade de Segurança:** O sistema deve avaliar o relatório de prontidão física do aluno antes de confirmar um horário para treinos classificados como alta intensidade.

### 1.4. Estrutura de Dados e Relacionamentos

Cada alocação conecta obrigatoriamente: **Atividade**, **Profissional** e opcionalmente **Sala** (para treinos externos). Deve incluir rastreabilidade do aluno, intervalo de tempo (início/fim) e status (Confirmado/Cancelado/Concluído).

## 2. Funcionalidades do Sistema

### 2.1 Calendário

#### 2.1.1 Descrição

Componente central para visualização e manipulação de agendamentos com suporte a múltiplas visualizações (semanal, diária, mensal) e operações diretas no calendário.

#### 2.1.2 Requisitos Funcionais

| ID     | Descrição                                                                      | Prioridade |
| ------ | ------------------------------------------------------------------------------ | ---------- |
| CAL-01 | Visualizar agenda semanal, diária e mensal                                     | Must       |
| CAL-02 | Filtrar eventos por profissional, sala, aluno ou tipo de atividade             | Should     |
| CAL-03 | Criar, editar e excluir agendamentos diretamente no calendário (drag-and-drop) | Must       |
| CAL-04 | Bloquear horários (indisponibilidade temporária)                               | Must       |
| CAL-05 | Receber notificações (e-mail, push) sobre agendamentos                         | Could      |
| CAL-06 | Integração com Google Calendar ou Outlook (exportar/importar)                  | Could      |

#### 2.1.3 Regras de Negócio Específicas

- Somente usuários autenticados podem criar agendamentos.
- O responsável pelo aluno escolhe o profissional disponível.
- Não é permitido agendar em horários passados.
- Conflitos de horário devem ser bloqueados em tempo real.

### 2.2 Salas (Espaços Físicos)

#### 2.2.1 Descrição

Gerenciamento dos espaços físicos (sala de avaliação, pista de corrida, piscina) para evitar conflitos de uso e controlar capacidade.

#### 2.2.2 Requisitos Funcionais

| ID     | Descrição                                                                         | Prioridade |
| ------ | --------------------------------------------------------------------------------- | ---------- |
| SAL-01 | Cadastro de salas com nome, capacidade, equipamentos e localização                | Must       |
| SAL-02 | Associar salas a tipos de atividade (ex.: avaliação física requer sala privativa) | Should     |
| SAL-03 | Verificar disponibilidade de sala para um determinado horário                     | Must       |
| SAL-04 | Relatório de ocupação de salas por período                                        | Could      |

#### 2.2.3 Regras de Negócio Específicas

- Uma sala não pode ser alocada para dois eventos simultâneos.
- Salas com equipamentos especiais (ex.: ergômetro) só podem ser usadas para atividades compatíveis.
- Algumas atividades podem não exigir sala (ex.: treino ao ar livre), simplificando a alocação.

### 2.3 Professores (Profissionais e Especialistas)

#### 2.3.1 Descrição

Gestão de preparadores físicos, fisioterapeutas e avaliadores, garantindo que cada criança seja atendida por profissionais com a especialidade exigida.

#### 2.3.2 Requisitos Funcionais

| ID     | Descrição                                                                       | Prioridade |
| ------ | ------------------------------------------------------------------------------- | ---------- |
| PRF-01 | Cadastrar profissionais com dados básicos e especialidades atreladas            | Must       |
| PRF-02 | Definir grade de horários disponíveis (turnos de trabalho e pausas)             | Must       |
| PRF-03 | Visualizar agenda individual do profissional e histórico de atendimentos        | Should     |
| PRF-04 | Bloquear a agenda do profissional por licenças, férias ou imprevistos médicos   | Must       |
| PRF-05 | Associar um profissional a uma sala específica por padrão (ex: fisio na maca 1) | Could      |

#### 2.3.3 Regras de Negócio Específicas

- O sistema deve validar a competência técnica: um profissional só pode ser alocado em atividades que exijam a sua especialidade registrada.
- O controle de jornada deve injetar automaticamente o tempo de descanso (buffer) entre os atendimentos sequenciais, evitando a sobrecarga do profissional.
- O mesmo professor não pode ser alocado em dois locais físicos diferentes no mesmo bloco de tempo.

## 3. Aplicativos Similares

### 3.1 Comparativo de Plataformas

| Sistema        | Foco Principal                                                      | Pontos Fortes                                                                      | Limitações para o Nosso Cenário                                                                                   | Site Oficial                                        |
| :------------- | :------------------------------------------------------------------ | :--------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------- |
| **Tecnofit**   | Gestão completa de academias tradicionais e centros de treinamento. | Controle eficiente de turmas, gestão de capacidade de salas e controle financeiro. | Focado no adulto autônomo; não separa claramente a conta do "responsável" da ficha de evolução da "criança".      | [tecnofit.com.br](https://www.tecnofit.com.br/)     |
| **Evo**        | Gestão de academias com foco na jornada e retenção do aluno.        | Interface muito amigável para reserva de aulas e controle de check-in.             | A estrutura assume como padrão que o usuário que agenda pelo aplicativo é o mesmo que realiza a atividade física. | [evo.com.br](https://evo.com.br/)                   |
| **Calendly**   | Agendamento genérico de horários e compromissos.                    | Fluxo de reserva de tempo extremamente limpo, direto e fácil de usar.              | Não gerencia recursos físicos (limitações de espaço de salas ou equipamentos disponíveis) de forma nativa.        | [calendly.com](https://calendly.com/)               |
| **Doctoralia** | Agendamento de consultas com especialistas de saúde e bem-estar.    | Ótimo fluxo de escolha de profissionais focado nas especialidades de cada um.      | Modelo engessado em atendimentos estritamente individuais (1:1), sem suporte nativo ideal para treinos em grupo.  | [doctoralia.com.br](https://www.doctoralia.com.br/) |

### 3.2 Funcionalidades Essenciais Extraídas

- **Visões de Usuário Distintas:** Interfaces separadas para responsável (agendador) e professor (executor/avaliador).
- **Gestão de Dependentes:** Conta principal gerenciando múltiplos perfis secundários (ex.: pai com 2 filhos).
- **Filtros Cruzados:** Busca simultânea por data, atividade e profissional.
- **Registro de Evolução:** Espaço para professor registrar desempenho físico e técnico pós-treino.
