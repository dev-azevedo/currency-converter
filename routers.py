from fastapi import APIRouter, Path, Query
from converter import sync_converter, async_converter
from asyncio import gather
from schemas import ConverterInput, ConverterOutput

router = APIRouter()
router.prefix = "/api/converter"



@router.get("/{from_currency}")
def sync_converter_router(
    from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'), 
    to_currencies: str = Query(max_length=30, regex='^[A-Z]{3}(,[A-Z]{3})*$'), 
    price: float = Query(gt=0)
    ):
    
    to_currencies = to_currencies.split(',')

    result = []
    for currency in to_currencies:
        response = sync_converter(from_currency=from_currency, to_currency=currency, price=price)
        result.append(response)

    return result

@router.get("/async/{from_currency}")
async def async_converter_router(    
    from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'), 
    to_currencies: str = Query(max_length=30, regex='^[A-Z]{3}(,[A-Z]{3})*$'), 
    price: float = Query(gt=0)
    ):

    to_currencies = to_currencies.split(',')

    couroutines = []
    for currency in to_currencies:
        coro = async_converter(from_currency=from_currency, to_currency=currency, price=price)
        couroutines.append(coro)


    results = await gather(*couroutines)
    return results

@router.post("/async/v2/{from_currency}", response_model=ConverterOutput)
async def async_converter_router(    
    body: ConverterInput,
    from_currency: str = Path(max_length=3, regex='^[A-Z]{3}$'), 
    ):

    to_currencies = body.to_currencies
    price = body.price

    couroutines = []
    for currency in to_currencies:
        coro = async_converter(from_currency=from_currency, to_currency=currency, price=price)
        couroutines.append(coro)


    results = await gather(*couroutines)
    return ConverterOutput(
        message="Success",
        data=results
    )