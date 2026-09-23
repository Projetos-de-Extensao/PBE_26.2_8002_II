---
id: mapa_mental
title: Mapas Mentais
---

## Introdução

<p align = "justify">
Mapa mental consiste em criar resumos cheios de símbolos, cores, setas e frases de efeito com o objetivo de organizar o conteúdo e facilitar associações entre as informações destacadas. Esse material é muito indicado para pessoas que têm facilidade de aprender de forma visual.
</p>
 
## Metodologia

<p align="justify">
O mapa foi elaborado a partir da consolidação das ideias levantadas no <a href="Brainstorm.md">Brainstorm</a>, no <a href="5w2h.md">5W2H</a> e no <a href="design_thinking.md">Design Thinking</a>. O tema central representa o sistema e seus ramos organizam o problema, os usuários, os cadastros, a operação, o acompanhamento, a administração e a base tecnológica. O diagrama foi escrito em PlantUML para permanecer versionável e fácil de atualizar durante as próximas iterações.
</p>
 
## Mapa mental geral
 
### Versão 1.0

O centro do mapa é o **Sistema para academia de alta perfomance**. A leitura parte do centro e segue os ramos para compreender:

- **Problema e objetivo:** por que o sistema é necessário e quais resultados deve apoiar;
- **Usuários e permissões:** quem utiliza a solução e quais informações cada perfil pode acessar;
- **Cadastros:** quais entidades sustentam a operação;
- **Operação dos treinamentos:** como o agendamento, as validações, os cancelamentos e os reagendamentos funcionam;
- **Acompanhamento e comunicação:** como registrar a rotina dos atletas e informar os envolvidos;
- **Administração e indicadores:** como a academia acompanha sua operação;
- **Base tecnológica:** quais decisões orientam o backend e o MVP.

```plantuml
@startmindmap
left to right direction 
skinparam monochrome false
skinparam backgroundColor #FFFFFF
skinparam ArrowColor #2F5D50
skinparam NodeFontSize 14
skinparam NodeFontColor #263238

* Academia de alta performance
** Problema e objetivo
*** Centralizar a rotina da academia
*** Evitar conflitos de agenda e superlotação
*** Apoiar a evolução física e técnica dos atletas

** Usuários e permissões
*** Responsável
**** Cadastra dependentes
**** Agenda e cancela treinamentos
**** Consulta agenda e evolução dos dependentes
*** Profissional
**** Consulta agenda e turmas atribuídas
**** Registra presença e avaliações autorizadas
*** Administração e recepção
**** Gerencia cadastros, conflitos e comunicados
**** Controla espaços, turmas e profissionais
*** Acesso por perfil e princípio do menor privilégio

** Cadastros
*** Usuários e responsáveis
**** Autenticação e recuperação de senha
**** Vínculo com um ou mais responsáveis legais
*** Alunos e atletas
**** Data de nascimento e validação de idade
**** Situação: ativo, afastado ou inativo
**** Saúde, restrições e autorizações com acesso restrito
*** Profissionais
**** Especialidades e disponibilidade
*** Espaços e turmas
**** Capacidade, modalidade, duração e faixa etária

** Operação dos treinamentos
*** Agendamento
**** Selecionar aluno, data, horário e turma
**** Verificar aluno, profissional, espaço e turma
**** Bloquear duplicidade e horários conflitantes
*** Regras de negócio
**** Idade compatível com a turma
**** Limite de vagas da turma e do espaço
**** Disponibilidade do profissional
*** Cancelamento e reagendamento
**** Respeitar prazo definido pela academia
**** Liberar a vaga após cancelamento
**** Manter histórico e responsável pela alteração
*** Evolução futura: fila de espera

** Acompanhamento e comunicação
*** Presença e frequência
**** Presente, ausente ou falta justificada
*** Evolução do atleta
**** Avaliações físicas e técnicas
**** Histórico de treinamentos
*** Notificações internas
**** Confirmações e alterações de agendamento
**** Inclusão ou remoção de aluno na turma
**** Cancelamento pela academia

** Administração e indicadores
*** Dashboard operacional
**** Ocupação e vagas por turma
**** Agenda de espaços e profissionais
**** Treinamentos do dia e alunos esperados
*** Relatórios básicos
**** Faltas, cancelamentos e reagendamentos
**** Alunos ativos, afastados e inativos
*** Evolução futura
**** Integração financeira e inadimplência
**** E-mail e SMS
**** Relatórios avançados

** Base tecnológica
*** Backend em Python e Django
*** Autenticação e autorização nativas
*** Validações automáticas das regras
*** Auditoria de alterações relevantes
*** MVP focado em cadastro e agendamento
@endmindmap
```

## Conclusão

<p align="justify">
O mapa organiza a proposta do projeto em uma visão única: a academia precisa de uma fonte confiável para gerenciar responsáveis, atletas, profissionais, espaços e treinamentos. O núcleo do MVP está no vínculo entre responsável e aluno e no agendamento com validação de idade, disponibilidade e vagas. Os demais ramos mostram capacidades que podem ser desenvolvidas de forma incremental.
</p>
 
## Referências

- [Brainstorm](Brainstorm.md)
- [5W2H](5w2h.md)
- [Design Thinking](design_thinking.md)
- [Documentação do PlantUML](https://plantuml.com/mindmap-diagram)

## Versionamento

| Data       | Versão | Descrição                                            | Autor(es) |
| ---------- | ------ | ---------------------------------------------------- | --------- |
| 13/09/2026 | 1.0    | Criação do mapa mental geral da proposta do sistema. | Luiz Fernando  |
