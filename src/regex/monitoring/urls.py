from django.urls import path

from .mysql_replica import ReplicaStatusView

app_name = "monitoring"

urlpatterns = [
    path("mysql-replica/", ReplicaStatusView.as_view(), name="mysql-replica-status"),
]
