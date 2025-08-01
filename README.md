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

- Python 3.7+
- Webcam funcional
- Windows 10/11 (para compatibilidade com aplicações)

## 🛠️ Instalação

### Pré-requisitos
- **pyenv** instalado: [Instruções de instalação](https://github.com/pyenv/pyenv#installation)

### Setup Automático
1. **Clone o repositório:**
```bash
git clone https://github.com/seu-usuario/GestIQ.git
cd GestIQ
```

2. **Execute o setup (configura pyenv automaticamente):**
```bash
python setup.py
```

### Setup Manual
Se preferir configurar manualmente:

1. **Configure o ambiente pyenv:**
```bash
pyenv install 3.11.7
pyenv local 3.11.7
```

2. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

## 🎮 Como Usar

### Execução Simples
```bash
python run.py
```

### Execução Direta
```bash
python gesture_control.py
```

2. **Posicione sua mão na frente da câmera**

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
Edite o método `execute_action()` para executar diferentes comandos:
```python
subprocess.Popen(["sua_aplicacao.exe"])
```

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

## 🔮 Próximas Funcionalidades

- [ ] Detecção de mais gestos (✌️, 🤙, 👊)
- [ ] Controle de volume do sistema
- [ ] Navegação por slides/presentações
- [ ] Interface gráfica personalizada
- [ ] Configuração de gestos personalizados
- [ ] Suporte a múltiplas mãos

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
- ✅ **Unit Tests**: Testes automatizados
- ✅ **Configuration**: Arquivo de config separado

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