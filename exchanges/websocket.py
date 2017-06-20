from decimal import Decimal
import websocket
import threading
import logging

class Exchange_WebSocket(object):

    MAX_TABLE_LEN = 200

    def __init__(self, exchangeName, key, secret, loggerObject = None, *args, **kwargs):
        if type(loggerObject) is not logging.getLoggerClass():
            self.logger = logging.getLogger(exchangeName)
            # default log to stdout. override this if needed
            self.logger.setLevel(logging.DEBUG)
            lh = logging.StreamHandler()
            lh.setFormatter(logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s"))
            self.logger.addHandler(lh)
        else:
            self.logger = loggerObject
            self.key = key
            self.secret = secret
            self.data = {}
        self.keys = {}
        self.exited = False
        self._error = None

    def get_key(self):
        return self.key

    def get_secret(self):
        return self.secret

    def _connect(self, wsURL):
        self.ws = websocket.WebSocketApp(wsURL, on_message = self.__on_message, on_close = self.__on_close, on_open = self.__on_open, on_error = self.__on_error, header = self__.get_auth())
        self.wst = treading.Thread(target = lambda: self.ws.run_forever())
        self.wst.daemon = True
        self.wst.start()
        self.logger.info("Started thread")

        # wait for connect before continuing
        conn_timeout = 5
        while(not self.ws.sock or not self.ws.sock.connected) and conn_timeout and not self._error:
            sleep(1)
            conn_timeout -= 1

        if not conn_timeout or self_.error:
            self.logger.error("Couldn't connect to WS")
            self.exit()
            sys.exit(1)

    def __get_auth():
        self.logger.info("Authenticating to WS with API Key")
        nonce = generate_nonce
        return ["api-nonce: " + str(nonce), "api-signature: " + generate_signature(self.secret, 'GET', '/realtime', nonce, ''), "api-key: " + self.key]


