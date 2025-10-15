"""
Provedor Kiwi.com - Implementação concreta usando API real (Open/Closed Principle)
"""
import requests
import logging
from typing import List
from datetime import datetime
from interfaces import IFlightProvider, FlightSearchParams, Flight, Airport
from config import Config

logger = logging.getLogger(__name__)


class KiwiFlightProvider(IFlightProvider):
    """Provedor de voos usando API Kiwi.com (Tequila API) - API gratuita com dados reais"""

    def __init__(self):
        self.api_key = Config.KIWI_API_KEY
        self.base_url = Config.KIWI_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT

    def search_flights(self, params: FlightSearchParams) -> List[Flight]:
        """Busca voos reais na API Kiwi.com"""
        if not self.is_available():
            logger.warning("Kiwi provider não está disponível - API key não configurada")
            return []

        try:
            headers = {'apikey': self.api_key}

            query_params = {
                'fly_from': params.origin,
                'fly_to': params.destination,
                'date_from': params.departure_date.strftime('%d/%m/%Y'),
                'date_to': params.departure_date.strftime('%d/%m/%Y'),
                'adults': params.adults,
                'children': params.children,
                'infants': params.infants,
                'curr': params.currency,
                'limit': params.max_results,
                'sort': 'price',
                'flight_type': 'round' if params.return_date else 'oneway'
            }

            if params.return_date:
                query_params['return_from'] = params.return_date.strftime('%d/%m/%Y')
                query_params['return_to'] = params.return_date.strftime('%d/%m/%Y')

            logger.info(f"Buscando voos Kiwi: {params.origin} -> {params.destination}")

            response = requests.get(
                f'{self.base_url}/v2/search',
                headers=headers,
                params=query_params,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            flights = self._parse_flights(data, params)

            logger.info(f"Kiwi: {len(flights)} voos encontrados")
            return flights

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição Kiwi: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Erro ao processar resposta Kiwi: {str(e)}")
            return []

    def _parse_flights(self, data: dict, params: FlightSearchParams) -> List[Flight]:
        """Converte resposta da API para modelo padronizado"""
        flights = []

        for item in data.get('data', []):
            try:
                route = item['route'][0] if item.get('route') else None
                if not route:
                    continue

                # Informações do aeroporto de origem
                origin = Airport(
                    code=route['flyFrom'],
                    name=route.get('cityFrom', route['flyFrom']),
                    city=route.get('cityFrom', ''),
                    country=route.get('countryFrom', {}).get('name', '') if isinstance(route.get('countryFrom'), dict) else ''
                )

                # Informações do aeroporto de destino
                destination = Airport(
                    code=route['flyTo'],
                    name=route.get('cityTo', route['flyTo']),
                    city=route.get('cityTo', ''),
                    country=route.get('countryTo', {}).get('name', '') if isinstance(route.get('countryTo'), dict) else ''
                )

                # Datas e horários
                departure_dt = datetime.fromtimestamp(route['dTime'])
                arrival_dt = datetime.fromtimestamp(route['aTime'])

                # Verifica voo de retorno
                return_departure_dt = None
                return_arrival_dt = None

                if len(item['route']) > 1 and params.return_date:
                    return_route = item['route'][-1]
                    return_departure_dt = datetime.fromtimestamp(return_route['dTime'])
                    return_arrival_dt = datetime.fromtimestamp(return_route['aTime'])

                flight = Flight(
                    id=item['id'],
                    provider='Kiwi.com',
                    airline=route.get('airline', 'N/A'),
                    airline_logo=f"https://images.kiwi.com/airlines/64/{route.get('airline', '')}.png" if route.get('airline') else None,
                    origin=origin,
                    destination=destination,
                    departure_datetime=departure_dt,
                    arrival_datetime=arrival_dt,
                    return_departure_datetime=return_departure_dt,
                    return_arrival_datetime=return_arrival_dt,
                    price=float(item['price']),
                    currency=item.get('currency', params.currency),
                    stops=len(item['route']) - 1,
                    duration_minutes=item.get('duration', {}).get('total', 0) // 60 if item.get('duration') else 0,
                    available_seats=item.get('availability', {}).get('seats') if item.get('availability') else 9,
                    booking_url=item.get('deep_link', ''),
                    cabin_class=params.cabin_class.value,
                    baggage_included=bool(item.get('baglimit', {}).get('hand_weight')),
                    baggage_weight=f"{item.get('baglimit', {}).get('hand_weight', 0)}kg" if item.get('baglimit') else None,
                    flight_number=route.get('flight_no'),
                    aircraft_type=route.get('vehicle_type')
                )

                flights.append(flight)

            except Exception as e:
                logger.error(f"Erro ao parsear voo Kiwi: {str(e)}")
                continue

        return flights

    def get_provider_name(self) -> str:
        return 'Kiwi.com'

    def is_available(self) -> bool:
        return bool(self.api_key)

    def get_priority(self) -> int:
        return 1  # Alta prioridade (API gratuita e confiável)

