---
id: requisitos
title: Levantamento de Requisitos e Caso de Uso
---

# 06 - Levantamento de Requisitos e Caso de Uso

**Sistema:** Sistema de gestão para uma academia de alta performance esportiva

## 1. Identificação dos Stakeholders

- **Responsável:** Pessoa legalmente responsável por um ou mais alunos. Cria conta, cadastra dependentes, agenda e cancela treinamentos e consulta a evolução dos filhos.
- **Aluno/Atleta:** Criança de 7 a 12 anos matriculada na academia. Não acessa o sistema diretamente, mas é o beneficiário direto dos cadastros e agendamentos feitos pelo responsável.
- **Profissional (Treinador):** Responsável por ministrar os treinamentos. Consulta sua agenda e registra presença e avaliações físicas/técnicas dos seus agendamentos.
- **Administrador:** Usuário com privilégio de escrita (staff) sobre profissionais, salas e serviços, gerenciado pelo Django Admin.

## 2. Requisitos Funcionais

| ID   | Descrição                                                                                                                        | Prioridade |
| ---- | --------------------------------------------------------------------------------------------------------------------------------- | ---------- |
| RF01 | O sistema deve permitir que qualquer pessoa crie uma conta com nome de usuário, e-mail e senha                                    | Alta       |
| RF02 | O sistema deve permitir login por token, logout com invalidação do token e proteção de todos os endpoints por autenticação         | Alta       |
| RF03 | O sistema deve permitir que o responsável autenticado cadastre um ou mais alunos vinculados à sua conta                           | Alta       |
| RF04 | O sistema deve validar automaticamente a idade do aluno (7 a 12 anos) no cadastro, gerando matrícula única no formato `ALU-<ano>-<código>` | Alta |
| RF05 | O sistema deve permitir o cadastro de profissionais com nome, ocupação (tipo de serviço) e disponibilidade, gerando código único no formato `PRO-<ano>-<código>` | Alta |
| RF06 | O sistema deve permitir que a administração gerencie as salas com nome, capacidade e disponibilidade                              | Alta       |
| RF07 | O sistema deve manter um catálogo de serviços (Nutrição Esportiva, Fisioterapia, Recuperação Muscular, Preparação Física, Treinamento Funcional e Avaliação de Performance), com descrição, duração e sala correspondente | Alta |
| RF08 | O sistema deve permitir associar profissionais aos serviços que ministram, sem duplicidade                                        | Média      |
| RF09 | O sistema deve permitir que o responsável agende um treinamento para um aluno, informando aluno, serviço, profissional, sala, data e hora | Alta |
| RF10 | O sistema deve comparar a quantidade de agendamentos ativos com a capacidade da sala no horário escolhido                          | Alta       |
| RF11 | O sistema deve posicionar automaticamente o agendamento em fila de espera quando a capacidade da sala no horário for atingida      | Alta       |
| RF12 | O sistema deve informar a posição do aluno na fila de espera, calculada pela ordem de criação dos agendamentos em espera            | Alta       |
| RF13 | O sistema deve impedir que um responsável agende treinamento para aluno que não é seu dependente                                   | Alta       |
| RF14 | O sistema deve permitir que o responsável consulte a agenda de treinamentos de cada dependente                                     | Alta       |
| RF15 | O sistema deve permitir que o responsável cancele um agendamento                                                                   | Alta       |
| RF16 | O sistema deve permitir que o profissional registre, por agendamento, presença, observações e avaliações física e técnica           | Média      |
| RF17 | O sistema deve restringir a criação de registros de treinamento aos usuários com perfil de profissional                             | Média      |
| RF18 | O sistema deve permitir que o responsável consulte os registros de treinamento apenas dos seus dependentes                          | Média      |

## 3. Requisitos Não Funcionais

- **Segurança:** toda a API exige autenticação por token, exceto o registro de conta; cada usuário acessa apenas os dados vinculados ao seu perfil (responsável ou profissional), conforme a LGPD aplicada a dados de menores.
- **Usabilidade:** a API segue padrão REST previsível, com schemas documentados automaticamente via drf-spectacular.
- **Consistência:** a mudança de status para fila de espera é calculada no ato da validação do agendamento, garantindo que o limite da sala seja respeitado em cada requisição.
- **Disponibilidade:** o sistema deve estar acessível para consulta e agendamento fora do horário comercial, já que os responsáveis podem agendar remotamente a qualquer momento.
- **Manutenibilidade:** o catálogo de serviços e salas é mantido pela administração por meio do Django Admin, sem necessidade de alteração de código.

## 4. Casos de Uso

### UC01 - Agendar Treinamento

- **Atores:** Responsável, Sistema
- **Pré-condição:** Responsável está autenticado e possui ao menos um aluno cadastrado.
- **Fluxo Principal:**
  1. Responsável seleciona o aluno.
  2. Responsável seleciona o serviço, o profissional, a sala e a data/hora.
  3. Sistema valida que o aluno é dependente do responsável autenticado.
  4. Sistema conta os agendamentos ativos para a mesma sala e horário.
  5. Se a quantidade for inferior à capacidade da sala, o sistema registra o agendamento com status "ativo".
  6. Se a capacidade foi atingida, o sistema registra o agendamento com status "fila_espera" e calcula a posição do aluno na fila.
- **Fluxos Alternativos:**
  - FA1: Aluno não pertence ao responsável → Sistema nega a operação e informa a falta de permissão.
  - FA2: Sala ou horário não informados → Sistema registra o agendamento sem controle de capacidade (campos opcionais).
- **Pós-condição:** Agendamento é registrado com status "ativo" ou "fila_espera", com posição da fila calculada quando aplicável.

### UC02 - Cancelar Agendamento

- **Atores:** Responsável, Sistema
- **Pré-condição:** Existe um agendamento vinculado a um aluno do responsável.
- **Fluxo Principal:**
  1. Responsável consulta a agenda dos dependentes.
  2. Responsável seleciona o agendamento a ser cancelado.
  3. Sistema altera o status do agendamento para "inativo".
- **Pós-condição:** O agendamento deixa de contar para a capacidade da sala, liberando vaga para novos agendamentos ativos.

### UC03 - Cadastrar Aluno

- **Atores:** Responsável, Sistema
- **Pré-condição:** Responsável possui conta ativa no sistema.
- **Fluxo Principal:**
  1. Responsável informa nome e data de nascimento do aluno.
  2. Sistema calcula a idade do aluno.
  3. Sistema verifica se a idade está entre 7 e 12 anos.
  4. Sistema vincula o aluno à conta do responsável autenticado.
  5. Sistema gera a matrícula única do aluno.
- **Fluxos Alternativos:**
  - FA1: Idade fora da faixa aceita → Sistema bloqueia o cadastro e informa que a academia atende exclusivamente crianças de 7 a 12 anos.
- **Pós-condição:** Aluno é registrado no sistema e vinculado ao responsável.

### UC04 - Registrar Treinamento

- **Atores:** Profissional, Sistema
- **Pré-condição:** Usuário autenticado possui perfil de profissional e existe um agendamento correspondente.
- **Fluxo Principal:**
  1. Profissional informa o agendamento e os dados do registro.
  2. Profissional registra a presença ou ausência do aluno.
  3. Profissional informa observações e as avaliações física e técnica.
  4. Sistema atribui o registro ao profissional autenticado.
- **Fluxos Alternativos:**
  - FA1: Usuário sem perfil de profissional → Sistema nega a operação.
- **Pós-condição:** Registro de treinamento criado, vinculado ao agendamento e ao profissional (relação 1:1 com o agendamento).

## 5. Diagrama de Casos de Uso

Diagrama de Caso de Uso (UML) representando os principais atores e funcionalidades do sistema, em **PlantUML**:

```
@startuml AcademiaEsportiva_CasosDeUso
left to right direction
skinparam actorStyle awesome

actor Responsavel
actor Profissional
actor Administrador

usecase (UC01: Agendar Treinamento) as UC01
usecase (UC02: Cancelar Agendamento) as UC02
usecase (UC03: Cadastrar Aluno) as UC03
usecase (UC04: Registrar Treinamento) as UC04
usecase (UC05: Consultar Agenda) as UC05

usecase (Fila de Espera Automatica) as FA1
usecase (Aluno nao vinculado) as FA2
usecase (Validar faixa etaria) as INC1
usecase (Validar capacidade da sala) as INC2

Responsavel --> UC01
Responsavel --> UC02
Responsavel --> UC03
Responsavel --> UC05

Profissional --> UC04
Profissional --> UC05

Administrador --> UC05

FA1 .> UC01 : <<extend>>
FA2 .> UC01 : <<extend>>

UC01 ..> INC1 : <<include>>
UC01 ..> INC2 : <<include>>

note right of UC01
  **Pré-condição**: Responsável logado.
  **Pós-condição**: Agendamento ativo ou em fila de espera.
end note

@enduml
```

**Explicação:**

1. **Atores:** Responsável (agenda, cancela e cadastra alunos), Profissional (registra treinamentos), Administrador (gerencia salas e serviços pelo Django Admin).
2. **Fluxo Principal (UC01):** Selecionar aluno → Selecionar serviço/profissional/sala/horário → Validar vínculo e capacidade → Registrar agendamento.
3. **Relacionamentos:** `<<extend>>` para fila de espera (quando a sala lota) e `<<include>>` para as validações obrigatórias.

## 6. Diagrama de Classes

Diagrama de classes conceitual representando as entidades implementadas no sistema:

```
@startuml AcademiaEsportiva_Classes

class Responsavel {
  + nome: String
  + cpf: String
  + telefone: String
}

class Aluno {
  + matricula: String
  + nome: String
  + data_nascimento: Date
  + status: String
  + idade: Integer
}

class Profissional {
  + codigo_profissional: String
  + nome: String
  + ocupacao: String
  + disponibilidade: String
}

class Sala {
  + nome: String
  + capacidade: Integer
  + disponivel: Boolean
}

class Servico {
  + nome: String
  + descricao: String
  + duracao_minutos: Integer
}

class Agendamento {
  + data_hora: DateTime
  + status: String
  + criado_em: DateTime
}

class RegistroTreinamento {
  + presenca: String
  + observacoes: String
  + avaliacao_fisica: String
  + avaliacao_tecnica: String
}

Responsavel "1" -- "1..*" Aluno : possui
Agendamento "0..*" --> "1" Aluno
Agendamento "0..*" --> "1" Profissional
Agendamento "0..*" --> "0..1" Sala
Agendamento "0..*" --> "1" Servico
Profissional "1" -- "0..*" Servico : ministra
Agendamento "1" -- "0..1" RegistroTreinamento : gera
Profissional "1" -- "0..*" RegistroTreinamento : registra

@enduml
```

**Explicação:**

1. **Classes principais:** Responsavel, Aluno, Profissional, Sala, Servico, Agendamento e RegistroTreinamento.
2. **Relacionamentos:** Um responsável possui um ou mais alunos; um agendamento pertence a um aluno, a um profissional, a um serviço e opcionalmente a uma sala; profissionais e serviços relacionam-se por muitos-para-muitos; cada agendamento gera no máximo um registro de treinamento.
3. **Fila de espera:** não é uma entidade separada — é o status `fila_espera` do próprio agendamento, com posição calculada pela ordem de criação.

## 7. Protótipo (Exemplo Simplificado)

Protótipo de telas alinhado ao caso de uso UC01, usando **Salt (PlantUML)**:

```
@startsalt
{
  Tela de Agendamento
  Aluno: ^Pedro (9 anos)^
  Serviço: ^Preparação Física^
  Profissional: ^Carlos Silva^
  Sala: ^Área de Treinamento Funcional^
  Data: "12/10/2026 14:00"
  [Confirmar Agendamento] | [Cancelar]
}
@endsalt
```

```
@startsalt
{
  **Agendamento Confirmado!**
  Treino de Pedro em 12/10/2026 às 14:00
  Serviço: Preparação Física - Profissional: Carlos
  Status: Ativo
  [Ver Agenda] | [Voltar ao Início]
}
@endsalt
```

**Telas previstas (fluxo do caso de uso UC01):**

1. **Seleção do aluno:** lista de dependentes vinculados ao responsável.
2. **Seleção do serviço e profissional:** serviços do catálogo com seus profissionais e salas.
3. **Confirmação:** resumo do agendamento (aluno, serviço, sala, data, profissional).
4. **Tela de sucesso:** confirmação do status — ativo ou posição na fila de espera.

## 8. Validação

- **Capacidade da sala:** validar com a administração a capacidade de cada espaço e se a fila de espera deve ter limite de tamanho.
- **Teste com usuários:** validar o fluxo de agendamento (UC01) com um responsável real ou representante do perfil, verificando se o fluxo é intuitivo.

## Autor(es)

| Data       | Versão | Descrição                                                                                          | Autor(es)     |
| ---------- | ------ | -------------------------------------------------------------------------------------------------- | ------------- |
| 23/09/2026 | 1.0    | Criação do documento de requisitos                                                                 | Ricardo Costa |
| 13/11/2026 | 2.0    | Reescrita para refletir o código implementado: agendamento individual por serviço, fila de espera por sala, sem turmas e sem pagamentos | Ricardo Costa |
