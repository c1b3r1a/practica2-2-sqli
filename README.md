# 🎯 Objetivos de Aprendizaje de la práctica de SQLinjection

Al finalizar esta práctica, el alumnado será capaz de:

1. **Identificar** vulnerabilidades de inyección SQL en código Python + SQL
2. **Explotar** (de forma ética y controlada) aplicaciones vulnerables mediante SQLi
3. **Defender** aplicaciones mediante consultas parametrizadas y buenas prácticas
4. **Evaluar** la seguridad de código ajeno desde la perspectiva del atacante y del defensor
5. **Aplicar** lo aprendido en la práctica de Faker: diferencia entre concatenación insegura y parametrización

---

## 📋 Contexto: ¿Qué puede ocurrir si no tomamos las medidas adecuadas(como la parametrización de consultas) en nuestras bases de datps ?

En la [**Práctica 2.1 (Faker)**](https://pythonisas.github.io/Pythonisas/), algunos estudiantes de ASIR1 generaban INSERT SQL así:

```python
# ❌ VULNERABLE - Concatenación directa con f-strings
sql = f"INSERT INTO usuarios (nombre, email) VALUES ('{nombre}', '{email}');"
```

**Problema:** Si `nombre` contiene `'; DROP TABLE usuarios; --`, se ejecutaría código malicioso.

**Solución vista:**
```python
# ✅ SEGURO - Consultas parametrizadas
cursor.execute("INSERT INTO usuarios (nombre, email) VALUES (?, ?)", (nombre, email))
```

**En esta práctica:** Vamos a explorar **qué pasa cuando NO se parametriza** en aplicaciones interactivas.

## Pero antes de lanzarnos a los teclados ...

Puedes consultar, más en profundidad... [¿Qué es una ataque de inyección SQLi ?](https://owasp-uruguay.github.io/sqli-en-la-practica/intro/), en el la web del grupo OWASP de Uruguay.
así [como las posibles contramedidas](https://owasp-uruguay.github.io/sqli-en-la-practica/prevention/).

---

## 🏗️ Descripción de la Práctica

### Fase 1: Desarrollo del Prototipo (Blue Team)

Cada equipo desarrollará un **prototipo de aplicación Python + SQLite** similar al proyecto del gimnasio, con:

1. **Base de datos SQLite** con al menos 3 tablas relacionadas
2. **Script Python** que permita:
   - Crear la BD desde archivo `.sql`
   - **Login de usuario** (username + password)
   - **Búsqueda de registros** (por ID, nombre, etc.)
   - Inserción de datos (opcional)

3. **Dos versiones del mismo prototipo:**
   - `app_vulnerable.py` → Usa concatenación directa (f-strings, format, +)
   - `app_segura.py` → Usa consultas parametrizadas (`?` o `%s`)

4. **Datos de prueba:** Usar Faker para poblar la BD con registros realistas

**Temáticas sugeridas:**
- Sistema de reservas (hotel, restaurante, cine)
- Tienda online (productos, usuarios, pedidos)
- Biblioteca (libros, préstamos, usuarios)
- Plataforma educativa (alumnos, cursos, notas)
- Red social básica (usuarios, posts, comentarios)

---

### Fase 2: Ataque (Red Team)

Cada equipo recibe el `app_vulnerable.py` de **otro equipo** y debe:

1. **Identificar puntos de entrada** (inputs del usuario)
2. **Probar payloads de SQLi:**
   - **Bypass de autenticación:** `' OR '1'='1`
   - **Extracción de datos:** `' UNION SELECT ...`
   - **Modificación:** `'; UPDATE ... ; --`
   - **Eliminación:** `'; DROP TABLE ... ; --`

3. **Documentar:**
   - Payloads que funcionaron
   - Datos obtenidos/modificados
   - Impacto del ataque (robo de datos, bypass login, etc.)
   - Captura de pantalla o log de la explotación exitosa

4. **Intentar explotar `app_segura.py`** del mismo equipo
   - Verificar que NO es vulnerable

---

### Fase 3: Defensa (Blue Team)

Cada equipo recibe el **informe de ataque** sobre su `app_vulnerable.py` y debe:

1. **Analizar** los payloads que funcionaron
2. **Revisar** el código de `app_segura.py` con el atacante
3. **Añadir capas adicionales de seguridad:**
   - Validación de entrada (whitelist, longitud)
   - Principio de mínimo privilegio en BD
   - Logging de consultas sospechosas
   - Sanitización adicional (escapado de caracteres)

4. **Documentar** las mejoras implementadas

---

### Fase 4: Rotación y Presentación

- **Rotación:** Cada equipo ataca a otro diferente (todos son blue y red team)
- **Presentación oral (10 min):**
  - Demostración en vivo del ataque exitoso
  - Explicación de la vulnerabilidad explotada
  - Mostrar la versión segura y por qué NO es vulnerable
  - Lecciones aprendidas

---

## 📁 Estructura de Entrega

```
equipo_[NombreEquipo]/
├── README.md                    # Documentación del proyecto
├── app_vulnerable.py            # Versión INSEGURA (concatenación)
├── app_segura.py                # Versión SEGURA (parametrización)
├── database.sql                 # Script de creación de BD
├── generar_datos.py             # Script con Faker para poblar BD
├── requirements.txt             # Dependencias (faker, etc.)
├── ATAQUES.md                   # Informe de ataques realizados como Red Team
├── DEFENSAS.md                  # Informe de defensas como Blue Team
└── capturas/                    # Capturas de pantalla de exploits
    ├── exploit_login_bypass.png
    ├── exploit_data_extraction.png
    └── app_segura_resistente.png
```

---

## 🛠️ Requisitos Técnicos

### Software necesario:
- Python 3.x
- SQLite3 (incluido en Python)
- Faker (`pip install faker`)
- Editor de código (VS Code, PyCharm, etc.)

### Conocimientos previos:
- Python básico (variables, funciones, bucles)
- SQL básico (SELECT, INSERT, WHERE, JOIN)
- Proyecto grupal de gimnasio (SGBD)
- Práctica de Faker (generación de datos)

---

## 📝 Ejemplo Mínimo: Login Vulnerable vs Seguro

### Versión VULNERABLE (`app_vulnerable.py`):

```python
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
```

### Versión SEGURA (`app_segura.py`):

```python
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
```

---

## 🎯 Payloads de Ejemplo (Red Team)

### 1. Bypass de Autenticación:
```
Username: admin' OR '1'='1' --
Password: (cualquier cosa)
```

### 2. Extracción de datos (UNION):
```
Username: ' UNION SELECT null, username, password FROM usuarios --
Password: (vacío)
```

### 3. Comentarios SQL:
```
Username: admin'--
Password: (se ignora por el comentario)
```

### 4. Stacked queries (si el SGBD lo permite):
```
Username: '; DROP TABLE usuarios; --
Password: (vacío)
```

### 5. Boolean-based blind SQLi:
```
Username: admin' AND '1'='1
Username: admin' AND '1'='2
(observar diferencias en respuesta)
```

---

## 🛡️ Checklist de Seguridad (Blue Team)

### Nivel 1: Básico (OBLIGATORIO)
- [ ] Usar consultas parametrizadas (`?` en SQLite, `%s` en MySQL)
- [ ] NO concatenar strings para construir SQL
- [ ] Activar `PRAGMA foreign_keys = ON` en SQLite

### Nivel 2: Intermedio (RECOMENDADO)
- [ ] Validar tipo de dato (entero, email, etc.)
- [ ] Limitar longitud de inputs (username <= 50 caracteres)
- [ ] Whitelist de caracteres permitidos (solo alfanuméricos para username)
- [ ] Hash de contraseñas (bcrypt, argon2) - NO almacenar en texto plano

### Nivel 3: Avanzado (OPCIONAL)
- [ ] Usar ORM (SQLAlchemy) en lugar de SQL directo
- [ ] Principio de mínimo privilegio: cuenta BD sin permisos DROP/CREATE
- [ ] Rate limiting (máximo 5 intentos de login por minuto)
- [ ] Logging de consultas sospechosas (patrones como `' OR`, `UNION`, `--`)
- [ ] Preparar respuestas genéricas (no revelar si user existe o password es incorrecta)

---

## 📚 Recursos y Referencias

### Documentación:
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [SQLite Security Best Practices](https://www.sqlite.org/security.html)
- [Python sqlite3 - Placeholders](https://docs.python.org/3/library/sqlite3.html#sqlite3-placeholders)

### Herramientas (solo para laboratorio autorizado):
- [sqlmap](https://sqlmap.org/) - Automatización de SQLi
- [Burp Suite Community](https://portswigger.net/burp/communitydownload) - Proxy HTTP

### CTFs y práctica legal:
- [DVWA (Damn Vulnerable Web App)](https://github.com/digininja/DVWA)
- [HackTheBox](https://www.hackthebox.com/) - Máquinas vulnerables legales
- [OverTheWire: Natas](https://overthewire.org/wargames/natas/) - Wargames web

---

## ⚖️ Nota Legal y Ética

> ⚠️ **ADVERTENCIA LEGAL**
>
> Realizar ataques de inyección SQL contra sistemas sin autorización explícita es **ILEGAL** según el Código Penal Español (Art. 197 - acceso sin autorización a sistemas informáticos).
>
> Esta práctica es **exclusivamente educativa** y debe realizarse:
> - ✅ En tus propias aplicaciones creadas para esta práctica
> - ✅ En aplicaciones de compañeros con su consentimiento explícito
> - ✅ En laboratorios autorizados (DVWA, HTB, CTFs)
> - ❌ NUNCA en sistemas reales sin autorización

---

## 🎓 Evaluación

La práctica se evaluará según la rúbrica adjunta (`RUBRICA-PRACTICA2.2.md`), considerando:

- **Desarrollo técnico:** Calidad del código vulnerable y seguro
- **Capacidad de ataque:** Efectividad como Red Team
- **Capacidad de defensa:** Robustez de las defensas implementadas
- **Documentación:** Calidad de informes ATAQUES.md y DEFENSAS.md
- **Presentación oral:** Claridad en la explicación y demostración

---

## 📅 Cronograma Sugerido

| Sesión | Actividad | Entregable |
|--------|-----------|------------|
| **1** | Fase 1: Desarrollo Blue Team (app vulnerable + segura) | `app_vulnerable.py`, `app_segura.py` |
| **2** | Fase 2: Ataques Red Team (explotar apps de otros equipos) | `ATAQUES.md` + capturas |
| **3** | Fase 3: Defensa Blue Team (analizar ataques recibidos) | `DEFENSAS.md` |
| **4** | Fase 4: Presentaciones (10 min/equipo + preguntas) | Presentación oral |

---

## 🤝 Formación de Equipos

- **3-4 estudiantes por equipo**
- Cada equipo elige una temática diferente (hotel, tienda, biblioteca, etc.). Podéis usar el proyecto grupal del módulo de SGBD.
- Todos los equipos actúan como Blue Team (desarrollo) y Red Team (ataque)
- Asignación de objetivos: Equipo A ataca a Equipo B, Equipo B ataca a Equipo C, etc.

---

## ✅ Criterios de Éxito

Un equipo tendrá éxito si:

1. **Como Blue Team:**
   - Su `app_vulnerable.py` es explotable (demuestra conocimiento de vulnerabilidades)
   - Su `app_segura.py` resiste ataques (consultas parametrizadas correctas)

2. **Como Red Team:**
   - Logra explotar al menos 2 vulnerabilidades diferentes en otra app
   - Documenta claramente los payloads y su impacto

3. **Como equipo:**
   - Presenta de forma clara y didáctica
   - Extrae aprendizajes útiles de la experiencia

---

## 💡 Consejos Finales

- **No reinventes la rueda:** Inspírate en el proyecto del gimnasio y adapta la estructura
- **Usa Faker para poblar datos:** Aprovecha lo aprendido en Práctica 2.1
- **Documenta mientras trabajas:** No dejes la documentación para el final
- **Colabora con otros equipos:** El objetivo es aprender, no "ganar"
- **Pregunta si tienes dudas:** Mejor preguntar que cometer errores de seguridad

---

**¿Dudas? ¿Sugerencias?** Abre un issue o contacta con tu profesor.

**¡Buena suerte, hackers!** 🔐👨‍💻👩‍💻


