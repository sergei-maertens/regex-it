from base64 import b64decode
from typing import Literal, Optional

from django.contrib.auth import authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import connections
from django.http import HttpRequest, JsonResponse
from django.views import View

from pydantic import BaseModel


def _get_cursor():
    return connections["mysql-replica"].cursor()


class ReplicaStatus(BaseModel):
    Slave_IO_State: Optional[str]
    Master_Host: str
    Master_Log_File: str
    Read_Master_Log_Pos: int
    Slave_IO_Running: Literal["Yes", "No", "Preparing"]
    Slave_SQL_Running: Literal["Yes", "No", "Preparing"]
    Seconds_Behind_Master: Optional[int]
    Last_Errno: int
    Last_Error: str

    @property
    def healthy(self) -> bool:
        conditions = (
            self.Slave_IO_Running == "Yes",
            self.Slave_SQL_Running == "Yes",
            self.Seconds_Behind_Master is not None and self.Seconds_Behind_Master < 60,
        )
        return all(conditions)


def get_replica_status() -> ReplicaStatus:
    with _get_cursor() as cursor:
        cursor.execute("show slave status")
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
    kwargs = dict(zip(columns, row))
    return ReplicaStatus(**kwargs)


class ReplicaStatusView(LoginRequiredMixin, View):
    raise_exception = True

    def dispatch(self, request: HttpRequest):
        if auth_header := self.request.headers.get("Authorization"):
            auth = auth_header.split()
            if auth and auth[0].lower() == "basic" and len(auth) == 2:
                auth_decoded = b64decode(auth[1].encode("utf-8")).decode("utf-8")
                userid, _, password = auth_decoded.partition(":")
                user = authenticate(request=request, username=userid, password=password)
                if user is not None:
                    request.user = user
        return super().dispatch(request)

    def get(self, request: HttpRequest):
        replica_status = get_replica_status()
        status_code = 200 if replica_status.healthy else 503
        return JsonResponse(data=replica_status.dict(), status=status_code)
