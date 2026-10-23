import pytest
from library import Library, Book, User, CONFIG, settings

# ==========================================
# 1. MONKEYPATCH.SETATTR()
# ==========================================
def test_tema_setattr(monkeypatch):
    libro = Book("The Great", "Autor", 1925, "003")
    
    # ESCRIBE AQUÍ TU FUNCIÓN FALSA Y TU MONKEYPATCH SETATTR:
    def estado_falso():
         return "perdido"
    monkeypatch.setattr(libro,"Check_status",estado_falso,raising=False)
    
    assert libro.check_status() == "Perdido"

# ==========================================
# 2. MONKEYPATCH.DELATTR()
# ==========================================
def test_tema_delattr(monkeypatch):
    libro = Book("The Great", "Autor", 1925, "003")
    
    # ESCRIBE AQUÍ TU MONKEYPATCH DELATTR:
    monkeypatch.delattr(libro,"title",raising=False)
    
    assert not hasattr(libro, "title")

# ==========================================
# 3. MONKEYPATCH.SETITEM()
# ==========================================
def test_tema_setitem(monkeypatch):
    # ESCRIBE AQUÍ TU MONKEYPATCH SETITEM:
    monkeypatch.setitem(CONFIG,"max_books",5)
    
    assert CONFIG["max_books"] == 5

# ==========================================
# 4 y 5. PYTEST.INI Y MARCADORES (2 PRUEBAS)
# ==========================================
# ESCRIBE AQUÍ TU DECORADOR DE MARCADOR:

def test_tema_marcador_uno():
    assert True

# ESCRIBE AQUÍ TU DECORADOR DE MARCADOR:

def test_tema_marcador_dos():
    assert True

# ==========================================
# 6. PARAMETRIZE
# ==========================================
# ESCRIBE AQUÍ TU DECORADOR PARAMETRIZE COMPLETO:
@pytest.mark.parametrize('titulo','isbn','expected'[
     ('Examen1','ISBN001','Examen1')
])


def test_tema_parametrize(libreria_base, titulo, isbn, expected):
    libreria_base.add_book(Book(titulo, "Autor Genérico", 2000, isbn))
    assert libreria_base.books[-1].title == expected

# ==========================================
# 7. FIXTURES
# ==========================================
# ESCRIBE AQUÍ EL DECORADOR DE FIXTURE:
@pytest.mark.fixture
def libreria_base():
    lib = Library()
    lib.add_book(Book("1984", "George Orwell", 1949, "ISBN001"))
    lib.add_user(User(1, "Ana"))
    return lib

# ==========================================
# 8. COBERTURA DE CAJA BLANCA
# ==========================================
def test_cobertura_usuario_falso(libreria_base, capsys):
    # ESCRIBE AQUÍ UN BLOQUE TRY-EXCEPT QUE BUSQUE AL USUARIO 999 Y ATRAPE EL ValueError:
    try:
         libreria_base._find_user(999)
    except ValueError:
         pass
    
    captured = capsys.readouterr()
    assert "User not found" in captured.out

# ==========================================
# 9. PYTEST.RAISES()
# ==========================================
def test_tema_raises(libreria_base):
    # ESCRIBE AQUÍ TU BLOQUE WITH PYTEST.RAISES:
    with pytest.raises("ISBN_INEXISTENTE"):
        libreria_base._find_book("ISBN_INEXISTENTE")

# ==========================================
# 10. TRY-EXCEPT
# ==========================================
def test_tema_try_except(libreria_base):
    # ESCRIBE AQUÍ TU BLOQUE TRY Y EXCEPT:
    try:
        libreria_base._find_book("ISBN_FALSO")
    except ValueError:
    
        assert True

# ==========================================
# 11. CAPSYS
# ==========================================
# AÑADE CAPSYS A LOS ARGUMENTOS DE ESTA FUNCIÓN:
def test_tema_capsys(libreria_base, monkeypatch,capsys):
    monkeypatch.setitem(settings, "loans_enabled", False)
    libreria_base.borrow_book(1, "ISBN001")
    
    # ESCRIBE AQUÍ EL CÓDIGO PARA CAPTURAR LA SALIDA:
    captured = capsys.readouterr()
    
    assert "Loans are disabled" in captured.out