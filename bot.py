import requests
import json
import time, datetime
IFTTT_WEBHOOK_URL = 'https://maker.ifttt.com/trigger/zcash/with/key/jMso1_4RFIMv9tbr4bq4RDXnRCBhTb3aIn7Rg_mNxg2'
ZEC_API_URL = 'https://api.coinmarketcap.com/v1/ticker/zcash/'

def format_zcash_history(zcash_history):
    rows = []
    for zec_price in zcash_history:
        date = zec_price['date'].strftime('%d.%m.%Y %H:%M')
        price = zec_price['price']
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)
    return '<br>'.join(rows)

def get_last_zec_price():
    response = requests.get(ZEC_API_URL).json()
    return float(response[0].get('price_usd'))

def post_ifttt_webhook(event, value):
    data = {'value1': value}
    ifttt_event_url = IFTTT_WEBHOOK_URL.format(event)
    requests.post(ifttt_event_url, json=data)
    
def main():
    zcash_history = []
    while 1:
        price = get_last_zec_price()
        date = datetime.datetime.now()
        zcash_history.append({'date': date, 'price': price})

        if len(zcash_history) == 5:
            post_ifttt_webhook('zcash_price_uptade',
                               format_zcash_history(zcash_history))
            zcash_history = []
        time.sleep(3)

if __name__ == '__main__':
    main()

