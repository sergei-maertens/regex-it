from regex.utils.connections import can_connect

from .utils import config

ALIAS = "mysql-replica"


def get_mysql_db_config() -> dict:
    settings_dict = {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config("MYSQL_REPLICA_DB_NAME", ""),
        "USER": config("MYSQL_REPLICA_DB_USER", "mysql"),
        "PASSWORD": config("MYSQL_REPLICA_DB_PASSWORD", "mysql"),
        "HOST": config("MYSQL_REPLICA_DB_HOST", "localhost"),
        "PORT": config("MYSQL_REPLICA_DB_PORT", 3306),
        "TEST": {
            "MIGRATE": False,
            "DEPENDENCIES": [],
        },
    }
    conn_host = f"{settings_dict['HOST']}:{settings_dict['PORT']}"
    if not can_connect(conn_host):
        return {}
    return {ALIAS: settings_dict}
