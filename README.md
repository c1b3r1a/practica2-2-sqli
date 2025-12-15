# 4punt3s :(){ :|:& };:

    💀 Apuntes para Hackers, desde las trincheras de Internet con amor.

## 🔓 Inyección SQL (SQLi) - Material Didáctico

> **Objetivo educativo:** Comprender qué es la inyección SQL, cómo funciona y cómo prevenirla mediante ejemplos prácticos.

> **Objetivo1:** Preparación del entorno de prueba :SQLite en memoria + Python : login.py scripting

> **Objetivo2:** Desarrollo de las 2 caras de la moneda : 

>               - un script Python + SQLite vulnerable ...

>               - y otro seguro 

>     practicarlos y extraer conclusiones.
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

>  En preparación ! PROXIMAMENTE EN SUS PANTALLAS :-)
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

### 🎓 Ejercicio 1: Investigación

Busca información sobre un caso real de inyección SQL:

- **Empresa afectada**
- **Año del ataque**
- **Datos comprometidos**
- **Causa técnica (qué fallaba en el código)**
- **Consecuencias (multas, pérdida de confianza, etc.)**

**Sugerencias:** Sony PSN (2011), TalkTalk (2015), Equifax (2017)


### 🎓 Ejercicio 2: (para la próxima semana)

Familiarizarse con  la [ interacción  que facilita el script Python + SQLite de ejemplo](login.py)

### 🎓 Ejercicio 3: (para la próxima semana)

Identificar posibles vulnerabilidades ..(en preparación ;-))
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
