"""Pruebas de comportamiento: python -m unittest -v test_crypto4."""

from copy import deepcopy
from datetime import datetime, timedelta
import unittest
from unittest.mock import patch

from Crypto4 import Blockchain


def transaction(value=50, sender="Alice", recipient="Bob"):
    return {"Value": value, "From": sender, "TO": recipient, "Concept": "Prueba"}


class BlockchainTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mined = Blockchain()
        cls.mined.add_transaction(transaction())
        cls.mined.add_transaction(transaction(25, "Bob", "Carol"))
        cls.mined.mine_block()

    def test_genesis_and_empty_mining(self):
        chain = Blockchain()
        before = deepcopy(chain.chain)
        self.assertEqual(chain.chain[0]["data"], [])
        self.assertEqual(chain.pending_transactions, [])
        self.assertTrue(chain.is_chain_valid())
        with self.assertRaises(ValueError):
            chain.mine_block()
        self.assertEqual(chain.chain, before)

    def test_batch_is_mined_once_and_cleared(self):
        chain = deepcopy(self.mined)
        self.assertEqual(len(chain.chain), 2)
        self.assertEqual(chain.chain[1]["data"], [transaction(), transaction(25, "Bob", "Carol")])
        self.assertEqual(chain.pending_transactions, [])
        next_transaction = transaction(10, "Carol", "Dana")
        self.assertEqual(chain.add_transaction(next_transaction), 3)
        next_block = chain.mine_block()
        self.assertEqual(next_block["data"], [next_transaction])
        self.assertEqual(len(chain.chain), 3)
        self.assertEqual(chain.pending_transactions, [])
        self.assertTrue(chain.is_chain_valid())

    def test_caller_cannot_mutate_pending_or_returned_blocks(self):
        chain = Blockchain()
        source = transaction()
        self.assertEqual(chain.add_transaction(source), 2)
        source["Value"] = 999
        pending_copy = chain.pending_transactions
        pending_copy[0]["Value"] = 888
        pending_copy.clear()
        self.assertEqual(chain.pending_transactions, [transaction()])
        block = chain.mine_block()
        block["data"][0]["Value"] = 777
        previous_copy = chain.get_previous_block()
        previous_copy["data"].clear()
        self.assertEqual(chain.chain[-1]["data"], [transaction()])
        self.assertTrue(chain.is_chain_valid())

    def test_invalid_transaction_does_not_change_pending(self):
        chain = Blockchain()
        chain.add_transaction(transaction())
        invalid = [None, {}, transaction(-1), transaction(0), transaction(True),
                   transaction(float("nan")), transaction(float("inf")),
                   transaction(sender=" "), {**transaction(), "Extra": 1}]
        for data in invalid:
            with self.subTest(data=data):
                with self.assertRaises((TypeError, ValueError)):
                    chain.add_transaction(data)
                self.assertEqual(chain.pending_transactions, [transaction()])

    def test_failed_mining_preserves_transactions_and_chain(self):
        chain = Blockchain()
        chain.add_transaction(transaction())
        before = deepcopy(chain.chain)
        with patch.object(chain, "_proof_of_work", side_effect=RuntimeError("Interrupción")):
            with self.assertRaises(RuntimeError):
                chain.mine_block()
        self.assertEqual(chain.pending_transactions, [transaction()])
        self.assertEqual(chain.chain, before)

    def test_detects_changes_in_the_last_block(self):
        changes = [
            lambda b: b["data"][0].update(Value=999),
            lambda b: b.update(previous_hash="incorrecto"),
            lambda b: b.update(proof=-1),
            lambda b: b.update(timestamp="2000-01-01T00:00:00+00:00"),
            lambda b: b.update(data=[]),
        ]
        for change in changes:
            with self.subTest(change=change):
                altered = deepcopy(self.mined)
                change(altered.chain[-1])
                self.assertFalse(altered.is_chain_valid())
        self.assertTrue(self.mined.is_chain_valid())

    def test_checks_index_even_after_mining_again(self):
        altered = deepcopy(self.mined)
        block = altered.chain[-1]
        block["index"] = 8
        block["proof"] = altered._proof_of_work(block)
        self.assertFalse(altered.is_chain_valid())

    def test_checks_timestamp_even_after_mining_again(self):
        altered = deepcopy(self.mined)
        block = altered.chain[-1]
        block["timestamp"] = (
            datetime.fromisoformat(altered.chain[0]["timestamp"]) - timedelta(seconds=1)
        ).isoformat()
        block["proof"] = altered._proof_of_work(block)
        self.assertFalse(altered.is_chain_valid())

    def test_genesis_and_malformed_chains_are_rejected(self):
        altered = deepcopy(self.mined)
        altered.chain[0]["data"].append(transaction())
        self.assertFalse(altered.is_chain_valid())
        for data in ([], [None], self.mined.chain[:1] + [{}]):
            with self.subTest(data=data):
                altered = deepcopy(self.mined)
                altered.chain = deepcopy(data)
                self.assertFalse(altered.is_chain_valid())

    def test_does_not_mine_on_an_altered_chain(self):
        altered = deepcopy(self.mined)
        altered.chain[-1]["data"][0]["Value"] = 999
        altered.add_transaction(transaction(10))
        before = deepcopy(altered.chain)
        with self.assertRaises(ValueError):
            altered.mine_block()
        self.assertEqual(altered.chain, before)
        self.assertEqual(altered.pending_transactions, [transaction(10)])


if __name__ == "__main__":
    unittest.main()
