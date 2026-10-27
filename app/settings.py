"""
Módulo de Configurações e Preferências
Persistência de preferências de usuário em JSON: tema, precisão, separadores e modo angular.
"""

import json
import os
from typing import Dict, Any


DEFAULT_SETTINGS = {
    "theme": "dark",             # "dark" ou "light"
    "precision": 6,              # casas decimais
    "decimal_separator": ",",    # padrão brasileiro ","
    "thousands_separator": ".",  # padrão brasileiro "."
    "angle_mode": "deg",         # "deg" ou "rad"
}


class SettingsManager:
    """Gerencia preferências e configurações do aplicativo com persistência local."""

    def __init__(self, config_path: str = "data/settings.json"):
        self.config_path = config_path
        self._ensure_dir()
        self.settings: Dict[str, Any] = self._load()

    def _ensure_dir(self):
        dir_name = os.path.dirname(self.config_path)
        if dir_name and not os.path.exists(dir_name):
            try:
                os.makedirs(dir_name, exist_ok=True)
            except OSError:
                pass

    def _load(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            return dict(DEFAULT_SETTINGS)
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                loaded = json.load(f)
                result = dict(DEFAULT_SETTINGS)
                if isinstance(loaded, dict):
                    result.update(loaded)
                return result
        except (json.JSONDecodeError, OSError):
            return dict(DEFAULT_SETTINGS)

    def save(self) -> bool:
        try:
            self._ensure_dir()
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
            return True
        except OSError:
            return False

    def get(self, key: str, default: Any = None) -> Any:
        return self.settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self.settings[key] = value
        self.save()

    def reset_defaults(self) -> None:
        self.settings = dict(DEFAULT_SETTINGS)
        self.save()
