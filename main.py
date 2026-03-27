import sys
from pathlib import Path

# === LINHA MÁGICA QUE RESOLVE O ERRO ===
sys.path.insert(0, str(Path(__file__).parent.resolve()))

from src.automation.waze_router import abrir_rotas_waze
from src.utils.logger import configurar_logger


def main():
    logger = configurar_logger()
    logger.info("🚀 INICIANDO ROBÔ DE GERAÇÃO E ABERTURA DE ROTAS NO WAZE")

    abrir_rotas_waze(
        caminho_planilha="data/input/entregas_exemplo.xlsx",
        coluna_endereco="endereco",
        delay_entre_rotas=7,
    )

    logger.info("🎉 ROBÔ FINALIZADO COM SUCESSO!")


if __name__ == "__main__":
    main()
