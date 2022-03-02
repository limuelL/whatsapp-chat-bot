from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()
crypto_list = cg.get_coins_list()


def count_characters(words):
    count = 0
    for ch in words:
        if ch == ' ':
            continue
        count += 1
    return count


def get_crypto_info(value):

    for crypto in crypto_list:
        if crypto['id'].lower() == value.lower():
            return crypto['id'], crypto['name'], crypto['symbol']
        if crypto['symbol'].lower() == value.lower():
            return crypto['id'], crypto['name'], crypto['symbol']
        if crypto['name'].lower() == value.lower():
            return crypto['id'], crypto['name'], crypto['symbol']


def similarity_values(occur_val):
    same_values = {}
    for crypto in crypto_list:
        if crypto['symbol'].lower() == occur_val.lower():
            same_values[crypto['name']] = crypto['symbol'].upper()
        elif occur_val.lower() == crypto['name'].lower():
            same_values[crypto['name']] = crypto['symbol'].upper()

    if len(same_values) != 0:
        return same_values
    else:
        return len(same_values)


def identify_similar_coin_name(occur_val):
    similar_names = {}
    for crypto in crypto_list:
        if occur_val.lower() in crypto['name'].lower():
            similar_names[crypto['name']] = crypto['symbol'].upper()
    return similar_names


def get_price(message):
    if cg.ping()['gecko_says'] == '(V3) To the Moon!':
        try:
            if len(similarity_values(message)) == 1:
                (coin_id, coin_name, coin_symbol) = get_crypto_info(message)

                info = cg.get_price(ids=coin_id, vs_currencies='usd', include_market_cap='true',
                                    include_24hr_vol='true', include_24hr_change='true',
                                    include_last_updated_at='true')[f"{coin_id}"]

                if info['usd'] < 0.0000001:
                    price_usd = f"$ {'{:,.12f}'.format(info['usd'])}"
                else:
                    price_usd = f"$ {'{:,.8f}'.format(info['usd'])}"
                market_cap = f"$ {'{:,.2f}'.format(info['usd_market_cap'])}"
                trading_volume = f"$ {'{:,.2f}'.format(info['usd_24h_vol'])}"
                percent_change = f"{'{:.2f}'.format(info['usd_24h_change'])}%"

                if market_cap == '$ 0.00':
                    market_cap = '(unable to display)'

                to_be_send = f"Coin/Token Name : {coin_name}\n" \
                    f"Symbol : {coin_symbol.upper()}\n" \
                    f"Price (USD) : {price_usd}\n" \
                    f"Market Cap : {market_cap}\n" \
                    f"Trading Volume : {trading_volume}\n" \
                    f"24Hour Percent Change : {percent_change}"

                return to_be_send

            else:
                res_msg = f"One or more similar coin/token exist. Do you mean any of this:" \
                    f"\n[COIN NAME : SYMBOL]\n"
                similar_symbol_list = similarity_values(message)
                for smbl in similar_symbol_list:
                    res_msg += f'{smbl} : {similar_symbol_list.get(smbl)}\n'
                return res_msg + '\nPlease use the exact COIN NAME or SYMBOL, with no similarities.'

        except TypeError:
            res_msg1 = 'Not Found! List of all similar coins:\nCOIN NAME : SYMBOL\n'
            similar_coins_list = identify_similar_coin_name(message)
            for coin in similar_coins_list:
                res_msg1 += f'{coin} : {similar_coins_list.get(coin)}\n'
            total_msg = res_msg1 + '\nPlease use the exact COIN NAME or SYMBOL.'

            if count_characters(total_msg) > 1500:
                return 'Invalid! Please make sure your sending a valid Coin/Token Name or Symbol.'

            else:
                return total_msg
    else:
        return "Coingecko server is down. Try again later!"
