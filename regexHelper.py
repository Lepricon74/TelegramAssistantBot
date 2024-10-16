import re
import logging

def getPrice(input: str) -> int | None:
    priceStr = getValueByKeyWord(input, r'([Ц,ц]ена)|(у.е)|(\$)', r'(\d{3,4})')
    if (priceStr):
        try:
            price = int(priceStr)
            return price
        except Exception:
            logging.error(f"Fail to int parse {priceStr} in string {input}")
    return None

def getRoomCount(input: str) -> str | None:
    return getValueByKeyWord(input, r'[К,к]омнат', r'(\dв\d)|(\d){1,1}')

def getFloor(input: str) -> int | None:
    isTotal = re.search(r'([Э,э]тажн)|([Э,э]тажка)|([Э,э]тажей)', input)
    if(isTotal): return None
    floorStr = getValueByKeyWord(input, r'([Э,э]таж)', r'(\d{1,2})')
    if (floorStr):
        try:
            floor = int(floorStr)
            return floor
        except Exception:
            logging.error(f"Fail to int parse {floor} in string {input}")
    return None

def getValueByKeyWord(input: str, keyWordSearcExpr: str, valueSearchExpr: str) -> int | str | None:
    hasPriceKeyWord = re.search(keyWordSearcExpr, input)
    if (hasPriceKeyWord):
        priceStrMatch = re.search(valueSearchExpr, input)
        if (priceStrMatch):
            return priceStrMatch[0]
    return None
