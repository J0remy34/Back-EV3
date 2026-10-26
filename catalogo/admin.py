from django.contrib import admin

from .models import Categoria, Objeto, PerfilUsuario


# Personalización del panel de administración
admin.site.site_header = "GameLoot - Administración"
admin.site.site_title = "GameLoot Admin"
admin.site.index_title = "Panel de gestión de GameLoot"


@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "activa")
    list_filter = ("activa",)
    search_fields = ("nombre", "descripcion")
    list_editable = ("activa",)

    fieldsets = (
        ("Información de la categoría", {
            "fields": ("nombre", "descripcion"),
        }),
        ("Estado", {
            "fields": ("activa",),
        }),
    )


@admin.register(Objeto)
class ObjetoAdmin(admin.ModelAdmin):
    list_display = (
        "codigo",
        "nombre",
        "categoria",
        "precio",
        "stock",
        "estado",
        "activo",
    )
    list_filter = ("categoria", "estado", "activo")
    search_fields = ("codigo", "nombre", "descripcion")
    list_editable = ("precio", "stock", "estado", "activo")
    list_per_page = 20
    readonly_fields = ("fecha_creacion", "fecha_actualizacion")

    fieldsets = (
        ("Información del objeto", {
            "fields": (
                "codigo",
                "nombre",
                "categoria",
                "descripcion",
                "imagen",
            ),
        }),
        ("Precio y disponibilidad", {
            "fields": (
                "precio",
                "stock",
                "estado",
                "activo",
            ),
        }),
        ("Fechas de registro", {
            "fields": (
                "fecha_creacion",
                "fecha_actualizacion",
            ),
            "classes": ("collapse",),
        }),
    )


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = (
        "usuario",
        "rut",
        "telefono",
        "rol",
    )
    list_filter = ("rol",)
    search_fields = (
        "usuario__username",
        "rut",
        "telefono",
    )
    list_per_page = 20

    # El rol se cambia desde el formulario de edición,
    # no mediante edición rápida en la lista.
    fieldsets = (
        ("Información del usuario", {
            "fields": ("usuario",),
        }),
        ("Datos de contacto", {
            "fields": ("rut", "telefono"),
        }),
        ("Permisos y rol del perfil", {
            "fields": ("rol",),
        }),
    )