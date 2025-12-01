"""
Test suite for the Gleam language server
"""

import os

import pytest

from solidlsp.ls import SolidLanguageServer
from solidlsp.ls_config import Language


@pytest.mark.gleam
class TestGleamLanguageServer:
    """Test basic functionality of the Gleam language server."""

    @pytest.mark.parametrize("language_server", [Language.GLEAM], indirect=True)
    def test_request_document_symbols(self, language_server: SolidLanguageServer) -> None:
        """Test request_document_symbols on the user.gleam file."""
        file_path = os.path.join("src", "test_repo", "user.gleam")
        all_symbols, root_symbols = language_server.request_document_symbols(file_path).get_all_symbols_and_roots()
        assert len(all_symbols) > 0

        # Find symbol names
        symbol_names = [symbol.get("name") for symbol in all_symbols if isinstance(symbol, dict) and "name" in symbol]

        assert "User" in symbol_names
        assert "new_user" in symbol_names

    @pytest.mark.parametrize("language_server", [Language.GLEAM], indirect=True)
    def test_request_references_user_type(self, language_server: SolidLanguageServer) -> None:
        """Test request_references on the User type."""
        file_path = os.path.join("src", "test_repo", "user.gleam")

        all_symbols, root_symbols = language_server.request_document_symbols(file_path).get_all_symbols_and_roots()

        # Find the User type symbol (kind 5 is class/type)
        user_symbols = [symbol for symbol in all_symbols if symbol.get("name") == "User"]

        assert len(user_symbols) >= 1, "Should find at least one User symbol"

        # Get position from selectionRange if available, otherwise from range
        user_type_symbols = [s for s in user_symbols if s.get("kind") == 5]  # 5 is class
        if not user_type_symbols:
            pytest.skip("No User type symbol found with kind=5")

        pos_info = user_type_symbols[0].get("selectionRange", user_type_symbols[0].get("range"))
        assert pos_info is not None and "start" in pos_info

        start = pos_info["start"]
        references = language_server.request_references(file_path, start["line"], start["character"])

        # Should find references in the main file
        main_references = [ref for ref in references if "test_repo.gleam" in ref["uri"]]
        assert len(main_references) >= 1, "User type should be referenced in main file"

    @pytest.mark.parametrize("language_server", [Language.GLEAM], indirect=True)
    def test_request_references_add_function(self, language_server: SolidLanguageServer) -> None:
        """Test request_references on the add function."""
        file_path = os.path.join("src", "test_repo", "math.gleam")
        all_symbols, root_symbols = language_server.request_document_symbols(file_path).get_all_symbols_and_roots()

        # Find the add function symbol
        add_symbol = None
        for symbol in all_symbols:
            if isinstance(symbol, dict) and symbol.get("name") == "add":
                add_symbol = symbol
                break

        if not add_symbol:
            pytest.skip("add function symbol not found in document symbols")

        # Get position from selectionRange if available, otherwise from range
        pos_info = add_symbol.get("selectionRange", add_symbol.get("range"))
        if not pos_info or "start" not in pos_info:
            pytest.skip("No position information available for add symbol")

        start = pos_info["start"]
        references = language_server.request_references(file_path, start["line"], start["character"])

        # Should find references in the main file
        main_references = [ref for ref in references if "test_repo.gleam" in ref["uri"]]
        assert len(main_references) > 0, "add function should be referenced in main file"
