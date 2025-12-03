#!/usr/bin/env python3
"""
SCRIPT VULNERABLE A INYECCIÓN SQL
⚠️  SOLO PARA FINES EDUCATIVOS - NO USAR EN PRODUCCIÓN ⚠️

Este script demuestra cómo NO proteger contra inyección SQL
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

    # Insertar usuarios de prueba
    usuarios_prueba = [
        ('admin', 'admin123', 'administrador'),
        ('profesor', 'profe456', 'docente'),
        ('alumno', 'estudiante789', 'estudiante')
    ]

    cursor.executemany('INSERT INTO usuarios (username, password, rol) VALUES (?, ?, ?)',
                       usuarios_prueba)
    conn.commit()
    return conn

def login_vulnerable(username, password):
    """
    ❌ VULNERABLE: Concatena directamente la entrada del usuario en la consulta SQL
    """
    conn = crear_base_datos()
    cursor = conn.cursor()

    # ⚠️ PELIGRO: Construcción de consulta SQL mediante concatenación de strings
    query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"

    print(f"[DEBUG] Consulta SQL ejecutada:")
    print(f"        {query}\n")

    try:
        cursor.execute(query)
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
    print("🔓 DEMOSTRACIÓN: LOGIN VULNERABLE A INYECCIÓN SQL")
    print("="*70)

    print("\n--- CASO 1: Login normal ---")
    login_vulnerable("alumno", "estudiante789")

    print("\n" + "-"*70)
    print("\n--- CASO 2: Credenciales incorrectas ---")
    login_vulnerable("alumno", "password_incorrecto")

    print("\n" + "-"*70)
    print("\n--- CASO 3: INYECCIÓN SQL - Bypass de autenticación ---")
    print("Input malicioso: username = admin' OR '1'='1")
    print("                 password = cualquier_cosa")
    login_vulnerable("admin' OR '1'='1", "cualquier_cosa")

    print("\n" + "-"*70)
    print("\n--- CASO 4: INYECCIÓN SQL - Comentario SQL ---")
    print("Input malicioso: username = admin'--")
    print("                 password = (vacío o cualquier cosa)")
    login_vulnerable("admin'--", "")

    print("\n" + "="*70)
    print("⚠️  CONCLUSIÓN: Este código es INSEGURO")
    print("   Un atacante puede acceder sin conocer la contraseña")
    print("="*70)

if __name__ == "__main__":
    main()
