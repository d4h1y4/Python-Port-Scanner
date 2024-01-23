import socket
import threading
import os

def scan_ports(target_ip, start_port, end_port, open_ports):
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)

        result = sock.connect_ex((target_ip, port))

        if result == 0:
            open_ports.append(port)

        sock.close()

def divide_range(num_threads, start_port, end_port):
    step = (end_port - start_port + 1) // num_threads
    ranges = [(i * step + start_port, (i + 1) * step + start_port - 1) for i in range(num_threads)]
    ranges[-1] = (ranges[-1][0], end_port)
    return ranges

def get_optimal_threads():
    return min(os.cpu_count() * 2, 32)  # Limit to a reasonable number, e.g., maximum 32 threads

def multi_threaded_scan(target_ip, start_port, end_port):
    open_ports = []
    num_threads = get_optimal_threads()
    thread_list = []

    ranges = divide_range(num_threads, start_port, end_port)

    print(f"Scanning ports on {target_ip} from {start_port} to {end_port} using {num_threads} threads")

    for i in range(num_threads):
        thread = threading.Thread(target=scan_ports, args=(target_ip, ranges[i][0], ranges[i][1], open_ports))
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join()

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

    multi_threaded_scan(target_ip, start_port, end_port)
