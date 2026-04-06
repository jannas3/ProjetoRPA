import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.resolve()))

from app.src.automation.waze_router import abrir_rotas_waze
from app.src.utils.logger import configurar_logger


def main():
    logger = configurar_logger()
    logger.info("🚀 INICIANDO ROBÔ DE GERAÇÃO E ABERTURA DE ROTAS NO WAZE")

    abrir_rotas_waze(
        caminho_planilha="app/data/input/entregas_exemplo.xlsx",
        coluna_endereco="endereco",
        coluna_telefone="telefone",  
    )

    logger.info("🎉 ROBÔ FINALIZADO COM SUCESSO!")


if __name__ == "__main__":
    main()