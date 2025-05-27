# Flight Journey Search API

Este proyecto implementa una API REST en FastAPI para buscar viajes (vuelos directos o con una conexión) entre dos ciudades, a partir de eventos de vuelo obtenidos desde un servicio mock.

## Características

- Permite buscar viajes desde un origen a un destino en una fecha específica.
- Soporta vuelos con 0 o 1 conexión.
- La duración total del viaje no puede superar las 24 horas.
- La espera entre conexiones no puede exceder las 4 horas.
- Consulta datos en tiempo real desde un servicio externo (mock).

---

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd <nombre-del-proyecto>
```

### 2. Crear un entorno virtual (opcional si no usas Docker)
```bash
python -m .venv venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
```

### 3. Instalar dependencias (opcional si no usas Docker)
```bash
pip install -r requirements.txt
```

---

## Ejecución local

```bash
uvicorn main:app --reload
# fastapi dev main.py
```

La API estará disponible en: [http://localhost:8000](http://localhost:8000)

---

## Ejecución con Docker

### Requisitos
- Docker
- Docker Compose

### Pasos

1. Construir e iniciar los contenedores:

```bash
docker-compose up --build
```

2. Acceder a la API en:

[http://localhost:8000/journeys/search](http://localhost:8000/journeys/search)

---

## Uso del endpoint

### `GET /journeys/search`

**Parámetros de consulta:**

- `date`: Fecha del viaje (formato `YYYY-MM-DD`)
- `from`: Código de ciudad de origen (3 letras)
- `to`: Código de ciudad de destino (3 letras)

**Ejemplo:**
```bash
curl "http://localhost:8000/journeys/search?date=2024-09-12&from=BUE&to=MAD"
```

**Respuesta:**
```json
[
  {
    "connections": 0,
    "path": [
      {
        "flight_number": "XX1234",
        "from": "BUE",
        "to": "MAD",
        "departure_time": "2024-09-12 12:00",
        "arrival_time": "2024-09-13 00:00"
      }
    ]
  }
]
```

---

## Notas técnicas

- Las fechas y horas se manejan en UTC.
- La API externa utilizada es un mock proporcionado por Apidog:
  https://mock.apidog.com/m1/814105-793312-default/flight-events

---

## Requisitos

- Python 3.8+ (solo si ejecutas sin Docker)
- FastAPI
- Uvicorn
- httpx

---

## Licencia

Este proyecto es solo para fines de evaluación técnica.
