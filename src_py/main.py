
# QT related
from sys import argv
from PyQt5 import QtWidgets, uic
# Socket connections
import socket
# Useful tools
import re

class MainUi(QtWidgets.QMainWindow):

    ''' Holds the Main Window Functions and Atributes '''

    def __init__(self) -> None:

        ''' Constructor, init window and connect widgets '''
        
        super(MainUi, self).__init__()

        # Load Ui Qt Designer file
        uic.loadUi("main.ui", self)

        # Initialize "connect" button
        self.connect_button = self.findChild(QtWidgets.QPushButton, "connectButton")
        self.connect_button.clicked.connect(self.connectButtonPressed)

        # Initialize IP input
        self.ip_addr_input = self.findChild(QtWidgets.QLineEdit, "ipAddrLineEdit")
        self.port = self.findChild(QtWidgets.QLineEdit, "portLineEdit")

        # Show Window
        self.show()
    
    def isIPAddressValid(self) -> bool:
        
        ''' Check for Valid IP Address format with Regex '''

        valid_ip_regex = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if re.search(valid_ip_regex, self.ip_addr_input.text()):
            return True
        else:
            return False
    
    def displayErrorMessage(self, error_msg : str, error_info : str) -> None:

        ''' Display error message in new window with OK button '''

        msg = QtWidgets.QMessageBox()
        msg.setText(error_msg)
        msg.setInformativeText(error_info)
        msg.setWindowTitle("Error")
        msg.exec_()
    
    def connectButtonPressed(self) -> None:

        ''' Check IP and try to connect to the client '''

        if not self.isIPAddressValid():
            self.displayErrorMessage("Invalid IP Address", "Please, try again with a valid IP address.")
        
        elif (not isinstance(self.port, int)) or (self.port < 1024) or (self.port > 65535):
            self.displayErrorMessage("Invalid Port number", "Please, use a port from 1024 to 65535.")
        
        else:
            self.connect_button.setText("Connecting...")
            # With statements are used to automatically close connections without calling "close"
            # AF_INET: IPV4, SOCK_STREAM: TCP connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # Bind to IP and Port
                s.bind((self.ip_addr_input, self.port))
                # Enable the server to accept connections
                s.listen()
                # This method will block and wait for connection
                conn, addr = s.accept()
                with conn:
                    print("Connected by {}".format(addr))
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break

# End of MainUi class #

# -------------------------- #
''' Main Call '''
if __name__ == "__main__":
    app = QtWidgets.QApplication(argv)
    window = MainUi()
    app.exec_()
# -------------------------- #
