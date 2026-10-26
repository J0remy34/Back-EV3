from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .models import PerfilUsuario

User = get_user_model()


@receiver(post_save, sender=User)
def asignar_rol_automatico(
    sender,
    instance,
    created,
    **kwargs
):
    # Si es la primera creación de un superusuario,
    # asignarle el rol DUENO.
    if created and instance.is_superuser:
        perfil, _ = PerfilUsuario.objects.get_or_create(
            usuario=instance,
            defaults={"rol": "DUENO"},
        )

        if perfil.rol != "DUENO":
            perfil.rol = "DUENO"
            perfil.save(update_fields=["rol"])

    # Los usuarios normales deben tener perfil de cliente.
    elif created:
        PerfilUsuario.objects.get_or_create(
            usuario=instance,
            defaults={"rol": "CLIENTE"},
        )