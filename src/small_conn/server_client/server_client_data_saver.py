from src.data_saver.secured_data_saver import SecuredDataSaver
from src.keys.key_collector import KeyCollector


class KeyValue:
    IS_CLIENT_KEYBOARD = "is_client_keyboard"
    IS_SERVER_KEYBOARD = "is_server_keyboard"
    IS_CLIENT_SHARE_SCREEN = "is_client_share_screen"
    IS_SERVER_SHARE_SCREEN = "is_server_share_screen"
    KEY_COLLECTOR = "key_collector"


class ServerClientDataSaver(SecuredDataSaver):
    def __init__(self):
        super().__init__()

        self.set_value(KeyValue.IS_CLIENT_KEYBOARD, False)
        self.set_value(KeyValue.IS_SERVER_KEYBOARD, False)
        self.set_value(KeyValue.IS_CLIENT_SHARE_SCREEN, False)
        self.set_value(KeyValue.IS_SERVER_SHARE_SCREEN, False)
        self.set_value(KeyValue.KEY_COLLECTOR, KeyCollector())
