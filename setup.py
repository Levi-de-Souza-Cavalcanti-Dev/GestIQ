#!/usr/bin/env python3
"""
Script de setup para o GestIQ - Controle por Gestos
Configurado para usar pyenv
"""

import subprocess
import sys
import os

def check_pyenv():
    """Verifica se pyenv está instalado e configurado"""
    print("🐍 Verificando pyenv...")
    try:
        result = subprocess.run(['pyenv', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pyenv detectado: {result.stdout.strip()}")
            return True
        else:
            print("❌ pyenv não encontrado!")
            return False
    except FileNotFoundError:
        print("❌ pyenv não está instalado!")
        print("💡 Instale pyenv primeiro: https://github.com/pyenv/pyenv")
        return False

def check_python_version():
    """Verifica se a versão do Python é compatível"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ é necessário!")
        print(f"Versão atual: {sys.version}")
        return False
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    return True

def setup_pyenv_environment():
    """Configura o ambiente pyenv"""
    print("🔧 Configurando ambiente pyenv...")
    
    # Verificar se .python-version existe
    if not os.path.exists('.python-version'):
        print("❌ Arquivo .python-version não encontrado!")
        return False
    
    # Ler versão do Python do arquivo
    with open('.python-version', 'r') as f:
        python_version = f.read().strip()
    
    print(f"📋 Versão Python especificada: {python_version}")
    
    # Verificar se a versão está instalada
    try:
        result = subprocess.run(['pyenv', 'versions', '--bare'], 
                              capture_output=True, text=True)
        if python_version in result.stdout:
            print(f"✅ Python {python_version} já está instalado")
        else:
            print(f"📦 Instalando Python {python_version}...")
            subprocess.run(['pyenv', 'install', python_version], check=True)
            print(f"✅ Python {python_version} instalado com sucesso!")
        
        # Configurar versão local
        subprocess.run(['pyenv', 'local', python_version], check=True)
        print(f"✅ Ambiente configurado para Python {python_version}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao configurar pyenv: {e}")
        return False

def install_requirements():
    """Instala as dependências do projeto"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def test_camera():
    """Testa se a câmera está funcionando"""
    print("📹 Testando câmera...")
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✅ Câmera funcionando corretamente!")
                return True
            else:
                print("⚠️  Câmera detectada mas não consegue capturar frames")
                return False
        else:
            print("❌ Câmera não detectada!")
            return False
    except ImportError:
        print("❌ OpenCV não está instalado!")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar câmera: {e}")
        return False

def test_mediapipe():
    """Testa se o MediaPipe está funcionando"""
    print("🤖 Testando MediaPipe...")
    try:
        import mediapipe as mp
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
        print("✅ MediaPipe funcionando corretamente!")
        return True
    except ImportError:
        print("❌ MediaPipe não está instalado!")
        return False
    except Exception as e:
        print(f"❌ Erro ao testar MediaPipe: {e}")
        return False

def main():
    """Função principal do setup"""
    print("🚀 Configurando GestIQ - Controle por Gestos (pyenv)")
    print("=" * 60)
    
    # Verificar pyenv
    if not check_pyenv():
        return False
    
    # Configurar ambiente pyenv
    if not setup_pyenv_environment():
        return False
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Instalar dependências
    if not install_requirements():
        return False
    
    # Testar câmera
    if not test_camera():
        print("\n💡 Dicas para resolver problemas de câmera:")
        print("   - Verifique se a webcam está conectada")
        print("   - Teste com diferentes índices: cv2.VideoCapture(1)")
        print("   - Verifique permissões de câmera no Windows")
        return False
    
    # Testar MediaPipe
    if not test_mediapipe():
        return False
    
    print("\n🎉 Setup concluído com sucesso!")
    print("\n📋 Para executar o programa:")
    print("   python gesture_control.py")
    print("\n📖 Para mais informações, consulte o README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        print("\n❌ Setup falhou! Verifique os erros acima.")
        sys.exit(1)
    else:
        print("\n✅ Setup concluído! Você pode executar o programa agora.") 