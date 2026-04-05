# 🚚 Waze Delivery Automation

**Automação para geração e envio de rotas no Waze via WhatsApp.**

Projeto RPA em **Python + Playwright** para automatizar abertura de rotas e envio de localização para entregadores.

---

## Funcionalidades

- Leitura automática de planilha Excel  
- Geocodificação via OpenStreetMap (Nominatim)  
- Geração de Deep Link oficial do Waze  
- Abertura automática da rota no navegador  
- Captura de screenshot da rota  
- Envio de mensagem no WhatsApp Web  
- Logs detalhados e tratamento de erros  

---

## Tecnologias

- Python 3.9+  
- Playwright  
- Pandas + openpyxl  
- Nominatim (OpenStreetMap)  
- Pathlib + logging  

---

## Pré-requisitos

- Python 3.9+  
- Google Chrome instalado  
- WhatsApp Web autenticado  
- Ambiente virtual recomendado  

---

## Execução

```bash
git clone https://github.com/jannas3/ProjetoRPA.git
cd ProjetoRPA
python -m venv .bot
# Ative o ambiente virtual:
# Windows: .\.bot\Scripts\activate
# Linux/Mac: source .bot/bin/activate
pip install -r requirements.txt
python main.py



ProjetoRPA/
├── .bot/
├── data/
│   ├── input/
│   └── output/rotas_waze_web/
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