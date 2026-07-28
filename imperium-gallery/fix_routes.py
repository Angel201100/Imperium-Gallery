from pathlib import Path
import re

root = Path(__file__).resolve().parent

# map old file names to standardized index.html location
rename_map = {
    root / 'artistas' / 'artistas.html': root / 'artistas' / 'index.html',
    root / 'fotografias' / 'fotografias.html': root / 'fotografias' / 'index.html',
    root / 'pinturas' / 'pinturas.html': root / 'pinturas' / 'index.html',
    root / 'licencias' / 'licencias.html': root / 'licencias' / 'index.html',
    root / 'nosotros' / 'nosotros.html': root / 'nosotros' / 'index.html',
    root / 'preguntas' / 'preguntas.html': root / 'preguntas' / 'index.html',
    root / 'contacto' / 'contacto.html': root / 'contacto' / 'index.html',
    root / 'obra' / 'obra.html': root / 'obra' / 'index.html',
}

# remove any old redirect placeholder if it exists before renaming actual content
placeholder = root / 'artistas' / 'index.html'
if placeholder.exists() and placeholder.is_file():
    try:
        text = placeholder.read_text(encoding='utf-8')
        if 'redirigiendo' in text.lower():
            placeholder.unlink()
    except Exception:
        pass

for src, dst in rename_map.items():
    if src.exists():
        if dst.exists():
            dst.unlink()
        src.replace(dst)

# update root redirect to canonical homepage path
root_index = root / 'index.html'
if root_index.exists():
    text = root_index.read_text(encoding='utf-8')
    text = re.sub(r'<meta http-equiv="refresh" content="0; url=[^"]+">', '<meta http-equiv="refresh" content="0; url=./inicio/index.html">', text)
    text = text.replace('href="./inicio/inicio.html"', 'href="./inicio/index.html"')
    root_index.write_text(text, encoding='utf-8')

# canonical link mapping for pages
path_updates = {
    '../inicio/inicio.html': '../inicio/index.html',
    '../fotografias/fotografias.html': '../fotografias/index.html',
    '../pinturas/pinturas.html': '../pinturas/index.html',
    '../artistas/artistas.html': '../artistas/index.html',
    '../artista/artista.html': '../artista/index.html',
    '../licencias/licencias.html': '../licencias/index.html',
    '../nosotros/nosotros.html': '../nosotros/index.html',
    '../preguntas/preguntas.html': '../preguntas/index.html',
    '../contacto/contacto.html': '../contacto/index.html',
    '../obra/obra.html': '../obra/index.html',
    'inicio/inicio.html': 'inicio/index.html',
    'fotografias/fotografias.html': 'fotografias/index.html',
    'pinturas/pinturas.html': 'pinturas/index.html',
    'artistas/artistas.html': 'artistas/index.html',
    'artista/artista.html': 'artista/index.html',
    'licencias/licencias.html': 'licencias/index.html',
    'nosotros/nosotros.html': 'nosotros/index.html',
    'preguntas/preguntas.html': 'preguntas/index.html',
    'contacto/contacto.html': 'contacto/index.html',
    'obra/obra.html': 'obra/index.html',
    '<a href="artistas.html"': '<a href="index.html"',
    '<a href="contacto.html"': '<a href="index.html"',
}

for html_file in sorted(root.rglob('*.html')):
    text = html_file.read_text(encoding='utf-8')
    original = text
    # ensure stylesheet is always root styles from subfolders
    if html_file.parent != root:
        text = re.sub(r'<link rel="stylesheet" href="[^"]+">', '<link rel="stylesheet" href="../styles.css">', text)
    for old, new in path_updates.items():
        text = text.replace(old, new)
    if text != original:
        html_file.write_text(text, encoding='utf-8')

print('route cleanup complete')
