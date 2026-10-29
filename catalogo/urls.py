from django.urls import path
from . import views


urlpatterns = [
    # =========================
    # CATÁLOGO DE OBJETOS
    # =========================
    path(
        "",
        views.lista_objetos,
        name="lista_objetos",
    ),
    path(
        "objeto/<int:objeto_id>/",
        views.detalle_objeto,
        name="detalle_objeto",
    ),

    # =========================
    # CARRITO DE COMPRAS
    # =========================
    path(
        "carrito/",
        views.ver_carrito,
        name="ver_carrito",
    ),
    path(
        "carrito/agregar/<int:objeto_id>/",
        views.agregar_carrito,
        name="agregar_carrito",
    ),
    path(
        "carrito/actualizar/<int:objeto_id>/",
        views.actualizar_carrito,
        name="actualizar_carrito",
    ),
    path(
        "carrito/eliminar/<int:objeto_id>/",
        views.eliminar_carrito,
        name="eliminar_carrito",
    ),
    path(
        "carrito/vaciar/",
        views.vaciar_carrito,
        name="vaciar_carrito",
    ),

    # =========================
    # AUTENTICACIÓN
    # =========================
    path(
        "login/",
        views.login_usuario,
        name="login",
    ),
    path(
        "registro/",
        views.registro_usuario,
        name="registro",
    ),
    path(
        "logout/",
        views.logout_usuario,
        name="logout",
    ),

    # =========================
    # GESTIÓN DE OBJETOS
    # =========================
    path(
        "gestionar/",
        views.gestionar_objetos,
        name="gestionar_objetos",
    ),
    path(
        "gestionar/crear/",
        views.crear_objeto,
        name="crear_objeto",
    ),
    path(
        "gestionar/editar/<int:objeto_id>/",
        views.editar_objeto,
        name="editar_objeto",
    ),
    path(
        "gestionar/eliminar/<int:objeto_id>/",
        views.eliminar_objeto,
        name="eliminar_objeto",
    ),
    path(
        "gestionar/reactivar/<int:objeto_id>/",
        views.reactivar_objeto,
        name="reactivar_objeto",
    ),
    path(
        "gestionar/eliminar-definitivamente/<int:objeto_id>/",
        views.eliminar_permanentemente_objeto,
        name="eliminar_permanentemente_objeto",
    ),
]