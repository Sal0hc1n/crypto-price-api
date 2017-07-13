#!/usr/bin/env python

from telegram import InlineQueryResultArticle,InputTextMessageContent
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler
from uuid import uuid4
import logging
import exchanges
import requests
import math

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOTNAME = '@BotName_Bot'
TOKEN = 'TOKEN'
CL_API_KEY = 'CLAPIKEY'

millnames = ['',' k',' mio',' bio',' trillion']

def millify(n):
    n = float(n)
    millidx = max(0,min(len(millnames)-1, int(math.floor(0 if n == 0 else math.log10(abs(n))/3))))
    return '{:.1f}{}'.format(n / 10**(3 * millidx), millnames[millidx])

def startMsg(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Type /list to get a list of supported exchanges and underlyings.\nType /price <underlying> <exchange> to retrieve a price.\nFor example /price btcusd kraken")

def unknownMsg(bot, update):
    logger.info("Received unknown command from %s: %s" % (update.effective_user, update.message.text))
    bot.send_message(chat_id=update.message.chat_id, text="Sorry, try /start again?")

def listExchangesMsg(bot, update):
    logger.info("Received /list command from %s" % update.effective_user)
    update.message.reply_text(list_text())

def list_text():
    exchange_text = 'List of supported exchanges:\n'+'\n'.join(sorted(exchanges.exchange_list.keys()))
    underlyings_text = 'List of available underlyings:\n'+'\n'.join(sorted(exchanges.get_underlyings_list()))
    end_text = 'Try /exchange <exchange> to price all underlyings availablle on an exchange'
    return exchange_text + '\n\n' + underlyings_text + '\n\n' + end_text

def summaryMsg(bot, update):
    logger.info("Received /summary command from %s" % update.effective_user)
    logger.info("Command content: %s" % update.message.text)
    if update.message.text.split().__len__() < 1:
        ccy = ['BTC']
    else:
        ccy = update.message.text.split()[1:]
    update.message.reply_text('\n'.join(summary(ccy)))

def summary(ccy_list):
    mapping = {
        'btc' : 'bitcoin',
        'eth' : 'ethereum',
        'snt' : 'status',
        'xrp' : 'ripple',
        'xmr' : 'monero',
        'gno' : 'gnosis-gno',
        'gnosis' : 'gnosis-gno'
    }
    results = []
    for ccy in ccy_list:
        ccy = ccy.lower()
        if ccy in mapping.keys():
            ccy = mapping[ccy]
        try:
            r = requests.get('https://api.coinmarketcap.com/v1/ticker/%s' % ccy)
            r.raise_for_status()
            j = r.json()
        except requests.exceptions.RequestException as err:
            print(err)
            results.append("Something went wrong for currency %s" % ccy)
            results.append('')
            continue
        name = j[0]['name']
        price_usd = j[0]['price_usd']
        price_btc = j[0]['price_btc']
        vol_usd = millify(j[0]['24h_volume_usd'])
        mktcap_usd = millify(j[0]['market_cap_usd'])
        rank = int(j[0]['rank'])
        pchg_1h = j[0]['percent_change_1h']
        pchg_24h = j[0]['percent_change_24h']
        pchg_7d = j[0]['percent_change_7d']
        results.append('%s: %s (USD), %s (BTC). Changes: %s%% (1h), %s%% (24h), %s%% (7d).' % (name, price_usd, price_btc, pchg_1h, pchg_24h, pchg_7d))
        if str(rank)[-1:] == '1' and str(rank)[-2:] != '11':
            suffix = 'st'
        elif str(rank)[-1:] == '2' and str(rank)[-2:] != '12':
            suffix = 'nd'
        elif str(rank)[-1:] == '3' and str(rank)[-2:] != '13':
            suffix = 'rd'
        else:
            suffix = 'th'
        results.append('%s: Volumes in past 24h: %s USD. Market cap: %s USD. %s%s market cap.' % (name, vol_usd, mktcap_usd, rank, suffix))
        results.append('')
    return results

def exchangeMsg(bot, update):
    logger.info("Received /exchange command from %s" % update.effective_user)
    logger.info("Command content: %s" % update.message.text)
    if update.message.text.split().__len__() <= 1:
        update.message.reply_text('Syntax is "/exchange <exchange1> <exchange2> <...>".\nTry "/exchange all" to price all underlying on all supported exchanges (can take a while).\nType /list to see supported exchanges')
        return
    exchange_list = update.message.text.split()[1:]
    if exchange_list == ['all']:
        exchange_list = exchanges.get_exchanges_list()
    update.message.reply_text('\n'.join(exchange(exchange_list)))

def exchange(exchange_list):
    results = []
    for en in exchange_list:
        try:
            e = exchanges.get_exchange(en.lower())
        except:
            results.append("Uknown exchange %s" % en)
            continue
        results.append("%s:\n" % en)
        for ul in e.get_supported_underlyings():
            bid = e.get_quote(ul,'bid')
            ask = e.get_quote(ul,'ask')
            last = e.get_quote(ul,'last')
            if bid == 0 or ask == 0:
                spread = 1
            else:
                spread = (ask - bid) / ((ask+bid)/2)
            if last > 1:
                results.append("%s: Last trade %.2f. Market %.2f/ %.2f (%.1f%% wide)" % (ul,last, bid, ask, spread * 100))
            else:
                results.append("%s: Last trade %.3g. Market %.3g / %.3g (%.1f%% wide)" % (ul,last, bid, ask, spread * 100))
        results.append("--------------")
    return results

def price(underlying, exchange_list):
    if underlying == 'BITCOIN':
        underlying = 'BTCUSD'
    all_requested = False
    if exchange_list == ['all']:
        all_requested = True
        exchange_list = exchanges.get_exchanges_list_for_underlying(underlying)
    if exchange_list == []:
        return ['No exchange support %s' % underlying]
    bestbid = 0.00000001
    bestask = 1000000000
    bestspread = 100
    bestbid_exch = exchange_list[0]
    bestask_exch = exchange_list[0]
    bestspread_exch = exchange_list[0]
    results = []
    i = 0
    for exchange_name in exchange_list:
        if exchange_name.lower() in exchanges.exchange_list.keys():
            exchange = exchanges.get_exchange(exchange_name.lower())
            if underlying in exchange.get_supported_underlyings():
                bid = exchange.get_quote(underlying, 'bid')
                ask = exchange.get_quote(underlying, 'ask')
                try:
                    price = (bid + ask) / 2
                    spread = 100 * (ask - bid) / price
                    if not all_requested or spread < 3.5:
                        if bid > bestbid:
                            bestbid = bid
                            bestbid_exch = exchange_name
                        if ask < bestask:
                            bestask = ask
                            bestask_exch = exchange_name
                        if spread < bestspread:
                            bestspread = spread
                            bestspread_exch = exchange_name
                        i = i + 1
                    if  price > 1:
                        results.append("%s %s price is %.2f: %.2f / %.2f (%.2f%% wide)" % (exchange_name, underlying, price, bid, ask, spread))
                    else:
                        results.append("%s %s price is %.4g: %.4g / %.4g (%.2f%% wide)" % (exchange_name, underlying, price, bid, ask, spread))
                except:
                    results.append("%s price update failed" % exchange_name)
            else:
                results.append('%s not supported for %s' % (underlying, exchange_name))
        else:
            results.append("Unknown exchange: %s" % exchange_name)
    if i >= 2:
        spread = 100 *(bestask / bestbid - 1)
        if price > 1:
            results.append("Max bid is on %s: %.2f\nMin offer is on %s: %.2f.\nBest spread is on %s: %.2f%%\nAggregated price is %.1f%% wide (negative means arbitrageable)" % (bestbid_exch, bestbid, bestask_exch, bestask, bestspread_exch, bestspread, spread))
        else:
            results.append("Max bid is on %s: %.4g\nMin offer is on %s: %.4g.\nBest spread is on %s: %.2f%%\nAggregated price is %.1f%% wide (negative means arbitrageable)" % (bestbid_exch, bestbid, bestask_exch, bestask, bestspread_exch, bestspread, spread))
    return results

def fx(underlying, exchange, cross_ccy):
    FORCCY = underlying[:3].upper()
    DOMCCY = underlying[-3:].upper()

    if cross_ccy in ('USD','EUR','JPY'):
        FORPAIR = DOMCCY+cross_ccy
        DOMPAIR = FORCCY+cross_ccy
    else:
        FORPAIR = cross_ccy+FORCCY
        DOMPAIR = cross_ccy+DOMCCY

    if exchange == "all":
        forExchanges = exchanges.get_exchanges_list_for_underlying(FORPAIR)
        domExchanges = exchanges.get_exchanges_list_for_underlying(DOMPAIR)
        intersectExchanges = list(set(forExchanges).intersection(domExchanges))
    elif exchange.lower() not in exchanges.get_exchanges_list():
        return ['Unsupported exchange %s' % exchange]
    else:
        if (FORPAIR in exchanges.get_exchange(exchange.lower()).get_supported_underlyings()) and (DOMPAIR in exchanges.get_exchange(exchange.lower()).get_supported_underlyings()):
            intersectExchanges = [exchange]
        else:
            return ["Exchange %s does not support %s and %s" % (exchange, FORPAIR, DOMPAIR)]
    results = []
    if cross_ccy in ('USD','EUR','JPY'):
        e = exchanges.get_exchange(intersectExchanges[0].lower())
        fxRate = float(e.get_quote(underlying,'last'))
        results.append('%s rate for %s is %.5g' % (intersectExchanges[0], underlying, fxRate))
    else:
        url = 'http://www.apilayer.net/api/live?access_key='+CL_API_KEY+'&currencies='+FORCCY+','+DOMCCY
        r = requests.get(url)
        r.raise_for_status()
        j = r.json()
        if j['success']:
            domOfficialRate = r.json()['quotes']['USD'+DOMCCY]
            forOfficialRate = r.json()['quotes']['USD'+FORCCY]
            fxRate = domOfficialRate / forOfficialRate
            results.append('Currency Layer %s FX rate is %.5g' % (underlying, fxRate))
        else:
            fxRate = 0
            results.append('Could not retrieve %s FX rate from CurrencyLayer' % underlying)

    results.append('Using %s as the cross currency: %s and %s' % (cross_ccy.upper(), FORPAIR, DOMPAIR))

    for exch in intersectExchanges:
        e = exchanges.get_exchange(exch.lower())
        try:
            fx_bid = e.get_quote(DOMPAIR,'bid') / e.get_quote(FORPAIR,'ask')
            fx_ask = e.get_quote(DOMPAIR,'ask') / e.get_quote(FORPAIR,'bid')
            if fxRate != 0 and (fx_bid > fxRate or fx_ask < fxRate):
                if fx_bid > fxRate:
                    arb = 100 * (float(fx_bid) / fxRate - 1)
                else:
                    arb = 100 * (fxRate / float(fx_ask) - 1)
                results.append('%s on %s: bid %.5g / %.5g ask. %.2f%% arb vs %.5g official rate' % (underlying, exch, fx_bid, fx_ask, arb, fxRate))
            else:
                results.append('%s on %s: bid %.5g / %.5g ask' % (underlying, exch, fx_bid, fx_ask))
        except ZeroDivisionError:
            results.append('%s: one of the quotes is worth 0' % exch)
    return results

def priceMsg(bot, update):
    logger.info("Received /price command from %s" % update.effective_user)
    logger.info("Command content: %s" % update.message.text)
    if update.message.text.split().__len__() <= 2:
        update.message.reply_text('Syntax is "/price <underlying> <exchange1> <exchange2> <...>".\nTry "/price <underlying> all" to price your underlying on all supported exchanges.\nType /list to see supported exchanges')
        return
    underlying = update.message.text.split()[1].upper()
    exchange_list = update.message.text.split()[2:]
    if exchange_list == []:
        update.message.reply_text('No exchange support underlying %s' % underlying)
        return
    messages = price(underlying, exchange_list)
    update.message.reply_text('\n'.join(messages))

def fxMsg(bot, update):
    logger.info("Received /fx command from %s" % update.effective_user)
    logger.info("Command content: %s" % update.message.text)
    if update.message.text.split().__len__() <= 2:
        update.message.reply_text('Syntax is "/fx <fxpair> <exchange> <cross>".\nTry "/fx <fxpair> all eth" to price your underlying on all supported exchanges with eth as the cross cryotocurrency.\nType /list to see supported exchanges')
        return
    underlying = update.message.text.split()[1].upper()
    exchange_list = update.message.text.split()[2]
    if update.message.text.split().__len__() == 4:
        cross_ccy = update.message.text.split()[3].upper()
    else:
        if underlying[-3:].upper() == 'BTC' or underlying[:3].upper() == 'BTC':
            cross_ccy = 'USD'
        else:
            cross_ccy = 'BTC'
    if exchange_list == []:
        update.message.reply_text('No exchange specified. Try all or gatecoin for example')
        return
    messages = fx(underlying, exchange_list, cross_ccy)
    update.message.reply_text('\n'.join(messages))

def inline_query(bot, update):
    query = update.inline_query.query
    if not query:
        return
    logger.info("Inline query received from %s: %s" % (update.inline_query.from_user, query))
    results = list()
    query_type = query.split()[0]
    messages = [BOTNAME]
    if query_type.lower() == 'price':
        if query.split().__len__() <= 2:
            return
        underlying = query.split()[1].upper()
        exchange_list = query.split()[2:]
        if exchange_list == []:
            return
        messages.extend(price(underlying, exchange_list))
    elif query_type.lower() == 'list':
        messages.append(list_text())
    else:
        messages.append('Try ' + BOTNAME + ' price bitcoin bitfinex, or ' + BOTNAME + ' list')
    reply_text = '\n'.join(messages)
    results.append(InlineQueryResultArticle(id=uuid4(), title='Enter to display results', input_message_content=InputTextMessageContent(reply_text)))
    bot.answer_inline_query(update.inline_query.id, results)

def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))

def main():
    # Create the EventHandler and pass it to the bot's token
    updater = Updater(token=TOKEN)

    # Get the dispathcher to register handlers
    dispatcher = updater.dispatcher

    # Add handlers
    start_handler = CommandHandler('start', startMsg)
    list_exchanges_handler = CommandHandler('list', listExchangesMsg)
    price_handler = CommandHandler('price', priceMsg)
    fx_handler = CommandHandler('fx',fxMsg)
    exchange_handler = CommandHandler('exchange',exchangeMsg)
    summary_handler = CommandHandler('summary',summaryMsg)
    inline_query_handler = InlineQueryHandler(inline_query)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_exchanges_handler)
    dispatcher.add_handler(price_handler)
    dispatcher.add_handler(fx_handler)
    dispatcher.add_handler(exchange_handler)
    dispatcher.add_handler(summary_handler)
    dispatcher.add_handler(inline_query_handler)

    unknown_handler = MessageHandler(Filters.text, unknownMsg)
    dispatcher.add_handler(unknown_handler)

    # log all errors
    dispatcher.add_error_handler(error)

    # start the bot
    logger.info("Starting bot.")
    updater.start_polling()

    # The above runs the bot until CTRL-C or SIGINT, SIGTERM, or SIGABRT is
    # received. start_polling() is non-blocking and this will stop the bot
    # gracefully
    updater.idle()
    logger.info("Exiting bot.")

if __name__ == '__main__':
    main()

