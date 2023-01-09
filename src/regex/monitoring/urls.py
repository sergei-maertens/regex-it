from django.urls import path

from .mysql_replica import ReplicaStatusView

urlpatterns = [
    path("mysql-replica/", ReplicaStatusView.as_view(), name="mysql-replica-status"),
]
