"""Spinner/loader."""
from __future__ import annotations

import customtkinter as ctk

from gui.theme import Theme


class Loader(ctk.CTkFrame):
    """Indeterminate progress indicator."""

    def __init__(self, master, **kwargs) -> None:
        super().__init__(master, fg_color="transparent", **kwargs)
        self._pb = ctk.CTkProgressBar(
            self, mode="indeterminate", progress_color=Theme.PRIMARY
        )
        self._pb.pack(fill="x", pady=10)

    def start(self) -> None:
        self._pb.start()

    def stop(self) -> None:
        self._pb.stop()
