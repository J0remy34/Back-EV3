
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

from catalogo.models import Categoria, Objeto


class Command(BaseCommand):
    help = "Carga categorías, objetos RPG y usuarios de prueba para GameLoot"

    def handle(self, *args, **options):
        User = get_user_model()

        # 1. Crear las cuatro categorías
        categorias = [
            ("Armas", "Espadas, arcos y armas mágicas."),
            ("Armaduras", "Cascos, escudos y protecciones."),
            ("Pociones", "Consumibles para aventuras RPG."),
            ("Accesorios", "Anillos, amuletos y objetos especiales."),
        ]

        objetos_categoria = {}

        for nombre, descripcion in categorias:
            categoria, _ = Categoria.objects.update_or_create(
                nombre=nombre,
                defaults={
                    "descripcion": descripcion,
                    "activa": True,
                },
            )
            objetos_categoria[nombre] = categoria

        self.stdout.write(
            self.style.SUCCESS("Categorías creadas correctamente.")
        )

        # 2. Crear ocho objetos de fantasía
        objetos = [
            {
                "codigo": "ARM001",
                "nombre": "Espada del Dragón",
                "categoria": "Armas",
                "descripcion": "Espada legendaria forjada con fuego de dragón.",
                "precio": Decimal("25000.00"),
                "stock": 10,
            },
            {
                "codigo": "ARM002",
                "nombre": "Arco del Bosque",
                "categoria": "Armas",
                "descripcion": "Arco mágico elaborado con madera ancestral.",
                "precio": Decimal("18000.00"),
                "stock": 8,
            },
            {
                "codigo": "ARM003",
                "nombre": "Báculo Arcano",
                "categoria": "Armas",
                "descripcion": "Báculo que canaliza energía mágica.",
                "precio": Decimal("32000.00"),
                "stock": 5,
            },
            {
                "codigo": "ARA001",
                "nombre": "Armadura del Guardián",
                "categoria": "Armaduras",
                "descripcion": "Armadura resistente para aventureros.",
                "precio": Decimal("45000.00"),
                "stock": 4,
            },
            {
                "codigo": "ARA002",
                "nombre": "Escudo de Plata",
                "categoria": "Armaduras",
                "descripcion": "Escudo reforzado contra ataques enemigos.",
                "precio": Decimal("22000.00"),
                "stock": 7,
            },
            {
                "codigo": "POC001",
                "nombre": "Poción de Vida",
                "categoria": "Pociones",
                "descripcion": "Poción que representa un objeto curativo RPG.",
                "precio": Decimal("1500.00"),
                "stock": 30,
            },
            {
                "codigo": "POC002",
                "nombre": "Elixir de Maná",
                "categoria": "Pociones",
                "descripcion": "Elixir mágico para recuperar energía.",
                "precio": Decimal("2000.00"),
                "stock": 20,
            },
            {
                "codigo": "ACC001",
                "nombre": "Amuleto del Lobo",
                "categoria": "Accesorios",
                "descripcion": "Amuleto encantado con el espíritu del bosque.",
                "precio": Decimal("12000.00"),
                "stock": 6,
            },
        ]

        for datos in objetos:
            categoria = objetos_categoria[datos.pop("categoria")]

            Objeto.objects.update_or_create(
                codigo=datos["codigo"],
                defaults={
                    **datos,
                    "categoria": categoria,
                    "estado": (
                        "DISPONIBLE"
                        if datos["stock"] > 0
                        else "AGOTADO"
                    ),
                    "activo": True,
                },
            )

        self.stdout.write(
            self.style.SUCCESS("Ocho objetos RPG cargados correctamente.")
        )

        # 3. Crear usuarios de prueba si no existen
        # Contraseñas únicamente para desarrollo y evaluación local.
        usuarios = [
            {
                "username": "gameloot_admin",
                "email": "admin@example.com",
                "password": "GameLootAdmin2026!",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "gameloot_user",
                "email": "usuario@example.com",
                "password": "GameLootUser2026!",
                "is_staff": False,
                "is_superuser": False,
            },
        ]

        for datos in usuarios:
            usuario, creado = User.objects.get_or_create(
                username=datos["username"],
                defaults={
                    "email": datos["email"],
                    "is_staff": datos["is_staff"],
                    "is_superuser": datos["is_superuser"],
                    "is_active": True,
                },
            )

            if creado:
                usuario.set_password(datos["password"])
                usuario.save()

            elif datos["is_superuser"]:
                # Garantizar permisos de administración del usuario existente.
                usuario.is_staff = True
                usuario.is_superuser = True
                usuario.save(update_fields=["is_staff", "is_superuser"])

        self.stdout.write(
            self.style.SUCCESS("Usuarios de prueba verificados.")
        )

        self.stdout.write(
            self.style.SUCCESS("¡GameLoot está listo para continuar!")
        )