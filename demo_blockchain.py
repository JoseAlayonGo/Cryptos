"""Demostración local de bloques, prueba de trabajo y detección de cambios.

Ejecutar desde la carpeta del proyecto:
    python demo_blockchain.py
"""

from copy import deepcopy
import json

from Crypto3_1 import Blockchain


def crear_cadena_demo() -> Blockchain:
    """Crear un génesis y añadir dos transacciones de ejemplo."""
    cadena = Blockchain()
    transacciones = (
        {
            "Value": 50,
            "From": "Alice",
            "TO": "Bob",
            "Concept": "Prueba",
        },
        {
            "Value": 25,
            "From": "Bob",
            "TO": "Carol",
            "Concept": "Segunda prueba",
        },
    )

    for transaccion in transacciones:
        cadena.mine_block(transaccion)

    return cadena


def main() -> int:
    """Mostrar la cadena y comprobar una alteración sobre una copia."""
    print("DEMO DE BLOCKCHAIN")
    print("\n1. Crear el génesis y minar dos bloques de ejemplo.")
    cadena = crear_cadena_demo()
    print(json.dumps(cadena.chain, indent=2, ensure_ascii=False))

    print("\n2. Comprobar la cadena original.")
    cantidad_bloques = len(cadena.chain)
    original_valida = cadena.is_chain_valid()
    print("Bloques:", cantidad_bloques)
    print("Cadena válida:", original_valida)

    print("\n3. Cambiar el valor del segundo bloque de 50 a 999 en una copia.")
    contenido_original = deepcopy(cadena.chain)
    cadena_alterada = deepcopy(cadena)
    cadena_alterada.chain[1]["data"]["Value"] = 999
    alterada_valida = cadena_alterada.is_chain_valid()
    original_intacta = (
        cadena.chain == contenido_original and cadena.is_chain_valid()
    )
    print("Copia alterada válida:", alterada_valida)
    print("Original intacta:", original_intacta)

    if cantidad_bloques != 3 or not original_valida or alterada_valida or not original_intacta:
        print("\nLa demostración no produjo el resultado esperado.")
        return 1

    print("\nDemostración completada: la alteración fue detectada.")
    print("Los datos de esta ejecución permanecen únicamente en memoria.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
