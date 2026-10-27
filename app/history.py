"""
Módulo de Histórico e Persistência
Armazenamento local persistente em JSON com busca, exclusão, reuso
e exportação para CSV e JSON estruturado.
"""

import csv
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional


class HistoryManager:
    """Gerenciador seguro de histórico de operações com persistência local em JSON."""

    def __init__(self, storage_path: str = "data/history.json"):
        self.storage_path = storage_path
        self._ensure_storage_dir()
        self.records: List[Dict[str, Any]] = self._load()

    def _ensure_storage_dir(self):
        directory = os.path.dirname(self.storage_path)
        if directory and not os.path.exists(directory):
            try:
                os.makedirs(directory, exist_ok=True)
            except OSError:
                pass

    def _load(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.storage_path):
            return []
        try:
            with open(self.storage_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            # Recuperação silenciosa com histórico limpo caso arquivo esteja corrompido
            return []

    def save(self) -> bool:
        try:
            self._ensure_storage_dir()
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    def add_entry(self, expression: str, result: str, category: str = "Geral") -> Dict[str, Any]:
        """Adiciona um novo registro ao histórico."""
        entry = {
            "id": len(self.records) + 1,
            "expressao": str(expression),
            "resultado": str(result),
            "categoria": category,
            "timestamp": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        }
        self.records.insert(0, entry)  # Mais recentes no topo
        self.save()
        return entry

    def get_all(self) -> List[Dict[str, Any]]:
        return self.records

    def search(self, query: str) -> List[Dict[str, Any]]:
        """Busca por termo na expressão, resultado ou categoria."""
        q = query.lower().strip()
        if not q:
            return self.records
        return [
            r for r in self.records
            if q in r.get("expressao", "").lower()
            or q in r.get("resultado", "").lower()
            or q in r.get("categoria", "").lower()
        ]

    def delete_entry(self, entry_id: int) -> bool:
        """Remove um registro específico pelo ID."""
        initial_len = len(self.records)
        self.records = [r for r in self.records if r.get("id") != entry_id]
        if len(self.records) != initial_len:
            self.save()
            return True
        return False

    def clear_all(self) -> None:
        """Limpa todo o histórico."""
        self.records = []
        self.save()

    def export_csv(self, target_filepath: str) -> bool:
        """Exporta os registros para um arquivo CSV estruturado."""
        try:
            directory = os.path.dirname(target_filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            with open(target_filepath, "w", encoding="utf-8", newline="") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["ID", "Data e Hora", "Categoria", "Expressão", "Resultado"])
                for r in self.records:
                    writer.writerow([
                        r.get("id", ""),
                        r.get("timestamp", ""),
                        r.get("categoria", ""),
                        r.get("expressao", ""),
                        r.get("resultado", ""),
                    ])
            return True
        except OSError:
            return False

    def export_json(self, target_filepath: str) -> bool:
        """Exporta os registros para um arquivo JSON estruturado."""
        try:
            directory = os.path.dirname(target_filepath)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)

            with open(target_filepath, "w", encoding="utf-8") as f:
                json.dump(self.records, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False
