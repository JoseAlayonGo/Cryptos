"""Blockchain educativa con varias transacciones por bloque.

Ejecutar la demostración: python Crypto4.py
Ejecutar las pruebas: python -m unittest -v test_crypto4
"""

from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
import math


class Blockchain:
    """Agrupar transacciones pendientes y validar los bloques en memoria."""

    _FIELDS = {"Value", "From", "TO", "Concept"}
    _BLOCK_FIELDS = {"index", "timestamp", "data", "proof", "previous_hash"}
    _PREFIX = "0000"

    def __init__(self):
        self._pending_transactions = []
        genesis = {
            "index": 1,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": [],
            "proof": 0,
            "previous_hash": "0",
        }
        self.chain = [genesis]
        self._genesis_hash = self._hash(genesis)

    @property
    def pending_transactions(self) -> list:
        """Devolver una copia de los pendientes para evitar cambios accidentales."""
        return deepcopy(self._pending_transactions)

    @classmethod
    def _validate_transaction(cls, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError("La transacción debe ser un diccionario.")
        if set(data) != cls._FIELDS:
            raise ValueError("Usa exactamente las claves Value, From, TO y Concept.")
        value = data["Value"]
        if type(value) not in (int, float) or value <= 0:
            raise ValueError("Value debe ser un número positivo.")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("Value debe ser un número finito.")
        for field in ("From", "TO", "Concept"):
            if not isinstance(data[field], str) or not data[field].strip():
                raise ValueError(f"{field} debe ser un texto no vacío.")

    def add_transaction(self, data: dict) -> int:
        """Añadir una copia de la transacción y devolver el índice del próximo bloque."""
        self._validate_transaction(data)
        self._pending_transactions.append(deepcopy(data))
        return len(self.chain) + 1

    def get_previous_block(self) -> dict:
        """Consultar una copia del último bloque."""
        return deepcopy(self.chain[-1])

    @staticmethod
    def _hash(block: dict) -> str:
        encoded = json.dumps(
            block, sort_keys=True, separators=(",", ":"),
            ensure_ascii=False, allow_nan=False,
        ).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()

    def _proof_of_work(self, block: dict) -> int:
        """Buscar una prueba cuyo hash del bloque completo empiece por cuatro ceros."""
        block["proof"] = 0
        while not self._hash(block).startswith(self._PREFIX):
            block["proof"] += 1
        return block["proof"]

    def mine_block(self) -> dict:
        """Minar todos los pendientes y retirarlos solo después de añadir el bloque."""
        if not self._pending_transactions:
            raise ValueError("No hay transacciones pendientes para minar.")
        if not self.is_chain_valid():
            raise ValueError("La cadena está alterada; no se puede añadir un bloque.")

        previous = self.chain[-1]
        transactions = deepcopy(self._pending_transactions)
        timestamp = max(
            datetime.now(timezone.utc),
            datetime.fromisoformat(previous["timestamp"]),
        )
        block = {
            "index": len(self.chain) + 1,
            "timestamp": timestamp.isoformat(),
            "data": transactions,
            "proof": 0,
            "previous_hash": self._hash(previous),
        }
        block["proof"] = self._proof_of_work(block)
        self.chain.append(block)
        del self._pending_transactions[:len(transactions)]
        return deepcopy(block)

    def is_chain_valid(self) -> bool:
        """Comprobar génesis, estructura, orden, enlaces y prueba de trabajo."""
        try:
            if not isinstance(self.chain, list) or not self.chain:
                return False
            if self._hash(self.chain[0]) != self._genesis_hash:
                return False

            for index, block in enumerate(self.chain[1:], start=2):
                previous = self.chain[index - 2]
                if set(block) != self._BLOCK_FIELDS:
                    return False
                if type(block["index"]) is not int or block["index"] != index:
                    return False
                if type(block["proof"]) is not int or block["proof"] < 0:
                    return False
                timestamp = datetime.fromisoformat(block["timestamp"])
                if timestamp.tzinfo is None:
                    return False
                if timestamp < datetime.fromisoformat(previous["timestamp"]):
                    return False
                if not isinstance(block["data"], list) or not block["data"]:
                    return False
                for transaction in block["data"]:
                    self._validate_transaction(transaction)
                if block["previous_hash"] != self._hash(previous):
                    return False
                if not self._hash(block).startswith(self._PREFIX):
                    return False
            return True
        except (KeyError, TypeError, ValueError, OverflowError):
            return False


def main() -> int:
    """Mostrar dos transacciones en un bloque y detectar una alteración."""
    print("DEMO: VARIAS TRANSACCIONES POR BLOQUE")
    cadena = Blockchain()
    cadena.add_transaction({
        "Value": 50, "From": "Alice", "TO": "Bob", "Concept": "Primera prueba",
    })
    cadena.add_transaction({
        "Value": 25, "From": "Bob", "TO": "Carol", "Concept": "Segunda prueba",
    })
    pendientes_antes = len(cadena.pending_transactions)
    print("Pendientes antes de minar:", pendientes_antes)
    bloque = cadena.mine_block()
    print(json.dumps(cadena.chain, indent=2, ensure_ascii=False))

    valida = cadena.is_chain_valid()
    pendientes_despues = len(cadena.pending_transactions)
    print("Bloques:", len(cadena.chain))
    print("Transacciones del nuevo bloque:", len(bloque["data"]))
    print("Pendientes después de minar:", pendientes_despues)
    print("Cadena válida:", valida)

    contenido_original = deepcopy(cadena.chain)
    copia = deepcopy(cadena)
    copia.chain[1]["data"][0]["Value"] = 999
    copia_valida = copia.is_chain_valid()
    original_intacta = cadena.chain == contenido_original and cadena.is_chain_valid()
    print("Copia alterada válida:", copia_valida)
    print("Original intacta:", original_intacta)

    correcto = (
        pendientes_antes == 2 and len(cadena.chain) == 2
        and len(bloque["data"]) == 2 and pendientes_despues == 0
        and valida and not copia_valida and original_intacta
    )
    if not correcto:
        print("La demostración no produjo el resultado esperado.")
        return 1
    print("Demostración completada. Los datos permanecen únicamente en memoria.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
