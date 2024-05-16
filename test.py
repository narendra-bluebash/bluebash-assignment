import unittest
from unittest.mock import patch, MagicMock
from app import fetch_geo_coordinates, validate_row, process_csv

class TestGeoCoordinates(unittest.TestCase):
    
    @patch('app.geolocator.geocode')
    def test_fetch_geo_coordinates_valid(self, mock_geocode):
        mock_geocode.return_value = MagicMock(latitude=-20.272494	, longitude=148.718147)
        
        lat, lng = fetch_geo_coordinates("AIRLIE BEACH QLD 4802")
        self.assertEqual(lat, -20.272494)
        self.assertEqual(lng, 148.718147)

        
class TestValidateRow(unittest.TestCase):

    def test_validate_row_valid(self):
        row = {
            'Email': 'test@example.com', 
            'First Name': 'John', 
            'Last Name': 'Doe',
            'Residential Address Street': '123 Main St', 
            'Residential Address Locality': 'Springfield',
            'Residential Address State': 'IL', 
            'Residential Address Postcode': '62701',
            'Postal Address Street': '123 Main St', 
            'Postal Address Locality': 'Springfield',
            'Postal Address State': 'IL', 
            'Postal Address Postcode': '62701'
        }
        self.assertTrue(validate_row(row))
    
    def test_validate_row_invalid(self):
        row = {
            'Email': '', 
            'First Name': 'John', 
            'Last Name': 'Doe',
            'Residential Address Street': '123 Main St', 
            'Residential Address Locality': 'Springfield',
            'Residential Address State': 'IL', 
            'Residential Address Postcode': '62701',
            'Postal Address Street': '123 Main St', 
            'Postal Address Locality': 'Springfield',
            'Postal Address State': 'IL', 
            'Postal Address Postcode': '62701'
        }
        self.assertFalse(validate_row(row))


if __name__ == '__main__':
    unittest.main()