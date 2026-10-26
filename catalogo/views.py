
from decimal import Decimal, ROUND_HALF_UP

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import AuthenticationForm
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ObjetoForm, RegistroUsuarioForm
from .models import Categoria, Objeto


# =========================
# CATÁLOGO
# =========================

def lista_objetos(request):
    objetos = Objeto.objects.filter(
        activo=True,
        categoria__activa=True,
        estado="DISPONIBLE",
        stock__gt=0,
    ).select_related("categoria")

    busqueda = request.GET.get("q", "").strip()
    categoria_seleccionada = request.GET.get("categoria", "")
    orden = request.GET.get("orden", "nombre")

    if busqueda:
        objetos = objetos.filter(
            Q(nombre__icontains=busqueda)
            | Q(codigo__icontains=busqueda)
            | Q(descripcion__icontains=busqueda)
            | Q(categoria__nombre__icontains=busqueda)
        )

    if categoria_seleccionada:
        objetos = objetos.filter(
            categoria_id=categoria_seleccionada
        )

    ordenes_permitidos = {
        "nombre": "nombre",
        "precio_asc": "precio",
        "precio_desc": "-precio",
    }

    objetos = objetos.order_by(
        ordenes_permitidos.get(orden, "nombre")
    )

    paginator = Paginator(objetos, 8)
    pagina = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "catalogo/lista_objetos.html",
        {
            "objetos": pagina,
            "categorias": Categoria.objects.filter(activa=True),
            "busqueda": busqueda,
            "categoria_seleccionada": categoria_seleccionada,
            "orden_seleccionado": orden,
        },
    )


def detalle_objeto(request, objeto_id):
    objeto = get_object_or_404(
        Objeto.objects.select_related("categoria"),
        id=objeto_id,
        activo=True,
        categoria__activa=True,
    )

    disponible = (
        objeto.estado == "DISPONIBLE"
        and objeto.stock > 0
    )

    return render(
        request,
        "catalogo/detalle_objeto.html",
        {
            "objeto": objeto,
            "disponible": disponible,
        },
    )


# =========================
# CARRITO
# =========================

def obtener_carrito(request):
    carrito = request.session.get("carrito", {})

    if not isinstance(carrito, dict):
        carrito = {}
        request.session["carrito"] = carrito

    return carrito


@require_POST
def agregar_carrito(request, objeto_id):
    objeto = get_object_or_404(
        Objeto,
        id=objeto_id,
        activo=True,
        estado="DISPONIBLE",
    )

    if objeto.stock <= 0:
        messages.error(request, "Este objeto no tiene stock.")
        return redirect("lista_objetos")

    carrito = obtener_carrito(request)
    clave = str(objeto.id)

    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except (ValueError, TypeError):
        cantidad = 1

    if cantidad < 1:
        messages.error(request, "La cantidad debe ser mayor que cero.")
    elif carrito.get(clave, 0) + cantidad > objeto.stock:
        messages.error(request, "No hay stock suficiente para esa cantidad.")
    else:
        carrito[clave] = carrito.get(clave, 0) + cantidad
        request.session["carrito"] = carrito
        request.session.modified = True
        messages.success(request, f"{objeto.nombre} se añadió al carrito.")

    referer = request.META.get("HTTP_REFERER")
    if referer:
        return redirect(referer)

    return redirect("detalle_objeto", objeto_id=objeto.id)


def ver_carrito(request):
    carrito = obtener_carrito(request)
    elementos = []
    subtotal = Decimal("0.00")

    for clave, cantidad in carrito.items():
        try:
            objeto_id = int(clave)
            cantidad = int(cantidad)
        except (ValueError, TypeError):
            continue

        if cantidad < 1:
            continue

        objeto = Objeto.objects.filter(
            id=objeto_id,
            activo=True,
        ).first()

        if objeto is None:
            continue

        cantidad = min(cantidad, objeto.stock)
        precio_total = objeto.precio * cantidad
        subtotal += precio_total

        elementos.append({
            "objeto": objeto,
            "cantidad": cantidad,
            "subtotal": precio_total,
        })

    iva = (subtotal * Decimal("0.19")).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP,
    )
    total = subtotal + iva

    return render(
        request,
        "catalogo/carrito.html",
        {
            "elementos": elementos,
            "subtotal": subtotal,
            "iva": iva,
            "total": total,
        },
    )


@require_POST
def actualizar_carrito(request, objeto_id):
    carrito = obtener_carrito(request)
    clave = str(objeto_id)

    objeto = get_object_or_404(
        Objeto,
        id=objeto_id,
        activo=True,
    )

    try:
        cantidad = int(request.POST.get("cantidad", 1))
    except (ValueError, TypeError):
        cantidad = 1

    if cantidad <= 0:
        carrito.pop(clave, None)
        messages.info(request, "Objeto eliminado del carrito.")
    elif cantidad > objeto.stock:
        messages.error(request, "La cantidad supera el stock disponible.")
    else:
        carrito[clave] = cantidad
        messages.success(request, "Cantidad actualizada.")

    request.session["carrito"] = carrito
    request.session.modified = True

    return redirect("ver_carrito")


@require_POST
def eliminar_carrito(request, objeto_id):
    carrito = obtener_carrito(request)
    carrito.pop(str(objeto_id), None)

    request.session["carrito"] = carrito
    request.session.modified = True

    messages.success(request, "Objeto eliminado del carrito.")
    return redirect("ver_carrito")


@require_POST
def vaciar_carrito(request):
    request.session["carrito"] = {}
    request.session.modified = True

    messages.success(request, "El carrito está vacío.")
    return redirect("ver_carrito")


# =========================
# AUTENTICACIÓN
# =========================

def login_usuario(request):
    if request.user.is_authenticated:
        return redirect("lista_objetos")

    if request.method == "POST":
        form = AuthenticationForm(
            request,
            data=request.POST,
        )

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            messages.success(request, "Has iniciado sesión correctamente.")

            destino = request.GET.get("next", "")
            if destino.startswith("/") and not destino.startswith("//"):
                return redirect(destino)

            return redirect("lista_objetos")
        else:
            messages.error(
                request,
                "No se pudo iniciar sesión. Revisa tu usuario y contraseña.",
            )
    else:
        form = AuthenticationForm(request)

    for campo in form.fields.values():
        campo.widget.attrs["class"] = "form-control"

    return render(
        request,
        "catalogo/login.html",
        {"form": form},
    )


def registro_usuario(request):
    if request.user.is_authenticated:
        return redirect("lista_objetos")

    if request.method == "POST":
        form = RegistroUsuarioForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                "¡Tu cuenta se creó correctamente! Ya puedes iniciar sesión.",
            )
            return redirect("login")
        else:
            messages.error(
                request,
                "Revisa los campos marcados para corregir el formulario.",
            )
    else:
        form = RegistroUsuarioForm()

    return render(
        request,
        "catalogo/registro.html",
        {"form": form},
    )


@require_POST
def logout_usuario(request):
    logout(request)
    messages.success(request, "Has cerrado sesión.")
    return redirect("lista_objetos")


# =========================
# ADMINISTRACIÓN DE OBJETOS
# =========================

def es_administrador(usuario):
    return usuario.is_authenticated and usuario.is_staff


@login_required
@user_passes_test(es_administrador)
def gestionar_objetos(request):
    objetos = Objeto.objects.select_related("categoria").order_by("nombre")

    return render(
        request,
        "catalogo/gestionar_objetos.html",
        {"objetos": objetos},
    )


@login_required
@user_passes_test(es_administrador)
def crear_objeto(request):
    if request.method == "POST":
        form = ObjetoForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Objeto creado correctamente.")
            return redirect("gestionar_objetos")
    else:
        form = ObjetoForm()

    return render(
        request,
        "catalogo/formulario_objeto.html",
        {
            "form": form,
            "titulo": "Crear objeto",
        },
    )


@login_required
@user_passes_test(es_administrador)
def editar_objeto(request, objeto_id):
    objeto = get_object_or_404(Objeto, id=objeto_id)

    if request.method == "POST":
        form = ObjetoForm(
            request.POST,
            request.FILES,
            instance=objeto,
        )

        if form.is_valid():
            form.save()
            messages.success(request, "Objeto actualizado correctamente.")
            return redirect("gestionar_objetos")
    else:
        form = ObjetoForm(instance=objeto)

    return render(
        request,
        "catalogo/formulario_objeto.html",
        {
            "form": form,
            "titulo": "Editar objeto",
            "objeto": objeto,
        },
    )


@login_required
@user_passes_test(es_administrador)
@require_POST
def eliminar_objeto(request, objeto_id):
    objeto = get_object_or_404(Objeto, id=objeto_id)
    objeto.activo = False
    objeto.save(update_fields=["activo"])

    messages.success(request, "Objeto desactivado correctamente.")
    return redirect("gestionar_objetos")