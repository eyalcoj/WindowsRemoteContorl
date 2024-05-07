from src.small_conn.client.client_connection import ClientServerConnection


class ClientConnectionWarper:
    def __init__(self, client_connection: ClientServerConnection):
        self.__client_connection = client_connection
        self.feedback = ""
        self.feedback_number = 0

    def input_user_name(self, name):
        self.__client_connection.name_input_request(name)
        feedback = self.__client_connection.get_name_input_feedback()
        while self.feedback_number == feedback[1]:
            feedback = self.__client_connection.get_name_input_feedback()

        self.feedback_number = feedback[1]
        self.feedback = feedback[0]

    def close(self):
        self.__client_connection.self_disconnect()

    def open(self):
        self.__client_connection.connect()
