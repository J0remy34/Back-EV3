# 🐉 GameLoot — Tienda de objetos RPG

## 📋 Descripción del proyecto

GameLoot es una aplicación web desarrollada con Python y Django que permite explorar y gestionar objetos de un mundo RPG. Los usuarios pueden consultar un catálogo de objetos, buscar artículos y agregarlos a un carrito de compras.

El sistema incluye registro de usuarios, inicio de sesión, perfiles con roles y herramientas administrativas para gestionar los objetos disponibles en la tienda.

## 🛠️ Tecnologías utilizadas

- **Python:** lenguaje de programación.
- **Django:** framework para el desarrollo web.
- **SQLite:** base de datos.
- **HTML5 y CSS3:** estructura y estilos de la interfaz.
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
- Asignación automática de perfiles mediante señales de Django.
- Protección de páginas según los permisos del usuario.
- Validación de los datos ingresados.
- Protección CSRF en los formularios.

### 👥 Roles y permisos

GameLoot contempla tres roles de usuario:

- **Dueño (`DUENO`):** cuenta responsable de la administración general, con acceso al panel de administración de Django.
- **Administrador (`ADMINISTRADOR`):** puede gestionar los objetos del catálogo mediante las funciones autorizadas de la tienda, sin acceso al panel de administración de Django ni a la gestión de usuarios y roles.
- **Cliente (`CLIENTE`):** puede consultar el catálogo y utilizar las funciones disponibles para los clientes.

#### Asignación de roles

- Las cuentas creadas como superusuario reciben el rol `DUENO` mediante la señal configurada.
- Los usuarios normales reciben el rol `CLIENTE` al crearse su perfil.
- El dueño puede asignar el rol `ADMINISTRADOR` a las cuentas autorizadas.

El registro público debe asignar siempre el rol `CLIENTE` y no permitir que el usuario elija o modifique sus propios permisos.

**Nota:** la señal actual asigna el rol `DUENO` a las cuentas creadas como superusuario; no comprueba si son la primera cuenta creada en el sistema.

### Administración

- Crear objetos.
- Editar información, precios y stock.
- Subir imágenes.
- Desactivar objetos sin eliminarlos definitivamente.
- Administrar categorías, objetos y perfiles desde Django Admin, según los permisos de la cuenta.

## 📁 Estructura del proyecto

```text
Back-EV3/
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── catalogo/
│   ├── management/
│   ├── templates/
│   ├── apps.py
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── signals.py
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

En Windows, ejecuta:

```powershell
py -m venv .venv
```

Para activarlo en PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar las dependencias

```powershell
python -m pip install -r requirements.txt
```

### 4. Configurar las variables de entorno

Crea un archivo `.env` local tomando como referencia `.env.example`. Configura una clave secreta propia y los valores necesarios para el entorno.

No publiques el archivo `.env` en GitHub ni incluyas contraseñas o claves secretas en el repositorio.

### 5. Aplicar las migraciones

```powershell
python manage.py makemigrations
python manage.py migrate
```

Si no hay cambios pendientes en los modelos, puede que `makemigrations` indique que no hay cambios que realizar.

### 6. Cargar datos de prueba

Si el comando de carga de datos está incluido en el proyecto:

```powershell
python manage.py poblar_datos
```

Si no existe ese comando, omite este paso.

### 7. Crear una cuenta de dueño

Si todavía no existe una cuenta de dueño, puedes crear una cuenta de superusuario:

```powershell
python manage.py createsuperuser
```

La señal configurada asignará el rol `DUENO` cuando detecte la creación de un superusuario.

Si ya existen cuentas, revisa sus perfiles y permisos antes de realizar cambios.

### 8. Ejecutar el servidor

```powershell
python manage.py runserver
```

Aplicación web:

http://127.0.0.1:8000/

Panel de administración de Django:

http://127.0.0.1:8000/admin/

## 🧪 Pruebas recomendadas

- Registrar una cuenta e iniciar sesión.
- Buscar objetos y aplicar filtros.
- Agregar objetos al carrito y modificar cantidades.
- Verificar los cálculos del subtotal, IVA y total.
- Comprobar las validaciones de precio, stock y código.
- Verificar que un cliente no pueda acceder a las funciones administrativas.
- Verificar que un administrador de la tienda no pueda entrar a Django Admin ni gestionar roles.
- Comprobar que solo el dueño pueda asignar roles.
- Crear, editar y desactivar objetos desde las funciones de administración correspondientes.

## 🔐 Consideraciones de seguridad

- No publicar claves secretas ni contraseñas en el repositorio.
- Mantener `.env`, `.venv/` y la base de datos local fuera de GitHub, según la configuración del proyecto.
- Utilizar contraseñas seguras para las cuentas administrativas.
- Restringir los cambios de roles a usuarios autorizados.
- Revisar las validaciones y los permisos antes de desplegar la aplicación en producción.
- No considerar una opción de interfaz como una medida de seguridad: los permisos deben comprobarse también en el servidor.

## 🤖 Uso de inteligencia artificial

Durante el desarrollo se utilizó ChatGPT como herramienta de apoyo para:

1. Orientar la estructura del proyecto Django y la organización de sus archivos.
2. Apoyar la implementación y revisión de formularios, validaciones y autenticación.
3. Ayudar a revisar errores, depurar funcionalidades y documentar la aplicación.

El código debe ser revisado y probado por el equipo antes de su entrega.

## 👥 Equipo de desarrollo

- **Integrante 1:** Jeremy Rincon.
- **Integrante 2:** [Nombre del integrante].

## 📦 Repositorio

Código fuente: [https://github.com/J0remy34/Back-EV3](https://github.com/J0remy34/Back-EV3)

---

**Proyecto académico — GameLoot**