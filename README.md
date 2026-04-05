# 🚚 Waze Delivery Automation

**Automação de Geração e Abertura de Rotas no Waze para Serviços de Entrega**

Robô RPA desenvolvido em **Python + Playwright** para o **Desafio Final** do curso *Python to Automation + RPA Intro*.

O projeto resolve um problema real: automatiza o processo manual que entregadores fazem todos os dias — abrir rotas no Waze e enviar localização por WhatsApp.

---

## ✨ Funcionalidades

- ✅ Leitura automática de planilha Excel
- ✅ Geocodificação de endereços via Nominatim (OpenStreetMap)
- ✅ Geração de Deep Link oficial do Waze
- ✅ Abertura automática da rota no navegador
- ✅ Screenshot do mapa com rota calculada
- ✅ Mensagem pronta no **WhatsApp Web** direcionada ao **entregador**
- ✅ Logs detalhados e tratamento de erros
- ✅ Delays configuráveis para demonstração

---

## 🛠️ Tecnologias Utilizadas

- **Playwright** – Automação de navegador (Chromium)
- **Pandas + openpyxl** – Leitura de planilhas Excel
- **Nominatim (OpenStreetMap)** – Geocodificação gratuita
- **Python 3.9+**
- **pathlib + logging** – Organização moderna

---

## 📋 Pré-requisitos

- Python 3.9 
- Google Chrome instalado
- WhatsApp Web já logado (o robô abre o navegador)
- (Recomendado) Ambiente virtual

---

## 🚀 Como executar (passo a passo)

1. git clone https://github.com/jannas3/ProjetoRPA.git
cd ProjetoRPA

2. Crie o ambiente virtual
Bashpython -m venv .bot
3. Ative o ambiente virtual
.\bot\Scripts\activate
4. Instale as dependências
Bashpip install -r requirements.txt
5. Execute o robô
  python main.py
---
  ## Estrutura do Projeto
ProjetoRPA/
├── .bot/
├── data/
│   ├── input/                  # planilhas de entrada
│   └── output/rotas_waze_web/  # screenshots gerados
├── src/
│   ├── data_handler/
│   │   └── excel_handler.py
│   ├── utils/
│   │   └── logger.py
│   └── __init__.py
├── main.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env 