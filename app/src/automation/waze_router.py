from playwright.sync_api import sync_playwright
import time
import requests
from typing import Optional, Tuple
from urllib.parse import quote
from pathlib import Path

from src.data_handler.excel_handler import carregar_entregas
from src.utils.logger import configurar_logger


# CONFIGURAÇÕES GERAIS
logger = configurar_logger()

DESKTOP_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0.0.0 Safari/537.36"
)

DELAY_ENTRE_ROTAS = 15
ENVIAR_WHATSAPP = True
MODO_ENVIO_AUTOMATICO = True  

# GEOLOCALIZAÇÃO

def geocodificar_endereco(endereco: str) -> Optional[Tuple[float, float]]:
    try:
        endereco_completo = f"{endereco}, Manaus, AM, Brasil"

        resp = requests.get(
            "https://nominatim.openstreetmap.org/search",
            params={"q": endereco_completo, "format": "json", "limit": 1},
            headers={"User-Agent": "robo-entregas/1.0"},
            timeout=10,
        )

        resp.raise_for_status()
        dados = resp.json()

        if dados:
            return float(dados[0]["lat"]), float(dados[0]["lon"])

    except Exception as e:
        logger.warning(f" Erro na geocodificação: {e}")

    return None


def geocodificar_com_retry(endereco: str, tentativas: int = 3) -> Optional[Tuple[float, float]]:
    for tentativa in range(1, tentativas + 1):
        coords = geocodificar_endereco(endereco)
        if coords:
            return coords
        logger.warning(f"   Tentativa {tentativa}/{tentativas} falhou")
        time.sleep(2)
    return None

# LINKS
def gerar_link_waze(lat: float, lng: float) -> str:
    return f"https://ul.waze.com/ul?ll={lat},{lng}&navigate=yes"


def gerar_link_whatsapp(
    telefone: str, lat: float, lng: float, cliente: str, endereco: str
) -> str:
    link_waze = gerar_link_waze(lat, lng)

    mensagem = (
        f"Olá! Segue a localização para entrega de *{cliente}*:\n\n"
        f"📍 Endereço: {endereco}\n\n"
        f" Abrir no Waze:\n{link_waze}"
    )

    return f"https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}"

# AUTOMAÇÃO PRINCIPAL


def abrir_rotas_waze(
    caminho_planilha: str,
    coluna_endereco: str = "endereco",
    coluna_telefone: str = "telefone",
):
    df = carregar_entregas(caminho_planilha)

    pasta_saida = Path("data/output/rotas_waze_web")
    pasta_saida.mkdir(parents=True, exist_ok=True)

    total = len(df)
    sucesso = 0
    falha_geo = 0
    falha_wpp = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
            slow_mo=250,
            args=["--start-maximized"],
        )

        context = browser.new_context(
            user_agent=DESKTOP_UA,
            viewport={"width": 1920, "height": 1080},
            locale="pt-BR",
            timezone_id="America/Manaus",
        )

        page = context.new_page()

        logger.info(f" Waze + WhatsApp Web — {total} entregas")

        for indice, linha in df.iterrows():
            cliente = str(linha.get("cliente", f"Entrega_{indice+1}"))
            endereco = str(linha.get(coluna_endereco, "")).strip()
            telefone = (
                str(linha.get(coluna_telefone, ""))
                .strip()
                .replace(" ", "")
                .replace("-", "")
            )

            logger.info(f"[{indice+1:02d}/{total}] PROCESSANDO ENTREGA")
            logger.info(f"   Cliente: {cliente}")
            logger.info(f"   📍 Endereço: {endereco}")

            if not endereco or endereco.lower() == "nan":
                logger.warning(" Endereço inválido")
                falha_geo += 1
                continue

            # 1️ Geocodificação
            coords = geocodificar_com_retry(endereco)
            if not coords:
                logger.warning("  Endereço não localizado")
                falha_geo += 1
                continue

            lat, lng = coords
            logger.info(f"  Coordenadas: {lat}, {lng}")

            # 2️ Abre Waze Web
            url_waze = (
                f"https://www.waze.com/pt-BR/live-map/directions"
                f"?to=ll.{lat},{lng}&navigate=yes"
            )

            page.goto(url_waze, wait_until="domcontentloaded", timeout=30000)

            try:
                page.wait_for_selector("canvas", timeout=12000)
            except Exception:
                page.wait_for_timeout(7000)

            # 3️ Screenshot
            nome_arquivo = f"{indice+1:03d}_{cliente.replace(' ', '_')}.png"
            page.screenshot(path=str(pasta_saida / nome_arquivo), full_page=True)
            logger.info(f"   📸 Screenshot salvo: {nome_arquivo}")

            # 4️ ENVIO WHATSAPP (ABA NOVA)
            if ENVIAR_WHATSAPP and telefone:
                logger.info(f" Enviando WhatsApp para {telefone}")

                envio_ok = False
                page_wpp = context.new_page()

                try:
                    page_wpp.goto(
                        gerar_link_whatsapp(telefone, lat, lng, cliente, endereco),
                        wait_until="domcontentloaded",
                        timeout=30000,
                    )

                    page_wpp.wait_for_selector(
                        'div[contenteditable="true"][data-tab]',
                        timeout=30000,
                    )

                    time.sleep(2)
                    page_wpp.click('div[contenteditable="true"][data-tab]')
                    time.sleep(1)

                    if MODO_ENVIO_AUTOMATICO:
                        page_wpp.keyboard.press("Enter")
                        logger.info("  WhatsApp enviado")
                        envio_ok = True
                    else:
                        logger.info("    WhatsApp pronto para envio manual")

                except Exception as e:
                    logger.warning(f"    Falha no WhatsApp: {e}")
                    falha_wpp += 1

                finally:
                    page_wpp.close()

                if envio_ok:
                    sucesso += 1

                time.sleep(DELAY_ENTRE_ROTAS)

            else:
                sucesso += 1
        # RESUMO FINAL
       
        logger.info(" RESUMO FINAL")
        logger.info(f"   Total de entregas: {total}")
        logger.info(f"   Sucesso: {sucesso}")
        logger.info(f"   Falha geocodificação: {falha_geo}")
        logger.info(f"   Falha WhatsApp: {falha_wpp}")

        logger.info(" ROBÔ FINALIZADO COM SUCESSO")

        context.close()
        browser.close()