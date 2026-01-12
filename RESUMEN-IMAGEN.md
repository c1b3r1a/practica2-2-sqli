# Resumen: Imagen WSL PRACTICA2.2-inyeccion-SQLi

**Fecha de creación**: $(date '+%Y-%m-%d %H:%M:%S')
**Archivo generado**: PRACTICA2.2-inyeccion-SQLi.tar.gz
**Tamaño**: 386 MB
**Ubicación**: /tmp/sqli-wsl+rootfs-workflow/

---

## Especificaciones Técnicas

**Sistema Base:**
- Debian 13 (Trixie) - Testing
- Kernel: Compatible con WSL2

**Software Instalado:**

### Lenguajes y Entornos
- Python 3.13.5
- SQLite 3.46.1

### Herramientas de Desarrollo
- Git 2.47.3
- Emacs 30.1 (emacs-nox)
- Nano (editor alternativo)
- Build-essential (compiladores)

### Bibliotecas Python
- pip (gestor de paquetes)
- python3-venv (entornos virtuales)
- Faker 40.1.0 (generación de datos)

### Herramientas de Red
- curl
- wget
- net-tools
- iputils-ping
- dnsutils

### Herramientas de Seguridad
- sqlmap 1.9.6 (testing de SQL injection)

### Utilidades del Sistema
- htop (monitor de procesos)
- bash-completion

---

## Configuración de Usuario

**Usuario por defecto**: alumno
**Password**: alumno123
**Permisos sudo**: Sin contraseña (NOPASSWD)
**Directorio de trabajo**: /home/alumno/practica-sqli

---

## Configuración WSL

**Archivo**: /etc/wsl.conf
```ini
[user]
default=alumno

[boot]
systemd=false
```

**Mensaje de bienvenida** (/etc/motd):
```
╔═══════════════════════════════════════════════════════════╗
║  Entorno WSL - PRACTICA 2.2: Inyección SQL               ║
║  Python 3.13 + SQLite3 + Faker + Git + Emacs             ║
║                                                           ║
║  Directorio de trabajo: ~/practica-sqli                  ║
║  Usuario: alumno / Password: alumno123                   ║
╚═══════════════════════════════════════════════════════════╝
```

---

## Instrucciones de Uso

### Para el Profesor (Distribución)

1. **Subir a plataforma**: Google Drive, Nextcloud, USB
2. **Compartir enlace** con los alumnos
3. **Proporcionar instrucciones** del documento Ed2

### Para los Alumnos (Importación)

```powershell
# En PowerShell (Windows)
mkdir C:\WSL\SQLi-Practica
wsl --import SQLi-Practica C:\WSL\SQLi-Practica PRACTICA2.2-inyeccion-SQLi.tar.gz
wsl -d SQLi-Practica
```

---

## Verificación de Instalación

Una vez importado, verificar que todo funciona:

```bash
# Verificar Python
python3 --version
# Esperado: Python 3.13.5

# Verificar SQLite
sqlite3 --version
# Esperado: 3.46.1

# Verificar Faker
python3 -c "from faker import Faker; print('OK')"
# Esperado: OK

# Verificar Git
git --version
# Esperado: git version 2.47.3

# Verificar Emacs
emacs --version | head -1
# Esperado: GNU Emacs 30.1

# Verificar sqlmap
sqlmap --version
# Esperado: 1.9.6
```

---

## Notas Técnicas

**Configuración de Red del Container LXC:**
- Bridge: lxcbr0 (10.0.3.0/24)
- IP container: 10.0.3.100/24
- Gateway: 10.0.3.1
- DNS: 8.8.8.8, 8.8.4.4
- NAT: Configurado con iptables MASQUERADE

**Optimizaciones aplicadas:**
- Cache de apt limpiado
- Archivos temporales eliminados
- Tamaño optimizado para distribución

---

## Compatibilidad

**Compatible con:**
- Windows 10 versión 2004+ (Build 19041+)
- Windows 11
- WSL2 instalado y habilitado

**No compatible con:**
- WSL1 (requiere WSL2)
- Windows 7, 8, 8.1

---

## Mantenimiento

**Para actualizar la imagen:**
1. Importar la imagen en WSL
2. Realizar cambios necesarios
3. Exportar: `wsl --export SQLi-Practica nueva-version.tar`
4. Comprimir con gzip si es necesario

**Para crear variantes:**
- Modificar el script de creación en sqli-wsl+rootfs-workflow_Ed2.md
- Recrear el container con nuevas especificaciones

---

## Soporte

**Problemas comunes**: Ver sección Troubleshooting en sqli-wsl+rootfs-workflow_Ed2.md

**Contacto**: Profesor de CIBERSEGURIDAD - ASIR2

---

**Filosofía**: *"Simplificar la configuración maximiza el tiempo de aprendizaje"*
