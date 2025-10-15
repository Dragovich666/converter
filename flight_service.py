"""
Serviço de busca de voos - Orquestra múltiplos provedores (Facade Pattern + Strategy Pattern)
Segue o princípio Single Responsibility: apenas coordena a busca entre provedores
"""
import logging
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from interfaces import IFlightProvider, FlightSearchParams, Flight

logger = logging.getLogger(__name__)


class FlightSearchService:
    """Serviço que agrega resultados de múltiplos provedores de voos"""

    def __init__(self, providers: List[IFlightProvider]):
        """
        Inicializa o serviço com uma lista de provedores

        Args:
            providers: Lista de provedores que implementam IFlightProvider
        """
        self.providers = providers
        logger.info(f"FlightSearchService inicializado com {len(providers)} provedores")

    def search_flights(self, params: FlightSearchParams) -> List[Flight]:
        """
        Busca voos em todos os provedores disponíveis em paralelo

        Args:
            params: Parâmetros de busca padronizados

        Returns:
            Lista de voos encontrados, ordenados por preço
        """
        all_flights = []

        # Filtra apenas provedores disponíveis e ordena por prioridade
        available_providers = [p for p in self.providers if p.is_available()]
        available_providers.sort(key=lambda p: p.get_priority())

        if not available_providers:
            logger.warning("Nenhum provedor de voos disponível")
            return []

        logger.info(f"Buscando em {len(available_providers)} provedores disponíveis")

        # Busca em paralelo usando ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=len(available_providers)) as executor:
            # Submete todas as buscas
            future_to_provider = {
                executor.submit(provider.search_flights, params): provider
                for provider in available_providers
            }

            # Coleta os resultados conforme ficam prontos
            for future in as_completed(future_to_provider):
                provider = future_to_provider[future]
                try:
                    flights = future.result(timeout=60)
                    all_flights.extend(flights)
                    logger.info(f"{provider.get_provider_name()}: {len(flights)} voos encontrados")
                except Exception as e:
                    logger.error(f"Erro no provedor {provider.get_provider_name()}: {str(e)}")

        # Remove duplicatas baseadas em características similares
        unique_flights = self._remove_duplicates(all_flights)

        # Ordena por preço (mais barato primeiro)
        unique_flights.sort(key=lambda x: x.price)

        logger.info(f"Total de {len(unique_flights)} voos únicos encontrados")
        return unique_flights

    def _remove_duplicates(self, flights: List[Flight]) -> List[Flight]:
        """
        Remove voos duplicados baseados em características chave

        Args:
            flights: Lista de voos

        Returns:
            Lista de voos sem duplicatas
        """
        seen = set()
        unique_flights = []

        for flight in flights:
            # Cria uma chave única baseada em características principais
            key = (
                flight.airline,
                flight.origin.code,
                flight.destination.code,
                flight.departure_datetime.strftime('%Y-%m-%d %H:%M'),
                flight.flight_number
            )

            if key not in seen:
                seen.add(key)
                unique_flights.append(flight)

        return unique_flights

    def get_cheapest_flights(self, params: FlightSearchParams, limit: int = 10) -> List[Flight]:
        """
        Retorna os voos mais baratos

        Args:
            params: Parâmetros de busca
            limit: Número máximo de resultados

        Returns:
            Lista com os voos mais baratos
        """
        flights = self.search_flights(params)
        return flights[:limit]

    def get_fastest_flights(self, params: FlightSearchParams, limit: int = 10) -> List[Flight]:
        """
        Retorna os voos mais rápidos

        Args:
            params: Parâmetros de busca
            limit: Número máximo de resultados

        Returns:
            Lista com os voos mais rápidos
        """
        flights = self.search_flights(params)
        flights.sort(key=lambda x: x.duration_minutes)
        return flights[:limit]

    def get_direct_flights(self, params: FlightSearchParams) -> List[Flight]:
        """
        Retorna apenas voos diretos (sem escalas)

        Args:
            params: Parâmetros de busca

        Returns:
            Lista com voos diretos
        """
        flights = self.search_flights(params)
        direct_flights = [f for f in flights if f.stops == 0]
        return direct_flights

