---
id: requisitos
title: Levantamento de Requisitos e Caso de Uso
---

# 06 - Levantamento de Requisitos e Caso de Uso

**Sistema:** Sistema de gestão para uma academia de alta performance esportiva

## 1. Identificação dos Stakeholders

- **Responsável:** Pessoa legalmente responsável por um ou mais alunos. Cria conta, cadastra dependentes, agenda e cancela treinamentos, consulta a evolução dos filhos e recebe comunicados.
- **Aluno/Atleta:** Criança de 7 a 12 anos matriculada na academia. Não acessa o sistema diretamente, mas é o beneficiário direto dos cadastros e agendamentos feitos pelo responsável.
- **Profissional (Treinador):** Responsável por ministrar os treinamentos. Consulta sua agenda, acompanha as turmas, registra presença e avaliações físicas/técnicas.
- **Administrador/Recepção:** Gerencia cadastros de usuários, profissionais, campos, turmas e horários. Acompanha conflitos, cancelamentos e relatórios operacionais.

## 2. Requisitos Funcionais

| ID | Descrição | Prioridade |
| --- | --- | --- |
| RF01 | O sistema deve permitir que o responsável crie uma conta com dados pessoais, contato e credenciais de acesso | Alta |
| RF02 | O sistema deve permitir login, logout e recuperação de senha | Alta |
| RF03 | O sistema deve permitir que o responsável cadastre um ou mais alunos vinculados à sua conta | Alta |
| RF04 | O sistema deve validar automaticamente a idade do aluno (7 a 12 anos) no cadastro | Alta |
| RF05 | O sistema deve permitir que a administração cadastre profissionais, suas especialidades e disponibilidade | Alta |
| RF06 | O sistema deve permitir que a administração cadastre campos/espaços com capacidade máxima | Alta |
| RF07 | O sistema deve permitir que a administração cadastre turmas com modalidade, faixa etária, capacidade, local e profissional responsável | Alta |
| RF08 | O sistema deve permitir que o responsável agende um treinamento para um aluno, selecionando turma, data e horário disponíveis | Alta |
| RF09 | O sistema deve validar disponibilidade do aluno, do profissional, do espaço e da turma antes de confirmar um agendamento | Alta |
| RF10 | O sistema deve bloquear novos agendamentos quando a turma atingir sua capacidade máxima | Alta |
| RF11 | O sistema deve impedir agendamentos duplicados para o mesmo aluno no mesmo horário | Alta |
| RF12 | O sistema deve permitir que o responsável consulte a agenda de treinamentos de cada dependente | Alta |
| RF13 | O sistema deve permitir que o responsável cancele um agendamento dentro do prazo definido pela academia | Alta |
| RF14 | O sistema deve liberar automaticamente a vaga da turma quando um agendamento for cancelado | Alta |
| RF15 | O sistema deve bloquear o cancelamento de um agendamento quando estiver fora do prazo mínimo definido pela academia (prazo a definir), salvo autorização da administração | Alta |
| RF16 | O sistema deve permitir que o profissional consulte sua agenda individual e a lista de alunos de cada turma | Média |
| RF17 | O sistema deve permitir que o profissional registre presença, ausência e observações de avaliação por treinamento | Média |
| RF18 | O sistema deve permitir que o responsável consulte a evolução física/técnica de seus dependentes | Média |
| RF19 | O sistema deve permitir que a administração cancele um treinamento por motivo operacional e identifique os usuários afetados | Média |
| RF20 | O sistema deve enviar notificações internas sobre criação, alteração ou cancelamento de agendamentos | Média |
| RF21 | O sistema deve disponibilizar um dashboard com a ocupação das turmas e a disponibilidade dos profissionais | Média |
| RF22 | O sistema deve permitir fila de espera automática para turmas lotadas | Média |


## 3. Requisitos Não Funcionais

- **Performance:** O sistema deve validar disponibilidade e responder a um pedido de agendamento em até 2 segundos, mesmo com requisições simultâneas.
- **Segurança:** O sistema deve proteger dados pessoais e de saúde de menores de idade conforme a LGPD, aplicando controle de acesso por perfil (responsável, profissional, administração) e registrando trilha de auditoria para alterações sensíveis.
- **Usabilidade:** A interface de agendamento deve ser simples o suficiente para uso por responsáveis sem familiaridade técnica, seguindo o princípio de reduzir atrito identificado no Design Thinking.
- **Confiabilidade:** O sistema deve garantir que nenhuma sala/turma/profissional seja alocado em conflito de horário, mesmo em caso de concorrência (duas requisições simultâneas).
- **Disponibilidade:** O sistema deve estar acessível para consulta e agendamento fora do horário comercial, já que os responsáveis podem agendar remotamente a qualquer momento.

## 4. Casos de Uso

### UC01 - Agendar Treinamento

- **Atores:** Responsável, Sistema
- **Pré-condição:** Responsável está autenticado e possui ao menos um aluno cadastrado.
- **Fluxo Principal:**
  1. Responsável seleciona o aluno.
  2. Responsável escolhe uma turma compatível com a faixa etária do aluno.
  3. Responsável seleciona data e horário disponíveis.
  4. Sistema valida disponibilidade do aluno, do profissional, do espaço e da turma.
  5. Sistema confirma o agendamento e notifica o profissional responsável.
- **Fluxos Alternativos:**
  - FA1: Turma lotada → Sistema informa indisponibilidade e sugere outra turma ou horário.
  - FA2: Conflito de horário para o aluno → Sistema bloqueia o agendamento e exibe o conflito.
- **Pós-condição:** Agendamento é registrado com status "confirmado" e a vaga da turma é reservada.

### UC02 - Cancelar Agendamento

- **Atores:** Responsável, Sistema
- **Pré-condição:** Existe um agendamento ativo vinculado ao aluno do responsável.
- **Fluxo Principal:**
  1. Responsável seleciona o agendamento a ser cancelado.
  2. Sistema verifica se o cancelamento está dentro do prazo permitido.
  3. Responsável confirma o cancelamento.
  4. Sistema atualiza o status do agendamento e libera a vaga da turma.
- **Fluxos Alternativos:**
  - FA1: Cancelamento com menos de 8 horas de antecedência → Sistema bloqueia a ação ou exige autorização da administração.
- **Pós-condição:** Agendamento passa para o status "cancelado" e a vaga fica disponível para outro aluno.

### UC03 - Cadastrar Aluno

- **Atores:** Responsável, Sistema
- **Pré-condição:** Responsável possui conta ativa no sistema.
- **Fluxo Principal:**
  1. Responsável informa nome, data de nascimento e dados de contato do aluno.
  2. Sistema valida se a idade está dentro da faixa aceita pela academia (7 a 12 anos).
  3. Responsável vincula o aluno à sua conta.
  4. Sistema confirma o cadastro.
- **Fluxos Alternativos:**
  - FA1: Idade fora da faixa aceita → Sistema bloqueia o cadastro e informa o motivo.
- **Pós-condição:** Aluno é registrado no sistema e vinculado ao responsável.

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
usecase (UC04: Cadastrar Turma) as UC04
usecase (UC05: Registrar Presenca e Avaliacao) as UC05
usecase (UC06: Consultar Agenda) as UC06

usecase (Turma Lotada) as FA1
usecase (Conflito de Horario) as FA2
usecase (Fora do Prazo de Cancelamento) as FA3

Responsavel --> UC01
Responsavel --> UC02
Responsavel --> UC03
Responsavel --> UC06

Administrador --> UC04
Administrador --> UC02

Profissional --> UC05
Profissional --> UC06

FA1 .> UC01 : <<extend>>
FA2 .> UC01 : <<extend>>
FA3 .> UC02 : <<extend>>

note right of UC01
  **Pré-condição**: Responsável logado.
  **Pós-condição**: Agendamento confirmado.
end note

@enduml
```

**Explicação:**

1. **Atores:** Responsável (agenda e cancela), Profissional (registra presença e consulta agenda), Administrador (cadastra turmas e pode cancelar por motivo operacional).
2. **Fluxo Principal (UC01):** Selecionar aluno → Selecionar turma/horário → Validar disponibilidade → Confirmar agendamento.
3. **Relacionamentos `<<extend>>`:** Representam os fluxos alternativos identificados nos casos de uso (turma lotada, conflito de horário, cancelamento fora do prazo).

## 6. Diagrama de Classes

Diagrama de classes conceitual representando as principais entidades do sistema:

```
@startuml AcademiaEsportiva_Classes

class Responsavel {
  - id: String
  - nome: String
  - email: String
  - telefone: String
  + cadastrarAluno()
  + agendarTreinamento()
  + cancelarAgendamento()
}

class Aluno {
  - id: String
  - nome: String
  - dataNascimento: Date
  - status: String
  + calcularIdade()
}

class Profissional {
  - id: String
  - nome: String
  - especialidade: String
  + registrarPresenca()
  + registrarAvaliacao()
}

class Turma {
  - id: String
  - modalidade: String
  - faixaEtariaMin: Integer
  - faixaEtariaMax: Integer
  - capacidadeMaxima: Integer
  + verificarDisponibilidade()
}

class Agendamento {
  - id: String
  - dataHora: DateTime
  - status: String
  + confirmar()
  + cancelar()
}

Responsavel "1" --> "1..*" Aluno
Aluno "1" --> "0..*" Agendamento
Turma "1" --> "0..*" Agendamento
Profissional "1" --> "0..*" Turma
Agendamento "0..*" --> "1" Turma

@enduml
```

**Explicação:**

1. **Classes principais:** Responsavel, Aluno, Profissional, Turma e Agendamento.
2. **Relacionamentos:** Um responsável possui 1 ou mais alunos; um aluno pode ter 0 ou mais agendamentos; uma turma está associada a exatamente um profissional; um agendamento pertence a exatamente uma turma.

## 7. Protótipo (Exemplo Simplificado)

Protótipo de telas alinhado ao caso de uso UC01, usando **Salt (PlantUML)**:

```
@startsalt
{
  Tela de Agendamento
  Aluno: ^Pedro (9 anos)^
  Turma: ^Iniciação - Ter/Qui 16h^
  Data: "12/10/2026"
  [Confirmar Agendamento] | [Cancelar]
}
@endsalt
```

```
@startsalt
{
  **Agendamento Confirmado!**
  Treino de Pedro em 12/10/2026 as 16h
  Local: Campo 2 - Professor Carlos
  [Ver Agenda] | [Voltar ao Início]
}
@endsalt
```

**Telas previstas (fluxo do caso de uso UC01):**

1. **Seleção do aluno:** lista de dependentes vinculados ao responsável.
2. **Seleção da turma:** turmas compatíveis com a idade do aluno, com horário e vagas.
3. **Confirmação:** resumo do agendamento (aluno, turma, data, local, profissional).
4. **Tela de sucesso:** confirmação com opção de ver agenda ou voltar ao início.

## 8. Validação

- **Prazo de cancelamento:** confirmar com a administração qual o prazo mínimo aceito antes do treino (ex: 2h, 24h).
- **Teste com usuários:** validar o fluxo de agendamento (UC01) com um responsável real ou representante do perfil, verificando se o fluxo é intuitivo.

## Autor(es)

| Data | Versão | Descrição | Autor(es) |
| --- | --- | --- | --- |
| 23/09/2026 | 1.0 | Criação do documento de requisitos | Ricardo Costa |