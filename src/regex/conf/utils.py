import logging
from typing import TypeVar, Union, cast

from django.utils.module_loading import import_string

from decouple import Csv, Undefined, config as _config, undefined
from sentry_sdk.integrations import DidNotEnable, django

logger = logging.getLogger(__name__)

T = TypeVar("T")


def config(option: str, default: Union[T, Undefined] = undefined, *args, **kwargs) -> T:
    """
    Pull a config parameter from the environment.

    Read the config variable ``option``. If it's optional, use the ``default`` value.
    Input is automatically cast to the correct type, where the type is derived from the
    default value if possible.

    Pass ``split=True`` to split the comma-separated input into a list.
    """
    if "split" in kwargs:
        kwargs.pop("split")
        kwargs["cast"] = Csv()
        if default == []:
            default = ""

    if default is not undefined and default is not None:
        kwargs.setdefault("cast", type(default))
    return cast(T, _config(option, default=default, *args, **kwargs))


SENTRY_EXTRAS = [
    "sentry_sdk.integrations.celery.CeleryIntegration",
    # "sentry_sdk.integrations.redis.RedisIntegration",
]


def get_sentry_integrations() -> list:
    """
    Determine which Sentry SDK integrations to enable.
    """
    default = [django.DjangoIntegration()]
    extra = []

    for _extra in SENTRY_EXTRAS:
        try:
            integration_cls = import_string(_extra)
        except DidNotEnable:  # happens if the celery import fails by the integration
            continue
        extra.append(integration_cls())

    return [*default, *extra]
