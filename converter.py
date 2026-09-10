"""
Conversor de Unidades - v1
Categorías incluidas: Length, Mass
(Area y Volumen se agregarán en una v2 sin tocar la lógica de conversión)

Cómo escala:
Para agregar una nueva categoría (ej. "Area") solo hay que añadir una
entrada nueva al diccionario CONVERSIONS con su unidad base y factores.
El resto de la app (dropdowns, cálculo, UI) funciona automáticamente.
"""

import customtkinter as ctk

from version import __version__

# ---------------------------------------------------------------------------
# DATOS DE CONVERSIÓN
# ---------------------------------------------------------------------------
# Cada categoría define una unidad "base" (factor 1.0) y el resto de unidades
# expresadas como "cuánto vale 1 unidad de esta, en unidades base".
# Para convertir: valor_en_base = valor * factor_origen
#                 resultado     = valor_en_base / factor_destino

CONVERSIONS = {
    "Length": {
        "meter": 1.0,
        "kilometer": 1000.0,
        "centimeter": 0.01,
        "millimeter": 0.001,
        "mile": 1609.34,
        "yard": 0.9144,
        "foot": 0.3048,
        "inch": 0.0254,
    },
    "Mass": {
        "kilogram": 1.0,
        "gram": 0.001,
        "milligram": 0.000001,
        "pound": 0.453592,
        "ounce": 0.0283495,
        "metric_ton": 1000.0,
    },
    # --- Para la v2, se agregaría algo así ---
    # "Area": {
    #     "square_meter": 1.0,
    #     "square_kilometer": 1_000_000.0,
    #     "hectare": 10_000.0,
    #     "acre": 4046.86,
    #     ...
    # },
    # "Volume": {
    #     "liter": 1.0,
    #     "milliliter": 0.001,
    #     "cubic_meter": 1000.0,
    #     "gallon": 3.78541,
    #     ...
    # },
}


def convert(category: str, value: float, from_unit: str, to_unit: str) -> float:
    """Convierte 'value' de 'from_unit' a 'to_unit' dentro de 'category'."""
    factors = CONVERSIONS[category]
    value_in_base = value * factors[from_unit]
    return value_in_base / factors[to_unit]


# ---------------------------------------------------------------------------
# INTERFAZ GRÁFICA
# ---------------------------------------------------------------------------

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class ConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Conversor de Unidades v{__version__}")
        self.geometry("420x400")
        self.resizable(False, False)

        # --- Título ---
        title_label = ctk.CTkLabel(
            self, text="Conversor de Unidades", font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(20, 10))

        # --- Selector de categoría ---
        self.category_var = ctk.StringVar(value=list(CONVERSIONS.keys())[0])
        category_menu = ctk.CTkOptionMenu(
            self,
            values=list(CONVERSIONS.keys()),
            variable=self.category_var,
            command=self.on_category_change,
        )
        category_menu.pack(pady=10)

        # --- Entrada de valor ---
        self.value_entry = ctk.CTkEntry(self, placeholder_text="Ingresá un valor")
        self.value_entry.pack(pady=10, padx=40, fill="x")

        # --- Frame con dos dropdowns (De -> A) ---
        units_frame = ctk.CTkFrame(self, fg_color="transparent")
        units_frame.pack(pady=10)

        self.from_var = ctk.StringVar()
        self.to_var = ctk.StringVar()

        self.from_menu = ctk.CTkOptionMenu(units_frame, values=[], variable=self.from_var)
        self.from_menu.grid(row=0, column=0, padx=10)

        arrow_label = ctk.CTkLabel(units_frame, text="→", font=ctk.CTkFont(size=18))
        arrow_label.grid(row=0, column=1, padx=5)

        self.to_menu = ctk.CTkOptionMenu(units_frame, values=[], variable=self.to_var)
        self.to_menu.grid(row=0, column=2, padx=10)

        # --- Botón convertir ---
        convert_btn = ctk.CTkButton(self, text="Convertir", command=self.on_convert)
        convert_btn.pack(pady=20)

        # --- Resultado ---
        self.result_label = ctk.CTkLabel(
            self, text="", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.result_label.pack(pady=10)

        # Inicializar dropdowns con la primera categoría
        self.on_category_change(self.category_var.get())

    def on_category_change(self, category: str):
        """Actualiza las opciones de los dropdowns 'de' y 'a' según la categoría."""
        units = list(CONVERSIONS[category].keys())
        self.from_menu.configure(values=units)
        self.to_menu.configure(values=units)
        self.from_var.set(units[0])
        self.to_var.set(units[1] if len(units) > 1 else units[0])
        self.result_label.configure(text="")

    def on_convert(self):
        category = self.category_var.get()
        from_unit = self.from_var.get()
        to_unit = self.to_var.get()

        try:
            value = float(self.value_entry.get())
        except ValueError:
            self.result_label.configure(text="⚠ Ingresá un número válido", text_color="red")
            return

        result = convert(category, value, from_unit, to_unit)
        self.result_label.configure(
            text=f"{value} {from_unit} = {result:.6g} {to_unit}",
            text_color="white",
        )


if __name__ == "__main__":
    app = ConverterApp()
    app.mainloop()