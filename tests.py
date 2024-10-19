from typing import Callable, List, Generic, Tuple

from regexHelper import getPrice, getRoomCount, getFloor

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
            ("🔹Price: 750$", 750),
            ("Price750$", 100),
            ("Price-1111$", 1111),
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
            ("• Комнаты:2", "2"),
            ("- 1 комнатная переделанная в 2 комнатную", "1"),
            ("Комнат-2", "2"),
            ("🏢2в3 - комнатная 77кв.м", "2в3"),
            ("Rooms: 2 - 55м²   +1", "2"),
            ("#3Хкомн  3/8/12", "3"),
            ("2/15/9", "2"),
            ("- комнатная переделанная в комнатную", None),
            ("Комнат-abc", None),
        ],
        lambda x: getRoomCount(x)
    ),
    (
        [
            ("🏢14-этаж", 14),
            ("💮Этаж-4", 4),
            ("🔸Этаж: 42", 42),
            ("2этаж", 2),
            ("99-этаж", 99),
            ("0: этаж", 0),
            ("🔹Floor: 2", 2),
            ("#3Хкомн  3/8/12", 8),
            ("2/1/12", 1),
            ("🔹Total floors:4 ", None),
            ("4-этажка", None),
            ("🏢9-этажное", None),
            ("9этажное", None),
            ("здание 9-этажей", None),
        ],
        lambda x: getFloor(x)
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
