import os
import pytest
from backend.app.core.security import validate_safe_path, sanitize_filename, mask_api_key

def test_sanitize_filename():
    assert sanitize_filename("my_book.docx") == "my_book.docx"
    assert sanitize_filename("../../../etc/passwd") == "etcpasswd"
    assert sanitize_filename("..\\..\\windows\\system32\\cmd.exe") == "windowssystem32cmd.exe"
    assert sanitize_filename("Book Title: Modern AI?.docx") == "Book_Title_Modern_AI.docx"

def test_validate_safe_path_valid(tmp_path):
    base_dir = str(tmp_path)
    safe_file = str(tmp_path / "valid_book.docx")
    # Touch file
    with open(safe_file, "w") as f:
        f.write("content")

    resolved = validate_safe_path(base_dir, "valid_book.docx")
    assert resolved == os.path.abspath(safe_file)

def test_validate_safe_path_traversal_blocked(tmp_path):
    base_dir = str(tmp_path)
    # Attempting to escape base_dir
    with pytest.raises(ValueError):
        validate_safe_path(base_dir, "../secret.txt")

    with pytest.raises(ValueError):
        validate_safe_path(base_dir, "..\\..\\boot.ini")

def test_mask_api_key():
    assert mask_api_key(None) == ""
    assert mask_api_key("AIzaSy1234567890abcdef") == "AIza...cdef"
    assert mask_api_key("short") == "***"

