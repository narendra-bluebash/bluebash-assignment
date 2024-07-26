import csv
import sys
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="bluebash_location")

def fetch_geo_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return location.latitude, location.longitude
    else:
        return None,None

def validate_row(row):
    required_fields = [row['Email'], row['First Name'], row['Last Name'],
                       row['Residential Address Street'], row['Residential Address Locality'],
                       row['Residential Address State'], row['Residential Address Postcode'],
                      row['Postal Address Street'], row['Postal Address Locality'],
                       row['Postal Address State'], row['Postal Address Postcode']]
    
    if not all(required_fields):
        return False
    else:
        return True

def process_csv(input_file, output_file):
    
    with open(input_file, mode='r') as infile, open(output_file, mode='w', newline='') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Residential_lat", "Residential_lng","Postal_lat","Postal_lng"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        c=0
        for row in reader:
            print(c)
            c=c+1
            if validate_row(row):
                res_address = f"{row['Residential Address Locality']}, {row['Residential Address State']} {row['Residential Address Postcode']}"
                res_lat, res_lng = fetch_geo_coordinates(res_address)
                    
                postal_address = f"{row['Postal Address Locality']}, {row['Postal Address State']} {row['Postal Address Postcode']}"
                postal_lat, postal_lng = fetch_geo_coordinates(postal_address)
                
                if res_lat and res_lng and postal_lat and postal_lng:
                    row['Residential_lat'] = res_lat
                    row['Residential_lng'] = res_lng
                    row['Postal_lat'] = postal_lat
                    row['Postal_lng'] = postal_lng
                    writer.writerow(row)


            
def main():
    if len(sys.argv) < 2 or sys.argv[1] == '--help':
        print("Usage: ./cli <input.csv> [> output.csv]")
        return
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    process_csv(input_file, output_file)

if __name__ == "__main__":
    main()