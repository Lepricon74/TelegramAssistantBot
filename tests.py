from typing import Callable, List, Generic, Tuple

from regexHelper import getPrice, getRoomCount

testCases: List[Tuple[List[Tuple[str, int | str]], Callable[[str], None | int | str]]] = [
    (
        [
            ("- 3 комнатная, 4 этаж, 4 этажный дом, хороший ремонт, мебель и техника, интернет, цена: 400$", 400),
            ("💰Цена - 800 $", 800),
            ("Цена: 800$", 800),
            ("Цена - 650$", 650),
            ("🔹Цена - 900$", 900),
            ("1500$", 1500),
            ("Цена $1500", 1500),
            ("Цена $   1500", 1500),
            ("💰Цена - 800", 800),
            ("Цена: 800", 800),
            ("Цена - 650", 650),
            ("🔹Цена - 900", 900),
            ("Цена1500", 1500),
            ("💰Цена - 800", 800),
            ("800  Цена:", 800),
            ("Цена - 650   - Цена", 650),
            ("🔹Цена - 900", 900),
            ("Цена   1500", 1500),
            ("Цена:", None),
            ("650", None),
            ("- 3 комнатная, 4 этаж, 4 этажный дом, хороший ремонт, мебель и техника, интернет, цена:", None),
            ("", None),
        ],
        lambda x: getPrice(x)
    ),
    (
        [
            ("Комнат - 2", "2"),
            ("Комнат - 1-2", "1"),
            ("- 1 комнатная переделанная в 2 комнатную", "1"),
            ("Комнат-2", "2"),
            ("🏢2в3 - комнатная 77кв.м", "2в3"),
            ("- комнатная переделанная в комнатную", None),
            ("Комнат-abc", None),
        ],
        lambda x: getRoomCount(x)
    )
]

def main():
    for (testCaseSet, funcToCall) in testCases:
        for (inputValue, expectedValue) in testCaseSet:
            result = funcToCall(inputValue)
            if (result == expectedValue):
                print(f"Passed: {inputValue}")
            else:
                print(f"Failed: {inputValue} Expected: {expectedValue} Actual: {result}")
        print("-------------")


main()
