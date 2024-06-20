# from serial.tools.list_ports_linux import comports
# from serial.tools.list_ports_osx import comports
# from serial.tools.list_ports_posix import comports
from serial.tools.list_ports_windows import comports

from data_backend.communication_system.domain.communication_system_client import CommunicationSystemClient
from data_backend.iclisten.domain.ICListenClient import ICListenClient
from apps.communication.communicator.serial_communicator import SerialCommunicator


def list_serial_ports():
    ports = comports()
    print("Dispositivos serie disponibles:")
    for port in ports:
        print(f"- {port.device}: {port.description}")


def choose_serial_port():
    while True:
        sel_port = input("Selecciona el puerto serie deseado (e.g. COM1, /dev/ttyUSB0): ").strip()
        if sel_port:
            return sel_port
        else:
            print("Por favor, introduce un puerto válido.")


# Ejemplo de uso:
if __name__ == "__main__":
    list_serial_ports()
    # selected_port = choose_serial_port()
    communicator = SerialCommunicator("COM3", 9600)
    # client = ICListenClient(communicator)
    client = CommunicationSystemClient(communicator)
    try:
        print("Sending a request...")
        # Enviar una solicitud
        response = client.ping_localizer()
        # response2 = client.ping_drifter()
        # response3 = client.ping_raspberry()

        # print(f"Response: {response}")

    finally:
        client.close()
