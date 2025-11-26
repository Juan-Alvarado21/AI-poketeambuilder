# Flujo de Trabajo Git

> Este documento asume que el repositorio remoto ya existe y que las ramas `gabi`, `hako`, `juan`, `backend`, `master` existen en origen.

---

## Para Hako y Gabi — Explicación Rápida

**¿Qué deben hacer y por qué?**

1. Ustedes trabajan **solo en su rama** (`hako` o `gabi`). Nunca hagan push directo a `master`.
2. Antes de empezar a trabajar SIEMPRE actualicen la última versión de `master` y mézclenla en su rama local para evitar conflictos grandes.
3. Cuando terminen una funcionalidad, hagan push a su rama personal y abran un **Pull Request** (rama `su_rama` → `master`) en GitHub. Juan revisará y realizará el merge a `master`.

---

## Comandos y Flujo Paso a Paso (Hako / Gabi)

### 1. Clonar el repositorio (solo se hace una sola vez)

```bash
git clone https://github.com/Juan-Alvarado21/AI-poketeambuilder.git    # Clona el repo remoto
cd AI-poketeambuilder                                                   # Entra en el proyecto desde tu terminal
```

```bash
git checkout gabi    # Cambiar a rama 'gabi' (Gabi)
git checkout hako    # Cambiar a rama 'hako' (Hako)
```

---

### 2. Se hace siempre para trabajar

#### Actualizar tu rama con la principal

```bash
git fetch origin                    # Trae todas las referencias remotas nuevas
git checkout <tu_rama-nombre>       # Asegúrate de estar en tu rama (gabi/hako)
git pull origin master              # Baja la última 'master' y hace merge automático en tu rama si es posible
```

#### Para cada que quieras modificar o trabajar en código y guardar cambios

```bash
git status                                          # Verifica archivos modificados
git add .                                           # Añade todos los cambios preparados
# o
git add ruta/al/archivo                             # Añade archivo específico
git commit -m "Descripción del cambio que realizaste"    # Crea commit local
```

#### Subir cambios a tu rama remota para que los pueda juntar en la principal

```bash
git push origin <tu_rama>    # Empuja commits locales a tu_rama
```

**Nota:** Antes de hacer un cambio verifica que tu código no tenga errores ni sintaxis errónea para prevenir conflictos en git.

**Ejemplo:**

```bash
git push origin gabi
git push origin hako
```

**Nota:** Cada que quieras hacer un cambio o abras tu editor para trabajar debes asegurarte de estar actualizado con la rama principal para que no hayan conflictos, del mismo modo coordinarte con los demás integrantes sobre en qué archivos modificar para que no surjan conflictos que rompan el flujo (únicamente encargarse de archivos que le corresponden a c/u y si no acordarlo).

---

## Instrucciones para Juan

### 1. Antes de revisar o integrar, mantener entorno actualizado

```bash
git fetch origin           # Trae todas las refs remotas (seguro)
git checkout master        # Cambia a master
git pull origin master     # Asegura que master local esté actualizado
```

### 2. Revisar ramas de los colaboradores localmente

```bash
git fetch origin                              # Trae ramas remotas nuevas
git checkout -b review/gabi origin/gabi       # Crea rama local para revisar el trabajo de Gabi o hako
                                              # Revisar cambios, probar, ejecutar tests
```

### 3. Integrar ramas del colaborador en entorno de staging local

```bash
git checkout master                 # Cambia a master
git pull origin master              # Actualiza master
git merge --no-ff origin/gabi       # Fusiona cambios de gabi en master, crea commit de merge
                                    # Probar todo localmente; si hay problemas, revertir o pedir cambios
git push origin master              # Sube master ya integrado
```

### 4. Resolver conflictos (si es necesario)

```bash
git status                          # Ver archivos en conflicto
# Editar archivos manualmente para resolver conflictos
git add <archivos-resueltos>        # Marcar conflictos como resueltos
git commit                          # Completar el merge
git push origin master              # Subir cambios integrados
```

---

## Comandos Útiles Adicionales

```bash
# Ver el historial de commits
git log --oneline --graph --all

# Deshacer el último commit (mantiene cambios)
git reset --soft HEAD~1

# Descartar cambios locales no commiteados
git checkout -- <archivo>

# Ver diferencias antes de hacer commit
git diff

# Ver todas las ramas (locales y remotas)
git branch -a
```

---

## Recordatorios Importantes

- Nunca hacer push directo a `master`
- Siempre actualizar desde `master` antes de trabajar
- Comunicarse con el equipo sobre archivos en los que están trabajando
- Probar el código antes de hacer push
- Usar commits descriptivos para mantener un historial claro
