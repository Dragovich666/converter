"""
Interface e modelos de domínio - Define contratos e estruturas de dados (Interface Segregation Principle)
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum


class CabinClass(Enum):
    """Enum para classes de cabine"""
    ECONOMY = "ECONOMY"
    PREMIUM_ECONOMY = "PREMIUM_ECONOMY"
    BUSINESS = "BUSINESS"
    FIRST = "FIRST"


@dataclass
class FlightSearchParams:
    """Parâmetros padronizados para busca de voos"""
    origin: str
    destination: str
    departure_date: datetime
    return_date: Optional[datetime] = None
    adults: int = 1
    children: int = 0
    infants: int = 0
    cabin_class: CabinClass = CabinClass.ECONOMY
    currency: str = 'BRL'
    max_results: int = 50

    def __post_init__(self):
        """Validação após inicialização"""
        self.origin = self.origin.upper()
        self.destination = self.destination.upper()

        if self.adults < 1:
            raise ValueError("Deve haver pelo menos 1 adulto")

        if self.departure_date < datetime.now():
            raise ValueError("Data de partida não pode ser no passado")

        if self.return_date and self.return_date <= self.departure_date:
            raise ValueError("Data de retorno deve ser posterior à data de partida")


@dataclass
class Airport:
    """Informações de aeroporto"""
    code: str
    name: str
    city: str
    country: str


@dataclass
class Flight:
    """Modelo padronizado de voo"""
    id: str
    provider: str
    airline: str

    origin: Airport
    destination: Airport

    departure_datetime: datetime
    arrival_datetime: datetime

    price: float
    currency: str

    airline_logo: Optional[str] = None
    return_departure_datetime: Optional[datetime] = None
    return_arrival_datetime: Optional[datetime] = None

    stops: int = 0
    duration_minutes: int = 0

    available_seats: int = 9
    booking_url: str = ""

    cabin_class: str = "ECONOMY"
    baggage_included: bool = False
    baggage_weight: Optional[str] = None

    flight_number: Optional[str] = None
    aircraft_type: Optional[str] = None

    def to_dict(self) -> Dict:
        """Converte para dicionário"""
        return {
            'id': self.id,
            'provider': self.provider,
            'airline': self.airline,
            'airline_logo': self.airline_logo,
            'origin': {
                'code': self.origin.code,
                'name': self.origin.name,
                'city': self.origin.city,
                'country': self.origin.country
            },
            'destination': {
                'code': self.destination.code,
                'name': self.destination.name,
                'city': self.destination.city,
                'country': self.destination.country
            },
            'departure_datetime': self.departure_datetime.isoformat(),
            'arrival_datetime': self.arrival_datetime.isoformat(),
            'return_departure_datetime': self.return_departure_datetime.isoformat() if self.return_departure_datetime else None,
            'return_arrival_datetime': self.return_arrival_datetime.isoformat() if self.return_arrival_datetime else None,
            'price': self.price,
            'currency': self.currency,
            'stops': self.stops,
            'duration_minutes': self.duration_minutes,
            'duration_formatted': f"{self.duration_minutes // 60}h {self.duration_minutes % 60}min",
            'available_seats': self.available_seats,
            'booking_url': self.booking_url,
            'cabin_class': self.cabin_class,
            'baggage_included': self.baggage_included,
            'baggage_weight': self.baggage_weight,
            'flight_number': self.flight_number,
            'aircraft_type': self.aircraft_type
        }


class IFlightProvider(ABC):
    """Interface que todos os provedores de voos devem implementar (Dependency Inversion Principle)"""

    @abstractmethod
    def search_flights(self, params: FlightSearchParams) -> List[Flight]:
        """Busca voos disponíveis"""
        pass

    @abstractmethod
    def get_provider_name(self) -> str:
        """Retorna o nome do provedor"""
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """Verifica se o provedor está disponível e configurado"""
        pass

    @abstractmethod
    def get_priority(self) -> int:
        """Retorna a prioridade do provedor (menor número = maior prioridade)"""
        pass
