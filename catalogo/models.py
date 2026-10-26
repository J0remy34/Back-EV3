from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator


class Categoria(models.Model):
    nombre = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre de la categoría"
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name="Descripción"
    )
    activa = models.BooleanField(
        default=True,
        verbose_name="Activa"
    )

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre


class Objeto(models.Model):
    ESTADOS = [
        ("DISPONIBLE", "Disponible"),
        ("AGOTADO", "Agotado"),
        ("SUSPENDIDO", "Suspendido"),
    ]

    codigo = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Código del objeto"
    )
    nombre = models.CharField(
        max_length=150,
        verbose_name="Nombre"
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.PROTECT,
        related_name="objetos",
        verbose_name="Categoría"
    )
    descripcion = models.TextField(
        verbose_name="Descripción"
    )
    precio = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name="Precio"
    )
    stock = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Stock"
    )
    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="DISPONIBLE",
        verbose_name="Estado"
    )
    imagen = models.ImageField(
        upload_to="objetos/",
        blank=True,
        null=True,
        verbose_name="Imagen"
    )
    activo = models.BooleanField(
        default=True,
        verbose_name="Activo"
    )
    fecha_creacion = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    fecha_actualizacion = models.DateTimeField(
        auto_now=True,
        verbose_name="Última actualización"
    )

    class Meta:
        verbose_name = "Objeto RPG"
        verbose_name_plural = "Objetos RPG"
        ordering = ["nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"


class PerfilUsuario(models.Model):
    ROLES = [
        ("DUENO", "Dueño"),
        ("ADMINISTRADOR", "Administrador"),
        ("CLIENTE", "Cliente"),
    ]

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="perfil",
        verbose_name="Usuario"
    )
    rut = models.CharField(
        max_length=12,
        unique=True,
        blank=True,
        null=True,
        verbose_name="RUT"
    )
    telefono = models.CharField(
        max_length=20,
        blank=True,
        verbose_name="Teléfono"
    )
    rol = models.CharField(
        max_length=20,
        choices=ROLES,
        default="CLIENTE",
        verbose_name="Rol"
    )

    class Meta:
        verbose_name = "Perfil de usuario"
        verbose_name_plural = "Perfiles de usuarios"

    def __str__(self):
        return f"Perfil de {self.usuario.username}"

    def save(self, *args, **kwargs):
        # Sincroniza los permisos de Django con el rol del perfil.
        # El acceso real a cambiar roles debe restringirse al dueño.
        if self.rol == "DUENO":
            self.usuario.is_staff = True
            self.usuario.is_superuser = True
        else:
            self.usuario.is_staff = False
            self.usuario.is_superuser = False

        self.usuario.save(
            update_fields=["is_staff", "is_superuser"]
        )

        super().save(*args, **kwargs)