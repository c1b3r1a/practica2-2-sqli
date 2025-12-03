# 🔓 Inyección SQL (SQLi) - Material Didáctico

> **Objetivo educativo:** Comprender qué es la inyección SQL, cómo funciona y cómo prevenirla mediante ejemplos prácticos.

---

## 📋 Índice

1. [¿Qué es la Inyección SQL?](#qué-es-la-inyección-sql)
2. [¿Por qué es peligroso?](#por-qué-es-peligroso)
3. [Demostración práctica](#demostración-práctica)
4. [Comparativa: Vulnerable vs Seguro](#comparativa-vulnerable-vs-seguro)
5. [Técnicas de ataque comunes](#técnicas-de-ataque-comunes)
6. [Prevención y buenas prácticas](#prevención-y-buenas-prácticas)
7. [Ejercicios propuestos](#ejercicios-propuestos)

---

## ¿Qué es la Inyección SQL?

**Definición:** Vulnerabilidad que permite a un atacante **insertar código SQL malicioso** en consultas de la aplicación, ejecutando comandos no autorizados en la base de datos.

### 🎯 Analogía del mundo real:

Imagina un formulario que pregunta: *"¿Cómo te llamas?"*

- Respuesta esperada: `"Juan"`
- Respuesta maliciosa: `"Juan' OR '1'='1"`

Si la aplicación concatena tu respuesta directamente en código, ejecutará comandos no previstos.

---

## ¿Por qué es peligroso?

### 💀 Impacto de una inyección SQL exitosa:

| Ataque | Consecuencia |
|--------|--------------|
| **Bypass de autenticación** | Acceso sin contraseña (como administrador) |
| **Robo de datos** | Extracción de toda la base de datos (GDPR breach) |
| **Modificación de datos** | Cambiar precios, notas, permisos |
| **Eliminación de datos** | `DROP TABLE usuarios; --` (borrado masivo) |
| **Ejecución de comandos** | En algunos SGBD, ejecutar comandos del sistema operativo |

### 📊 Estadísticas:

- **OWASP Top 10:** Inyección SQL está en el **#3** (2021)
- **Coste medio de un breach:** $4.35 millones (IBM 2022)
- **Casos reales:** Sony PSN (2011), Yahoo (2012), Equifax (2017)

---

## Demostración práctica

### 📂 Archivos incluidos:

| Archivo | Descripción |
|---------|-------------|
| `login_vulnerable.py` | ❌ Script **INSEGURO** con concatenación directa |
| `login_seguro.py` | ✅ Script **SEGURO** con consultas parametrizadas |

### 🚀 Ejecución:

```bash
# Script vulnerable
python3 login_vulnerable.py

# Script seguro
python3 login_seguro.py
```

---

## Comparativa: Vulnerable vs Seguro

### ❌ Código VULNERABLE (concatenación)

```python
# ⚠️ PELIGRO: Los valores se insertan directamente en el string SQL
username = input("Usuario: ")
password = input("Contraseña: ")

query = f"SELECT * FROM usuarios WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)
```

**Problema:** Si el usuario introduce `admin' OR '1'='1`, la consulta se convierte en:

```sql
SELECT * FROM usuarios WHERE username = 'admin' OR '1'='1' AND password = 'cualquier_cosa'
```

Como `'1'='1'` siempre es TRUE, el `OR` hace que toda la condición sea TRUE → **login exitoso sin contraseña**.

---

### ✅ Código SEGURO (consultas parametrizadas)

```python
# ✅ SEGURO: Los valores se pasan como parámetros separados
username = input("Usuario: ")
password = input("Contraseña: ")

query = "SELECT * FROM usuarios WHERE username = ? AND password = ?"
cursor.execute(query, (username, password))
```

**Protección:** Los placeholders (`?`) indican que ahí irán **datos**, no **código**. La librería escapa automáticamente los caracteres especiales.

Si el usuario introduce `admin' OR '1'='1`, se busca literalmente un usuario con ese nombre (que no existe).

---

## Técnicas de ataque comunes

### 1️⃣ Bypass de autenticación con OR

**Payload:** `admin' OR '1'='1`

```sql
-- Consulta original
SELECT * FROM usuarios WHERE username = 'admin' OR '1'='1' AND password = '...'

-- Resultado: Siempre TRUE, bypass exitoso
```

---

### 2️⃣ Comentarios SQL

**Payload:** `admin'--`

```sql
-- Consulta original
SELECT * FROM usuarios WHERE username = 'admin'-- ' AND password = '...'

-- Todo después de -- es un comentario, se ignora la verificación de contraseña
```

---

### 3️⃣ UNION-based SQLi (extracción de datos)

**Payload:** `' UNION SELECT username, password, 1 FROM usuarios--`

```sql
-- Permite extraer datos de otras tablas
SELECT * FROM productos WHERE id = '1' UNION SELECT username, password, 1 FROM usuarios--
```

---

### 4️⃣ Time-based Blind SQLi

**Payload:** `' OR SLEEP(5)--`

```sql
-- Si la página tarda 5 segundos, confirma que hay inyección SQL
SELECT * FROM usuarios WHERE id = '1' OR SLEEP(5)--
```

---

### 5️⃣ Stacked queries (múltiples comandos)

**Payload:** `'; DROP TABLE usuarios; --`

```sql
-- Ejecuta múltiples comandos separados por ;
SELECT * FROM productos WHERE id = '1'; DROP TABLE usuarios; --'
```

---

## Prevención y buenas prácticas

### 🛡️ Defensa #1: Consultas parametrizadas (Prepared Statements)

**Python (SQLite):**
```python
cursor.execute("SELECT * FROM usuarios WHERE username = ? AND password = ?", (user, pwd))
```

**Python (MySQL/PostgreSQL):**
```python
cursor.execute("SELECT * FROM usuarios WHERE username = %s AND password = %s", (user, pwd))
```

**PHP (PDO):**
```php
$stmt = $pdo->prepare("SELECT * FROM usuarios WHERE username = :user AND password = :pwd");
$stmt->execute(['user' => $username, 'pwd' => $password]);
```

**Java (JDBC):**
```java
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM usuarios WHERE username = ? AND password = ?");
stmt.setString(1, username);
stmt.setString(2, password);
```

---

### 🛡️ Defensa #2: ORM (Object-Relational Mapping)

Frameworks como **SQLAlchemy** (Python), **Hibernate** (Java), **Eloquent** (PHP) gestionan automáticamente la parametrización.

**Ejemplo con SQLAlchemy:**
```python
user = session.query(Usuario).filter_by(username=username, password=password).first()
```

---

### 🛡️ Defensa #3: Validación de entrada

- **Whitelist:** Solo permitir caracteres esperados (ej: `[a-zA-Z0-9_]` para usernames)
- **Longitud máxima:** Limitar tamaño de inputs
- **Tipo de dato:** Validar que sea el esperado (entero, email, etc.)

**⚠️ IMPORTANTE:** La validación es una capa adicional, NO reemplaza las consultas parametrizadas.

---

### 🛡️ Defensa #4: Principio de mínimo privilegio

- La cuenta de BD de la aplicación **NO debe ser root/admin**
- Permisos mínimos: `SELECT`, `INSERT`, `UPDATE` (sin `DROP`, `CREATE USER`, etc.)
- Usar cuentas diferentes para lectura/escritura

---

### 🛡️ Defensa #5: WAF y monitorización

- **WAF (Web Application Firewall):** ModSecurity, Cloudflare
- **IDS/IPS:** Detectar patrones de ataque (Snort, Suricata)
- **Logging:** Registrar todas las consultas SQL para auditoría

---

## Ejercicios propuestos

### 🎓 Ejercicio 1: Identificar vulnerabilidades

Analiza este código PHP y explica por qué es vulnerable:

```php
$id = $_GET['id'];
$query = "SELECT * FROM productos WHERE id = $id";
$result = mysqli_query($conn, $query);
```

**Tareas:**
1. ¿Qué payload usarías para extraer datos de la tabla `usuarios`?
2. Reescribe el código de forma segura usando `mysqli_prepare()`

---

### 🎓 Ejercicio 2: Práctica con los scripts

1. Ejecuta `login_vulnerable.py` e intenta:
   - Login con credenciales correctas
   - Bypass con `admin' OR '1'='1`
   - Bypass con `admin'--`

2. Ejecuta `login_seguro.py` con los mismos payloads
   - ¿Por qué los ataques no funcionan?
   - Consulta el [DEBUG] para ver cómo se procesan los parámetros

---

### 🎓 Ejercicio 3: Investigación

Busca información sobre un caso real de inyección SQL:

- **Empresa afectada**
- **Año del ataque**
- **Datos comprometidos**
- **Causa técnica (qué fallaba en el código)**
- **Consecuencias (multas, pérdida de confianza, etc.)**

**Sugerencias:** Sony PSN (2011), TalkTalk (2015), Equifax (2017)

---

### 🎓 Ejercicio 4: Laboratorio CTF

Practica en entornos controlados:

- [HackTheBox](https://www.hackthebox.com/) - Máquinas con SQLi
- [PortSwigger Web Security Academy](https://portswigger.net/web-security/sql-injection) - Labs gratuitos
- [DVWA (Damn Vulnerable Web Application)](https://github.com/digininja/DVWA) - Para montar localmente

---

## 📚 Referencias y recursos

### Documentación oficial:
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [CWE-89: SQL Injection](https://cwe.mitre.org/data/definitions/89.html)
- [SQLite Security](https://www.sqlite.org/security.html)

### Herramientas de testing:
- [sqlmap](https://sqlmap.org/) - Herramienta automática de explotación SQLi
- [Burp Suite](https://portswigger.net/burp) - Proxy para interceptar/modificar requests
- [OWASP ZAP](https://www.zaproxy.org/) - Scanner de vulnerabilidades

### Lecturas recomendadas:
- *The Web Application Hacker's Handbook* (Stuttard & Pinto)
- *SQL Injection Attacks and Defense* (Clarke)

---

## ⚖️ Nota legal

> **Este material es exclusivamente educativo** para ciclos formativos de **ASIR**, **DAW** y **Ciberseguridad**.
>
> ⚠️ **Realizar ataques SQLi contra sistemas sin autorización explícita es ILEGAL** (Código Penal art. 197 - acceso sin autorización).
>
> Solo practica en:
> - Tus propias aplicaciones
> - Laboratorios autorizados (HTB, DVWA, etc.)
> - CTFs y competiciones legítimas

---

## 👨‍🏫 Autor

Material didáctico para ciclos de Formación Profesional
Enfoque: Aprendizaje Basado en Problemas (ABP)
Licencia: Uso educativo

---

**¿Dudas? ¿Sugerencias?** Abre un issue o contacta con tu profesor.
