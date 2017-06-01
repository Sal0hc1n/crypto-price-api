#!/usr/bin/env python

from telegram import InlineQueryResultArticle,InputTextMessageContent
from telegram.ext import Updater
from telegram.ext import CommandHandler, MessageHandler, Filters, InlineQueryHandler
from uuid import uuid4
import logging
import exchanges

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s-%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

BOTNAME = '@CryptoHelper_Bot'
TOKEN = 'TOKEN'

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
    return exchange_text + '\n\n' + underlyings_text

def price(underlying, exchange_list):
    if underlying == 'BITCOIN':
        underlying = 'BTCUSD'
    if exchange_list == ['all']:
        exchange_list = exchanges.get_exchanges_list_for_underlying(underlying)
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
    inline_query_handler = InlineQueryHandler(inline_query)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(list_exchanges_handler)
    dispatcher.add_handler(price_handler)
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

quit()
