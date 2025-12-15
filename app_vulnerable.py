import sqlite3

def login_vulnerable(username, password):
    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    # ❌ CONCATENACIÓN DIRECTA - VULNERABLE
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
    print(f"[DEBUG] Query: {query}")

    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()

    if user:
        print(f"✅ Login exitoso! Bienvenido {user[1]}")
        return True
    else:
        print("❌ Credenciales incorrectas")
        return False

# Test normal
login_vulnerable("admin", "123456")

# Test con SQLi
login_vulnerable("admin' OR '1'='1", "cualquier_cosa")
