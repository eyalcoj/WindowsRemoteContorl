from src.data_saver.secured_data_saver import SecuredDataSaver


class KeyValue:
    IS_CLIENT_KEYBOARD = "is_client_keyboard"
    IS_CLIENT_SHARE_SCREEN = "is_client_share_screen"


class ClientDataSaver(SecuredDataSaver):
    def __init__(self):
        super().__init__()
        self.set_value(KeyValue.IS_CLIENT_SHARE_SCREEN, False)
        self.set_value(KeyValue.IS_CLIENT_KEYBOARD, False)
