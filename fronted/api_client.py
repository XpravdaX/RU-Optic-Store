import requests
import json
from typing import List, Dict, Optional


class OpticStoreAPI:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url

    def get_products(self, **filters) -> List[Dict]:
        try:
            response = requests.get(
                f"{self.base_url}/api/products",
                params=filters,
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API Error: {e}")
            return []

    def get_product(self, product_id: int) -> Optional[Dict]:
        try:
            response = requests.get(
                f"{self.base_url}/api/products/{product_id}",
                timeout=5
            )
            response.raise_for_status()
            return response.json()
        except:
            return None

    def get_categories(self) -> List[str]:
        try:
            response = requests.get(f"{self.base_url}/api/categories")
            return response.json()
        except:
            return []

    def get_brands(self) -> List[str]:
        try:
            response = requests.get(f"{self.base_url}/api/brands")
            return response.json()
        except:
            return []

    def create_order(self, order_data: Dict) -> Dict:
        try:
            response = requests.post(
                f"{self.base_url}/api/orders",
                json=order_data,
                headers={"Content-Type": "application/json"}
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def check_connection(self) -> bool:
        try:
            response = requests.get(self.base_url, timeout=3)
            return response.status_code == 200
        except:
            return False