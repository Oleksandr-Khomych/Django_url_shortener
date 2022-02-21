# from typing import List, Optional
#
# from django.conf import settings
# from django.contrib.admin.models import CHANGE, LogEntry
# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import Group, PermissionsMixin
# from django.contrib.contenttypes.models import ContentType
# from django.core.serializers.json import DjangoJSONEncoder
# from django.db import connection, models, transaction
# from django.utils import timezone
# from django.utils.functional import cached_property
# from django.utils.translation import ugettext_lazy as _
# from fcm_django.models import FCMDevice
# from model_utils import FieldTracker
# from oxm_constants.enums.oxygen_backend import UserDocumentType
# from rest_framework_jwt.settings import api_settings
#
#
# )
#
#
# class User(AbstractBaseUser):
#     # Base info
#     email = models.EmailField(unique=True)
#
#     # A timestamp representing when this object was created.
#     created_at = models.DateTimeField(auto_now_add=True, db_index=True)
#     # A timestamp representing when this object was last updated.
#     updated_at = models.DateTimeField(auto_now=True, db_index=True)
#
#     objects = UserManager()
#     tracker = FieldTracker()
#
#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS: List[str] = []
#
#
#
#     class Meta:
#         verbose_name = _("user")  # noqa: WPS121
#         verbose_name_plural = _("users")  # noqa: WPS121
#         indexes = [
#         ]
#
#     def __str__(self):
#         return self.email
#
#     @property
#     def token(self):
#         """Get user jwt token."""
#         return self._generate_jwt_token()
#
#     def _generate_jwt_token(self):
#         """Generate user jwt token"""
#         jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
#         jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
#
#         payload = jwt_payload_handler(self)
#         return jwt_encode_handler(payload)
#
#
#
#
#     # -------------------------------------------------------------------------------------------------------------------------------------
