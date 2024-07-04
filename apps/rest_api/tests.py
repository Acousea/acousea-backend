import serial.tools.list_ports

if __name__ == "__main__":
    # Print available ports
    ports = serial.tools.list_ports.comports()
    print("Ports: ", [(
        port.device,
        port.name,
        port.product,
        port.serial_number,
        port.description,
        port.hwid,
        port.manufacturer,
        port.interface,
        port.location,
        port.pid) for port in ports])
    print("Ports: ", ports)
