# Guía de ejecución

[Volver a la portada](../README.md) | [Guía para la clase](GUIA_CLASE.md)

Instrucciones para ejecutar las versiones del laboratorio de criptoactivos, consultar sus resultados y guardar cambios en GitHub. Todos los comandos de PowerShell se ejecutan desde la carpeta raíz del repositorio, donde están los archivos `.py`.

En las instrucciones se distingue entre **PowerShell** y **Python**: el indicador `PS ...>` corresponde a PowerShell y `>>>` corresponde a Python. Los indicadores no se copian al ejecutar los ejemplos.

## Requisitos

- Python 3. Los ejemplos de esta guía se comprobaron con Python **3.14.6** en Windows.
- PowerShell para seguir los comandos de esta guía.
- Git para descargar el repositorio y publicar cambios.

Los programas utilizan únicamente módulos incluidos con Python: `hashlib`, `time`, `datetime`, `json`, `copy` y `math`. Las pruebas usan `unittest` y los ejemplos interactivos también usan `pprint`, ambos incluidos en Python. No necesitas instalar paquetes con `pip`.

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

## Varias transacciones por bloque: `Crypto4.py`

### Ejecutar la nueva demostración

En **PowerShell**, desde la carpeta del proyecto:

```powershell
python .\Crypto4.py
```

La demostración registra dos transacciones pendientes, las incluye en un único bloque y muestra la cadena completa. Después altera una copia para comprobar que la validación detecta el cambio. Entre sus mensajes aparecen estos resultados, en este orden:

```text
Pendientes antes de minar: 2
Bloques: 2
Transacciones del nuevo bloque: 2
Pendientes después de minar: 0
Cadena válida: True
Copia alterada válida: False
Original intacta: True
```

Son **dos bloques**: un génesis con una lista de transacciones vacía y un segundo bloque con las dos transacciones. Cada ejecución parte de una cadena nueva en memoria y termina automáticamente en PowerShell.

### Usar la nueva clase paso a paso

Para abrir una sesión de **Python**, ejecuta `python` desde la carpeta del proyecto. Cuando aparezca `>>>`, copia:

```python
from Crypto4 import Blockchain

cadena_lotes = Blockchain()
destino = cadena_lotes.add_transaction({
    "Value": 50, "From": "Alice", "TO": "Bob", "Concept": "Primera prueba"
})
destino = cadena_lotes.add_transaction({
    "Value": 25, "From": "Bob", "TO": "Carol", "Concept": "Segunda prueba"
})

print("Pendientes:", len(cadena_lotes.pending_transactions))
bloque_lote = cadena_lotes.mine_block()
print("Transacciones del bloque:", len(bloque_lote["data"]))
print("Pendientes después:", len(cadena_lotes.pending_transactions))
print("Cadena válida:", cadena_lotes.is_chain_valid())
```

Resultado esperado:

```text
Pendientes: 2
Transacciones del bloque: 2
Pendientes después: 0
Cadena válida: True
```

Para consultar los datos completos, usa `print(bloque_lote)` o `print(cadena_lotes.chain)`. Para otro bloque, registra nuevas transacciones y vuelve a llamar a `mine_block()`; las transacciones ya minadas no vuelven a entrar en la lista de pendientes. Escribe `exit()` para regresar a PowerShell.

| Operación | Comportamiento |
| --- | --- |
| `add_transaction(datos)` | Valida y guarda una copia de los datos; devuelve el índice del bloque al que se destinarán. |
| `pending_transactions` | Devuelve una copia de la lista de pendientes para consultarla. |
| `mine_block()` | Agrupa todos los pendientes, busca la prueba de trabajo y añade el bloque. Devuelve una copia del bloque creado. |
| `get_previous_block()` | Devuelve una copia del último bloque. |
| `is_chain_valid()` | Comprueba el génesis, la estructura, el orden de índices y fechas, los enlaces y la prueba de trabajo. |

Cada transacción debe tener exactamente las claves `Value`, `From`, `TO` y `Concept`. `Value` debe ser un entero o decimal positivo y finito; los otros tres campos deben ser textos no vacíos. Esta comprobación no verifica saldos ni identidades.

`mine_block()` no recibe argumentos en esta versión: primero se registran las transacciones con `add_transaction()`. Si no hay pendientes o la cadena está alterada, lanza `ValueError`. Los pendientes solo se retiran después de que el nuevo bloque se haya añadido; un fallo durante la búsqueda de la prueba de trabajo los conserva.

Modificar el diccionario original, la copia devuelta de los pendientes o el bloque devuelto por `mine_block()` no modifica la cadena interna. El atributo `chain` se mantiene accesible para los ejercicios de alteración; `is_chain_valid()` comprueba su contenido.

### Ejecutar las pruebas automáticas

En **PowerShell**:

```powershell
python -m unittest -v test_crypto4
```

La suite ejecuta diez pruebas y debe terminar con `OK`. Comprueba la agrupación en bloques, que los pendientes no se repitan, el aislamiento de copias, los datos inválidos, la conservación de pendientes cuando falla la minería, las alteraciones y el orden de índices y fechas. No requiere paquetes adicionales.

### Diferencias con las versiones anteriores

- En `Crypto4.py`, `data` siempre es una lista de transacciones. El génesis tiene una lista vacía.
- La prueba de trabajo busca un hash del **bloque completo** que comience con `0000`. El cálculo incluye las transacciones, la fecha, el índice, el enlace anterior y `proof`.
- La representación JSON ordena las claves antes de calcular el hash. La validación conserva el orden de las transacciones, pero no depende del orden de las claves de sus diccionarios.
- Las fechas se guardan en UTC y no retroceden respecto al bloque anterior. Se permite que dos bloques tengan la misma fecha y hora.
- El hash original del génesis se conserva en el objeto para detectar cambios incluso cuando la cadena tiene un solo bloque. El génesis no se mina.

Esta versión crea su propia cadena: no importa ni convierte cadenas de los archivos anteriores. Es un ejercicio local, sin persistencia, firmas, saldos verificados, consenso ni comunicación entre nodos. La nueva clase no incorpora el registro de nodos ni la conversión a objetos `Block` de `Crypto2.py`; ese archivo se conserva.

## Demostración anterior con un solo comando

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

- `Crypto2.py` conserva el registro de direcciones de nodos y la conversión de datos a objetos `Block`. `Crypto4.py` incorpora una lista de pendientes y comprobaciones de índice y orden de fechas, con una implementación propia. El registro de nodos de `Crypto2.py` es una colección local; no implementa comunicación entre equipos. Las demostraciones de `Crypto4.py` y `demo_blockchain.py` no dependen de este archivo.
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

## Qué comprueba la validación de las versiones anteriores

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

Ese estado indica que la copia local no tiene cambios pendientes y que su referencia de seguimiento coincide con `main`. Para confirmar que se incorporó un archivo nuevo, comprueba también que exista, que forme parte del commit y que `git push` haya terminado correctamente. Por ejemplo:

```powershell
Get-Item -LiteralPath '.\Crypto4.py'
git ls-files -- Crypto4.py
git log -1 --oneline
```

Un archivo puede estar en la carpeta de entregables y todavía no haberse copiado al repositorio. Antes de ejecutarlo o publicarlo, comprueba que aparezca en la raíz del proyecto.

Para guardar documentación, sustituye `Crypto3_1.py` por `README.md` y usa un mensaje que describa ese cambio. Un archivo nuevo sin seguimiento no aparece en `git diff`; puedes abrirlo para revisarlo o consultarlo con `git diff --cached` después de añadirlo.

## Problemas frecuentes

| Situación | Qué revisar |
| --- | --- |
| Python indica `can't open file` aunque Git muestre un estado limpio. | Comprueba el archivo con `Get-Item` y la ruta con `Get-Location`. Incorpora la actualización que lo contiene antes de ejecutarlo. |
| `Crypto4.py` muestra `No hay transacciones pendientes para minar`. | Registra al menos una transacción con `add_transaction()` antes de llamar a `mine_block()`. |
| Al cambiar de versión, `mine_block(datos)` produce `TypeError`. | En `Crypto4.py` se usa primero `add_transaction(datos)` y después `mine_block()` sin argumentos. |
| `demo_blockchain.py` indica `No module named 'Crypto3_1'`. | Coloca los dos archivos juntos en la carpeta del proyecto y conserva el nombre `Crypto3_1.py`. |
| `Crypto3_1.py` termina sin mostrar nada. | Es el comportamiento esperado al ejecutarlo sin `-i`: solo define una clase. Sigue la demostración interactiva. |
| Python indica que no encuentra el archivo. | Comprueba que PowerShell esté en la carpeta del repositorio; usa `Get-Location` y `Get-ChildItem`. |
| Un comando de PowerShell produce `SyntaxError`. | Si ves `>>>`, estás dentro de Python. Escribe `exit()` antes de usar `git`, `Set-Location` o `python`. |
| Aparece `NameError` al usar `cadena`. | La sesión actual no tiene esa variable. Carga `Crypto3_1.py` con `-i` y ejecuta `cadena = Blockchain()`. |
| Aparece `Repository not found` al publicar. | Comprueba que el repositorio exista, que `git remote -v` muestre la dirección correcta y que Git use una cuenta con acceso. |

## Referencia indicada en el código

El encabezado de `Crypto2.py` cita este [tutorial de freeCodeCamp sobre una criptomoneda con Python](https://www.freecodecamp.org/news/create-cryptocurrency-using-python/).
