from __future__ import annotations

import os
from typing import Any, MutableMapping

from nicegui import app, context

# Fallback storage for environments without NiceGUI client context (e.g. tests)
_fallback_store: dict[str, dict[str, Any]] = {}

DEBUG_AUTH = os.getenv('AUTH_STORAGE_DEBUG', '').lower() in {'1', 'true', 'yes'}


def _debug(message: str) -> None:
    if DEBUG_AUTH:
        print(f'[auth_storage] {message}')


def _get_session() -> MutableMapping[str, Any] | None:
    client = getattr(context, 'client', None)
    request = getattr(client, 'request', None) if client else None
    session = getattr(request, 'session', None) if request else None
    if session is not None:
        _debug(f'Using session storage for client={getattr(client, "id", "?")}')
    return session


def _resolve_store() -> MutableMapping[str, Any]:
    """Return a storage dict that is safe to use in any context."""
    try:
        return app.storage.browser
    except RuntimeError:
        pass

    try:
        return app.storage.user
    except RuntimeError:
        client = getattr(context, 'client', None)
        if client and hasattr(client, 'storage'):
            return client.storage
        key = getattr(client, 'id', 'default') if client else 'default'
        return _fallback_store.setdefault(key, {})


def get_store() -> MutableMapping[str, Any]:
    return _resolve_store()


def set_auth_data(data: dict[str, Any]) -> None:
    store = get_store()
    store.update(data)
    _debug(f'set_auth_data -> store keys={list(store.keys())}')

    session = _get_session()
    if session is not None:
        session.update(data)
        _debug(f'set_auth_data -> session keys={list(session.keys())}')


def get_auth_value(key: str, default: Any = None) -> Any:
    store = get_store()
    if key in store:
        return store.get(key, default)

    session = _get_session()
    if session is not None:
        _debug(f'get_auth_value({key}) -> session hit')
        return session.get(key, default)

    return default


def is_authenticated() -> bool:
    store_value = bool(get_auth_value('authenticated', False))
    if store_value:
        _debug('is_authenticated -> True via store/get_auth_value')
        return True

    session = _get_session()
    if session is not None:
        session_value = bool(session.get('authenticated', False))
        _debug(f'is_authenticated -> {session_value} via session fallback')
        return session_value

    _debug('is_authenticated -> False (no store, no session)')
    return False


def clear_auth_data() -> None:
    get_store().clear()

    session = _get_session()
    if session is not None:
        for key in ('authenticated', 'token', 'username', 'email', 'role'):
            session.pop(key, None)
