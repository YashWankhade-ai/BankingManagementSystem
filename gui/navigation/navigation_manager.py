"""Navigation manager — registers screens and switches the active view."""
from __future__ import annotations

from typing import Callable, Dict, Optional

import customtkinter as ctk


class NavigationManager:
    def __init__(self, container: ctk.CTkFrame) -> None:
        self._container = container
        self._factories: Dict[str, Callable[[ctk.CTkFrame], ctk.CTkFrame]] = {}
        self._current: Optional[ctk.CTkFrame] = None
        self._current_name: Optional[str] = None
        self._on_change: Optional[Callable[[str], None]] = None

    def register(self, name: str, factory: Callable[[ctk.CTkFrame], ctk.CTkFrame]) -> None:
        self._factories[name] = factory

    def on_change(self, callback: Callable[[str], None]) -> None:
        self._on_change = callback

    def navigate(self, name: str, **kwargs) -> None:
        if name not in self._factories:
            raise KeyError(f"Unknown screen '{name}'")
        if self._current is not None:
            self._current.destroy()
        screen = self._factories[name](self._container, **kwargs) if kwargs else self._factories[name](self._container)
        screen.pack(fill="both", expand=True)
        self._current = screen
        self._current_name = name
        if self._on_change:
            self._on_change(name)

    @property
    def current_name(self) -> Optional[str]:
        return self._current_name
