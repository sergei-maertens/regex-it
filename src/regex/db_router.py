class MariadbReplicaRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return db == "default"
