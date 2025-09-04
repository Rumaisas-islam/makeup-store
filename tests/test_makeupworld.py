import pytest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import MakeupWorld


# Fixture to create a temp file and object
@pytest.fixture
def makeup_obj(tmp_path):
    test_file = tmp_path / "record.txt"
    return MakeupWorld(filename=str(test_file))

def test_add_product(makeup_obj, monkeypatch):
    # Arrange: mock user input for add_product
    inputs = iter(["Lipstick", "1200", "Maybelline", "Makeup"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Act
    makeup_obj.add_product()

    # Assert file content
    with open(makeup_obj.filename, "r", encoding="UTF-8") as f:
        content = f.read()
    assert "Lipstick" in content
    assert "Maybelline" in content
    assert "1200" in content

def test_search_product(makeup_obj, monkeypatch, capsys):
    # Arrange: write a product directly
    with open(makeup_obj.filename, "w", encoding="UTF-8") as f:
        f.write("Product:Lipstick\nPrice:1200\nCompany:Maybelline\nUse:Makeup\n---------------------------\n")

    # Mock input for search
    monkeypatch.setattr("builtins.input", lambda _: "Lipstick")

    # Act
    makeup_obj.search_product("Product")
    captured = capsys.readouterr()

    # Assert output
    assert "Lipstick" in captured.out
    assert "Maybelline" in captured.out

def test_delete_product(makeup_obj, monkeypatch, capsys):
    # Arrange
    with open(makeup_obj.filename, "w", encoding="UTF-8") as f:
        f.write("Product:Lipstick\nPrice:1200\nCompany:Maybelline\nUse:Makeup\n---------------------------\n")

    # Mock inputs → first search value, then confirmation "yes"
    inputs = iter(["Lipstick", "yes"])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Act
    makeup_obj.delete_product("Product")
    captured = capsys.readouterr()

    # Assert
    assert "Selected product deleted" in captured.out

    # File should be empty after delete
    with open(makeup_obj.filename, "r", encoding="UTF-8") as f:
        content = f.read()
    assert "Lipstick" not in content

def test_edit_product(makeup_obj, monkeypatch, capsys):
    # Arrange: write original record
    with open(makeup_obj.filename, "w", encoding="UTF-8") as f:
        f.write("Product:Foundation\nPrice:2500\nCompany:Loreal\nUse:Makeup\n---------------------------\n")

    # Mock inputs: search value + confirmation + new details
    inputs = iter([
        "Foundation",   # search value
        "yes",          # confirm edit
        "Powder",       # new Product
        "1800",         # new Price
        "Maybelline",   # new Company
        "Makeup"        # new Use
    ])
    monkeypatch.setattr("builtins.input", lambda _: next(inputs))

    # Act
    makeup_obj.edit_product("Product")
    captured = capsys.readouterr()

    # Assert
    assert "Selected product updated successfully" in captured.out

    # File should contain updated product
    with open(makeup_obj.filename, "r", encoding="UTF-8") as f:
        content = f.read()
    assert "Powder" in content
    assert "1800" in content
    assert "Maybelline" in content
    assert "Foundation" not in content
