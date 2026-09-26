# Cryptos: ejemplos de blockchain en Python

Ejemplos educativos para explorar hashes SHA-256, prueba de trabajo (*proof of work*), bloques y validación de una cadena. Los cálculos se realizan localmente; las transacciones son datos de ejemplo y no transfieren dinero.

Para empezar, ejecuta **`demo_blockchain.py`**: crea una cadena, añade dos transacciones y muestra cómo se detecta una alteración. Utiliza la clase de `Crypto3_1.py`, que representa cada transacción con un valor, un remitente, un destinatario y un concepto.

## Contenido del repositorio

| Archivo | Qué muestra | Cómo se utiliza |
| --- | --- | --- |
| [`demo_blockchain.py`](demo_blockchain.py) | Demostración completa con tres bloques y una alteración controlada sobre una copia. | Ejecuta `python .\demo_blockchain.py`; no requiere escribir instrucciones dentro de Python. |
| [`Cryptos.py`](Cryptos.py) | Búsqueda de un nonce cuyo hash comienza con cuatro ceros. | Ejecuta una demostración y muestra el resultado en la consola. |
| [`Crypto2.py`](Crypto2.py) | Clases `Block` y `BlockChain`, datos pendientes y construcción de bloques. | Ejecuta una demostración que imprime una cadena inicial y una cadena con un segundo bloque. |
| [`crypto3.py`](crypto3.py) | Clase `Blockchain` con datos de texto, minería y validación. | Se usa desde Python interactivo; ejecutarlo por sí solo no imprime resultados. |
| [`Crypto3_1.py`](Crypto3_1.py) | Variante de `Blockchain` con datos de transacción en un diccionario. | Se usa desde Python interactivo; el archivo define la clase sin crear una cadena automáticamente. |

## Requisitos

- Python 3. Los ejemplos de esta guía se comprobaron con Python **3.14.6** en Windows.
- PowerShell para seguir los comandos de esta guía.
- Git para descargar el repositorio y publicar cambios.

Los programas utilizan únicamente módulos incluidos con Python: `hashlib`, `time`, `datetime`, `json` y `copy`. Los ejemplos interactivos de esta guía también usan `pprint`, incluido en Python. No necesitas instalar paquetes con `pip`.

Comprueba que Python está disponible:

```powershell
python --version
```

Si tu instalación utiliza el lanzador `py`, comprueba `py --version` y sustituye `python` por `py` en los comandos siguientes.

## Abrir la carpeta del proyecto

Si ya tienes el repositorio en `D:\Proyectos\Cryptos`, ejecuta en PowerShell:

```powershell
Set-Location -LiteralPath 'D:\Proyectos\Cryptos'
```

Para descargar una copia en otro equipo, abre PowerShell en la carpeta donde quieres guardarla y ejecuta:

```powershell
git clone https://github.com/JoseAlayonGo/Cryptos.git
Set-Location -LiteralPath '.\Cryptos'
```

Si el repositorio es privado, necesitarás acceso con tu cuenta de GitHub. La clonación se hace una sola vez por copia local.

## Demostración con un solo comando

Desde la carpeta del proyecto, ejecuta en **PowerShell**:

```powershell
python .\demo_blockchain.py
```

El programa realiza lo siguiente:

1. Crea el bloque génesis definido en `Crypto3_1.py`.
2. Añade un bloque con una transacción de Alice a Bob por 50 y otro de Bob a Carol por 25.
3. Muestra los tres bloques y comprueba la validez de la cadena.
4. Crea una copia independiente y cambia de 50 a 999 el valor del segundo bloque.
5. Comprueba que la copia alterada es inválida y que la cadena original conserva su contenido y sigue siendo válida.

Además de los bloques y de los mensajes de cada paso, verás estos resultados, en este orden:

```text
Bloques: 3
Cadena válida: True
Copia alterada válida: False
Original intacta: True
```

Las fechas y los hashes de los bloques cambian entre ejecuciones. Al terminar, vuelves automáticamente a PowerShell. El programa no solicita datos ni guarda la cadena en un archivo; cada ejecución comienza con una cadena nueva.

Mantén `demo_blockchain.py` y `Crypto3_1.py` en la misma carpeta. La demostración utiliza la clase existente, sin duplicar su implementación. Importar `demo_blockchain` desde otro programa no inicia la demostración; esta se ejecuta cuando se llama a `main()` o se abre el archivo con Python como en el comando anterior.

## Demostración interactiva: `Crypto3_1.py`

### 1. Cargar el programa

Desde la carpeta del proyecto, ejecuta en **PowerShell**:

```powershell
python -i .\Crypto3_1.py
```

La opción `-i` carga el archivo y deja abierta una sesión interactiva de Python. Cuando veas `>>>`, escribe código Python. No copies los caracteres `>>>`.

### 2. Crear una cadena y añadir una transacción

Copia lo siguiente en **Python**:

```python
cadena = Blockchain()

bloque = cadena.mine_block({
    'Value': 50,
    'From': 'Alice',
    'TO': 'Bob',
    'Concept': 'Prueba'
})

print("Bloques:", len(cadena.chain))
print("Cadena válida:", cadena.is_chain_valid())
```

Resultado esperado:

```text
Bloques: 2
Cadena válida: True
```

`Blockchain()` crea el primer bloque, llamado **génesis**. `mine_block()` busca una prueba de trabajo y añade un segundo bloque con la transacción de ejemplo.

### 3. Consultar los bloques

En la misma sesión de **Python**:

```python
from pprint import pprint

pprint(cadena.chain)
```

Para consultar únicamente el último bloque:

```python
pprint(cadena.get_previous_block())
```

Cada bloque contiene:

| Campo | Significado en este programa |
| --- | --- |
| `index` | Posición del bloque; el génesis comienza en 1. |
| `timestamp` | Fecha y hora local de creación, guardadas como texto. |
| `data` | Datos de la transacción. |
| `proof` | Número utilizado por el cálculo de prueba de trabajo. |
| `previous_hash` | Hash del bloque anterior; el génesis usa `"0"`. |

En esta versión, `data` es un diccionario con las claves `Value`, `From`, `TO` y `Concept`. Conserva esas mayúsculas en los ejemplos. Los nombres de personas de esta guía son etiquetas de demostración; el código no comprueba identidades ni saldos.

### 4. Añadir otro bloque

Continúa en la misma sesión de **Python**:

```python
otro_bloque = cadena.mine_block({
    'Value': 25,
    'From': 'Bob',
    'TO': 'Carol',
    'Concept': 'Segunda prueba'
})

print("Bloques:", len(cadena.chain))
print("Cadena válida:", cadena.is_chain_valid())
```

Resultado esperado:

```text
Bloques: 3
Cadena válida: True
```

### 5. Observar qué sucede al alterar un bloque

Este ejemplo modifica una copia de la cadena en memoria:

```python
from copy import deepcopy

cadena_alterada = deepcopy(cadena)
cadena_alterada.chain[0]['data']['Value'] = 999

print("Original válida:", cadena.is_chain_valid())
print("Copia alterada válida:", cadena_alterada.is_chain_valid())
```

Resultado esperado:

```text
Original válida: True
Copia alterada válida: False
```

Al cambiar el génesis, su hash deja de coincidir con el `previous_hash` almacenado en el segundo bloque. La comprobación detecta esa diferencia. Este ejemplo requiere haber creado al menos un bloque después del génesis, como en los pasos anteriores.

### 6. Volver a PowerShell

En **Python**, escribe:

```python
exit()
```

Cuando aparezca de nuevo `PS ...>`, puedes ejecutar comandos de PowerShell y Git.

La cadena vive en memoria: se pierde al cerrar Python. Para repetir la demostración, vuelve a cargar el archivo y crear `cadena`.

## Ejecutar los otros ejemplos

Antes de ejecutar los siguientes comandos, sal de Python con `exit()` si todavía ves `>>>`.

### `Cryptos.py`: prueba de trabajo

En **PowerShell**:

```powershell
python .\Cryptos.py
```

El programa busca un nonce, informa el tiempo transcurrido y muestra un hash que comienza con `0000`, según su dificultad actual de cuatro ceros. El tiempo depende del equipo. El mensaje del código que menciona bitcoins corresponde a esta simulación local.

### `Crypto2.py`: bloques y datos pendientes

En **PowerShell**:

```powershell
python .\Crypto2.py
```

La demostración imprime primero una cadena con el bloque inicial y después otra con un segundo bloque que incluye datos de una transacción.

Notas sobre la versión actual:

- `Crypto2.py` se conserva porque incluye una lista de transacciones pendientes, registro de direcciones de nodos, conversión de datos a objetos `Block` y comprobaciones de índice y orden de fechas que `Crypto3_1.py` no incorpora. El registro de nodos es una colección local; no implementa comunicación entre equipos. La nueva demostración no depende de este archivo.
- El método `block_mining()` llama a `new_data()` con `receiver`, pero el parámetro definido se llama `recipient`. Invocar ese método produce un `TypeError`; la demostración principal usa otro recorrido y sí se ejecuta.
- El archivo ejecuta la demostración también al importarlo. Al final vuelve a asignar `blockchain = BlockChain()`, por lo que esa variable queda con una cadena nueva que contiene solo el génesis.

### `crypto3.py`: datos de texto

En **PowerShell**:

```powershell
python -i .\crypto3.py
```

Después, en **Python**:

```python
cadena_texto = Blockchain()
bloque_texto = cadena_texto.mine_block("Alice envia 50 a Bob")

print("Bloques:", len(cadena_texto.chain))
print("Cadena válida:", cadena_texto.is_chain_valid())
```

Resultado esperado:

```text
Bloques: 2
Cadena válida: True
```

Usa `exit()` para volver a PowerShell.

## Qué comprueba la validación

En `crypto3.py` y `Crypto3_1.py`, `is_chain_valid()` recorre la cadena a partir del segundo bloque y comprueba:

1. Que `previous_hash` coincide con el hash del bloque anterior.
2. Que el cálculo de prueba de trabajo del bloque produce un hash que comienza con cuatro ceros.

La prueba de trabajo utiliza las pruebas numéricas del bloque actual y del anterior, el índice y los datos. No equivale a aplicar SHA-256 al bloque completo. El hash del bloque completo se utiliza para enlazarlo con el siguiente.

El resultado `True` indica que pasan esas comprobaciones; no verifica saldos, firmas, identidades ni autorización de las transacciones. El génesis no tiene una prueba de trabajo que se valide por separado.

Estas implementaciones son ejercicios locales: no incluyen comunicación entre nodos, consenso distribuido, carteras ni almacenamiento persistente. En `Crypto3_1.py`, la prueba de trabajo convierte el diccionario con `str(data)`; no usa una representación canónica independiente del orden de las claves.

## Guardar cambios en GitHub

Desde **PowerShell**, dentro del repositorio, revisa primero lo que cambió:

```powershell
git status
git diff
```

Por ejemplo, para publicar un cambio en `Crypto3_1.py`:

```powershell
git add -- Crypto3_1.py
git diff --cached
```

Si la revisión es correcta:

```powershell
git commit -m "Actualizar ejemplo de blockchain"
git push
git status -sb
```

Con la rama de seguimiento ya configurada y sin cambios pendientes, el último comando debe mostrar únicamente:

```text
## main...origin/main
```

Para guardar documentación, sustituye `Crypto3_1.py` por `README.md` y usa un mensaje que describa ese cambio. Un archivo nuevo sin seguimiento no aparece en `git diff`; puedes abrirlo para revisarlo o consultarlo con `git diff --cached` después de añadirlo.

## Problemas frecuentes

| Situación | Qué revisar |
| --- | --- |
| `demo_blockchain.py` indica `No module named 'Crypto3_1'`. | Coloca los dos archivos juntos en la carpeta del proyecto y conserva el nombre `Crypto3_1.py`. |
| `Crypto3_1.py` termina sin mostrar nada. | Es el comportamiento esperado al ejecutarlo sin `-i`: solo define una clase. Sigue la demostración interactiva. |
| Python indica que no encuentra el archivo. | Comprueba que PowerShell esté en la carpeta del repositorio; usa `Get-Location` y `Get-ChildItem`. |
| Un comando de PowerShell produce `SyntaxError`. | Si ves `>>>`, estás dentro de Python. Escribe `exit()` antes de usar `git`, `Set-Location` o `python`. |
| Aparece `NameError` al usar `cadena`. | La sesión actual no tiene esa variable. Carga `Crypto3_1.py` con `-i` y ejecuta `cadena = Blockchain()`. |
| Aparece `Repository not found` al publicar. | Comprueba que el repositorio exista, que `git remote -v` muestre la dirección correcta y que Git use una cuenta con acceso. |

## Referencia indicada en el código

El encabezado de `Crypto2.py` cita este [tutorial de freeCodeCamp sobre una criptomoneda con Python](https://www.freecodecamp.org/news/create-cryptocurrency-using-python/).
