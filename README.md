# GestIQ - Controle por Gestos 🤖

Um sistema inteligente de controle por gestos usando OpenCV e MediaPipe que permite controlar aplicações do computador através de movimentos das mãos.

## 🎯 Funcionalidades

- **Detecção de gestos em tempo real**
- **Controle de aplicações do Windows**
- **Interface visual com landmarks das mãos**
- **Sistema anti-spam de ações**

## 🚀 Gestos Suportados

| Gesto | Ação | Descrição |
|-------|------|-----------|
| 👌 OK | Abre o Notepad | Polegar e indicador formando círculo, outros dedos estendidos |
| 👍 Joinha | Abre a Calculadora | Polegar para cima, outros dedos fechados |

## 📋 Pré-requisitos

- **Python 3.11+** (recomendado para compatibilidade com MediaPipe)
- **Webcam funcional**
- **Windows 10/11** (para compatibilidade com aplicações)
- **Git** (para clonar o repositório)

## 🛠️ Instalação

### Pré-requisitos
- Python 3.11+ (recomendado para compatibilidade com MediaPipe)
- Webcam funcional

### Setup com Ambiente Virtual (Recomendado)

1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/GestIQ.git
cd GestIQ
```

2. **Crie e ative o ambiente virtual:**
```bash
# Windows
py -3.11 -m venv venv
.\venv\Scripts\Activate.ps1

# Linux/Mac
python3.11 -m venv venv
source venv/bin/activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

**✅ Pronto!** O ambiente virtual está configurado e isolado do sistema.

### Setup Manual (Sem Ambiente Virtual)
```bash
pip install -r requirements.txt
```

**⚠️ Nota:** O MediaPipe pode não funcionar com Python 3.13+. Use Python 3.11 ou 3.12 para melhor compatibilidade.

## 🎮 Como Usar

### Com Ambiente Virtual
```bash
# Ativar ambiente virtual
.\venv\Scripts\Activate.ps1

# Executar o programa
python gesture_control.py
```

### Execução Simples
```bash
python run.py
```

### Execução Direta
```bash
python gesture_control.py
```

### Atalho Rápido (Windows)
```bash
# Use o arquivo batch para ativar automaticamente
activate_env.bat
```

### Primeira Execução
1. **Posicione sua mão na frente da câmera**

3. **Faça os gestos:**
   - 👌 **Gesto OK**: Abre o Notepad
   - 👍 **Joinha**: Abre a Calculadora

4. **Para sair:** Pressione 'q' ou feche a janela

## 🔧 Como Funciona

### OpenCV + MediaPipe
- **OpenCV**: Captura e processa frames da câmera
- **MediaPipe**: Detecta 21 pontos-chave da mão em tempo real
- **Algoritmo de detecção**: Calcula distâncias entre pontos para identificar gestos

### Detecção de Gestos
```python
# Exemplo: Detecção do gesto OK
thumb_index_distance = np.sqrt(
    (thumb_tip.x - index_tip.x)**2 + 
    (thumb_tip.y - index_tip.y)**2
)
return thumb_index_distance < 0.05 and other_fingers_extended
```

## 🎨 Personalização

### Adicionar Novos Gestos
1. Crie uma nova função de detecção:
```python
def detect_new_gesture(self, hand_landmarks):
    # Sua lógica de detecção aqui
    pass
```

2. Adicione a ação no método `execute_action()`:
```python
elif gesture_type == "NEW_GESTURE":
    print("Novo gesto detectado!")
    # Sua ação aqui
```

### Modificar Ações
Edite o arquivo `config.py` para adicionar novas ações:
```python
ACTIONS = {
    "OK": {
        "app": "notepad.exe",
        "description": "Abre o Notepad",
        "color": COLORS['ok_gesture']
    },
    "NOVO_GESTO": {
        "app": "sua_aplicacao.exe",
        "description": "Sua descrição",
        "color": COLORS['text']
    }
}
```

### Configurações Avançadas
O arquivo `config.py` permite personalizar:
- **Câmera**: Resolução e FPS
- **MediaPipe**: Sensibilidade de detecção
- **Gestos**: Distância e cooldown
- **Cores**: Interface visual
- **Debug**: Informações de desenvolvimento

## 🐛 Solução de Problemas

### Câmera não detectada
- Verifique se a webcam está conectada
- Teste com `cv2.VideoCapture(1)` se tiver múltiplas câmeras

### Gestos não detectados
- Ajuste a iluminação
- Mantenha a mão a uma distância adequada da câmera
- Verifique se a mão está completamente visível

### Performance lenta
- Reduza a resolução da câmera
- Ajuste `min_detection_confidence` para valores menores

### Problemas de Import
- **Erro "Import cv2 could not be resolved"**: Ative o ambiente virtual primeiro
- **Erro MediaPipe**: Use Python 3.11+ e ambiente virtual
- **Dependências não encontradas**: Execute `pip install -r requirements.txt` no ambiente virtual

## 🔮 Próximas Funcionalidades

- [ ] Detecção de mais gestos (✌️, 🤙, 👊)
- [ ] Controle de volume do sistema
- [ ] Navegação por slides/presentações
- [ ] Interface gráfica personalizada
- [ ] Configuração de gestos personalizados
- [ ] Suporte a múltiplas mãos

## 📁 Estrutura do Projeto

```
GestIQ/
├── gesture_control.py      # Código principal do sistema
├── config.py              # Configurações centralizadas
├── requirements.txt        # Dependências do projeto
├── README.md              # Documentação
├── activate_env.bat       # Script de ativação (Windows)
├── .gitignore            # Configuração Git
├── venv/                 # Ambiente virtual (ignorado pelo Git)
└── __pycache__/          # Cache Python (ignorado pelo Git)
```

## 📚 Recursos Técnicos

### Bibliotecas Utilizadas
- **OpenCV**: Processamento de imagens e captura de vídeo
- **MediaPipe**: Detecção de pontos-chave das mãos
- **NumPy**: Cálculos matemáticos para detecção de gestos
- **Subprocess**: Execução de aplicações do sistema
- **Type Hints**: Tipagem estática para melhor desenvolvimento

### Arquitetura Melhorada
```
GestureController
├── __init__()              # Inicialização modular
├── _setup_mediapipe()      # Configuração MediaPipe
├── _setup_camera()         # Configuração câmera
├── _setup_controls()       # Configuração controles
├── _get_landmark_points()  # Extração pontos-chave
├── detect_ok_gesture()     # Detecção gesto OK
├── detect_thumbs_up()      # Detecção joinha
├── execute_action()        # Execução ações
├── _process_gestures()     # Processamento gestos
├── _draw_gesture_text()    # Interface visual
├── _cleanup()             # Limpeza recursos
└── run()                  # Loop principal
```

### Melhorias de Code Quality
- ✅ **Type Hints**: Tipagem estática completa
- ✅ **Error Handling**: Tratamento robusto de erros
- ✅ **Modular Design**: Funções pequenas e focadas
- ✅ **Constants**: Configurações centralizadas
- ✅ **Documentation**: Docstrings detalhadas
- ✅ **Environment Management**: Ambiente virtual isolado
- ✅ **Git Configuration**: `.gitignore` configurado corretamente
- ✅ **Cross-Platform**: Suporte Windows/Linux/Mac

## 🤝 Contribuição

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🙏 Agradecimentos

- **OpenCV** pela biblioteca de visão computacional
- **MediaPipe** pela detecção precisa de pontos-chave
- **Google** pelo desenvolvimento do MediaPipe

---

**Desenvolvido com ❤️ para facilitar a interação homem-computador**