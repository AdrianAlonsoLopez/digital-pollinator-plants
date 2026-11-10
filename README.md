# Polinizadores Digitales — documentación técnica y de usuario

## Alcance
Aplicación web de consulta preliminar de especies incluidas en `BDPoli.csv`. **No genera nuevas infografías ni valida ecológicamente las especies**: selecciona registros de la base de datos y presenta sus nombres junto con las URL de infografías existentes, cuando están disponibles.

## Funcionamiento
1. El usuario contesta el cuestionario web.
2. `PlantasJ.js` envía las respuestas como JSON a `POST /procesar_respuestas`.
3. `app.py` comprueba la estructura de entrada, convierte campos numéricos e invoca `procesar_respuestas` de `Arbol.py`.
4. `Arbol.py` lee `BDPoli.csv`, aplica restricciones ambientales y de espacio (estado, área, temperatura, heladas, riego, sol, suelo, materia orgánica y pH cuando se conoce), y luego evalúa preferencias (forma, subtipo herbáceo, frutos, hojas, uso, color de flor, altura y velocidad de crecimiento).
5. La respuesta JSON contiene `preferidas`, `alternativas` y `total`. Ambas listas incluyen objetos `{ "especie": "...", "foto": "..." }`. La interfaz muestra los dos grupos, recuperando las imágenes a partir de las URL registradas en el CSV.

**Importante:** los filtros ambientales reproducen las reglas codificadas, no una verificación de idoneidad ecológica local. El criterio de estado no prueba que una planta sea nativa de una localidad específica.

## Requisitos
- Python 3 y `pip`.
- Dependencias Python: `Flask`, `pandas`.
- Navegador web moderno.
- Conexión a Internet para visualizar imágenes hospedadas externamente, si corresponde.

## Estructura de carpetas
```text
proyecto/
├── app.py
├── Arbol.py
├── BDPoli.csv
├── pruebas_revisor1_observacion3.py
├── templates/
│   ├── PlantaHTML.html
│   └── layout.html
└── static/
    ├── js/
    │   └── PlantasJ.js
    └── css/
        └── PlantasC.css
```
El archivo `PlantasC.css` debe conservarse de la versión original del proyecto: no está incluido en este paquete.

## Instalación y ejecución
Desde la carpeta raíz del proyecto:
```bash
python -m pip install Flask pandas
python app.py
```
Abrir `http://127.0.0.1:5000/` en el navegador. El servidor utiliza `debug=True` en esta versión de desarrollo; **no desplegar así en producción**.

## Uso
Responder todas las preguntas obligatorias. Si no se conoce el pH, seleccionar la opción correspondiente; el filtro de pH se omite. Al enviar, se muestran (a) especies compatibles con las condiciones ambientales y todas las preferencias seleccionadas, y (b) otras especies ambientalmente compatibles. Si no hay coincidencias ambientales, aparece un mensaje indicándolo. Las fotografías/infografías son recursos existentes referenciados por `FOTO` en el CSV; no son generados por el software.

## API
`POST /procesar_respuestas`, encabezado `Content-Type: application/json`.

Ejemplo de estructura de salida (ilustrativo, no resultado de un caso específico):
```json
{
  "preferidas": [{"especie": "Nombre científico", "foto": "https://..."}],
  "alternativas": [],
  "total": 1
}
```
Entradas ausentes, inválidas o fuera de rango producen un objeto `{"error": "..."}` y estado HTTP 400 cuando se detectan en la ruta. Consultar `PlantasJ.js` para las opciones y códigos exactos del cuestionario; consultar `Arbol.py` para la implementación normativa de las reglas.

## Pruebas
Desde la carpeta raíz:
```bash
python pruebas_revisor1_observacion3.py
```
Incluye casos de una, varias y ninguna especie; preferencias; pH opcional; entradas inválidas; y comparaciones con registros del CSV. El registro de una ejecución anterior se encuentra en `resultados_pruebas_revisor1.txt`. Estas pruebas verifican concordancia con reglas implementadas, no validez botánica independiente. La integración Flask/navegador aún debe probarse en el entorno de despliegue.

## Datos, imágenes y mantenimiento
- `BDPoli.csv`: cada fila representa una especie; `ESPECIE` contiene el nombre y `FOTO` una referencia a una infografía preexistente. Mantener los encabezados y categorías esperados por `Arbol.py`.
- Las imágenes pueden dejar de estar disponibles si cambian sus URL o permisos. Verificar su accesibilidad y derechos de uso antes de publicar.
- Para modificar las reglas, actualizar `Arbol.py` y las pruebas correspondientes; para cambiar las preguntas, revisar la correspondencia entre `PlantasJ.js` y `Arbol.py`.
- Ejecutar las pruebas después de cualquier modificación de la base de datos o del algoritmo.

## Versión y reproducibilidad
Este paquete integra las correcciones de las observaciones 1–3 del Revisor 1 y la documentación de la observación 4. **No se ha asignado un número de versión publicado, DOI, etiqueta Git ni commit verificado.** Antes de responder definitivamente al revisor, depositar el código y los datos evaluados en un repositorio versionado, crear una etiqueta de lanzamiento y un archivo inmutable (por ejemplo, una versión archivada con DOI), y añadir aquí:

- Versión / etiqueta: **PENDIENTE**
- Commit: **PENDIENTE**
- URL permanente / DOI: **PENDIENTE**
- Fecha de publicación: **PENDIENTE**

No sustituir estos campos por enlaces a una rama cambiante como `main`.
