# 🐧 Usar Imagen SQLi en Debian/Linux

**Guía para usar el entorno preconfigurado en sistemas Debian/Linux** (alternativa a WSL en Windows).

---

## 📦 ¿Qué es esto?

La imagen `PRACTICA2.2-inyeccion-SQLi.tar.gz` es un **rootfs de Debian 13 (Trixie)** que se puede usar de múltiples formas en Linux:

1. **Importar en LXC** (recomendado - containers ligeros)
2. **Usar como chroot** (ejecución aislada)
3. **Extraer y explorar** (inspección de contenido)

**Ventajas:**
- ✅ Mismo entorno que los alumnos en Windows/WSL
- ✅ Testing rápido de la práctica
- ✅ Crear variantes de la imagen
- ✅ Portabilidad entre sistemas Linux

---

## 🎯 Método 1: Importar en LXC (Recomendado)

### Requisitos

```bash
# Instalar LXC si no lo tienes
sudo apt update
sudo apt install lxc lxc-templates
```

### Importar la Imagen

```bash
# Crear directorio para el container
sudo mkdir -p /var/lib/lxc/sqli-alumno

# Extraer rootfs
sudo tar -xzf PRACTICA2.2-inyeccion-SQLi.tar.gz -C /var/lib/lxc/sqli-alumno/

# Renombrar directorio
sudo mv /var/lib/lxc/sqli-alumno /var/lib/lxc/sqli-alumno-rootfs
sudo mkdir /var/lib/lxc/sqli-alumno
sudo mv /var/lib/lxc/sqli-alumno-rootfs /var/lib/lxc/sqli-alumno/rootfs

# Crear archivo de configuración
sudo bash -c 'cat > /var/lib/lxc/sqli-alumno/config << EOF
lxc.include = /usr/share/lxc/config/debian.common.conf
lxc.arch = linux64
lxc.rootfs.path = dir:/var/lib/lxc/sqli-alumno/rootfs
lxc.uts.name = sqli-alumno
lxc.net.0.type = veth
lxc.net.0.link = lxcbr0
lxc.net.0.flags = up
lxc.net.0.hwaddr = 00:16:3e:xx:xx:xx
EOF'
```

**Nota**: Sustituye las `xx` por valores aleatorios (ejemplo: `00:16:3e:a1:b2:c3`).

### Iniciar el Container

```bash
# Iniciar
sudo lxc-start -n sqli-alumno

# Verificar estado
sudo lxc-info -n sqli-alumno

# Entrar al container
sudo lxc-attach -n sqli-alumno
```

**Dentro del container:**
```bash
# Ya estás dentro como root
su - alumno  # Cambiar a usuario alumno

# Verificar instalación
python3 --version
sqlite3 --version
```

### Detener el Container

```bash
# Salir del container
exit

# Detener
sudo lxc-stop -n sqli-alumno

# Eliminar (si ya no lo necesitas)
sudo lxc-destroy -n sqli-alumno
```

---

## 🎯 Método 2: Usar como Chroot

Útil para ejecutar comandos aislados sin crear un container completo.

### Extraer Rootfs

```bash
# Crear directorio
mkdir ~/sqli-chroot
cd ~/sqli-chroot

# Extraer
tar -xzf ~/Downloads/PRACTICA2.2-inyeccion-SQLi.tar.gz

# Verificar contenido
ls -la
```

### Entrar al Chroot

```bash
# Montar sistemas de archivos necesarios
sudo mount --bind /proc ~/sqli-chroot/proc
sudo mount --bind /sys ~/sqli-chroot/sys
sudo mount --bind /dev ~/sqli-chroot/dev

# Entrar al chroot
sudo chroot ~/sqli-chroot /bin/bash

# Ya estás dentro
whoami  # root
su - alumno  # Cambiar a alumno
```

### Verificar Instalación

```bash
python3 --version
sqlite3 --version
cd ~/practica-sqli
```

### Salir del Chroot

```bash
# Salir
exit
exit

# Desmontar sistemas de archivos
sudo umount ~/sqli-chroot/proc
sudo umount ~/sqli-chroot/sys
sudo umount ~/sqli-chroot/dev
```

---

## 🎯 Método 3: Systemd-nspawn (Containers Systemd)

Alternativa moderna a chroot con mejor aislamiento.

### Requisitos

```bash
sudo apt install systemd-container
```

### Preparar el Container

```bash
# Crear directorio
sudo mkdir -p /var/lib/machines/sqli-alumno
cd /var/lib/machines/sqli-alumno

# Extraer
sudo tar -xzf ~/Downloads/PRACTICA2.2-inyeccion-SQLi.tar.gz
```

### Iniciar el Container

```bash
# Iniciar sesión interactiva
sudo systemd-nspawn -D /var/lib/machines/sqli-alumno

# Cambiar a usuario alumno
su - alumno

# Verificar
python3 --version
```

### Iniciar como Servicio

```bash
# Arrancar como servicio persistente
sudo systemd-nspawn -D /var/lib/machines/sqli-alumno -b

# Entrar al container en ejecución
sudo machinectl shell sqli-alumno

# Ver containers en ejecución
machinectl list

# Detener
sudo machinectl stop sqli-alumno
```

---

## 🔍 Método 4: Solo Inspección (sin ejecutar)

Para explorar el contenido sin ejecutar nada.

### Extraer y Explorar

```bash
# Extraer en directorio temporal
mkdir /tmp/sqli-inspect
cd /tmp/sqli-inspect
tar -xzf ~/Downloads/PRACTICA2.2-inyeccion-SQLi.tar.gz

# Ver estructura
tree -L 2 -h

# Ver software instalado
cat etc/motd

# Ver usuarios
cat etc/passwd | grep alumno

# Ver paquetes Python instalados
ls usr/local/lib/python3.13/

# Limpiar
cd ~
rm -rf /tmp/sqli-inspect
```

---

## 📊 Comparación de Métodos

| Método | Aislamiento | Complejidad | Uso Recomendado |
|:-------|:------------|:------------|:----------------|
| **LXC** | ⭐⭐⭐⭐⭐ | Media | Testing completo, desarrollo |
| **Chroot** | ⭐⭐ | Baja | Pruebas rápidas |
| **Systemd-nspawn** | ⭐⭐⭐⭐ | Media | Containers modernos |
| **Inspección** | N/A | Muy baja | Ver contenido |

---

## 🛠️ Configuración de Red en Containers

### Verificar Conectividad

```bash
# Dentro del container
ping -c 3 8.8.8.8

# Si no funciona, configurar DNS
echo "nameserver 8.8.8.8" | sudo tee /etc/resolv.conf
```

### Configurar NAT (si es necesario)

En el **host** (fuera del container):

```bash
# Habilitar IP forwarding
sudo sysctl -w net.ipv4.ip_forward=1

# Configurar NAT para lxcbr0
sudo iptables -t nat -A POSTROUTING -s 10.0.3.0/24 -j MASQUERADE
sudo iptables -I FORWARD -i lxcbr0 -j ACCEPT
sudo iptables -I FORWARD -o lxcbr0 -j ACCEPT
```

---

## 🧪 Testing de la Práctica desde Linux

### Clonar Repositorio (dentro del container)

```bash
su - alumno
cd ~/practica-sqli

git clone https://github.com/PROFESOR/PRACTICA2.2-inyeccion-SQLi.git
cd PRACTICA2.2-inyeccion-SQLi
```

### Ejecutar Ejemplos

```bash
# Probar app vulnerable
python3 app_vulnerable.py

# Probar app segura
python3 app_segura.py

# Generar datos con Faker
python3 generar_datos.py
```

### Testing con sqlmap

```bash
# Dentro del container
sqlmap --version

# Ejemplo básico (solo en entorno de laboratorio)
sqlmap -u "http://localhost:5000/login" --data "username=admin&password=123"
```

---

## 📦 Crear Variantes de la Imagen

### Modificar y Re-exportar

```bash
# 1. Entrar al container
sudo lxc-attach -n sqli-alumno

# 2. Hacer cambios
apt update
apt install -y nuevo-paquete
pip3 install nueva-libreria

# 3. Limpiar
apt clean
rm -rf /tmp/* /var/tmp/*
exit

# 4. Detener container
sudo lxc-stop -n sqli-alumno

# 5. Exportar nueva versión
sudo tar -czf PRACTICA2.2-inyeccion-SQLi-v2.tar.gz \
    -C /var/lib/lxc/sqli-alumno/rootfs .

# 6. Ajustar permisos
sudo chown $USER:$USER PRACTICA2.2-inyeccion-SQLi-v2.tar.gz
```

---

## 🐳 Bonus: Convertir a Docker

Si prefieres usar Docker en lugar de LXC:

```bash
# Importar como imagen Docker
docker import PRACTICA2.2-inyeccion-SQLi.tar.gz sqli-practica:latest

# Ejecutar
docker run -it --name sqli-test sqli-practica:latest /bin/bash

# Cambiar a usuario alumno
su - alumno

# Verificar
python3 --version
```

---

## ❓ Troubleshooting

### "Container no tiene red"

```bash
# Verificar bridge lxcbr0
ip addr show lxcbr0

# Si no existe, inicializar LXC
sudo systemctl restart lxc-net
sudo lxc-start -n sqli-alumno
```

### "No puedo ejecutar comandos como alumno"

```bash
# Dentro del container como root
su - alumno

# Si falla, verificar usuario existe
cat /etc/passwd | grep alumno

# Verificar home directory
ls -la /home/alumno
```

### "Python no encuentra Faker"

```bash
# Verificar instalación
python3 -c "from faker import Faker; print('OK')"

# Si falla, reinstalar
pip3 install --break-system-packages faker
```

---

## 🗑️ Limpiar Todo

### Eliminar Container LXC

```bash
sudo lxc-stop -n sqli-alumno
sudo lxc-destroy -n sqli-alumno
```

### Eliminar Chroot

```bash
# Desmontar todo
sudo umount ~/sqli-chroot/proc 2>/dev/null
sudo umount ~/sqli-chroot/sys 2>/dev/null
sudo umount ~/sqli-chroot/dev 2>/dev/null

# Eliminar directorio
rm -rf ~/sqli-chroot
```

### Eliminar Systemd-nspawn

```bash
sudo machinectl stop sqli-alumno
sudo rm -rf /var/lib/machines/sqli-alumno
```

---

## 📚 Documentación Relacionada

**Archivos en este directorio:**
- `README-wsl-SQLi-img.md` - Instrucciones para Windows/WSL
- `sqli-wsl+rootfs-workflow_Ed2.md` - Cómo se creó esta imagen
- `RESUMEN-IMAGEN.md` - Especificaciones técnicas

**Enlaces útiles:**
- [LXC Documentation](https://linuxcontainers.org/lxc/)
- [systemd-nspawn Manual](https://www.freedesktop.org/software/systemd/man/systemd-nspawn.html)
- [Chroot Guide](https://wiki.debian.org/chroot)

---

## 💡 Casos de Uso

**Para Profesores:**
- ✅ Testing de la práctica antes de distribuir
- ✅ Crear variantes para diferentes grupos
- ✅ Debugging de problemas de alumnos
- ✅ Evaluación automatizada de entregas

**Para Estudiantes Linux:**
- ✅ Hacer la práctica sin Windows
- ✅ Experimentar sin romper el sistema
- ✅ Aprender sobre containers

**Para DevOps/SysAdmins:**
- ✅ Entornos reproducibles
- ✅ CI/CD con containers
- ✅ Laboratorios desechables

---

**Sistema Base**: Debian 13 (Trixie)
**Creado para**: ASIR2 - Ciberseguridad
**Práctica**: 2.2 - Inyección SQL

---

**Filosofía**: *"Un tarball, múltiples formas de usarlo"* 🐧
