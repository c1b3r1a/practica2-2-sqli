# 🐧 Imagen WSL para Práctica 2.2 - Inyección SQL

**Entorno preconfigurado para Windows** con todas las herramientas necesarias para realizar la práctica de SQL Injection.

---

## 📦 ¿Qué es esto?

Es una **imagen de Debian lista para usar en WSL** (Windows Subsystem for Linux) que incluye:

- ✅ Python 3.13.5
- ✅ SQLite 3.46.1
- ✅ Faker (generación de datos)
- ✅ Git, Emacs, Nano
- ✅ sqlmap (herramienta de testing)
- ✅ Herramientas de red

**Ventajas:**
- No necesitas instalar nada manualmente
- Todos tenéis el mismo entorno
- Funciona en Windows 10/11
- Listos para trabajar en 5 minutos

---

## 📋 Requisitos Previos

### Verificar que tienes WSL instalado

Abre **PowerShell** y ejecuta:

```powershell
wsl --version
```

**Si funciona**: Continúa al siguiente paso ✅

**Si da error**: Instala WSL ejecutando esto en PowerShell como **Administrador**:

```powershell
wsl --install
```

Después **reinicia el equipo**.

---

## 📥 Paso 1: Descargar la Imagen

**Opciones de descarga:**

1. **Google Drive / Nextcloud**: (enlace proporcionado por el profesor)
2. **USB**: Copia el archivo desde el USB del profesor
3. **Red local**: (si está disponible en servidor interno)

**Archivo a descargar:**
```
PRACTICA2.2-inyeccion-SQLi.tar.gz
Tamaño: 386 MB
```

**Importante:** Guarda el archivo en una ubicación fácil de recordar, por ejemplo:
- `C:\Users\TuUsuario\Downloads\`
- `C:\WSL\`

---

## 📥 Paso 2: Importar en WSL

Abre **PowerShell** (no necesitas ser Administrador) y ejecuta:

```powershell
# Crear directorio para la distribución
mkdir C:\WSL\SQLi-Practica

# Importar la imagen (ajusta la ruta si descargaste en otro lugar)
wsl --import SQLi-Practica C:\WSL\SQLi-Practica C:\Users\TuUsuario\Downloads\PRACTICA2.2-inyeccion-SQLi.tar.gz

# Verificar que se importó correctamente
wsl --list -v
```

**Deberías ver algo como:**
```
  NAME            STATE           VERSION
* SQLi-Practica   Stopped         2
```

---

## 🚀 Paso 3: Entrar al Entorno

En PowerShell, ejecuta:

```powershell
wsl -d SQLi-Practica
```

**Verás el mensaje de bienvenida:**
```
╔═══════════════════════════════════════════════════════════╗
║  Entorno WSL - PRACTICA 2.2: Inyección SQL               ║
║  Python 3.13 + SQLite3 + Faker + Git + Emacs             ║
║                                                           ║
║  Directorio de trabajo: ~/practica-sqli                  ║
║  Usuario: alumno / Password: alumno123                   ║
╚═══════════════════════════════════════════════════════════╝
```

🎉 **¡Ya estás dentro de Linux desde Windows!**

---

## ✅ Paso 4: Verificar que Todo Funciona

Ejecuta estos comandos uno por uno dentro de WSL:

```bash
# Verificar Python
python3 --version
# Debe mostrar: Python 3.13.5

# Verificar SQLite
sqlite3 --version
# Debe mostrar: 3.46.1

# Verificar Faker
python3 -c "from faker import Faker; print('Faker OK')"
# Debe mostrar: Faker OK

# Verificar Git
git --version
# Debe mostrar: git version 2.47.3
```

**Si todos los comandos funcionan**: ✅ **Todo listo para empezar**

---

## 📂 Paso 5: Clonar el Repositorio de la Práctica

Dentro de WSL, en tu directorio de trabajo:

```bash
cd ~/practica-sqli

# Clonar el repositorio (URL proporcionada por el profesor)
git clone https://github.com/PROFESOR/PRACTICA2.2-inyeccion-SQLi.git
cd PRACTICA2.2-inyeccion-SQLi

# Ver archivos
ls -la
```

**Archivos que deberías ver:**
- `app_vulnerable.py` - Aplicación vulnerable a SQLi
- `app_segura.py` - Aplicación protegida
- `README.md` - Enunciado de la práctica
- `database.sql` - Script de creación de BD

---

## 🔧 Uso Diario

### Entrar al entorno

```powershell
# Desde PowerShell
wsl -d SQLi-Practica
```

### Salir del entorno

```bash
# Desde dentro de WSL
exit
```

### Acceder a archivos de Windows desde WSL

```bash
# Tus archivos de Windows están en /mnt/
cd /mnt/c/Users/TuUsuario/Documents
```

### Acceder a archivos de WSL desde Windows

En el Explorador de Windows, ve a:
```
\\wsl$\SQLi-Practica\home\alumno\practica-sqli
```

---

## 🛠️ Comandos Útiles

### Python

```bash
# Ejecutar script Python
python3 app_vulnerable.py

# Crear entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar paquetes
pip install nombre-paquete
```

### SQLite

```bash
# Abrir base de datos
sqlite3 usuarios.db

# Dentro de SQLite
.tables           # Ver tablas
.schema usuarios  # Ver estructura
SELECT * FROM usuarios;  # Consultar datos
.quit             # Salir
```

### Git

```bash
# Configurar Git (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu@email.com"

# Comandos básicos
git status
git add .
git commit -m "mensaje"
git push
```

### Emacs (Editor)

```bash
# Abrir archivo
emacs archivo.py

# Comandos dentro de Emacs
Ctrl+X Ctrl+S  # Guardar
Ctrl+X Ctrl+C  # Salir
```

**Alternativa**: Usa `nano` si prefieres algo más sencillo:
```bash
nano archivo.py
```

---

## ❓ Problemas Comunes

### "No puedo importar la imagen"

**Solución 1**: Verifica que WSL2 está instalado
```powershell
wsl --set-default-version 2
```

**Solución 2**: Verifica la ruta del archivo .tar.gz
```powershell
# Listar archivos en Downloads
dir C:\Users\TuUsuario\Downloads\*.tar.gz
```

### "No me deja entrar como root"

**No necesitas root**. El usuario `alumno` tiene permisos sudo sin contraseña:
```bash
sudo apt update  # No pedirá contraseña
```

### "He borrado archivos por error"

**Solución**: Reimportar la imagen (borra la actual primero)
```powershell
wsl --unregister SQLi-Practica
wsl --import SQLi-Practica C:\WSL\SQLi-Practica PRACTICA2.2-inyeccion-SQLi.tar.gz
```

### "Faker no funciona"

Dentro de WSL:
```bash
python3 -c "from faker import Faker; print('OK')"
```

Si falla:
```bash
pip3 install --user faker
```

### "No tengo conexión a internet desde WSL"

```bash
# Verificar conectividad
ping -c 3 8.8.8.8

# Si falla, reinicia WSL desde PowerShell
wsl --shutdown
wsl -d SQLi-Practica
```

---

## 🗑️ Desinstalar

Si quieres eliminar completamente el entorno:

```powershell
# 1. Eliminar la distribución de WSL
wsl --unregister SQLi-Practica

# 2. Borrar archivos (opcional)
rmdir /s C:\WSL\SQLi-Practica
```

---

## 📚 Documentación Adicional

**En este mismo directorio encontrarás:**

- `sqli-wsl+rootfs-workflow_Ed2.md` - Guía completa con instrucciones avanzadas
- `RESUMEN-IMAGEN.md` - Especificaciones técnicas de la imagen
- `README.md` - Enunciado de la práctica de SQL Injection

**Enlaces útiles:**
- [Documentación oficial de WSL](https://learn.microsoft.com/es-es/windows/wsl/)
- [OWASP SQL Injection](https://owasp.org/www-community/attacks/SQL_Injection)
- [Documentación de Python](https://docs.python.org/3/)

---

## 💡 Consejos Finales

✅ **Haz commits frecuentes** de tu trabajo con Git

✅ **Usa entornos virtuales** de Python para cada proyecto

✅ **No tengas miedo de experimentar** - puedes reimportar la imagen si rompes algo

✅ **Colabora con tus compañeros** - todos tenéis el mismo entorno

❌ **NO subas contraseñas** reales a Git

❌ **NO uses estos conocimientos** fuera del entorno de laboratorio sin autorización

---

## 🆘 Soporte

**¿Problemas técnicos?**
1. Consulta la sección "Problemas Comunes" arriba
2. Pregunta a tus compañeros
3. Consulta al profesor

**¿Dudas sobre la práctica?**
- Lee el `README.md` con el enunciado completo
- Revisa los ejemplos `app_vulnerable.py` y `app_segura.py`

---

**Creado para**: ASIR2 - Ciberseguridad
**Práctica**: 2.2 - Inyección SQL
**Sistema**: Debian 13 (Trixie) en WSL2

---

**Filosofía**: *"Todos con el mismo entorno = Más tiempo aprendiendo, menos tiempo configurando"* 🚀
