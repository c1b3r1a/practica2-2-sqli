# Imagen WSL para Práctica 2.2 - Inyección SQLi

**Propósito**: Facilitar a los alumnos un entorno Debian 13 (Trixie) preconfigurado con Python 3.13, SQLite y herramientas necesarias para la práctica de inyección SQL.

**Filosofía**: Profesor crea → Alumnos importan → Todos trabajan igual

---

## Tabla de Contenidos

1. [Introducción](#introducción)
2. [PARTE 1: Profesor (Linux)](#parte-1-profesor-linux)
   - [Crear Container](#crear-container)
   - [Instalar Software](#instalar-software)
   - [Personalizar Entorno](#personalizar-entorno)
   - [Exportar Imagen](#exportar-imagen)
3. [PARTE 2: Alumnos (Windows)](#parte-2-alumnos-windows)
   - [Requisitos Previos](#requisitos-previos)
   - [Descargar Imagen](#descargar-imagen)
   - [Importar en WSL](#importar-en-wsl)
   - [Verificar Instalación](#verificar-instalación)
   - [Primeros Pasos](#primeros-pasos)
4. [Verificación del Entorno](#verificación-del-entorno)
5. [Troubleshooting](#troubleshooting)

---

## Introducción

Esta guía facilita la creación y distribución de una imagen Debian para WSL con todo el software necesario para realizar la **PRACTICA2.2-inyeccion-SQLi**.

**Ventajas**:
- Entorno idéntico para todos los alumnos
- Sin instalaciones complejas en Windows
- Listos para trabajar en 5 minutos

---

## PARTE 1: Profesor (Linux)

### Crear Container

```bash
# Instalar LXC (si no lo tienes)
sudo apt update
sudo apt install lxc lxc-templates debootstrap

# Crear container Debian 13 (Trixie) para SQLi
sudo lxc-create -n sqli-practica -t debian -- -r trixie

# Iniciar container
sudo lxc-start -n sqli-practica

# Verificar estado
sudo lxc-info -n sqli-practica

# Entrar al container
sudo lxc-attach -n sqli-practica
```

### Instalar Software

Dentro del container:

```bash
# Actualizar sistema
apt update && apt upgrade -y

# Python 3 y herramientas básicas
apt install -y python3 python3-pip python3-venv sqlite3

# Git y herramientas de desarrollo
apt install -y git curl wget emacs-nox nano htop

# Herramientas de red y testing
apt install -y net-tools iputils-ping dnsutils

# Instalar Faker globalmente
pip3 install --break-system-packages faker

# Opcional: sqlmap para testing avanzado
apt install -y sqlmap

# Limpiar cache
apt clean
rm -rf /var/cache/apt/archives/*
rm -rf /tmp/*
```

### Personalizar Entorno

Dentro del container:

```bash
# Crear usuario alumno
useradd -m -s /bin/bash alumno
echo "alumno:alumno123" | chpasswd

# Dar permisos sudo sin password
echo "alumno ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Crear directorio de trabajo
mkdir -p /home/alumno/practica-sqli
chown -R alumno:alumno /home/alumno/practica-sqli

# Configurar wsl.conf para usuario por defecto
cat > /etc/wsl.conf << 'EOF'
[user]
default=alumno

[boot]
systemd=false
EOF

# Mensaje de bienvenida
cat > /etc/motd << 'EOF'
╔═══════════════════════════════════════════════════════════╗
║  Entorno WSL - PRACTICA 2.2: Inyección SQL               ║
║  Python 3 + SQLite3 + Faker + Git                        ║
║                                                           ║
║  Directorio de trabajo: ~/practica-sqli                  ║
║  Usuario: alumno / Password: alumno123                   ║
╚═══════════════════════════════════════════════════════════╝
EOF

# Salir del container
exit
```

### Exportar Imagen

```bash
# Detener container
sudo lxc-stop -n sqli-practica

# Exportar a .tar.gz (más compatible con WSL)
sudo tar -czf PRACTICA2.2-inyeccion-SQLi.tar.gz -C /var/lib/lxc/sqli-practica/rootfs .

# Cambiar permisos
sudo chown $USER:$USER PRACTICA2.2-inyeccion-SQLi.tar.gz

# Verificar tamaño
ls -lh PRACTICA2.2-inyeccion-SQLi.tar.gz

# Opcional: Limpiar container
sudo lxc-destroy -n sqli-practica
```

**Resultado**: Archivo `PRACTICA2.2-inyeccion-SQLi.tar.gz` (aprox. 200-400 MB comprimido)

**Distribución**: Subir a Google Drive, Nextcloud, USB, o repositorio Git LFS.

---

## PARTE 2: Alumnos (Windows)

### Requisitos Previos

**Verificar que WSL está instalado**:

```powershell
# En PowerShell como Administrador
wsl --version
```

**Si no está instalado**:

```powershell
# Instalar WSL
wsl --install

# Reiniciar el equipo después de la instalación
```

### Descargar Imagen

Descargar el archivo `PRACTICA2.2-inyeccion-SQLi.tar.gz` desde la ubicación indicada por el profesor (Drive, USB, etc.)

**Ejemplo**: Guardar en `C:\Users\TuUsuario\Downloads\`

### Importar en WSL

Abrir PowerShell (no necesita ser administrador):

```powershell
# Crear directorio para WSL
mkdir C:\WSL\SQLi-Practica

# Importar imagen
wsl --import SQLi-Practica C:\WSL\SQLi-Practica C:\Users\TuUsuario\Downloads\PRACTICA2.2-inyeccion-SQLi.tar.gz

# Verificar que se importó correctamente
wsl --list -v
```

**Salida esperada**:
```
  NAME            STATE           VERSION
* SQLi-Practica   Stopped         2
```

### Verificar Instalación

```powershell
# Entrar a la distribución
wsl -d SQLi-Practica
```

Ahora estás dentro de Debian. Verás el mensaje de bienvenida.

### Primeros Pasos

```bash
# Verificar usuario (debe ser 'alumno')
whoami

# Verificar Python
python3 --version

# Verificar Faker
python3 -c "import faker; print(faker.__version__)"

# Verificar SQLite
sqlite3 --version

# Ir al directorio de trabajo
cd ~/practica-sqli

# Clonar el repositorio de la práctica (ejemplo)
git clone https://github.com/tu-profesor/PRACTICA2.2-inyeccion-SQLi.git
cd PRACTICA2.2-inyeccion-SQLi

# Probar aplicación vulnerable
python3 app_vulnerable.py
```

---

## Verificación del Entorno

**Checklist para alumnos**:

```bash
# 1. Python 3
python3 --version
# Esperado: Python 3.11.x o superior

# 2. SQLite3
sqlite3 --version
# Esperado: 3.x.x

# 3. Faker
python3 -c "import faker; print('Faker OK')"
# Esperado: Faker OK

# 4. Git
git --version
# Esperado: git version 2.x.x

# 5. Permisos sudo
sudo echo "Sudo OK"
# Esperado: Sudo OK (sin pedir password)
```

**Si todos los comandos funcionan, el entorno está listo** ✅

---

## Troubleshooting

**Error: "WSL no está instalado"**

```powershell
# Instalar WSL en PowerShell como Administrador
wsl --install
# Reiniciar el equipo
```

**Error: "No se puede importar el archivo .tar.gz"**

- Verificar que el archivo no está corrupto
- Descargar nuevamente
- Verificar la ruta del archivo (sin espacios raros)

**Error: "No puedo entrar a la distribución"**

```powershell
# Ver distribuciones disponibles
wsl --list -v

# Entrar especificando el nombre exacto
wsl -d SQLi-Practica
```

**Dentro de WSL: "Faker no está instalado"**

```bash
# Instalar Faker como usuario
pip3 install --user faker

# O con venv (recomendado)
python3 -m venv venv
source venv/bin/activate
pip install faker
```

**Dentro de WSL: "No tengo permisos sudo"**

```bash
# Salir de WSL
exit

# En PowerShell, entrar como root
wsl -d SQLi-Practica -u root

# Añadir usuario alumno a sudoers
echo "alumno ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers
exit

# Volver a entrar como alumno
wsl -d SQLi-Practica
```

**"La distribución consume mucho espacio"**

```bash
# Limpiar cache de APT
sudo apt clean
sudo apt autoclean

# Limpiar pip cache
pip3 cache purge
```

**"Quiero eliminar la distribución y empezar de nuevo"**

```powershell
# En PowerShell
wsl --unregister SQLi-Practica

# Volver a importar desde el .tar.gz
wsl --import SQLi-Practica C:\WSL\SQLi-Practica PRACTICA2.2-inyeccion-SQLi.tar.gz
```

---

## Notas Finales

**Para el profesor**:
- El archivo .tar.gz se puede reutilizar cada año
- Considera subir el archivo a un servidor institucional permanente
- Puedes crear variantes (con/sin sqlmap, con/sin herramientas avanzadas)

**Para los alumnos**:
- El entorno es portátil: puedes usarlo en cualquier PC con Windows + WSL
- Todos los cambios se guardan en `C:\WSL\SQLi-Practica\ext4.vhdx`
- Para hacer backup: copiar ese archivo .vhdx
- Para exportar tu trabajo: `wsl --export SQLi-Practica mi-trabajo.tar`

---

**Filosofía**: *"Simplificar la configuración maximiza el tiempo de aprendizaje"*
