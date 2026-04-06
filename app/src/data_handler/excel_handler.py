import pandas as pd
from pathlib import Path
from app.src.utils.logger import configurar_logger

logger = configurar_logger()


def carregar_entregas(caminho_planilha: str) -> pd.DataFrame:
    """
    Carrega a planilha de entregas e faz validações básicas.
    """
    caminho = Path(caminho_planilha)

    if not caminho.exists():
        logger.error(f" Planilha não encontrada: {caminho}")
        raise FileNotFoundError(f"Planilha não encontrada: {caminho}")

    logger.info(f" Carregando planilha: {caminho.name}")
    df = pd.read_excel(caminho)

    logger.info(f" {len(df)} entregas carregadas com sucesso.")
    return df
