import time
import requests
import logging

BASE_URL = "https://api.millnorwaycloud.com"
TOKEN_REFRESH_TIME = 540


class MillAPI:
    def __init__(self, email, password, access_token=None, refresh_token=None, token_expires=None):
        self.email = email
        self.password = password
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_expires = token_expires or 0

    def _is_token_expired(self):
        return not self.access_token or time.time() >= self.token_expires

    def authenticate(self):
        url = f"{BASE_URL}/customer/auth/sign-in"
        resp = requests.post(url, json={"login": self.email, "password": self.password})
        resp.raise_for_status()
        data = resp.json()
        self.access_token = data.get("idToken")
        self.refresh_token = data.get("refreshToken")
        self.token_expires = time.time() + TOKEN_REFRESH_TIME
        if not self.access_token:
            raise Exception("No idToken in response")
        return self.access_token

    def refresh(self):
        if not self.refresh_token:
            return self.authenticate()
        url = f"{BASE_URL}/customer/auth/refresh"
        resp = requests.post(url, json={"refreshToken": self.refresh_token})
        resp.raise_for_status()
        data = resp.json()
        self.access_token = data.get("idToken")
        self.token_expires = time.time() + TOKEN_REFRESH_TIME
        return self.access_token

    def get_access_token(self):
        if self._is_token_expired():
            try:
                return self.refresh()
            except Exception:
                return self.authenticate()
        return self.access_token

    def _headers(self):
        return {"Authorization": f"Bearer {self.get_access_token()}"}

    def get_houses(self):
        url = f"{BASE_URL}/houses"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        data = resp.json()  # <-- remove .get("body", {})
    
        houses = []
    
        for h in data.get("ownHouses", []):
            if isinstance(h, dict) and "id" in h:
                houses.append(h)
            elif isinstance(h, str):
                houses.append({"id": h, "name": "Unknown House"})
    
        for h in data.get("sharedHouses", []):
            inner = h.get("house") if isinstance(h, dict) else None
            if isinstance(inner, dict) and "id" in inner:
                houses.append(inner)
    
        
        return houses

        
    def get_rooms(self, house_id):
        url = f"{BASE_URL}/houses/{house_id}/rooms"
        resp = requests.get(url, headers=self._headers())
        resp.raise_for_status()
        data = resp.json()
        rooms = data.get("rooms", [])
        return data.get("rooms", [])

    def set_room_temperature(self, room_id, temperature):
        url = f"{BASE_URL}/rooms/{room_id}/temperature"
        payload = {
            "roomAwayTemperature": int(temperature),
            "roomComfortTemperature": int(temperature),
            "roomSleepTemperature": int(temperature),
        }
        resp = requests.post(
            url,
            headers={**self._headers(), "Content-Type": "application/json"},
            json=payload
        )
        resp.raise_for_status()
        return resp.json()
        
    def set_override_mode(self, room_id, mode = "comfort"):
        url = f"{BASE_URL}/rooms/{room_id}/mode/override"
        payload = {
            "overrideModeType": "continuous",  
            "overrideEndDate": 9999999999,  
            "mode": mode  
        }
        resp = requests.post(
            url,
            headers={**self._headers(), "Content-Type": "application/json"},
            json=payload
        )
        resp.raise_for_status()
        return resp.json()
        
