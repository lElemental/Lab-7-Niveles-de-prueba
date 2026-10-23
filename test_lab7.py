import pytest
from library import Library, Book, User, CONFIG, settings

# ==========================================
# 7. FIXTURES
# ==========================================
@pytest.fixture
def libreria_base():
    lib = Library()
    lib.add_book(Book("1984", "George Orwell", 1949, "ISBN001"))
    lib.add_user(User(1, "Ana")) 
    return lib

@pytest.mark.unit
def test_tema_fixture(libreria_base):
    assert len(libreria_base.books) > 0

# ==========================================
# 4 y 5. MARCADORES Y PYTEST.INI
# (No olvides agregar 'examen' en tu pytest.ini)
# ==========================================
@pytest.mark.examen
def test_tema_marcador_uno():
    assert True

@pytest.mark.examen
def test_tema_marcador_dos():
    assert True

# ==========================================
# 6. PARAMETRIZE 
# ==========================================
@pytest.mark.unit
# Fíjate que aquí dice 'titulo'
@pytest.mark.parametrize('titulo, isbn, expected', [
    ('Moby Dick', 'ISBN004', 'Moby Dick'),
    ('Pride', 'ISBN005', 'Pride'),
    ('Dune', 'ISBN006', 'Dune') 
])
# Y aquí abajo también debe decir 'titulo'
def test_tema_parametrize(libreria_base, titulo, isbn, expected):
    libreria_base.add_book(Book(titulo, "Autor Genérico", 2000, isbn))
    assert libreria_base.books[-1].title == expected

# ==========================================
# 8. COBERTURA DE CAJA BLANCA
# ==========================================
@pytest.mark.system
def test_cobertura_usuario_falso(libreria_base):
    try:
        libreria_base._find_user(999) 
    except ValueError as e:
        # Aquí verificamos que el mensaje del error interno sea el correcto, sin usar capsys
        assert "User not found" in str(e)
# ==========================================
# 9. PYTEST.RAISES()
# ==========================================
@pytest.mark.system
def test_tema_raises(libreria_base):
    # Intentamos buscar un libro que no existe para forzar el ValueError
    with pytest.raises(ValueError):
        libreria_base._find_book("ISBN_INEXISTENTE")

# ==========================================
# 11. CAPSYS
# ==========================================
@pytest.mark.system
def test_tema_capsys(libreria_base, capsys, monkeypatch):
    # Desactivamos los préstamos temporalmente para que imprima en consola
    monkeypatch.setitem(settings, "loans_enabled", False)
    libreria_base.borrow_book(1, "ISBN001")
    
    captured = capsys.readouterr()
    # Verificamos que tu print("Loans are disabled") se haya capturado
    assert "Loans are disabled" in captured.out

# ==========================================
# 10. TRY-EXCEPT
# ==========================================
@pytest.mark.unit
def test_tema_try_except(libreria_base):
    try:
        # Forzamos un error mandando strings vacíos
        libreria_base.borrow_book("", "")
    except ValueError:
        # Atrapamos exitosamente el ValueError
        assert True
    except Exception:
        pytest.fail("Fallo: no se atrapó correctamente la excepción")

# ==========================================
# 3. MONKEYPATCH.SETITEM()
# ==========================================
@pytest.mark.system
def test_tema_setitem(monkeypatch):
    monkeypatch.setitem(CONFIG, "max_books", 5)
    assert CONFIG["max_books"] == 5

# ==========================================
# 1. MONKEYPATCH.SETATTR()
# ==========================================
@pytest.mark.unit
def test_tema_setattr(monkeypatch):
    libro = Book("The Great", "Autor", 1925, "003")
    
    def estado_falso(): 
        return "Perdido"
        
    monkeypatch.setattr(libro, "check_status", estado_falso, raising=False)
    assert libro.check_status() == "Perdido"

# ==========================================
# 2. MONKEYPATCH.DELATTR()
# ==========================================
@pytest.mark.unit
def test_tema_delattr(monkeypatch):
    libro = Book("The Great", "Autor", 1925, "003")
    monkeypatch.delattr(libro, "title", raising=False)
    assert not hasattr(libro, "title")