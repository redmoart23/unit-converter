"""
Fuente única de verdad para la versión de la app.
- El instalador (Inno Setup) lee este valor para nombrar el release.
- La app lo usa para compararse contra la última versión en GitHub.
- El workflow de CI también lo puede leer para taggear el build.

Convención: Semantic Versioning (MAJOR.MINOR.PATCH)
"""

__version__ = "1.0.0"