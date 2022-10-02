import json
import requests
from config import exchanges


class APIException(Exception):
    pass


class Convertor:
    @staticmethod
    def get_price(base, sym, amount):

        try:
            base_key = exchanges[base.lower()]
        except KeyError:
            raise APIException(f"Валюта {base} не найдена!")

        try:
            sym_key = exchanges[sym.lower()]
        except KeyError:
            raise APIException(f"Валюта {sym} не найдена!")

        if base_key == sym_key:
            message = f"Цена {amount} {base} в {sym} : 1.0"
            return message

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не корректный ввод количества волюты {amount}!')

        headers = {"apikey": "rLmbjAtc6j7CPZDXnRlbwCLXbA0fhM8v"}
        r = requests.get(f"https://api.apilayer.com/fixer/convert?to={sym_key}&from={base_key}&amount={amount}", headers )
        resp = json.loads(r.content)
        new_price = str(resp['result'])
        message = f"Цена {amount} {base} в {sym} : {new_price}"
        return message