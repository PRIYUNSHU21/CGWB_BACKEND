# District coordinates for West Bengal (approximate centroids based on district headquarters)
# Source: Standard geographical data (lat, lon in degrees)

DISTRICT_COORDS = {
    "Alipurduar": (26.4837, 89.5330),
    "Bankura": (23.2324, 87.0714),
    "Birbhum": (23.8320, 87.5840),
    "Cooch Behar": (26.3240, 89.4510),
    "Dakshin Dinajpur": (25.4300, 88.3100),
    "Darjeeling": (27.0360, 88.2627),
    "Hooghly": (22.8960, 88.2460),
    "Howrah": (22.5958, 88.2636),
    "Jalpaiguri": (26.5435, 88.7205),
    "Jhargram": (22.4530, 86.9950),
    "Kalimpong": (27.0600, 88.4700),
    "Kolkata": (22.5726, 88.3639),
    "Malda": (25.0100, 88.1400),
    "Murshidabad": (24.1750, 88.2700),
    "Nadia": (23.4700, 88.5100),
    "North 24 Parganas": (22.4700, 88.4200),
    "Paschim Bardhaman": (23.2400, 87.8600),
    "Paschim Medinipur": (22.4200, 87.3200),
    "Purba Bardhaman": (23.2400, 87.8600),  # Note: Same as Paschim for approximation
    "Purba Medinipur": (22.4200, 87.3200),  # Note: Same as Paschim for approximation
    "Purulia": (23.3300, 86.3600),
    "South 24 Parganas": (22.1600, 88.4300),
    "Uttar Dinajpur": (25.9000, 88.1300)
}

# Function to get coordinates
def get_district_coords(district):
    return DISTRICT_COORDS.get(district, None)