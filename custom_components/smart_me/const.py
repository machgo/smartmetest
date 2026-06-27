DOMAIN = "smart_me"
API_BASE_URL = "https://api.smart-me.com/api"
DEFAULT_SCAN_INTERVAL = 60  # seconds

METER_ENERGY_TYPE_NAMES: dict[int, str] = {
    0: "Unknown",
    1: "Electricity",
    2: "Water",
    3: "Gas",
    4: "Heat",
    5: "HCA",
    6: "All Meters",
    7: "Temperature",
    8: "M-BUS Gateway",
    9: "RS-485 Gateway",
    10: "Custom Device",
    11: "Compressed Air",
    12: "Solar Log",
    13: "Virtual Meter",
    14: "Wireless M-BUS Gateway",
}
