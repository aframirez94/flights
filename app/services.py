import httpx
from app import mock_test_data

async def fetch_flight_events():
    url = "https://mock.apidog.com/m1/814105-793312-default/flight-events"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
    # return mock_test_data.MOCK_EVENTS # uncomment this line to run the tests