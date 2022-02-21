# from django.contrib.auth.models import BaseUserManager
# from django.db.models import Manager
#
#
# class UserManager(BaseUserManager):
#     use_in_migrations = True
#
#     def create_user(self, email, password=None, **extra_fields):
#         """Create user"""
#
#         extra_fields.setdefault("is_superuser", False)  # noqa: WPS425
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         """Create superuser"""
#
#         extra_fields.setdefault("is_superuser", True)  # noqa: WPS425
#         extra_fields.setdefault("is_staff", True)  # noqa: WPS425
#
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")
#
#         if password is None:
#             raise TypeError("Superusers must have a password.")
#
#         return self._create_user(email, password, **extra_fields)
#
#     def get_by_email_hash(self, email_hash: str):
#         """Get user by MD5 email hash"""
#         from apps.authentication.models import User  # noqa: WPS433
#
#         user = self.extra(where=["MD5(email)=%s"], params=[email_hash]).first()
#         if not user:
#             raise User.DoesNotExist()
#         return user
#
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError("Users must have an email address.")
#
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#
#         return user
