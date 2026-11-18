import builtins
from registration import *

def test_is_banned():
    assert is_banned("admin")
    assert is_banned("Admin")
    assert not is_banned("user")

def test_validate_username():
    assert validate_username("user1")
    assert not validate_username("")
    assert not validate_username("user name")
    assert not validate_username("admin")

def test_validate_email():
    assert validate_email("vu@email.com")
    assert not validate_email("vu@emailcom")
    assert not validate_email("vuemail.com")

def test_validate_display_name():
    assert validate_display_name("Vu_Display")
    assert not validate_display_name("ab") 
    assert not validate_display_name("a" * 21)
    assert not validate_display_name("Invalid-Name")
    assert not validate_display_name("1Invalid")  # starts with digit
    assert not validate_display_name("Invalid Name")  # contains space
    assert not validate_display_name("admin")  # banned word

def test_resolve_display_name():
    assert resolve_display_name("Vu_Display", "vu_anh") == "Vu_Display"
    assert resolve_display_name("", "vu_anh") == "vu_anh"

def test_register_valid():
    user = register("vu_anh", "vu@example.com", "Vu_Display")
    assert user["username"] == "vu_anh"
    assert user["email"] == "vu@example.com"
    assert user["display_name"] == "Vu_Display"

def test_register_invalid():
    try:
        register("admin", "invalid_email", "ab")
    except ValueError as e:
        assert "Invalid username" in str(e)
        assert "Invalid email" in str(e)
        assert "Invalid display name" in str(e)

def test_register_empty_display_name():
    user = register("vu_anh", "vu@example.com", "")
    assert user["username"] == "vu_anh"
    assert user["email"] == "vu@example.com"
    assert user["display_name"] == "vu_anh"

def test_main_valid_input(monkeypatch, capsys):
    answers = iter(["vu_anh", "vu@example.com", "Vu_Display"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(answers))

    main()

    assert "Registered" in capsys.readouterr().out

def test_main_invalid_input(monkeypatch, capsys):
    answers = iter(["admin", "invalid_email", "ab"])
    monkeypatch.setattr(builtins, "input", lambda prompt="": next(answers))

    main()

    output = capsys.readouterr().out
    assert "Invalid username" in output
    assert "Invalid email" in output
    assert "Invalid display name" in output