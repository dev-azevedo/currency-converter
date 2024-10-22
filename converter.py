from os import getenv
import requests
import aiohttp
from fastapi import HTTPException

ALPHAVANTAGE_APIKEY = getenv('ALPHAVANTAGE_APIKEY')


def sync_converter(from_currency: str, to_currency: str, price: float):
    # url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}'
    url = f'https://economia.awesomeapi.com.br/last/{from_currency}-{to_currency}'
    compare_currency = f'{from_currency}{to_currency}'

    try:
        response = requests.get(url)
    except Exception as error:
        raise HTTPException(status_code=400, detail=f'Error: {error}')
    
    data = response.json()
    if compare_currency not in data:
        raise HTTPException(status_code=400, detail=f'Realtime Currency Exchange Rate not in response')
    
    exchange_rate = float(data[compare_currency]['low'])

    return price * exchange_rate


async def async_converter(from_currency: str, to_currency: str, price: float):
    # url = f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency={from_currency}&to_currency={to_currency}&apikey={ALPHAVANTAGE_APIKEY}'
    url = f'https://economia.awesomeapi.com.br/last/{from_currency}-{to_currency}'
    compare_currency = f'{from_currency}{to_currency}'

    try:
        async with aiohttp.ClientSession() as session:
           async with session.get(url=url) as response:
               data = await response.json()
    except Exception as error:
        raise HTTPException(status_code=400, detail=f'Error: {error}')
    
    if compare_currency not in data:
        raise HTTPException(status_code=400, detail=f'Realtime Currency Exchange Rate not in response')
    
    exchange_rate = float(data[compare_currency]['low'])

    return {to_currency: price * exchange_rate}


