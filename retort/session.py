# -*- coding: utf-8 -*-
"""
Session
~~~~~~~

Session handling objects.

"""
from . import utils


class SessionBase:
    """
    Base class for defining managing a session.
    """
    def __init__(self, session_key: str=None):
        self._session_key = session_key
        self.accessed = False
        self.modified = False

    def __contains__(self, key: str) -> bool:
        return key in self._session

    def __getitem__(self, key: str):
        return self._session[key]

    def __setitem__(self, key, value):
        self._session[key] = value
        self.modified = True

    def __delitem__(self, key):
        del self._session[key]
        self.modified = True

    def _get_new_session_key(self):
        return utils.token(128)

    def _get_or_create_session_key(self):
        if self._session_key is None:
            self._session_key = self._get_new_session_key()
        return self._session_key

    @property
    def session_key(self):
        return self._session_key

    @property
    def _session(self):
        self.accessed = True
        try:
            return self._session_cache
        except AttributeError:
            if self.session_key is None:
                self._session_cache = {}
            else:
                self._session_cache = self.load()
        return self._session_cache

    def exists(self, session_key):
        """
        Returns True if the given session_key already exists.
        """
        raise NotImplementedError('subclasses of SessionBase must provide an exists() method')

    def create(self):
        """
        Creates a new session instance. Guaranteed to create a new object with
        a unique key and will have saved the result once (with empty data)
        before the method returns.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a create() method')

    def save(self, must_create=False):
        """
        Saves the session data. If 'must_create' is True, a new session object
        is created (otherwise a CreateError exception is raised). Otherwise,
        save() can update an existing object with the same key.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a save() method')

    def delete(self, session_key=None):
        """
        Deletes the session data under this key. If the key is None, the
        current session key value is used.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a delete() method')

    def load(self):
        """
        Loads the session data and returns a dictionary.
        """
        raise NotImplementedError('subclasses of SessionBase must provide a load() method')
