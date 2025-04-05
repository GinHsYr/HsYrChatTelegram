# NOTE: This feature uses browser local storage! AKA it stores data on a viewer's
# machine. This may have privacy and compliance implications for your app. Be sure
# to take that into account with any usage.

import json
from typing import Any
import uuid
import streamlit as st

# Requires `pip install streamlit-js`
# https://github.com/toolittlecakes/streamlit_js
from streamlit_js import st_js

KEY_PREFIX = "st_localstorage_"


class StLocalStorage:
    """An Dict-like wrapper around browser local storage.

    Values are stored JSON encoded."""

    def __init__(self):
        # Keep track of a UUID for each key to enable reruns
        if "_ls_unique_keys" not in st.session_state:
            st.session_state["_ls_unique_keys"] = {}

        # Hide the JS iframes
        self._container = st.container()
        with self._container:
            st.html(""" 
                <style>
                    .element-container:has(iframe[height="0"]) {
                        display: none;
                    }
                </style>
            """)

    def __getitem__(self, key: str) -> Any:
        if key not in st.session_state["_ls_unique_keys"]:
            st.session_state["_ls_unique_keys"][key] = str(uuid.uuid4())
        code = f"""
        // The UUID changes on save, which causes this to rerun and update
        console.debug('{st.session_state["_ls_unique_keys"][key]}');
        return JSON.parse(localStorage.getItem('{KEY_PREFIX + key}'));
        """
        with self._container:
            result = st_js(code, key=st.session_state["_ls_unique_keys"][key])
        if result and result[0]:
            return json.loads(result[0])
        return None

    def __setitem__(self, key: str, value: Any) -> None:
        value = json.dumps(value, ensure_ascii=False)
        st.session_state["_ls_unique_keys"][key] = str(uuid.uuid4())
        code = f"""
        console.debug('setting {key} to local storage');
        localStorage.setItem('{KEY_PREFIX + key}', JSON.stringify('{value}'));
        """
        with self._container:
            return st_js(code, key=st.session_state["_ls_unique_keys"][key] + "_set")

    def __delitem__(self, key: str) -> None:
        st.session_state["_ls_unique_keys"][key] = str(uuid.uuid4())
        code = f"localStorage.removeItem('{KEY_PREFIX + key}');"
        with self._container:
            return st_js(code, key=st.session_state["_ls_unique_keys"][key] + "_del")

    def __contains__(self, key: str) -> bool:
        return self.__getitem__(key) is not None

    def get(self, key: str) -> Any:
        try:
            return self.__getitem__(key)
        except:
            return None

    def set(self, key: str, value: Any) -> None:
        try:
            self.__setitem__(key, value)
        except:
            return None
