# Cryptos · Laboratorio para una clase de criptoactivos

Material docente en Python para observar cómo se representan datos en bloques, cómo se enlazan mediante hashes y cómo una validación local detecta ciertas alteraciones. Las versiones permiten avanzar desde una búsqueda de prueba de trabajo hasta una cadena con varias transacciones por bloque.

Los programas son **ejemplos ilustrativos que se ejecutan en un solo equipo**. Los nombres y valores de las transacciones son datos de clase: no representan cuentas verificadas, saldos disponibles ni transferencias de criptoactivos.

## Empezar

Necesitas Python 3. Los programas se han comprobado con **Python 3.14.6 en Windows** y utilizan únicamente la biblioteca estándar; no hay paquetes que instalar con `pip`.

Si aún no tienes el repositorio, abre PowerShell en la carpeta donde quieras descargarlo:

```powershell
git clone https://github.com/JoseAlayonGo/Cryptos.git
Set-Location -LiteralPath '.\Cryptos'
```

Si el repositorio es privado, tu cuenta de GitHub debe tener acceso. Si ya tienes una copia, abre PowerShell en esa carpeta. En el equipo donde se preparó este material, la ruta es `D:\Proyectos\Cryptos`.

Ejecuta la demostración de transacciones pendientes:

```powershell
python .\Crypto4.py
```

Verás dos bloques: un génesis sin transacciones y un segundo bloque que agrupa dos transacciones. Además de la cadena completa y de otros mensajes, aparecen estos resultados:

```text
Pendientes antes de minar: 2
Bloques: 2
Transacciones del nuevo bloque: 2
Pendientes después de minar: 0
Cadena válida: True
Copia alterada válida: False
Original intacta: True
```

Para comprobar el comportamiento de esta versión:

```powershell
python -m unittest -v test_crypto4
```

Las diez pruebas deben terminar con `OK`. Al cerrar el programa, la cadena creada en esa ejecución no se guarda: permanece únicamente en memoria.

## Documentación

- **[Guía de ejecución](docs/GUIA_EJECUCION.md):** preparación, comandos de cada versión, uso interactivo, campos de los bloques, pruebas y solución de errores frecuentes.
- **[Guía para la clase](docs/GUIA_CLASE.md):** objetivos de aprendizaje, recorrido sugerido, registro de observaciones y preguntas para discutir las simulaciones.

## Recorrido sugerido

Todos los comandos de esta tabla se ejecutan en PowerShell desde la raíz del repositorio.

| Paso | Archivo o comando | Qué observar |
| --- | --- | --- |
| 1. Prueba de trabajo | `python .\Cryptos.py` | Búsqueda de un nonce, hash obtenido y tiempo de ejecución. |
| 2. Cadena con un bloque por transacción | `python .\demo_blockchain.py` | Génesis, dos bloques adicionales y comprobación de una alteración. |
| 3. Varias transacciones en un bloque | `python .\Crypto4.py` | Lista de pendientes, agrupación en un bloque y vaciado de la lista. |
| 4. Comprobación reproducible | `python -m unittest -v test_crypto4` | Casos de prueba válidos, datos incorrectos, fallos de minería y alteraciones. |

Los números de bloques de las dos demostraciones son distintos por diseño. `demo_blockchain.py` crea **tres bloques**; `Crypto4.py` crea **dos**. La guía de ejecución conserva también los ejercicios interactivos para construir la cadena paso a paso.

## Archivos del proyecto

| Archivo | Función |
| --- | --- |
| [`Crypto4.py`](Crypto4.py) | Clase `Blockchain` independiente, lista de pendientes, minería por grupos y demostración integrada. |
| [`test_crypto4.py`](test_crypto4.py) | Diez pruebas automáticas de la versión con transacciones pendientes. |
| [`demo_blockchain.py`](demo_blockchain.py) | Demostración ejecutable basada en `Crypto3_1.py`. |
| [`Crypto3_1.py`](Crypto3_1.py) | Clase con un diccionario de datos por bloque, usada por la demostración anterior. |
| [`crypto3.py`](crypto3.py) | Versión que usa texto como datos del bloque. |
| [`Cryptos.py`](Cryptos.py) | Ejemplo inicial de búsqueda de una prueba de trabajo. |
| [`Crypto2.py`](Crypto2.py) | Versión anterior con clases `Block` y `BlockChain`, conservada para comparar implementaciones. |

`Crypto2.py` mantiene funciones que no se han trasladado a la versión nueva y tiene limitaciones conocidas, descritas en la guía de ejecución. Las versiones se conservan para estudiar su evolución; sus estructuras de datos no se convierten automáticamente entre sí.

## Alcance del laboratorio

| Los programas muestran | No implementan |
| --- | --- |
| Hashes y enlaces entre bloques. | Una red de nodos que acuerde un historial compartido. |
| Una búsqueda local de prueba de trabajo. | Competencia entre mineros, ajuste de dificultad de una red o recompensas monetarias reales. |
| Transacciones representadas como datos. | Firmas, claves privadas, autorización de pagos o comprobación de saldos. |
| Detección de alteraciones según las reglas de cada versión. | Una garantía general de inmutabilidad o una auditoría de seguridad. |
| Listas y objetos que viven en la memoria de Python. | Almacenamiento persistente, carteras o integración con mercados. |

`Cadena válida: True` indica que pasan las comprobaciones programadas en esa versión. No demuestra que alguien pueda realizar un pago, que los datos sean verdaderos o que una red haya aceptado la cadena. Los valores `50` y `25` no tienen una unidad monetaria definida por el programa.

## Referencia de la versión inicial

El encabezado de `Crypto2.py` cita este [tutorial de freeCodeCamp sobre una criptomoneda con Python](https://www.freecodecamp.org/news/create-cryptocurrency-using-python/). La documentación de este repositorio describe el comportamiento de los archivos locales, incluidas sus diferencias respecto de otras implementaciones.
