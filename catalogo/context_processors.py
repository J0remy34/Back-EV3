
def resumen_carrito(request):
    carrito = request.session.get("carrito", {})

    cantidad_total = 0

    if isinstance(carrito, dict):
        for cantidad in carrito.values():
            try:
                cantidad_total += max(0, int(cantidad))
            except (ValueError, TypeError):
                continue

    return {
        "carrito_cantidad": cantidad_total
    }