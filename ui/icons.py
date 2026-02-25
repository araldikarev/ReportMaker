"""Centralised icon factory — vibrant modern palette."""
from __future__ import annotations

import qtawesome as qta
from PyQt6.QtGui import QIcon

# ── Palette (Modern Vibrant) ──
_WHITE      = "#f8fafc"   # Яркий белый для текста
_DIM        = "#64748b"   # Slate-500 для второстепенных иконок
_BLUE       = "#3b82f6"   # Яркий синий (Primary)
_BLUE_SOFT  = "#60a5fa"   # Более мягкий синий
_GREEN      = "#10b981"   # Emerald-500 (Успех)
_RED        = "#f43f5e"   # Rose-500 (Опасность)
_ORANGE     = "#f59e0b"   # Amber-500 (Акцент)


def _ic(name: str, color: str = _WHITE, **kw) -> QIcon:
    return qta.icon(name, color=color, **kw)


# ── Tab icons ──
def file_word():     return _ic("fa5s.file-alt",       _BLUE)
def file_code():     return _ic("fa5s.code",           _GREEN)
def chart_bar():     return _ic("fa5s.layer-group",    _ORANGE)

# ── Actions ──
def folder_open():   return _ic("fa5s.folder-open",    _DIM)
def bolt():          return _ic("fa5s.bolt",           _WHITE)
def copy():          return _ic("fa5s.copy",           _DIM)
def refresh():       return _ic("fa5s.redo",           _DIM)
def plus():          return _ic("fa5s.plus",           _GREEN)
def times():         return _ic("fa5s.times",          _RED)
def image():         return _ic("fa5s.image",          _BLUE_SOFT)
def link_ext():      return _ic("fa5s.external-link-alt", _BLUE)
def hammer():        return _ic("fa5s.hammer",         _WHITE)
def save():          return _ic("fa5s.save",           _DIM)
def clipboard():     return _ic("fa5s.clipboard-check",_GREEN)
def cog():           return _ic("fa5s.cog",            _DIM)