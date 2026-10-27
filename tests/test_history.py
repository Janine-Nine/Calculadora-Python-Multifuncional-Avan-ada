"""
Testes de persistência de histórico em JSON, busca, exclusão e exportação.
"""

import os
import tempfile
import unittest
from app.history import HistoryManager


class TestHistoryManager(unittest.TestCase):

    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.tmp_file.close()
        self.mgr = HistoryManager(storage_path=self.tmp_file.name)

    def tearDown(self):
        if os.path.exists(self.tmp_file.name):
            try:
                os.remove(self.tmp_file.name)
            except OSError:
                pass

    def test_add_and_retrieve(self):
        self.mgr.add_entry("2 + 2", "4", "Básica")
        self.mgr.add_entry("sqrt(9)", "3", "Científica")

        records = self.mgr.get_all()
        self.assertEqual(len(records), 2)
        self.assertEqual(records[0]["expressao"], "sqrt(9)")  # Mais recente no topo

    def test_search(self):
        self.mgr.add_entry("10 * 5", "50", "Básica")
        self.mgr.add_entry("juros_compostos", "1200", "Financeiro")

        results = self.mgr.search("Financeiro")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["categoria"], "Financeiro")

    def test_delete_and_clear(self):
        entry = self.mgr.add_entry("1 + 1", "2", "Básica")
        self.assertEqual(len(self.mgr.get_all()), 1)

        deleted = self.mgr.delete_entry(entry["id"])
        self.assertTrue(deleted)
        self.assertEqual(len(self.mgr.get_all()), 0)

        self.mgr.add_entry("a", "b")
        self.mgr.clear_all()
        self.assertEqual(len(self.mgr.get_all()), 0)

    def test_export_csv_and_json(self):
        self.mgr.add_entry("5 ^ 2", "25", "Básica")
        csv_path = self.tmp_file.name + ".csv"
        json_path = self.tmp_file.name + ".export.json"

        try:
            self.assertTrue(self.mgr.export_csv(csv_path))
            self.assertTrue(os.path.exists(csv_path))

            self.assertTrue(self.mgr.export_json(json_path))
            self.assertTrue(os.path.exists(json_path))
        finally:
            if os.path.exists(csv_path):
                os.remove(csv_path)
            if os.path.exists(json_path):
                os.remove(json_path)


if __name__ == "__main__":
    unittest.main()
