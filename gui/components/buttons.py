"""Reusable button widgets."""
from __future__ import annotations

from typing import Callable, Optional

import customtkinter as ctk

from gui.theme import Theme


class PrimaryButton(ctk.CTkButton):
    def __init__(
        self,
        master,
        text: str,
        command: Optional[Callable] = None,
        width: int = 160,
        height: int = 44,
        **kwargs,
    ) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            width=width,
            height=height,
            fg_color=Theme.PRIMARY,
            hover_color=Theme.PRIMARY_HOVER,
            text_color="#FFFFFF",
            corner_radius=Theme.RADIUS,
            font=Theme.FONT_BODY_BOLD,
            **kwargs,
        )


class SecondaryButton(ctk.CTkButton):
    def __init__(
        self, master, text: str, command: Optional[Callable] = None, **kwargs
    ) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            height=44,
            fg_color=Theme.SURFACE_2,
            hover_color=Theme.SURFACE_3,
            text_color=Theme.TEXT,
            border_width=1,
            border_color=Theme.BORDER,
            corner_radius=Theme.RADIUS,
            font=Theme.FONT_BODY_BOLD,
            **kwargs,
        )


class GhostButton(ctk.CTkButton):
    def __init__(
        self, master, text: str, command: Optional[Callable] = None, **kwargs
    ) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            height=36,
            fg_color="transparent",
            hover_color=Theme.SURFACE_2,
            text_color=Theme.TEXT_MUTED,
            corner_radius=Theme.RADIUS_SM,
            font=Theme.FONT_BODY,
            **kwargs,
        )


class DangerButton(ctk.CTkButton):
    def __init__(
        self, master, text: str, command: Optional[Callable] = None, **kwargs
    ) -> None:
        super().__init__(
            master,
            text=text,
            command=command,
            height=40,
            fg_color=Theme.DANGER,
            hover_color="#D94864",
            text_color="#FFFFFF",
            corner_radius=Theme.RADIUS,
            font=Theme.FONT_BODY_BOLD,
            **kwargs,
        )
