from base64 import b64encode
from unittest.mock import patch

from django.conf import settings
from django.db import connections
from django.test import TestCase
from django.urls import reverse_lazy

from regex.accounts.tests.factories import UserFactory

from ..mysql_replica import ReplicaStatus

HOST_REPLICA = "localhost:3308"  # see docker-compose.mariadb.yml

if "mysql-replica" in settings.DATABASES:

    class ReplicaHealtCheckTests(TestCase):
        databases = {"default", "mysql-replica"}
        url = reverse_lazy("monitoring:mysql-replica-status")

        def setUp(self):
            super().setUp()
            user = UserFactory.create()
            self.client.force_login(user=user)

        def test_replica_up_and_running(self):
            response = self.client.get(self.url)

            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data["Slave_IO_Running"], "Yes")
            self.assertEqual(data["Slave_SQL_Running"], "Yes")

        def test_replica_not_up(self):
            conn = connections["mysql-replica"]
            try:
                with conn.cursor() as cursor:
                    cursor.execute("stop slave;")

                response = self.client.get(self.url)

            finally:
                with conn.cursor() as cursor:
                    cursor.execute("start slave;")

            self.assertEqual(response.status_code, 503)
            data = response.json()
            self.assertEqual(data["Slave_IO_Running"], "No")
            self.assertEqual(data["Slave_SQL_Running"], "No")


class ReplicaHealtCheckAuthTests(TestCase):
    url = reverse_lazy("monitoring:mysql-replica-status")

    def setUp(self):
        super().setUp()

        patcher = patch(
            "regex.monitoring.mysql_replica.get_replica_status",
            return_value=ReplicaStatus(
                Slave_IO_State="",
                Master_Host="primary",
                Master_Log_File="primary1.bin",
                Read_Master_Log_Pos=10,
                Slave_IO_Running="Yes",
                Slave_SQL_Running="Yes",
                Seconds_Behind_Master=0,
                Last_Errno=0,
                Last_Error="",
            ),
        )
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_auth_required(self):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 403)

    def test_logged_in_as_user(self):
        user = UserFactory.create()
        self.client.force_login(user=user)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)

    def test_basic_auth_header(self):
        user = UserFactory.create(email="uptimerobot@example.com", password="letme:in")
        credentials = b64encode(b"uptimerobot@example.com:letme:in").decode("ascii")

        response = self.client.get(self.url, HTTP_AUTHORIZATION=f"Basic {credentials}")

        self.assertEqual(response.status_code, 200)
