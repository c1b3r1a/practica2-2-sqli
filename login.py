#!/usr/bin/env python3
"""
LOGIN VULNERABLE - Versión KISS
⚠️  SOLO EDUCATIVO - NO USAR EN PRODUCCIÓN
"""

import sqlite3

# Crear BD en memoria con usuarios
conn = sqlite3.connect(':memory:')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE usuarios (
        username TEXT,
        password TEXT,
        rol TEXT
    )
''')

cursor.executemany(
    'INSERT INTO usuarios VALUES (?, ?, ?)',
    [('admin', 'admin123', 'administrador'),
     ('alumno', 'estudiante789', 'estudiante')]
)
conn.commit()

# Login vulnerable
username = input("Usuario: ")
password = input("Contraseña: ")

# ⚠️ VULNERABLE: Concatenación directa
query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"

print(f"\n[SQL] {query}\n")

cursor.execute(query)
resultado = cursor.fetchone()

if resultado:
    print(f"✅ Bienvenido {resultado[0]} ({resultado[2]})")
else:
    print("❌ Acceso denegado")

conn.close()
