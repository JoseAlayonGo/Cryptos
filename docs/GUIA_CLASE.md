# Guía para la clase de criptoactivos

[Volver a la portada](../README.md) | [Consultar la guía de ejecución](GUIA_EJECUCION.md)

Este material organiza una práctica con los programas del repositorio. Sirve para preparar la ejecución y registrar evidencia; la discusión detallada de las simulaciones puede hacerse después, a partir de las salidas obtenidas por el grupo.

## Objetivos de aprendizaje

Al trabajar con los ejemplos, se busca que el estudiante pueda:

1. Localizar los datos, el índice, la fecha, la prueba y el enlace anterior de un bloque.
2. Seguir el recorrido de una transacción desde la lista de pendientes hasta su inclusión en un bloque.
3. Reconocer qué cambia entre un bloque por transacción y varias transacciones por bloque.
4. Ejecutar una comprobación de integridad y registrar su resultado.
5. Explicar el alcance de lo observado sin atribuir al programa funciones que no tiene.

## Preparación

- Saber abrir una terminal y reconocer una lista o un diccionario de Python ayuda a seguir la práctica.
- Abrir PowerShell en la raíz del repositorio. En el equipo del docente se utiliza `D:\Proyectos\Cryptos`; cada participante debe usar su propia ruta.
- Comprobar que están disponibles Python y los archivos. Los siguientes comandos solo consultan el entorno:

```powershell
python --version
Get-Item -LiteralPath '.\Cryptos.py', '.\demo_blockchain.py', '.\Crypto3_1.py', '.\Crypto4.py', '.\test_crypto4.py'
```

- Si falta un archivo, resolverlo antes de comenzar. Un estado limpio de Git no garantiza que una actualización concreta haya sido incorporada.
- Si la terminal muestra `>>>`, se está dentro de Python. Usar `exit()` para regresar a PowerShell antes de ejecutar los comandos de esta guía.

## Secuencia de la práctica

### Actividad 1. Ejecutar la búsqueda de prueba de trabajo

```powershell
python .\Cryptos.py
```

Registrar el nonce encontrado, el hash y el tiempo informado por el programa. Mantener el código y sus entradas sin cambios para esta primera observación.

El mensaje que menciona bitcoins pertenece al texto de esta demostración. Su ejecución no se conecta a una red ni genera activos transferibles.

### Actividad 2. Observar la cadena de tres bloques

```powershell
python .\demo_blockchain.py
```

Registrar la cantidad de bloques, los campos del bloque inicial y los resultados de las tres comprobaciones: cadena original, copia alterada y conservación de la original. Esta demostración depende de `Crypto3_1.py`.

Para inspeccionar la construcción paso a paso, usar el apartado de demostración interactiva de la guía de ejecución.

### Actividad 3. Observar la agrupación de transacciones

```powershell
python .\Crypto4.py
```

Registrar la cantidad de pendientes antes de minar, las transacciones incluidas en el bloque, los pendientes posteriores y las comprobaciones de integridad. Esta demostración utiliza una clase independiente y comienza con un génesis vacío.

### Actividad 4. Ejecutar las pruebas

```powershell
python -m unittest -v test_crypto4
```

Registrar la cantidad de pruebas y el resultado final. Si alguna falla, conservar el nombre de la prueba y su mensaje de error. El resultado esperado de la versión actual es diez pruebas y `OK`.

Los casos de prueba cubren comportamientos concretos del programa. Su aprobación no certifica una implementación para operar una red o custodiar activos.

## Registro de observaciones

Completar esta tabla con los resultados de la ejecución. El valor de `proof` y los hashes pueden cambiar entre versiones y ejecuciones; para compararlos es necesario anotar también las entradas y el archivo utilizado.

| Archivo o actividad | Dato que se debe registrar | Resultado observado |
| --- | --- | --- |
| `Cryptos.py` | Nonce, hash y tiempo de búsqueda. | |
| `demo_blockchain.py` | Cantidad de bloques y cantidad de transacciones añadidas por la demostración. | |
| `demo_blockchain.py` | `Cadena válida`, `Copia alterada válida` y `Original intacta`. | |
| `Crypto4.py` | Pendientes antes y después de minar. | |
| `Crypto4.py` | Cantidad de bloques y transacciones del bloque nuevo. | |
| `Crypto4.py` | `Cadena válida`, `Copia alterada válida` y `Original intacta`. | |
| Pruebas | Cantidad de pruebas y resultado final. | |

Para facilitar una comparación posterior, anotar también:

- Versión de Python, consultada con `python --version`.
- Versión del código, consultada con `git rev-parse --short HEAD`.
- Fecha de ejecución y cualquier modificación local.

No usar el tiempo de ejecución como una constante: depende del equipo y del trabajo que efectivamente se haya realizado en esa ejecución.

## Preguntas para la siguiente discusión

Estas preguntas organizan la revisión posterior de las simulaciones; conviene conservar primero las salidas y formular una explicación propia.

1. ¿Qué papel tienen `data`, `proof` y `previous_hash` en cada versión?
2. ¿Por qué una demostración termina con tres bloques y la otra con dos?
3. ¿En qué momento una transacción deja de estar pendiente?
4. ¿Qué entrada se usa para calcular la prueba de trabajo en cada programa?
5. ¿Qué comprobación detecta la modificación introducida en la copia?
6. ¿Qué significa que la cadena original siga intacta después del ejercicio?
7. ¿Qué aspectos de una transacción no comprueba `is_chain_valid()`?
8. ¿Qué cambia si el atacante también puede volver a calcular hashes y pruebas?
9. ¿Qué funciones adicionales harían falta para pasar de estos objetos locales a una red de participantes?
10. ¿Qué no puede concluirse sobre un criptoactivo a partir de estas simulaciones?

## Convenciones para presentar los ejemplos

| Elemento mostrado | Cómo describirlo en esta práctica |
| --- | --- |
| `Alice`, `Bob`, `Carol` | Etiquetas de participantes usadas como datos; no direcciones verificadas ni claves. |
| `Value` | Valor numérico ilustrativo, sin unidad monetaria definida ni comprobación de disponibilidad. |
| `True` / `False` | Resultado de las reglas de validación programadas en la versión ejecutada. |
| Lista de pendientes | Estructura local en memoria; no una lista compartida entre nodos. |
| Copia alterada | Objeto creado para un ejercicio controlado; no representa por sí solo un ataque completo contra una red. |

No se requiere crear cuentas en una plataforma de negociación, conectar una cartera ni realizar pagos para completar la práctica.
