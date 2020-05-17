from datetime import datetime

records = [
    {'source': '48-996355555', 'destination': '48-666666666', 'end': 1564610974, 'start': 1564610674},
    {'source': '41-885633788', 'destination': '41-886383097', 'end': 1564506121, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-886383097', 'end': 1564630198, 'start': 1564629838},
    {'source': '48-999999999', 'destination': '41-885633788', 'end': 1564697158, 'start': 1564696258},
    {'source': '41-833333333', 'destination': '41-885633788', 'end': 1564707276, 'start': 1564704317},
    {'source': '41-886383097', 'destination': '48-996384099', 'end': 1564505621, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '48-996383697', 'end': 1564505721, 'start': 1564504821},
    {'source': '41-885633788', 'destination': '48-996384099', 'end': 1564505721, 'start': 1564504821},
    {'source': '48-996355555', 'destination': '48-996383697', 'end': 1564505821, 'start': 1564504821},
    {'source': '48-999999999', 'destination': '41-886383097', 'end': 1564610750, 'start': 1564610150},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564505021, 'start': 1564504821},
    {'source': '48-996383697', 'destination': '41-885633788', 'end': 1564627800, 'start': 1564626000}
]
FIXED_PRICE = 0.36
VAR_PRICE_DAY_TIME = 0.09
START_DAY = 6
END_DAY = 22
MINUTE = 60

def cost_call(end_call, start_call):
    '''função que calcula o custo da chamada de acordo com o periodo'''

    start_diurn_call = START_DAY<=datetime.fromtimestamp(start_call).hour<=END_DAY
    end_diurn_call = START_DAY<=datetime.fromtimestamp(end_call).hour<=END_DAY

    if start_diurn_call and end_diurn_call:
        return 0.36+VAR_PRICE_DAY_TIME*int((end_call-start_call)/MINUTE)
    elif start_diurn_call:
        endday = datetime.timestamp(datetime(datetime.fromtimestamp(start_call).year,
                     datetime.fromtimestamp(start_call).month,
                     datetime.fromtimestamp(start_call).day,END_DAY, 00, 00))
        return 0.36+VAR_PRICE_DAY_TIME*int((endday-start_call)/MINUTE)
    elif end_diurn_call:
        startday = datetime.timestamp(datetime(datetime.fromtimestamp(end_call).year,datetime.fromtimestamp(end_call).month,
                     datetime.fromtimestamp(end_call).day, START_DAY, 00,00))
        return 0.36 + VAR_PRICE_DAY_TIME * int((end_call-startday) / MINUTE), 2
    else:
        return 0.36


def classify_by_phone_number(records):
    '''Retorna uma lista contendo cujo os itens são dicionários contendo a fonte da chamada com o
    valor total de todas as chamadas ordenado por valor'''

    total = []

    for record in records:
        newreg = True
        for reg in total:
            if record['source'] is reg['source']:
                reg['total'] += cost_call(record['end'], record['start'])
                newreg = False
                reg['total'] = round(reg['total'], 2)
                break

        if newreg:
            total.append({'source': record['source'], 'total': cost_call(record['end'], record['start'])})
        total[-1]['total'] = round(total[-1]['total'], 2)

    return sorted(total, key=lambda k: k['total'], reverse=True)



