from dotenv import load_dotenv
import os
import requests


# Get api key from the .env file
load_dotenv()
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise ValueError("API key not found.")

# Make request
def fetch_rate(base_currency, target_currency):
    URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{base_currency}"
    try:
        res = requests.get(URL)
        res.raise_for_status()
        data = res.json()

        # Extract the target currency's rate
        if data["result"] == "success" and data["conversion_rates"].get(target_currency):
            rate_obj = {
                "time": data["time_last_update_utc"],
                "rate": data["conversion_rates"][target_currency]
            }
            print(rate_obj)
            return rate_obj
        else:
            raise ValueError(f"Currency {target_currency} not found.")
    except requests.RequestException as e:
        print(f"Error fetching data: {e}.")
        return None