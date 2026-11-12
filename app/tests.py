from datetime import date, datetime, timedelta

from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from app.models import (
    Agendamento,
    Aluno,
    Profissional,
    Responsavel,
    Sala,
    Servico,
)


class AuthenticationApiTests(APITestCase):
    def test_root_redirects_to_api(self):
        response = self.client.get("/")

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response["Location"], "/api/")

    def test_user_can_register_and_obtain_token(self):
        register_response = self.client.post(
            reverse("api_register"),
            {
                "username": "responsavel",
                "email": "responsavel@example.com",
                "password": "senha-segura-123",
            },
            format="json",
        )

        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        token_response = self.client.post(
            reverse("api_auth_token"),
            {"username": "responsavel", "password": "senha-segura-123"},
            format="json",
        )

        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        self.assertTrue(token_response.data["token"])

    def test_protected_routes_require_authentication(self):
        response = self.client.get(reverse("sala-list"))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_invalidates_current_token(self):
        user = User.objects.create_user(username="user", password="senha-segura-123")
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

        logout_response = self.client.post(reverse("api_logout"))
        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)

        protected_response = self.client.get(reverse("sala-list"))
        self.assertEqual(protected_response.status_code, status.HTTP_401_UNAUTHORIZED)


class CompleteApiFlowTests(APITestCase):
    def get_token(self, username, password):
        response = self.client.post(
            reverse("api_auth_token"),
            {"username": username, "password": password},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["token"]

    def test_complete_authenticated_academy_flow(self):
        admin = User.objects.create_user(
            username="admin-fluxo",
            password="senha-segura-123",
            is_staff=True,
        )
        responsible_password = "senha-responsavel-123"

        register_response = self.client.post(
            reverse("api_register"),
            {
                "username": "responsavel-fluxo",
                "email": "fluxo@example.com",
                "password": responsible_password,
            },
            format="json",
        )
        self.assertEqual(register_response.status_code, status.HTTP_201_CREATED)
        responsible_token = self.get_token(
            "responsavel-fluxo", responsible_password
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {responsible_token}")

        profile_response = self.client.post(
            reverse("responsavel-list"),
            {"nome": "Responsável do fluxo", "telefone": "11999999999"},
            format="json",
        )
        self.assertEqual(profile_response.status_code, status.HTTP_201_CREATED)

        underage_student_response = self.client.post(
            reverse("aluno-list"),
            {
                "nome": "Aluno menor de 7 anos",
                "data_nascimento": f"{date.today().year - 6}-01-01",
            },
            format="json",
        )
        self.assertEqual(
            underage_student_response.status_code, status.HTTP_400_BAD_REQUEST
        )
        self.assertIn(
            "a partir de 7 anos",
            underage_student_response.data["data_nascimento"][0],
        )

        admin_token = self.get_token("admin-fluxo", "senha-segura-123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {admin_token}")
        professional_response = self.client.post(
            reverse("profissional-list"),
            {"nome": "Profissional do fluxo", "ocupacao": "Fisioterapia"},
            format="json",
        )
        self.assertEqual(
            professional_response.status_code, status.HTTP_201_CREATED
        )
        professional_code = professional_response.data["codigo_profissional"]

        services_response = self.client.get(reverse("servico-list"))
        self.assertEqual(services_response.status_code, status.HTTP_200_OK)
        service = next(
            item
            for item in services_response.data
            if item["nome"] == "Fisioterapia"
        )
        self.assertTrue(service["descricao"])

        association_response = self.client.post(
            reverse("servico-adicionar-profissional", args=[service["id"]]),
            {"profissional_codigo": professional_code},
            format="json",
        )
        self.assertEqual(
            association_response.status_code, status.HTTP_201_CREATED
        )

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {responsible_token}")
        professionals_response = self.client.get(reverse("profissional-list"))
        self.assertEqual(professionals_response.status_code, status.HTTP_200_OK)
        self.assertTrue(
            any(
                item["matricula"] == professional_code
                for item in professionals_response.data
            )
        )

        student_response = self.client.post(
            reverse("aluno-list"),
            {
                "nome": "Aluno do fluxo",
                "data_nascimento": "2018-01-01",
            },
            format="json",
        )
        self.assertEqual(student_response.status_code, status.HTTP_201_CREATED)
        student_registration = student_response.data["matricula"]

        appointment_response = self.client.post(
            reverse("agendamento-list"),
            {
                "aluno_matricula": student_registration,
                "profissional_codigo": professional_code,
                "servico_nome": "Fisioterapia",
                "data_hora": "2020-01-01T10:00:00Z",
            },
            format="json",
        )
        self.assertEqual(
            appointment_response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            appointment_response.data["sala"],
            "Espaço de Fisioterapia e Recovery",
        )

        conflict_response = self.client.post(
            reverse("agendamento-list"),
            {
                "aluno_matricula": student_registration,
                "profissional_codigo": professional_code,
                "servico_nome": "Fisioterapia",
                "data_hora": "2020-01-01T10:15:00Z",
            },
            format="json",
        )
        self.assertEqual(
            conflict_response.status_code, status.HTTP_400_BAD_REQUEST
        )

        professional_token = self.get_token(
            "admin-fluxo", "senha-segura-123"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {professional_token}")
        report_response = self.client.post(
            reverse("registro-treinamento-list"),
            {
                "agendamento": student_registration,
                "presenca": "presente",
                "observacoes": "Fluxo completo.",
                "avaliacao_fisica": "Avaliação concluída.",
                "avaliacao_tecnica": "Avaliação concluída.",
            },
            format="json",
        )
        self.assertEqual(report_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(report_response.data["agendamento"], student_registration)


class RelationshipApiTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin", password="senha-segura-123", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.responsavel = Responsavel.objects.create(
            profile=self.user,
            nome="Responsável",
            telefone="11999999999",
        )
        self.aluno = Aluno.objects.create(
            nome="Aluno",
            data_nascimento=date(date.today().year - 8, 1, 1),
            responsavel=self.responsavel,
        )
        self.sala = Sala.objects.get(nome="Espaço de Fisioterapia e Recovery")
        self.servico = Servico.objects.get(nome="Fisioterapia")

    def test_agendamento_accepts_sala_and_servico_relationships(self):
        response = self.client.post(
            reverse("profissional-list"),
            {"nome": "Profissional", "ocupacao": "Fisioterapia"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        agendamento_response = self.client.post(
            reverse("agendamento-list"),
            {
                "aluno_matricula": self.aluno.matricula,
                "profissional_codigo": response.data["codigo_profissional"],
                "servico_nome": self.servico.nome,
                "data_hora": "2030-01-01T10:00:00Z",
            },
            format="json",
        )

        self.assertEqual(
            agendamento_response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(agendamento_response.data["sala"], str(self.sala))
        self.assertEqual(agendamento_response.data["servico"], str(self.servico))

    def test_agendamento_rejects_unknown_service_name(self):
        response = self.client.post(
            reverse("agendamento-list"),
            {
                "aluno_matricula": self.aluno.matricula,
                "profissional_codigo": "PRO-NAO-EXISTE",
                "servico_nome": "Serviço inexistente",
                "data_hora": "2030-01-01T10:00:00Z",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("servico_nome", response.data)

    def test_agendamento_rejects_overlapping_student_schedule(self):
        profissional_user = User.objects.create_user(username="profissional-conflito")
        profissional = Profissional.objects.create(
            profile=profissional_user,
            nome="Profissional conflito",
            ocupacao="Fisioterapia",
        )
        Agendamento.objects.create(
            data_hora=timezone.make_aware(datetime(2030, 1, 1, 10, 0)),
            aluno=self.aluno,
            profissional=profissional,
            sala=self.sala,
            servico=self.servico,
        )

        response = self.client.post(
            reverse("agendamento-list"),
            {
                "aluno_matricula": self.aluno.matricula,
                "profissional_codigo": profissional.codigo_profissional,
                "servico_nome": self.servico.nome,
                "data_hora": "2030-01-01T10:15:00Z",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("data_hora", response.data)

    def test_salas_are_read_only_in_the_api(self):
        response = self.client.post(
            reverse("sala-list"),
            {
                "nome": "Sala não autorizada",
                "capacidade": 1,
                "disponivel": True,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_salas_have_capacities_appropriate_to_their_services(self):
        response = self.client.get(reverse("sala-list"))
        capacities = {sala["nome"]: sala["capacidade"] for sala in response.data}

        self.assertEqual(
            capacities["Área de Treinamento Funcional e Gramado Sintético"], 20
        )
        self.assertEqual(capacities["Laboratório de Avaliação Física"], 10)
        self.assertEqual(capacities["Consultório de Nutrição Esportiva"], 4)
        self.assertEqual(capacities["Espaço de Fisioterapia e Recovery"], 4)

    def test_responsavel_can_list_professionals_with_summary_fields(self):
        profissional_user = User.objects.create_user(username="profissional")
        profissional = Profissional.objects.create(
            profile=profissional_user,
            nome="Profissional listado",
            ocupacao="Preparação Física",
        )

        response = self.client.get(reverse("profissional-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        professional_data = next(
            item for item in response.data if item["id"] == profissional.id
        )
        self.assertEqual(professional_data["nome"], "Profissional listado")
        self.assertEqual(
            professional_data["matricula"], profissional.codigo_profissional
        )
        self.assertEqual(professional_data["formacao"], "Preparação Física")

    def test_services_are_read_only_except_for_professional_association(self):
        create_response = self.client.post(
            reverse("servico-list"),
            {"nome": "Fisioterapia"},
            format="json",
        )
        self.assertEqual(
            create_response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )

        profissional_user = User.objects.create_user(username="profissional-servico")
        profissional = Profissional.objects.create(
            profile=profissional_user,
            nome="Profissional do serviço",
            ocupacao="Fisioterapia",
        )
        associate_response = self.client.post(
            reverse("servico-adicionar-profissional", args=[self.servico.id]),
            {"profissional_codigo": profissional.codigo_profissional},
            format="json",
        )

        self.assertEqual(
            associate_response.status_code, status.HTTP_201_CREATED
        )
        self.assertTrue(
            self.servico.profissionais.filter(pk=profissional.pk).exists()
        )

    def test_profissional_formacao_must_match_an_offered_service(self):
        response = self.client.post(
            reverse("profissional-list"),
            {"nome": "Profissional inválido", "ocupacao": "Fisioterapeuta"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("ocupacao", response.data)

    def test_registro_uses_aluno_matricula_for_agendamento(self):
        profissional_user = User.objects.create_user(username="profissional-registro")
        profissional = Profissional.objects.create(
            profile=profissional_user,
            nome="Profissional do registro",
            ocupacao="Fisioterapia",
        )
        agendamento = Agendamento.objects.create(
            data_hora=timezone.make_aware(datetime(2020, 1, 1, 10, 0)),
            aluno=self.aluno,
            profissional=profissional,
            sala=self.sala,
            servico=self.servico,
        )
        self.client.force_authenticate(profissional_user)

        response = self.client.post(
            reverse("registro-treinamento-list"),
            {
                "agendamento": self.aluno.matricula,
                "presenca": "presente",
                "observacoes": "Sem observações.",
                "avaliacao_fisica": "Avaliação inicial.",
                "avaliacao_tecnica": "Avaliação técnica.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["agendamento"], self.aluno.matricula)

    def test_responsavel_cannot_create_registro_treinamento(self):
        response = self.client.post(
            reverse("registro-treinamento-list"),
            {
                "agendamento": self.aluno.matricula,
                "presenca": "presente",
                "observacoes": "Sem observações.",
                "avaliacao_fisica": "Avaliação inicial.",
                "avaliacao_tecnica": "Avaliação técnica.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_registro_cannot_be_created_before_training_time(self):
        profissional_user = User.objects.create_user(
            username="profissional-registro-futuro"
        )
        profissional = Profissional.objects.create(
            profile=profissional_user,
            nome="Profissional futuro",
            ocupacao="Fisioterapia",
        )
        Agendamento.objects.create(
            data_hora=timezone.now() + timedelta(days=1),
            aluno=self.aluno,
            profissional=profissional,
            sala=self.sala,
            servico=self.servico,
        )
        self.client.force_authenticate(profissional_user)

        response = self.client.post(
            reverse("registro-treinamento-list"),
            {
                "agendamento": self.aluno.matricula,
                "presenca": "presente",
                "observacoes": "Sem observações.",
                "avaliacao_fisica": "Avaliação inicial.",
                "avaliacao_tecnica": "Avaliação técnica.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("agendamento", response.data)
