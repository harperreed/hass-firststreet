"""FirstStreet API SDK."""
import requests
import json
from typing import Dict, List, Any
import logging
from .property_queries import PROPERTY_BY_FSID_QUERY

_LOGGER = logging.getLogger(__name__)


class FirstStreetAPIError(Exception):
    """Exception raised for errors in the FirstStreet API."""

    def __init__(self, message: str, details: Any = None):
        """Initialize the exception with a message and optional details."""
        self.message = message
        self.details = details
        super().__init__(self.message)

        # Log the error
        _LOGGER.error("FirstStreetAPIError: %s", self.message)
        if self.details:
            _LOGGER.error("Error details: %s", self.details)

class FirstStreetAPI:
    def __init__(self, base_url: str = "https://firststreet.org/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json; charset=utf-8"
        })

    def get_property_data(self, fsid: int, building_id: int = 0) -> Dict[str, Any]:
        """
        Fetch property data from the FirstStreet API.

        :param fsid: The FirstStreet ID of the property
        :param building_id: The building ID (default is 0)
        :return: Parsed JSON response
        :raises FirstStreetAPIError: If the API returns an error or unexpected data
        """
        endpoint = f"{self.base_url}api/fsfapi/"
        
        variables = {
            "fsid": str(fsid),
            "buildingId": str(building_id)
        }
        
        payload = {
            "query": PROPERTY_BY_FSID_QUERY,
            "variables": variables
        }
        
        try:
            response = self.session.post(endpoint, json=payload)
            response.raise_for_status()
            data = response.json()
            
            _LOGGER.debug("API Response: %s", json.dumps(data, indent=2))
            
            if 'errors' in data:
                raise FirstStreetAPIError("API returned an error", data['errors'])
            
            if 'data' not in data:
                raise FirstStreetAPIError("Unexpected API response structure: 'data' key missing", data)
            
            if 'property' not in data['data']:
                raise FirstStreetAPIError("Unexpected API response structure: 'property' key missing", data['data'])
            
            if data['data']['property'] is None:
                raise FirstStreetAPIError("Property data is None", data['data'])
            
            return data['data']['property']
        except requests.RequestException as e:
            raise FirstStreetAPIError(f"Request to FirstStreet API failed: {str(e)}", str(e))


    def parse_flood_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse flood-related data from the API response."""
        flood_data = data['property']['flood']
        return {
            'flood_factor': flood_data['floodFactor'],
            'risk_direction': flood_data['riskDirection'],
            'insurance_requirement': flood_data['insuranceRequirement'],
            'adaptation_count': flood_data['adaptationConnection']['totalCount'],
            'probability': flood_data['probability'],
            'insurance_quotes': flood_data['insuranceQuotes']['rates'] if flood_data['insuranceQuotes'] else None,
            'historic_events': flood_data['historic'],
            'insights': flood_data['insights']
        }

    def parse_fire_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse fire-related data from the API response."""
        fire_data = data['property']['fire']
        return {
            'fire_factor': fire_data['fireFactor'],
            'risk_direction': fire_data['riskDirection'],
            'defensible_space': fire_data['defensibleSpace'],
            'usfs_relative_risk': fire_data['usfsRelativeRisk'],
            'prescribed_burns_count': fire_data['prescribedBurns']['totalCount'],
            'probability': fire_data['probability'],
            'historic_events': [event['node'] for event in fire_data['historicConnection']['edges']],
            'insurance_quotes': fire_data['insuranceHippo']['rates'] if fire_data['insuranceHippo'] else None,
            'insights': fire_data['insights']
        }

    def parse_heat_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse heat-related data from the API response."""
        heat_data = data['property']['heat']
        return {
            'heat_factor': heat_data['heatFactor'],
            'hot_temperature': heat_data['hotTemperature'],
            'anomaly_temperature': heat_data['anomalyTemperature'],
            'temperature_average_high': heat_data['temperatureAverageHigh'],
            'cooling': heat_data['cooling'],
            'heat_waves': heat_data['heatWaves'],
            'days': heat_data['days'],
            'insights': heat_data['insights']
        }

    def parse_wind_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse wind-related data from the API response."""
        wind_data = data['property']['wind']
        return {
            'wind_factor': wind_data['windFactor'],
            'factor_scale': wind_data['factorScale'],
            'risk_direction': wind_data['riskDirection'],
            'has_tornado_risk': wind_data['hasTornadoRisk'],
            'has_thunderstorm_risk': wind_data['hasThunderstormRisk'],
            'has_cyclone_risk': wind_data['hasCycloneRisk'],
            'greatest_wind_risk': wind_data['greatestWindRisk'],
            'missile_environment': wind_data['missileEnvironment'],
            'primary_wind_direction': wind_data['primaryWindDirection'],
            'probability': wind_data['probability'],
            'historic_events': [event['node'] for event in wind_data['historicConnection']['edges']]
        }

    def parse_air_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse air quality-related data from the API response."""
        air_data = data['property']['air']
        return {
            'air_factor': air_data['airFactor'],
            'factor_scale': air_data['factorScale'],
            'risk_direction': air_data['riskDirection'],
            'days': air_data['days'],
            'greatest_risk': air_data['greatestRisk'],
            'tri_nearby': air_data['triNearby'],
            'tri_facilities': [facility['node'] for facility in air_data['triFacilityConnection']['edges']],
            'historic': air_data['historic'],
            'insights': air_data['insights'],
            'percentile': air_data['percentile']
        }

    def get_all_risk_data(self, fsid: int, building_id: int = 0) -> Dict[str, Any]:
        """
        Fetch and parse all risk data for a property.

        :param fsid: The FirstStreet ID of the property
        :param building_id: The building ID (default is 0)
        :return: Dictionary containing all parsed risk data
        :raises FirstStreetAPIError: If the API returns an error or unexpected data
        """
        raw_data = self.get_property_data(fsid, building_id)
        
        if 'data' not in raw_data or 'property' not in raw_data['data']:
            raise FirstStreetAPIError("Unexpected API response structure")

        property_data = raw_data['data']['property']
        
        return {
            'flood': self.parse_flood_data(property_data),
            'fire': self.parse_fire_data(property_data),
            'heat': self.parse_heat_data(property_data),
            'wind': self.parse_wind_data(property_data),
            'air': self.parse_air_data(property_data)
        }
