#!/usr/bin/env python3
"""
Script de execução para GestIQ com verificação de ambiente pyenv
"""
import sys
import subprocess


def check_pyenv_environment():
    """Verifica se o ambiente pyenv está configurado corretamente"""
    print("🔍 Verificando ambiente pyenv...")
    
    # Verificar se estamos usando pyenv
    try:
        result = subprocess.run(['pyenv', 'version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            current_version = result.stdout.strip()
            print(f"✅ Ambiente pyenv ativo: {current_version}")
            return True
        else:
            print("⚠️  pyenv não está configurado corretamente")
            return False
    except FileNotFoundError:
        print("❌ pyenv não encontrado!")
        print("💡 Configure o ambiente virtual manualmente:")
        print("   py -3.11 -m venv venv")
        print("   .\\venv\\Scripts\\Activate.ps1")
        print("   pip install -r requirements.txt")
        return False

def main():
    """Função principal"""
    print("🚀 GestIQ - Controle por Gestos")
    print("=" * 40)
    
    # Verificar ambiente
    if not check_pyenv_environment():
        print("\n💡 Para configurar o ambiente:")
        print("   py -3.11 -m venv venv")
        print("   .\\venv\\Scripts\\Activate.ps1")
        print("   pip install -r requirements.txt")
        return False
    
    # Executar o programa principal
    try:
        print("\n🎮 Iniciando programa...")
        subprocess.run([sys.executable, "gesture_control.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar programa: {e}")
        return False
    except KeyboardInterrupt:
        print("\n👋 Programa interrompido pelo usuário")
        return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 