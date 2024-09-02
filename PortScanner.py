import socket
import tkinter as tk
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Thread  # İlgili import eklenmiş

# Scan a range of ports on a given host
def scan_port(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  # Set timeout for socket connection
            result = s.connect_ex((host, port))
            return port if result == 0 else None
    except Exception as e:
        return None

def scan_ports(host, start_port, end_port, result_text):
    open_ports = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(scan_port, host, port): port for port in range(start_port, end_port + 1)}
        for future in as_completed(future_to_port):
            port = future_to_port[future]
            result = future.result()
            if result:
                open_ports.append(result)
    
    # Update the result_text widget with the results
    result_text.delete(1.0, tk.END)
    if open_ports:
        result_text.insert(tk.END, f"Open ports on {host}:\n")
        for port in open_ports:
            result_text.insert(tk.END, f"Port {port} is open\n")
    else:
        result_text.insert(tk.END, f"No open ports found on {host}\n")

# GUI Functions
def start_scan():
    host = host_entry.get()
    try:
        start_port = int(start_port_entry.get())
        end_port = int(end_port_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Port numbers must be integers.")
        return
    
    if not host:
        messagebox.showerror("Error", "Host is required.")
        return
    
    result_text.delete(1.0, tk.END)
    thread = Thread(target=scan_ports, args=(host, start_port, end_port, result_text))
    thread.start()

# Initialize Tkinter GUI
def create_gui():
    global host_entry, start_port_entry, end_port_entry, result_text

    root = tk.Tk()
    root.title("Network Port Scanner")

    # Create and place widgets
    tk.Label(root, text="Host:").grid(row=0, column=0, padx=10, pady=10)
    host_entry = tk.Entry(root)
    host_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Start Port:").grid(row=1, column=0, padx=10, pady=10)
    start_port_entry = tk.Entry(root)
    start_port_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="End Port:").grid(row=2, column=0, padx=10, pady=10)
    end_port_entry = tk.Entry(root)
    end_port_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Button(root, text="Start Scan", command=start_scan).grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    result_text = tk.Text(root, height=10, width=50)
    result_text.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
