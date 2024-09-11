import unittest
from unittest.mock import patch, MagicMock
from firststreet_api import FirstStreetAPI, FirstStreetAPIError

class TestFirstStreetAPI(unittest.TestCase):

    def setUp(self):
        self.api = FirstStreetAPI()

    @patch('firststreet_api.requests.Session')
    def test_get_property_data_success(self, mock_session):
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': {
                'property': {
                    'flood': {'floodFactor': 5},
                    'fire': {'fireFactor': 3},
                    'heat': {'heatFactor': 4},
                    'wind': {'windFactor': 2},
                    'air': {'airFactor': 1}
                }
            }
        }
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.post.return_value = mock_response

        result = self.api.get_property_data(12345)
        self.assertEqual(result['flood']['floodFactor'], 5)
        self.assertEqual(result['fire']['fireFactor'], 3)
        self.assertEqual(result['heat']['heatFactor'], 4)
        self.assertEqual(result['wind']['windFactor'], 2)
        self.assertEqual(result['air']['airFactor'], 1)

    @patch('firststreet_api.requests.Session')
    def test_get_property_data_api_error(self, mock_session):
        mock_response = MagicMock()
        mock_response.json.return_value = {'errors': ['API Error']}
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.post.return_value = mock_response

        with self.assertRaises(FirstStreetAPIError):
            self.api.get_property_data(12345)

    @patch('firststreet_api.requests.Session')
    def test_get_property_data_unexpected_structure(self, mock_session):
        mock_response = MagicMock()
        mock_response.json.return_value = {'unexpected': 'structure'}
        mock_response.raise_for_status.return_value = None
        mock_session.return_value.post.return_value = mock_response

        with self.assertRaises(FirstStreetAPIError):
            self.api.get_property_data(12345)

    def test_parse_flood_data(self):
        mock_data = {
            'property': {
                'flood': {
                    'floodFactor': 5,
                    'riskDirection': 'increasing',
                    'insuranceRequirement': 'required',
                    'adaptationConnection': {'totalCount': 2},
                    'probability': {'cumulative': [{'threshold': 1, 'mid': 0.5}]},
                    'insuranceQuotes': {'rates': [{'minPrice': 100, 'maxPrice': 200}]},
                    'historic': [{'eventId': '123', 'name': 'Flood 2020'}],
                    'insights': [{'name': 'Insight 1', 'details': [{'name': 'Detail 1', 'value': 'Value 1'}]}]
                }
            }
        }
        result = self.api.parse_flood_data(mock_data)
        self.assertEqual(result['flood_factor'], 5)
        self.assertEqual(result['risk_direction'], 'increasing')
        self.assertEqual(result['insurance_requirement'], 'required')
        self.assertEqual(result['adaptation_count'], 2)
        self.assertEqual(result['probability']['cumulative'][0]['threshold'], 1)
        self.assertEqual(result['insurance_quotes'][0]['minPrice'], 100)
        self.assertEqual(result['historic_events'][0]['eventId'], '123')
        self.assertEqual(result['insights'][0]['name'], 'Insight 1')

    def test_parse_fire_data(self):
        mock_data = {
            'property': {
                'fire': {
                    'fireFactor': 3,
                    'riskDirection': 'stable',
                    'defensibleSpace': 'good',
                    'usfsRelativeRisk': 'low',
                    'prescribedBurns': {'totalCount': 1},
                    'probability': {'burn': [{'emberZone': 1, 'percent': 0.2}]},
                    'historicConnection': {'edges': [{'node': {'eventId': '456', 'name': 'Fire 2021'}}]},
                    'insuranceHippo': {'rates': [{'minPrice': 150, 'maxPrice': 250}]},
                    'insights': [{'name': 'Insight 2', 'details': [{'name': 'Detail 2', 'value': 'Value 2'}]}]
                }
            }
        }
        result = self.api.parse_fire_data(mock_data)
        self.assertEqual(result['fire_factor'], 3)
        self.assertEqual(result['risk_direction'], 'stable')
        self.assertEqual(result['defensible_space'], 'good')
        self.assertEqual(result['usfs_relative_risk'], 'low')
        self.assertEqual(result['prescribed_burns_count'], 1)
        self.assertEqual(result['probability']['burn'][0]['emberZone'], 1)
        self.assertEqual(result['historic_events'][0]['eventId'], '456')
        self.assertEqual(result['insurance_quotes'][0]['minPrice'], 150)
        self.assertEqual(result['insights'][0]['name'], 'Insight 2')

    def test_parse_heat_data(self):
        mock_data = {
            'property': {
                'heat': {
                    'heatFactor': 4,
                    'hotTemperature': 95,
                    'anomalyTemperature': 5,
                    'temperatureAverageHigh': [{'relativeYear': 2020, 'mmt': 85}],
                    'cooling': [{'coolingTemp': 75, 'cost': 100}],
                    'heatWaves': {'hotHeatWave': [{'length': 3, 'probability': 0.7}]},
                    'days': {
                        'distribution': [{'relativeYear': 2020, 'binLower': 80, 'days': 30}],
                        'hotDays': [{'relativeYear': 2020, 'days': 20}],
                        'anomalyDays': [{'relativeYear': 2020, 'days': 10}],
                        'coolingDays': [{'relativeYear': 2020, 'days': 50}],
                        'dangerousDays': [{'relativeYear': 2020, 'days': 5}],
                        'healthCautionDays': [{'relativeYear': 2020, 'days': 15}]
                    },
                    'insights': [{'name': 'Insight 3', 'details': [{'name': 'Detail 3', 'value': 'Value 3'}]}]
                }
            }
        }
        result = self.api.parse_heat_data(mock_data)
        self.assertEqual(result['heat_factor'], 4)
        self.assertEqual(result['hot_temperature'], 95)
        self.assertEqual(result['anomaly_temperature'], 5)
        self.assertEqual(result['temperature_average_high'][0]['mmt'], 85)
        self.assertEqual(result['cooling'][0]['cost'], 100)
        self.assertEqual(result['heat_waves']['hotHeatWave'][0]['length'], 3)
        self.assertEqual(result['days']['distribution'][0]['days'], 30)
        self.assertEqual(result['insights'][0]['name'], 'Insight 3')

    def test_parse_wind_data(self):
        mock_data = {
            'property': {
                'wind': {
                    'windFactor': 2,
                    'factorScale': 'moderate',
                    'riskDirection': 'decreasing',
                    'hasTornadoRisk': True,
                    'hasThunderstormRisk': True,
                    'hasCycloneRisk': False,
                    'greatestWindRisk': 'tornado',
                    'missileEnvironment': 'moderate',
                    'primaryWindDirection': 'NW',
                    'probability': {
                        'speed': [{'maxSpeed': 100, 'maxGust': 120}],
                        'direction': [{'direction': 'NW', 'percent': 0.6}]
                    },
                    'historicConnection': {
                        'edges': [
                            {'node': {'eventId': '789', 'eventType': 'tornado', 'date': '2022-05-01'}}
                        ]
                    }
                }
            }
        }
        result = self.api.parse_wind_data(mock_data)
        self.assertEqual(result['wind_factor'], 2)
        self.assertEqual(result['factor_scale'], 'moderate')
        self.assertEqual(result['risk_direction'], 'decreasing')
        self.assertTrue(result['has_tornado_risk'])
        self.assertTrue(result['has_thunderstorm_risk'])
        self.assertFalse(result['has_cyclone_risk'])
        self.assertEqual(result['greatest_wind_risk'], 'tornado')
        self.assertEqual(result['missile_environment'], 'moderate')
        self.assertEqual(result['primary_wind_direction'], 'NW')
        self.assertEqual(result['probability']['speed'][0]['maxSpeed'], 100)
        self.assertEqual(result['historic_events'][0]['eventId'], '789')

    def test_parse_air_data(self):
        mock_data = {
            'property': {
                'air': {
                    'airFactor': 1,
                    'factorScale': 'low',
                    'riskDirection': 'stable',
                    'days': {'outdoorDays': [{'year': 2020, 'totalDays': 300}]},
                    'greatestRisk': {'name': 'Ozone', 'description': 'High ozone levels'},
                    'triNearby': 2,
                    'triFacilityConnection': {
                        'totalCount': 1,
                        'edges': [{'node': {'triFacilityId': '123', 'name': 'Facility A'}}]
                    },
                    'historic': {
                        'aqi': [{'year': 2020, 'aqiAvg': 50, 'aqiMax': 100}],
                        'days': [{'year': 2020, 'totalDays': 10}]
                    },
                    'insights': [{'name': 'Insight 4', 'details': [{'name': 'Detail 4', 'value': 'Value 4'}]}],
                    'percentile': {'national': 20, 'state': 30}
                }
            }
        }
        result = self.api.parse_air_data(mock_data)
        self.assertEqual(result['air_factor'], 1)
        self.assertEqual(result['factor_scale'], 'low')
        self.assertEqual(result['risk_direction'], 'stable')
        self.assertEqual(result['days']['outdoorDays'][0]['totalDays'], 300)
        self.assertEqual(result['greatest_risk']['name'], 'Ozone')
        self.assertEqual(result['tri_nearby'], 2)
        self.assertEqual(result['tri_facilities'][0]['triFacilityId'], '123')
        self.assertEqual(result['historic']['aqi'][0]['aqiAvg'], 50)
        self.assertEqual(result['insights'][0]['name'], 'Insight 4')
        self.assertEqual(result['percentile']['national'], 20)

    @patch.object(FirstStreetAPI, 'get_property_data')
    @patch.object(FirstStreetAPI, 'parse_flood_data')
    @patch.object(FirstStreetAPI, 'parse_fire_data')
    @patch.object(FirstStreetAPI, 'parse_heat_data')
    @patch.object(FirstStreetAPI, 'parse_wind_data')
    @patch.object(FirstStreetAPI, 'parse_air_data')
    def test_get_all_risk_data(self, mock_air, mock_wind, mock_heat, mock_fire, mock_flood, mock_get_property):
        mock_get_property.return_value = {'data': {'property': {}}}
        mock_flood.return_value = {'flood_factor': 5}
        mock_fire.return_value = {'fire_factor': 3}
        mock_heat.return_value = {'heat_factor': 4}
        mock_wind.return_value = {'wind_factor': 2}
        mock_air.return_value = {'air_factor': 1}

        result = self.api.get_all_risk_data(12345)

        self.assertEqual(result['flood']['flood_factor'], 5)
        self.assertEqual(result['fire']['fire_factor'], 3)
        self.assertEqual(result['heat']['heat_factor'], 4)
        self.assertEqual(result['wind']['wind_factor'], 2)
        self.assertEqual(result['air']['air_factor'], 1)

        mock_get_property.assert_called_once_with(12345, 0)
        mock_flood.assert_called_once()
        mock_fire.assert_called_once()
        mock_heat.assert_called_once()
        mock_wind.assert_called_once()
        mock_air.assert_called_once()

if __name__ == '__main__':
    unittest.main()
