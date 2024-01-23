import socket

def scan_ports(target_ip, start_port, end_port):
    open_ports = []

    print(f"Scanning ports on {target_ip} from {start_port} to {end_port}")

    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(f"  Port {port}")
    else:
        print("No open ports found.")

if __name__ == "__main__":
    target_ip = input("Enter target IP address: ")
    start_port = int(input("Enter starting port: "))
    end_port = int(input("Enter ending port: "))

    scan_ports(target_ip, start_port, end_port)
