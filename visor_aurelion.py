import os
import re

def cargar_secciones_markdown(archivo_md):
    """
    Carga y parsea el archivo Markdown específico de Aurelion
    """
    try:
        with open(archivo_md, 'r', encoding='utf-8') as file:
            contenido = file.read()
        
        # Definir las secciones principales manualmente para mejor organización
        secciones = {
            "🏗️ ESTRUCTURA DE LA BASE DE DATOS": "",
            "📊 DETALLE ESTRUCTURAL POR TABLA": "",
            "📈 ESCALA Y VOLUMEN DE DATOS": "",
            "🔢 TIPOS DE DATOS Y DOMINIOS": "",
            "🎯 CARACTERÍSTICAS TÉCNICAS": "",
            "📊 POTENCIAL ANALÍTICO": "",
            "📋 PREGUNTAS CLAVE": ""
        }
        
        # Dividir el contenido por las secciones principales
        contenido_completo = contenido
        
        # Extraer introducción (antes de la primera sección)
        intro_match = re.search(r'<div style="text-align: justify;">(.*?)(?=## 🏗️|</div>)', contenido, re.DOTALL)
        if intro_match:
            secciones["📖 INTRODUCCIÓN"] = intro_match.group(1).strip()
        
        # Extraer cada sección
        secciones_keys = list(secciones.keys())
        for i in range(len(secciones_keys)):
            current_section = secciones_keys[i]
            next_section = secciones_keys[i + 1] if i + 1 < len(secciones_keys) else None
            
            # Crear patrón de búsqueda
            if next_section:
                pattern = f"## {re.escape(current_section)}(.*?)(?=## {re.escape(next_section)})"
            else:
                pattern = f"## {re.escape(current_section)}(.*?)(?=</div>|$)"
            
            match = re.search(pattern, contenido, re.DOTALL)
            if match:
                secciones[current_section] = match.group(1).strip()
        
        # Filtrar secciones vacías
        secciones = {k: v for k, v in secciones.items() if v.strip()}
        
        return secciones
    
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo '{archivo_md}'")
        print("💡 Asegúrate de que el archivo 'DOCUMENTACION.md' esté en la misma carpeta")
        return {}
    except Exception as e:
        print(f"❌ Error al leer el archivo: {e}")
        return {}

def mostrar_menu_aurelion(secciones):
    """
    Muestra el menú específico para la documentación de Aurelion
    """
    print("\n" + "="*70)
    print("           🏪 VISOR DE DOCUMENTACIÓN - TIENDA AURELION")
    print("="*70)
    
    opciones = list(secciones.keys())
    
    if not opciones:
        print("⚠️  No se encontraron secciones en el documento.")
        return
    
    print("📑 Secciones disponibles:")
    print("-" * 50)
    
    for i, opcion in enumerate(opciones, 1):
        print(f"  {i:2d}. {opcion}")
    
    print("-" * 50)
    print(f"  {len(opciones) + 1:2d}. 🚪 Salir del programa")
    print("="*70)

def mostrar_seccion_aurelion(secciones, numero):
    """
    Muestra una sección específica con formato optimizado para Aurelion
    """
    opciones = list(secciones.keys())
    
    if 1 <= numero <= len(opciones):
        seccion = opciones[numero - 1]
        contenido = secciones[seccion]
        
        # Limpiar y formatear el contenido
        contenido = re.sub(r'<[^>]+>', '', contenido)  # Remover HTML
        contenido = re.sub(r'!\[.*?\]\(.*?\)', '', contenido)  # Remover imágenes
        
        print(f"\n{'╔' + '═' * 68 + '╗'}")
        print(f"║ {'🏪 TIENDA AURELION - ' + seccion.upper():^66} ║")
        print(f"{'╠' + '═' * 68 + '╣'}")
        
        # Dividir en líneas y mostrar con formato
        lineas = contenido.split('\n')
        lineas_contenido = []
        
        for linea in lineas:
            linea = linea.strip()
            if linea and not linea.startswith('#'):
                # Procesar tablas y listas
                if linea.startswith('|') and '---' not in linea:
                    print(f"║ {linea:<66} ║")
                else:
                    # Wrap de texto para líneas largas
                    while len(linea) > 66:
                        parte = linea[:66]
                        linea = linea[66:]
                        print(f"║ {parte:<66} ║")
                    if linea:
                        print(f"║ {linea:<66} ║")
            elif linea.startswith('###'):
                # Subsecciones
                subseccion = re.sub(r'^#+\s*', '', linea)
                print(f"{'╠' + '─' * 68 + '╣'}")
                print(f"║ 📌 {subseccion:<62} ║")
                print(f"{'╠' + '─' * 68 + '╣'}")
        
        print(f"{'╚' + '═' * 68 + '╝'}")
        
        # Mostrar estadísticas de la sección
        lineas_utiles = [l for l in lineas if l.strip() and not l.startswith('#') and '---' not in l]
        print(f"📊 Contenido: {len(lineas_utiles)} líneas informativas")
        
    else:
        print("❌ Opción no válida")

def mostrar_resumen_aurelion(secciones):
    """
    Muestra un resumen general de la base de datos
    """
    print(f"\n{'⭐' * 35}")
    print(f"⭐           RESUMEN EJECUTIVO - BASE DE DATOS AURELION           ⭐")
    print(f"{'⭐' * 35}")
    print(f"📊 Total de secciones disponibles: {len(secciones)}")
    print(f"🏪 Clientes registrados: 95")
    print(f"📦 Productos en catálogo: 100")
    print(f"💰 Transacciones de venta: 120")
    print(f"📋 Líneas de detalle: 343")
    print(f"🌍 Cobertura: 6 ciudades de Córdoba, Argentina")
    print(f"{'⭐' * 35}")

def main():
    """
    Función principal del programa específico para Aurelion
    """
    print("\n🔍 Iniciando Visor de Documentación - Tienda Aurelion...")
    
    # Intentar diferentes nombres de archivo
    archivos_posibles = ['DOCUMENTACION.md', 'documentacion.md', 'DOCUMENTACION.MD']
    archivo_md = None
    
    for archivo in archivos_posibles:
        if os.path.exists(archivo):
            archivo_md = archivo
            break
    
    if not archivo_md:
        print("❌ No se encontró el archivo de documentación.")
        print("💡 Archivos buscados:", ", ".join(archivos_posibles))
        return
    
    print(f"📖 Cargando: {archivo_md}")
    secciones = cargar_secciones_markdown(archivo_md)
    
    if not secciones:
        print("\n⚠️  No se pudieron cargar las secciones.")
        return
    
    print(f"✅ Se cargaron {len(secciones)} secciones de la base de datos")
    mostrar_resumen_aurelion(secciones)
    
    while True:
        mostrar_menu_aurelion(secciones)
        
        try:
            opcion = input("\n🎯 Selecciona una sección (número): ").strip()
            
            if opcion.lower() in ['salir', 'exit', 'q', 'quit']:
                print("\n👋 ¡Hasta luego! Gracias por usar el visor de Tienda Aurelion")
                break
                
            numero_opcion = int(opcion)
            total_opciones = len(secciones)
            
            if numero_opcion == total_opciones + 1:
                print("\n👋 ¡Hasta luego! Gracias por usar el visor de Tienda Aurelion")
                break
            elif 1 <= numero_opcion <= total_opciones:
                print(f"\n📖 Cargando sección {numero_opcion}...")
                mostrar_seccion_aurelion(secciones, numero_opcion)
                
                # Pausa antes de mostrar el menú nuevamente
                input("\n⏎ Presiona Enter para continuar...")
            else:
                print("❌ Opción no válida. Intenta nuevamente.")
                
        except ValueError:
            print("❌ Por favor, ingresa un número válido.")
        except KeyboardInterrupt:
            print("\n\n👋 Programa interrumpido por el usuario.")
            break
# Fin del código
if __name__ == "__main__":
    main()