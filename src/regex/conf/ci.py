# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2019 - 2020 Dimpact
"""
Continuous integration settings module.
"""
import os
import warnings

os.environ.setdefault("IS_HTTPS", "no")
os.environ.setdefault("SECRET_KEY", "dummy")

from .base import *  # noqa isort:skip

# CACHES.update(
#     {
#         "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"},
#     }
# )

ENVIRONMENT = "CI"

# Django privates
SENDFILE_BACKEND = "django_sendfile.backends.development"

# THOU SHALT NOT USE NAIVE DATETIMES
warnings.filterwarnings(
    "error",
    r"DateTimeField .* received a naive datetime",
    RuntimeWarning,
    r"django\.db\.models\.fields",
)
