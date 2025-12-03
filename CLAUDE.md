# CLAUDE.md

Este archivo proporciona orientación a Claude Code (claude.ai/code) cuando trabaja con código en este repositorio.

## Propósito del Repositorio

Material educativo para enseñar vulnerabilidades de **Inyección SQL (SQLi)** en cursos de ciberseguridad (ASIR, DAW, Ciberseguridad). Este es un **entorno de aprendizaje controlado** para que los estudiantes comprendan vectores de ataque y técnicas defensivas.

## Arquitectura Clave

### Scripts de Demostración Educativa

**Enfoque de Aprendizaje Comparativo:** Implementaciones vulnerable vs. segura lado a lado

1. **`login.py`** - ❌ Versión KISS vulnerable
   - Versión minimalista (40 líneas) para comprensión rápida
   - Input interactivo directo
   - Perfecto para demostraciones en clase de 5 minutos


2. **`login_vulnerable.py`** - ❌ Código deliberadamente inseguro
   - Demuestra inyección SQL mediante concatenación de strings (f-strings)
   - Muestra técnicas de bypass: `OR '1'='1`, `admin'--`
   - Incluye salida de debug mostrando las consultas SQL ejecutadas
   - Usado para demostrar vulnerabilidades OWASP Top 10

3. **`login_seguro.py`** - ✅ Implementación de referencia segura
   - Usa consultas parametrizadas (placeholders: `?`)
   - Previene SQLi separando código SQL de datos
   - Muestra por qué los ataques fallan con escapado adecuado
   - Comentarios educativos explican el mecanismo de protección


### Patrones Comunes de Ataque SQLi en las Demos

- **Bypass con OR:** `admin' OR '1'='1` (condición siempre verdadera)
- **Comentarios SQL:** `admin'--` (ignora verificación de contraseña)
- **UNION-based:** Extrae datos de otras tablas
- **Time-based Blind:** `SLEEP(5)` para ataques de inferencia
- **Stacked Queries:** `'; DROP TABLE usuarios; --` (destructivo)

## Ejecutar las Demostraciones

```bash
# Ejecutar script vulnerable (muestra ataques funcionando)
python3 login_vulnerable.py

# Ejecutar script seguro (muestra ataques bloqueados)
python3 login_seguro.py

# Ejecutar versión KISS interactiva
python3 login.py
```

Todos los scripts usan **bases de datos SQLite en memoria** (`:memory:`) con usuarios de prueba:
- `admin` / `admin123` (administrador)
- `profesor` / `profe456` (docente)
- `alumno` / `estudiante789` (estudiante)

## Contexto de Seguridad

⚠️ **Aviso Legal:** Este repositorio contiene **código intencionalmente vulnerable** solo para uso educativo autorizado. Atacar sistemas reales sin permiso es ilegal (Código Penal Español art. 197).

### Casos de Uso Autorizados
- ✅ Demostraciones en aula en programas de FP acreditados
- ✅ Aprendizaje personal en máquinas locales
- ✅ Competiciones CTF (HackTheBox, PortSwigger Academy, DVWA)
- ✅ Investigación de seguridad en entornos de laboratorio aislados

### Al Trabajar con Este Código
- **NUNCA desplegar código vulnerable en producción**
- **NUNCA usar técnicas contra sistemas no autorizados**
- Tratar scripts vulnerables como **muestras de malware** (analizar, no mejorar)
- Enfocarse en entender patrones defensivos de las implementaciones seguras

## Metodología de Enseñanza

**Enfoque ABP (Aprendizaje Basado en Problemas):**
1. Mostrar la vulnerabilidad con exploits reales
2. Explicar el fallo técnico subyacente
3. Demostrar la alternativa segura
4. Los estudiantes practican en laboratorios controlados

## Dependencias

- Python 3.x (predeterminado del sistema)
- Módulo `sqlite3` (incluido)
- No se requieren paquetes externos

## Documentación Relacionada

- **README.md** - Explicación teórica completa con:
  - Referencias OWASP
  - Estudios de caso de brechas reales (Sony PSN, Equifax)
  - Estrategias de defensa (consultas parametrizadas, ORMs, WAFs)
  - Ejercicios prácticos para estudiantes

## Estilo de Código para Este Repositorio

- **Claridad sobre brevedad** (el código educativo debe ser autoexplicativo)
- Comentarios y sentencias print en español (público objetivo: estudiantes de FP españoles)
- Salida de debug extensa para mostrar ejecución interna
- Marcadores emoji para identificación visual rápida (✅ ❌ ⚠️)

## Notas Importantes para Asistentes IA

1. **NO sugerir "mejoras" al código vulnerable** - está intencionalmente roto para enseñar
2. **NO añadir manejo de errores que enmascare la vulnerabilidad**
3. **SÍ mantener la estructura comparativa** (vulnerable vs. seguro)
4. **SÍ preservar comentarios educativos** explicando el "por qué" no solo el "qué"
5. Al crear nuevos ejemplos, proporcionar SIEMPRE AMBAS versiones
