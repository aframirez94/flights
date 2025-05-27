import requests
import pytest

BASE_URL = "http://localhost:8000"

TEST_CASES = [
    # 1. Viaje directo válido (sin conexiones)
    {"date": "2024-09-12", "from": "BUE", "to": "MAD", "expected_connections": [0]},

    # 2. Viaje válido con 1 conexión
    {"date": "2024-09-12", "from": "BUE", "to": "PMI", "expected_connections": [1]},

    # 3. Ruta que excede 24h de duración → NO válido
    {"date": "2024-09-12", "from": "BUE", "to": "JFK", "expected_connections": []},

    # 4. Conexión mayor a 4 horas → NO válido
    {"date": "2024-09-12", "from": "MAD", "to": "PMI", "expected_connections": [1]},

    # 5. No hay vuelos en ese día
    {"date": "2024-09-11", "from": "BUE", "to": "MAD", "expected_connections": []},

    # 6. Conexión válida pero excede los 2 tramos → NO válido
    {"date": "2024-09-12", "from": "CDG", "to": "PMI", "expected_connections": []},

    # 7. Ruta sin conexión posible
    {"date": "2024-09-12", "from": "BOG", "to": "LAX", "expected_connections": []},
]


@pytest.mark.parametrize("case", TEST_CASES)
def test_journey_search(case):
    params = {
        "date": case["date"],
        "from_": case["from"],
        "to": case["to"]
    }
    response = requests.get(f"{BASE_URL}/journeys/search", params=params)
    
    assert response.status_code == 200, f"Expected 200 but got {response.status_code}"
    
    journeys = response.json()
    assert isinstance(journeys, list), "Response should be a list"

    actual_connections = [j["connections"] for j in journeys]
    
    # Ordenamos para comparar fácilmente
    assert sorted(actual_connections) == sorted(case["expected_connections"]), (
        f"\nInput: {params}"
        f"\nExpected: {case['expected_connections']}"
        f"\nActual: {actual_connections}"
    )
