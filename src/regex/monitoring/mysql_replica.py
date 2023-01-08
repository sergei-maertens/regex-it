from django.db import connections


def _get_cursor():
    return connections["mysql-replica"].cursor()


def get_replica_status():
    with _get_cursor() as cursor:
        cursor.execute("show slave status")
        columns = [col[0] for col in cursor.description]
        row = cursor.fetchone()
        result = dict(zip(columns, row))

    print(result)
