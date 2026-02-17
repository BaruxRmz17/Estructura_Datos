#!/usr/bin/env python3
"""
Script de instalación y configuración para Navegador de Rutas
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Imprime un encabezado"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def create_directories():
    """Crea las carpetas necesarias"""
    Path("templates").mkdir(exist_ok=True)
    print("✓ Carpetas creadas")

def install_dependencies():
    """Instala las dependencias"""
    print_header("Instalando dependencias...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("✗ Error al instalar dependencias")
        return False

def verify_files():
    """Verifica que existan los archivos necesarios"""
    required_files = {
        "app.py": "Backend Flask",
        "templates/index.html": "Frontend HTML",
        "requirements.txt": "Dependencias",
        "README.md": "Documentación"
    }
    
    print_header("Verificando archivos...")
    
    all_exist = True
    for file, description in required_files.items():
        if os.path.exists(file):
            print(f"✓ {file:<30} ({description})")
        else:
            print(f"✗ {file:<30} FALTA")
            all_exist = False
    
    return all_exist

def main():
    """Función principal"""
    print_header("Configuración de Navegador de Rutas")
    
    # Verificar archivos
    if not verify_files():
        print("\n✗ Faltan archivos. Asegúrate de descargar todos los archivos del proyecto.")
        return False
    
    # Crear directorios
    create_directories()
    
    # Instalar dependencias
    if not install_dependencies():
        return False
    
    print_header("✓ Instalación completada")
    
    print("\nPróximos pasos:")
    print("  1. Ejecuta: python app.py")
    print("  2. Abre: http://localhost:5000")
    print("  3. Disfruta! 🗺️\n")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)