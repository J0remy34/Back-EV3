# 🐉 GameLoot — Tienda de objetos RPG

## 📋 Descripción del proyecto

GameLoot es una aplicación web desarrollada con Python y Django que permite explorar y gestionar objetos de un mundo RPG. Los usuarios pueden consultar un catálogo de objetos, buscar artículos y agregarlos a un carrito de compras.

El sistema incluye registro de usuarios, inicio de sesión y herramientas de administración para gestionar los objetos disponibles en la tienda.

## 🛠️ Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Django:** framework para el desarrollo web.
- **SQLite:** base de datos.
- **HTML5 y CSS3:** estructura y estilos.
- **Bootstrap 5:** diseño adaptable a distintos dispositivos.
- **Git y GitHub:** control de versiones y almacenamiento del código.
- **Pillow:** soporte para imágenes.

## ✨ Funcionalidades

### Catálogo de objetos
- Visualización de objetos disponibles.
- Búsqueda por nombre, código, descripción o categoría.
- Filtros por categoría.
- Ordenamiento por nombre y precio.
- Paginación de resultados.
- Vista de detalles de cada objeto.

### Carrito de compras
- Agregar objetos al carrito.
- Modificar cantidades.
- Eliminar objetos individuales.
- Vaciar el carrito.
- Calcular subtotal, IVA del 19 % y total.
- Validar el stock disponible.

### Usuarios y seguridad
- Registro de nuevas cuentas.
- Inicio y cierre de sesión.
- Perfiles con RUT, teléfono y rol.
- Protección de páginas administrativas.
- Validación de los datos ingresados.
- Protección CSRF en los formularios.

### Administración
- Crear objetos.
- Editar información, precios y stock.
- Subir imágenes.
- Desactivar objetos sin eliminarlos definitivamente.
- Administrar categorías, objetos y perfiles desde Django Admin.

## 📁 Estructura del proyecto

```text
back/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── catalogo/
│   ├── management/
│   ├── templates/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
├── media/
├── .env.example
├── .gitignore
├── manage.py
├── requirements.txt
└── README.md
```

*La estructura puede variar según los archivos presentes en el proyecto.*

## ⚙️ Requisitos

- Python 3.13 o una versión compatible con las dependencias del proyecto.
- pip.
- Git.
- Un navegador web moderno.

## 🚀 Instalación y ejecución

### 1. Clonar el repositorio

```bash
git clone https://github.com/J0remy34/Back-EV3.git
cd Back-EV3
```

### 2. Crear un entorno virtual

En Windows:

```powershell
py -m venv .venv
```

Activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Copia `.env.example` y crea un archivo `.env` local. Configura una clave secreta propia y los valores adecuados para tu entorno.

No publiques el archivo `.env` en GitHub.

### 5. Aplicar las migraciones

```powershell
python manage.py migrate
```

### 6. Cargar datos de prueba

Si el comando de carga de datos está incluido:

```powershell
python manage.py poblar_datos
```

### 7. Crear un administrador

Si todavía no existe una cuenta administrativa:

```powershell
python manage.py createsuperuser
```

### 8. Ejecutar el servidor

```powershell
python manage.py runserver
```

Abre la aplicación en:

http://127.0.0.1:8000/

El panel de administración de Django se encuentra en:

http://127.0.0.1:8000/admin/

## 🧪 Pruebas recomendadas

- Registrar una cuenta e iniciar sesión.
- Buscar objetos y aplicar filtros.
- Agregar objetos al carrito y modificar cantidades.
- Verificar los cálculos del subtotal, IVA y total.
- Comprobar las validaciones de precio, stock y código.
- Verificar que un usuario normal no pueda acceder a las funciones administrativas.
- Crear, editar y desactivar objetos desde la administración.

## 🔐 Consideraciones de seguridad

- No publicar claves secretas ni contraseñas en el repositorio.
- Mantener `.env`, `.venv/` y la base de datos local fuera de GitHub, según la configuración del proyecto.
- Utilizar contraseñas seguras para las cuentas administrativas.
- Revisar las validaciones y los permisos antes de desplegar la aplicación en producción.

## 🤖 Uso de inteligencia artificial

Durante el desarrollo se utilizó ChatGPT como herramienta de apoyo para:

1. Orientar la estructura del proyecto Django y la organización de sus archivos.
2. Apoyar la implementación y revisión de formularios, validaciones y autenticación.
3. Ayudar a revisar errores, depurar funcionalidades y documentar la aplicación.

El código debe ser revisado y probado por el equipo antes de su entrega.

## 👥 Equipo de desarrollo

- **Integrante 1:** Jeremy Rincon
- **Integrante 2:** [Nombre del integrante]

## 📦 Repositorio

Código fuente: https://github.com/J0remy34/Back-EV3

---

**Proyecto académico — GameLoot**