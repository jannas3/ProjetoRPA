from playwright.sync_api import sync_playwright
import time
from urllib.parse import quote
from pathlib import Path
from src.data_handler.excel_handler import carregar_entregas
from src.utils.logger import configurar_logger

logger = configurar_logger()


def gerar_link_waze(endereco: str) -> str:
    """Gera Deep Link oficial do Waze conforme documentação oficial."""
    endereco_codificado = quote(endereco.strip())
    return (
        f"https://waze.com/ul?q={endereco_codificado}"
        "&navigate=yes"  # inicia navegação automaticamente
        "&z=17"  # zoom ideal para entregas urbanas
    )


def abrir_rotas_waze(
    caminho_planilha: str, coluna_endereco: str = "endereco", delay_entre_rotas: int = 7
):
    df = carregar_entregas(caminho_planilha)

    # Cria pasta de screenshots
    pasta_saida = Path("data/output/rotas_geradas")
    pasta_saida.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=400)
        page = browser.new_page()

        logger.info(f"🌐 Browser Playwright aberto - Processando {len(df)} rotas")

        for indice, linha in df.iterrows():
            endereco = str(linha[coluna_endereco])
            cliente = str(linha.get("cliente", f"Entrega_{indice+1}"))

            logger.info(f"[{indice+1:02d}/{len(df)}] 📍 {cliente} → {endereco[:60]}...")

            url_waze = gerar_link_waze(endereco)
            page.goto(url_waze, wait_until="networkidle", timeout=30000)

            # Aguarda carregamento completo do mapa do Waze
            page.wait_for_timeout(4500)

            # Screenshot
            nome_arquivo = (
                f"{indice+1:03d}_{cliente.replace(' ', '_').replace('/', '')}.png"
            )
            caminho_screenshot = pasta_saida / nome_arquivo
            page.screenshot(path=str(caminho_screenshot), full_page=True)

            logger.info(f"   📸 Screenshot salvo → {nome_arquivo}")

            time.sleep(delay_entre_rotas)  # pausa para visualização na apresentação

        logger.info("✅ TODAS AS ROTAS FORAM GERADAS E ABERTAS COM SUCESSO!")
        browser.close()
