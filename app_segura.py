import sqlite3

def login_seguro(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # ✅ CONSULTA PARAMETRIZADA - SEGURO
    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
    print(f"[DEBUG] Query: {query}")
    print(f"[DEBUG] Params: {(username, password)}")

    cursor.execute(query, (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Login exitoso! Bienvenido {user[1]}")
        return True
    else:
        print("❌ Credenciales incorrectas")
        return False

# Test normal
login_seguro("admin", "123456")

# Test con SQLi (NO funciona)
login_seguro("admin' OR '1'='1", "cualquier_cosa")
