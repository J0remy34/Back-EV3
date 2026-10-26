
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Categoria, Objeto, PerfilUsuario


class ObjetoForm(forms.ModelForm):
    class Meta:
        model = Objeto
        fields = [
            "codigo",
            "nombre",
            "categoria",
            "descripcion",
            "precio",
            "stock",
            "estado",
            "imagen",
            "activo",
        ]
        widgets = {
            "codigo": forms.TextInput(attrs={"class": "form-control"}),
            "nombre": forms.TextInput(attrs={"class": "form-control"}),
            "categoria": forms.Select(attrs={"class": "form-select"}),
            "descripcion": forms.Textarea(
                attrs={"class": "form-control", "rows": 4}
            ),
            "precio": forms.NumberInput(
                attrs={"class": "form-control", "min": "0", "step": "0.01"}
            ),
            "stock": forms.NumberInput(
                attrs={"class": "form-control", "min": "0"}
            ),
            "estado": forms.Select(attrs={"class": "form-select"}),
            "imagen": forms.ClearableFileInput(
                attrs={"class": "form-control"}
            ),
            "activo": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
        }

    def clean_codigo(self):
        codigo = self.cleaned_data["codigo"].strip().upper()

        if not codigo.isalnum():
            raise forms.ValidationError(
                "El código debe contener solamente letras y números."
            )

        return codigo

    def clean_nombre(self):
        nombre = self.cleaned_data["nombre"].strip()

        if not nombre:
            raise forms.ValidationError("El nombre es obligatorio.")

        return nombre

    def clean_precio(self):
        precio = self.cleaned_data["precio"]

        if precio < 0:
            raise forms.ValidationError(
                "El precio no puede ser negativo."
            )

        return precio

    def clean_stock(self):
        stock = self.cleaned_data["stock"]

        if stock < 0:
            raise forms.ValidationError(
                "El stock no puede ser negativo."
            )

        return stock


class RegistroUsuarioForm(UserCreationForm):
    rut = forms.CharField(
        max_length=12,
        required=False,
        label="RUT",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej.: 12345678-9",
            }
        ),
    )

    telefono = forms.CharField(
        max_length=20,
        required=False,
        label="Teléfono",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ej.: +56912345678",
            }
        ),
    )

    email = forms.EmailField(
        required=True,
        label="Correo electrónico",
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "correo@ejemplo.com",
            }
        ),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for campo in self.fields.values():
            campo.help_text = ""
            if not isinstance(campo.widget, forms.CheckboxInput):
                campo.widget.attrs["class"] = "form-control"

        self.fields["username"].label = "Nombre de usuario"
        self.fields["password1"].label = "Contraseña"
        self.fields["password2"].label = "Confirmar contraseña"

    def clean_rut(self):
        rut = self.cleaned_data.get("rut", "").strip().upper()

        if rut and PerfilUsuario.objects.filter(rut=rut).exists():
            raise forms.ValidationError(
                "Este RUT ya está registrado."
            )

        return rut

    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.email = self.cleaned_data["email"]

        if commit:
            usuario.save()
            PerfilUsuario.objects.create(
                usuario=usuario,
                rut=self.cleaned_data.get("rut") or None,
                telefono=self.cleaned_data.get("telefono", ""),
                rol="CLIENTE",
            )

        return usuario