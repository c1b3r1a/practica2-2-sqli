#!/usr/bin/env python3
"""
SCRIPT SEGURO CONTRA INYECCIÓN SQL
✅ BUENAS PRÁCTICAS - Usa consultas parametrizadas

Este script demuestra cómo proteger correctamente contra inyección SQL
"""

import sqlite3

def crear_base_datos():
    """Crea una base de datos de ejemplo con usuarios"""
    conn = sqlite3.connect(':memory:')  # Base de datos en memoria (temporal)
    cursor = conn.cursor()

    # Crear tabla usuarios
    cursor.execute('''
        CREATE TABLE usuarios (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            rol TEXT NOT NULL
        )
    ''')

    # Insertar usuarios de prueba usando consultas parametrizadas
    usuarios_prueba = [
        ('admin', 'admin123', 'administrador'),
        ('profesor', 'profe456', 'docente'),
        ('alumno', 'estudiante789', 'estudiante')
    ]

    cursor.executemany('INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)',
                       usuarios_prueba)
    conn.commit()
    return conn

def login_seguro(username, password):
    """
    ✅ SEGURO: Usa consultas parametrizadas (placeholders)
    Los valores del usuario se pasan por separado, no se concatenan en el SQL
    """
    conn = crear_base_datos()
    cursor = conn.cursor()

    # ✅ SEGURO: Uso de placeholders (?) para parámetros
    query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"

    print(f"[DEBUG] Consulta SQL (con placeholders):")
    print(f"        {query}")
    print(f"[DEBUG] Parámetros: username='{username}', password='{password}'\n")

    try:
        # Los parámetros se pasan como tupla separada de la consulta
        cursor.execute(query, (username, password))
        resultado = cursor.fetchone()

        if resultado:
            print(f"✅ Login exitoso!")
            print(f"   Usuario: {resultado[1]}")
            print(f"   Rol: {resultado[3]}")
            return True
        else:
            print("❌ Credenciales incorrectas")
            return False
    except sqlite3.Error as e:
        print(f"⚠️  Error SQL: {e}")
        return False
    finally:
        conn.close()

def main():
    print("="*70)
    print("🔒 DEMOSTRACIÓN: LOGIN SEGURO CONTRA INYECCIÓN SQL")
    print("="*70)

    print("\n--- CASO 1: Login normal ---")
    login_seguro("alumno", "estudiante789")

    print("\n" + "-"*70)
    print("\n--- CASO 2: Credenciales incorrectas ---")
    login_seguro("alumno", "password_incorrecto")

    print("\n" + "-"*70)
    print("\n--- CASO 3: Intento de INYECCIÓN SQL - Bypass bloqueado ---")
    print("Input malicioso: username = admin' OR '1'='1")
    print("                 password = cualquier_cosa")
    print("Resultado esperado: El ataque NO funciona\n")
    login_seguro("admin' OR '1'='1", "cualquier_cosa")

    print("\n" + "-"*70)
    print("\n--- CASO 4: Intento de INYECCIÓN SQL - Comentario bloqueado ---")
    print("Input malicioso: username = admin'--")
    print("                 password = (vacío)")
    print("Resultado esperado: El ataque NO funciona\n")
    login_seguro("admin'--", "")

    print("\n" + "="*70)
    print("✅ CONCLUSIÓN: Este código es SEGURO")
    print("   Las consultas parametrizadas previenen inyección SQL")
    print("   Los caracteres especiales se tratan como datos, no como código")
    print("="*70)

    print("\n" + "="*70)
    print("📚 ¿POR QUÉ ES SEGURO?")
    print("="*70)
    print("""
Cuando usas placeholders (?):
1. La consulta SQL se compila primero
2. Los parámetros se vinculan después como DATOS, no como CÓDIGO
3. Las comillas simples se escapan automáticamente
4. No hay manera de inyectar comandos SQL

Alternativas según el lenguaje:
- Python SQLite: ? o :nombre
- Python MySQL/PostgreSQL: %s o %(nombre)s
- PHP PDO: :nombre o ?
- Java JDBC: ? (PreparedStatement)
""")

if __name__ == "__main__":
    main()
