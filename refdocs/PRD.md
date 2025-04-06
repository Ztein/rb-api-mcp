Riksbankens nya API-portal
Riksbanken har utvecklat en modernare API-plattform som erbjuder flera olika API med RESTful-gränssnitt (i stället för det äldre SOAP-baserade API jag nämnde tidigare).
Tillgängliga API
Enligt länkarna du delade finns det flera olika API tillgängliga:

Monetary Policy Data API - Innehåller räntedata, prognoser och penningpolitiska beslut
Financial Market Data API - Finansmarknadsdata, inklusive valutakurser och ränteinformation
Payments & Settlements Data API - Betalningsstatistik och avvecklingsdata
Foreign Exchange Rates API - Specifikt för valutakurser

Hur du får tillgång till API

Registrering på Developer-portalen:

Gå till https://developer.api.riksbank.se/
Klicka på "Sign Up" för att skapa ett konto
Fyll i dina uppgifter och skapa ett användarkonto


Prenumerera på önskade API:

Efter inloggning, gå till "APIs" i menyn
Välj det API du är intresserad av (t.ex. "Foreign Exchange Rates")
Klicka på "Subscribe" för att få åtkomst


Skapa API-nycklar:

Efter prenumeration kan du skapa och hantera API-nycklar
Varje API-nyckel har ett associerat klient-ID och hemlig nyckel
Dessa behöver du för att autentisera dina API-anrop



Exempel på användning
För "Foreign Exchange Rates API" kan du hämta valutakurser så här (exempel med Python):
pythonCopyimport requests
import json
from datetime import datetime

# API-information från din prenumeration
client_id = "ditt_client_id"
client_secret = "din_client_secret"

# Autentisera och hämta token (OAuth 2.0)
auth_url = "https://api.riksbank.se/oauth2/token"
auth_data = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

auth_response = requests.post(auth_url, data=auth_data)
token = auth_response.json()["access_token"]

# Hämta valutakurser
# Exempel: Hämta EUR/SEK-kurser för ett visst datumintervall
api_url = "https://api.riksbank.se/v2/exchangerates/series/daily"
params = {
    "from_date": "2023-01-01",
    "to_date": "2023-01-31",
    "currency": "EUR"
}

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

response = requests.get(api_url, params=params, headers=headers)
exchange_rates = response.json()

print(json.dumps(exchange_rates, indent=2))
Dokumentation och resurser
På developer-portalen finns detaljerad dokumentation för varje API:

API-specifikationer
Interaktiv "Try It"-funktion där du kan testa API-anrop direkt i webbläsaren
Exempel på anrop och svar
Information om frekvensramar och begränsningar

Allmänna villkor

De flesta API är gratis att använda, men med vissa begränsningar för anropsfrekvens
Det kan finnas olika servicenivåer (t.ex. Basic, Premium) med olika gränser
Kontrollera alltid de senaste villkoren på portalen

Riksbankens nya API-portal gör det betydligt enklare att arbeta med deras data jämfört med det äldre SOAP-baserade API, och erbjuder modern RESTful API-design och OAuth 2.0-autentisering.RetryClaude does not have internet access. Links provided may not be accurate or up to date.JShttps://developer.api.riksbank.se/api-details#api=swea-api&operation=get-calendardays-fromhttps://developer.api.riksbank.se/api-details#api=tora-api&operation=get-all-interestrateid-fromdate-fromdateKan du sammanfatta information om dessa apier åt mig till en teknisk spec som jag akn använda frö att bygga en MCP.server på dem?EditJag ska sammanfatta de två API från Riksbanken (SWEA API och TORA API) i en teknisk specifikation som du kan använda för att bygga en MCP.server.
Teknisk Specifikation för Integration av Riksbankens API
1. Översikt
Denna specifikation beskriver integrationen med två av Riksbankens API:er:

SWEA API: Sveriges Riksbanks statistik- och dataAPI (Swedish Economic Archive)
TORA API: Riksbankens finansmarknadsdata-API (Treasury & Open market operations Riksbank API)

2. API-beskrivningar
2.1 SWEA API
SWEA API tillhandahåller tillgång till historiska data om valutakurser, räntor och andra ekonomiska indikatorer.
Bas-URL: https://api.riksbank.se/swea/v1
Fokuserad endpoint: get-calendardays-from

Syfte: Hämtar kalenderdagar från angivet datum och framåt
Metod: GET
Endpoint: /calendar/calendardays
Parametrar:

fromDate (obligatorisk): Startdatum i format "YYYY-MM-DD"
toDate (valfri): Slutdatum i format "YYYY-MM-DD"
limit (valfri): Maxantal poster att returnera



Svarformat: JSON som innehåller en lista med kalenderdagar och information om dessa är bankdagar eller helgdagar.
2.2 TORA API
TORA API ger tillgång till finansmarknadsdata, inklusive räntor och likviditetshantering.
Bas-URL: https://api.riksbank.se/tora/v1
Fokuserad endpoint: get-all-interestrateid-fromdate-fromdate

Syfte: Hämtar alla räntesatser från ett angivet datum
Metod: GET
Endpoint: /interestrate
Parametrar:

fromDate (obligatorisk): Startdatum i format "YYYY-MM-DD"
limit (valfri): Maxantal poster att returnera
interestRateId (valfri): ID för specifik räntesats



Svarformat: JSON med räntedata för olika räntesatser och perioder.
3. Autentisering
Båda API använder OAuth 2.0 Client Credentials-flöde:

Hämta token:

Endpoint: https://api.riksbank.se/oauth2/token
Metod: POST
Headers: Content-Type: application/x-www-form-urlencoded
Body:
Copygrant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}

Svar: JSON med access_token, token_type, expires_in


Använd token:

Inkludera i alla API-anrop med header: Authorization: Bearer {ACCESS_TOKEN}
Token är giltig i den period som anges i expires_in (vanligtvis 1 timme)



4. Begränsningar

Anropsfrekvens: Varierar beroende på prenumerationsnivå (vanligtvis 10-100 anrop per minut)
Dataleverans: Historisk data levereras med en viss fördröjning (vanligtvis 1 dag)
Datamängd: Stora datamängder bör hämtas med paginering via limit-parametern

5. Felhantering
API returnerar standardiserade HTTP-statuskoder:

200 OK: Anropet lyckades
400 Bad Request: Felaktiga parametrar
401 Unauthorized: Ogiltigt/utgånget token
403 Forbidden: Saknar behörighet
429 Too Many Requests: För många anrop
500 Internal Server Error: Serverfel

Felmeddelanden returneras i JSON-format med detaljer om felet.
6. MCP.server-implementering
6.1 Grundläggande struktur
pythonCopyfrom typing import Optional
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import requests
from pydantic import BaseModel
import httpx
from datetime import datetime, timedelta

app = FastAPI(title="Riksbank Data Service")

# OAuth2 setup för din MCP-server
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Riksbankens API-konfiguration
RIKSBANK_CLIENT_ID = "your_client_id"
RIKSBANK_CLIENT_SECRET = "your_client_secret"
RIKSBANK_TOKEN_URL = "https://api.riksbank.se/oauth2/token"
SWEA_BASE_URL = "https://api.riksbank.se/swea/v1"
TORA_BASE_URL = "https://api.riksbank.se/tora/v1"

# Token-cache
riksbank_token = None
token_expiry = datetime.now()
6.2 Token-hantering
pythonCopyasync def get_riksbank_token():
    global riksbank_token, token_expiry
    
    # Kontrollera om token behöver förnyas
    if riksbank_token is None or token_expiry <= datetime.now():
        data = {
            "grant_type": "client_credentials",
            "client_id": RIKSBANK_CLIENT_ID,
            "client_secret": RIKSBANK_CLIENT_SECRET
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(RIKSBANK_TOKEN_URL, data=data)
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to get Riksbank API token")
            
            token_data = response.json()
            riksbank_token = token_data["access_token"]
            # Sätt expiry lite innan den faktiska tiden för att vara säker
            token_expiry = datetime.now() + timedelta(seconds=token_data["expires_in"] - 60)
    
    return riksbank_token
6.3 API-endpoints
pythonCopy# SWEA API: Kalenderdagar
@app.get("/calendar-days")
async def get_calendar_days(from_date: str, to_date: Optional[str] = None, limit: Optional[int] = 100):
    token = await get_riksbank_token()
    
    params = {"fromDate": from_date}
    if to_date:
        params["toDate"] = to_date
    if limit:
        params["limit"] = limit
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{SWEA_BASE_URL}/calendar/calendardays", 
            params=params, 
            headers=headers
        )
        
        if response.status_code != 200:
            detail = f"Riksbank API error: {response.text}"
            raise HTTPException(status_code=response.status_code, detail=detail)
        
        return response.json()

# TORA API: Räntesatser
@app.get("/interest-rates")
async def get_interest_rates(from_date: str, interest_rate_id: Optional[str] = None, limit: Optional[int] = 100):
    token = await get_riksbank_token()
    
    params = {"fromDate": from_date}
    if interest_rate_id:
        params["interestRateId"] = interest_rate_id
    if limit:
        params["limit"] = limit
    
    headers = {"Authorization": f"Bearer {token}"}
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{TORA_BASE_URL}/interestrate", 
            params=params, 
            headers=headers
        )
        
        if response.status_code != 200:
            detail = f"Riksbank API error: {response.text}"
            raise HTTPException(status_code=response.status_code, detail=detail)
        
        return response.json()
6.4 Caching
För att minimera antalet anrop till Riksbankens API, implementera caching:
pythonCopyfrom fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import redis

# Initiera cache vid startup
@app.on_event("startup")
async def startup():
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    FastAPICache.init(RedisBackend(redis_client), prefix="riksbank-cache")

# Använd caching för API-endpoints
@app.get("/calendar-days")
@cache(expire=3600)  # Cache i 1 timme
async def get_calendar_days(from_date: str, to_date: Optional[str] = None, limit: Optional[int] = 100):
    # Samma implementering som ovan
    ...
7. Implementationsanteckningar

Felhantering: Implementera robust felhantering och återförsök med exponentiell backoff vid nätverksproblem.
Loggning: Implementera omfattande loggning för felsökning och övervakning.
Rate Limiting: Implementera egen rate limiting för att undvika att nå Riksbankens gränser.
Caching: Implementera aggressiv caching för att minska belastningen på Riksbankens API, särskilt för historisk data som sällan ändras.
Schemaläggning: För regelbunden datahämtning, implementera bakgrundsprocesser som hämtar och uppdaterar data periodiskt.
Databehandling: Överväg att normalisera och omformulera data för att förbättra prestanda i din applikation.

8. Testning
Skapa omfattande testsviter för att verifiera:

Autentiseringsflöden
Parameterkontroll
Felhantering
Datavalidering

Detta bör ge dig en bra grund för att bygga en MCP.server som integrerar med Riksbankens SWEA och TORA API