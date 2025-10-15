"""
Provedor Amadeus - Implementação usando API real (Open/Closed Principle)
"""
import requests
import logging
from typing import List, Optional
from datetime import datetime, timedelta
from interfaces import IFlightProvider, FlightSearchParams, Flight, Airport
from config import Config

logger = logging.getLogger(__name__)


class AmadeusFlightProvider(IFlightProvider):
    """Provedor de voos usando API Amadeus - Requer credenciais"""

    def __init__(self):
        self.api_key = Config.AMADEUS_API_KEY
        self.api_secret = Config.AMADEUS_API_SECRET
        self.base_url = Config.AMADEUS_BASE_URL
        self.timeout = Config.REQUEST_TIMEOUT
        self._access_token: Optional[str] = None
        self._token_expiry: Optional[datetime] = None

    def _get_access_token(self) -> str:
        """Obtém token OAuth2 da API Amadeus"""
        # Verifica se token ainda é válido
        if self._access_token and self._token_expiry:
            if datetime.now() < self._token_expiry:
                return self._access_token

        try:
            response = requests.post(
                f'{self.base_url}/v1/security/oauth2/token',
                data={
                    'grant_type': 'client_credentials',
                    'client_id': self.api_key,
                    'client_secret': self.api_secret
                },
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            self._access_token = data['access_token']
            # Token expira em X segundos, subtraímos 60s para segurança
            expires_in = data.get('expires_in', 1800) - 60
            self._token_expiry = datetime.now() + timedelta(seconds=expires_in)

            logger.info("Token Amadeus obtido com sucesso")
            return self._access_token

        except Exception as e:
            logger.error(f"Erro ao obter token Amadeus: {str(e)}")
            raise

    def search_flights(self, params: FlightSearchParams) -> List[Flight]:
        """Busca voos reais na API Amadeus"""
        if not self.is_available():
            logger.warning("Amadeus provider não está disponível - credenciais não configuradas")
            return []

        try:
            token = self._get_access_token()
            headers = {'Authorization': f'Bearer {token}'}

            query_params = {
                'originLocationCode': params.origin,
                'destinationLocationCode': params.destination,
                'departureDate': params.departure_date.strftime('%Y-%m-%d'),
                'adults': params.adults,
                'currencyCode': params.currency,
                'max': params.max_results,
                'travelClass': params.cabin_class.value
            }

            if params.return_date:
                query_params['returnDate'] = params.return_date.strftime('%Y-%m-%d')

            if params.children > 0:
                query_params['children'] = params.children

            if params.infants > 0:
                query_params['infants'] = params.infants

            logger.info(f"Buscando voos Amadeus: {params.origin} -> {params.destination}")

            response = requests.get(
                f'{self.base_url}/v2/shopping/flight-offers',
                headers=headers,
                params=query_params,
                timeout=self.timeout
            )
            response.raise_for_status()

            data = response.json()
            flights = self._parse_flights(data)

            logger.info(f"Amadeus: {len(flights)} voos encontrados")
            return flights

        except requests.exceptions.RequestException as e:
            logger.error(f"Erro na requisição Amadeus: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Erro ao processar resposta Amadeus: {str(e)}")
            return []

    def _parse_flights(self, data: dict) -> List[Flight]:
        """Converte resposta da API para modelo padronizado"""
        flights = []

        for offer in data.get('data', []):
            try:
                itinerary = offer['itineraries'][0]
                first_segment = itinerary['segments'][0]
                last_segment = itinerary['segments'][-1]

                # Origem
                origin = Airport(
                    code=first_segment['departure']['iataCode'],
                    name=first_segment['departure'].get('terminal', ''),
                    city=first_segment['departure'].get('at', '').split('T')[0],
                    country=''
                )

                # Destino
                destination = Airport(
                    code=last_segment['arrival']['iataCode'],
                    name=last_segment['arrival'].get('terminal', ''),
                    city=last_segment['arrival'].get('at', '').split('T')[0],
                    country=''
                )

                # Datas
                departure_dt = datetime.fromisoformat(first_segment['departure']['at'].replace('Z', '+00:00'))
                arrival_dt = datetime.fromisoformat(last_segment['arrival']['at'].replace('Z', '+00:00'))

                # Voo de retorno
                return_departure_dt = None
                return_arrival_dt = None

                if len(offer['itineraries']) > 1:
                    return_itinerary = offer['itineraries'][1]
                    return_first = return_itinerary['segments'][0]
                    return_last = return_itinerary['segments'][-1]
                    return_departure_dt = datetime.fromisoformat(return_first['departure']['at'].replace('Z', '+00:00'))
                    return_arrival_dt = datetime.fromisoformat(return_last['arrival']['at'].replace('Z', '+00:00'))

                # Duração em minutos
                duration_str = itinerary.get('duration', 'PT0H0M')
                duration_minutes = self._parse_duration(duration_str)

                flight = Flight(
                    id=offer['id'],
                    provider='Amadeus',
                    airline=first_segment['carrierCode'],
                    airline_logo=None,
                    origin=origin,
                    destination=destination,
                    departure_datetime=departure_dt,
                    arrival_datetime=arrival_dt,
                    return_departure_datetime=return_departure_dt,
                    return_arrival_datetime=return_arrival_dt,
                    price=float(offer['price']['total']),
                    currency=offer['price']['currency'],
                    stops=len(itinerary['segments']) - 1,
                    duration_minutes=duration_minutes,
                    available_seats=offer.get('numberOfBookableSeats', 9),
                    booking_url='',
                    cabin_class=first_segment.get('cabin', 'ECONOMY'),
                    baggage_included=True,
                    baggage_weight=None,
                    flight_number=f"{first_segment['carrierCode']}{first_segment['number']}",
                    aircraft_type=first_segment.get('aircraft', {}).get('code')
                )

                flights.append(flight)

            except Exception as e:
                logger.error(f"Erro ao parsear voo Amadeus: {str(e)}")
                continue

        return flights

    def _parse_duration(self, duration_str: str) -> int:
        """Converte string de duração ISO 8601 para minutos"""
        try:
            # Formato: PT2H30M
            duration_str = duration_str.replace('PT', '')
            hours = 0
            minutes = 0

            if 'H' in duration_str:
                parts = duration_str.split('H')
                hours = int(parts[0])
                duration_str = parts[1] if len(parts) > 1 else ''

            if 'M' in duration_str:
                minutes = int(duration_str.replace('M', ''))

            return hours * 60 + minutes
        except:
            return 0

    def get_provider_name(self) -> str:
        return 'Amadeus'

    def is_available(self) -> bool:
        return bool(self.api_key and self.api_secret)

    def get_priority(self) -> int:
        return 2  # Prioridade média (API paga mas confiável)

