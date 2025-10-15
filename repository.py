"""
Repositório de buscas - Gerencia persistência de dados (Repository Pattern)
Segue o princípio Single Responsibility: apenas gerencia dados de buscas
"""
from typing import Dict, List, Optional
from datetime import datetime
import uuid
import logging

logger = logging.getLogger(__name__)


class SearchRepository:
    """Repositório para gerenciar buscas e resultados"""

    def __init__(self):
        """Inicializa o repositório com armazenamento em memória"""
        self.searches: Dict[str, dict] = {}
        self.results: Dict[str, List[dict]] = {}
        logger.info("SearchRepository inicializado")

    def save_search(self, search_data: dict) -> str:
        """
        Salva uma nova busca

        Args:
            search_data: Dados da busca realizada

        Returns:
            ID único da busca
        """
        search_id = str(uuid.uuid4())

        self.searches[search_id] = {
            'id': search_id,
            'data': search_data,
            'timestamp': datetime.now().isoformat(),
            'status': 'completed'
        }

        logger.info(f"Busca salva com ID: {search_id}")
        return search_id

    def save_results(self, search_id: str, results: List[dict]) -> None:
        """
        Salva os resultados de uma busca

        Args:
            search_id: ID da busca
            results: Lista de resultados
        """
        self.results[search_id] = results
        logger.info(f"Resultados salvos para busca {search_id}: {len(results)} voos")

    def get_search(self, search_id: str) -> Optional[dict]:
        """
        Recupera uma busca pelo ID

        Args:
            search_id: ID da busca

        Returns:
            Dados da busca ou None se não encontrada
        """
        return self.searches.get(search_id)

    def get_results(self, search_id: str) -> Optional[List[dict]]:
        """
        Recupera os resultados de uma busca

        Args:
            search_id: ID da busca

        Returns:
            Lista de resultados ou None se não encontrada
        """
        return self.results.get(search_id)

    def list_all_searches(self) -> List[dict]:
        """
        Lista todas as buscas realizadas

        Returns:
            Lista com todas as buscas
        """
        return list(self.searches.values())

    def get_search_stats(self) -> dict:
        """
        Retorna estatísticas das buscas

        Returns:
            Dicionário com estatísticas
        """
        total_searches = len(self.searches)
        total_results = sum(len(results) for results in self.results.values())

        return {
            'total_searches': total_searches,
            'total_results': total_results,
            'average_results_per_search': total_results / total_searches if total_searches > 0 else 0
        }

    def delete_search(self, search_id: str) -> bool:
        """
        Remove uma busca e seus resultados

        Args:
            search_id: ID da busca

        Returns:
            True se removido com sucesso, False caso contrário
        """
        if search_id in self.searches:
            del self.searches[search_id]
            if search_id in self.results:
                del self.results[search_id]
            logger.info(f"Busca {search_id} removida")
            return True
        return False

