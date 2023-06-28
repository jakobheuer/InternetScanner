import socket
import ctypes, sys
import subprocess
import datetime
import concurrent.futures

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def test_port_number(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(3)
        try:
            sock.connect((host, port))
            return True
        except:
            return False

def port_scan(host, ports, f):
    print(f'Scanning {host}...')
    with concurrent.futures.ThreadPoolExecutor(len(ports)) as executor:
        results = executor.map(test_port_number, [host]*len(ports), ports)
        for port,is_open in zip(ports,results):
            if is_open:
                f.write(" - {}\n".format(port))
                f.flush()

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

f = open("List.txt",'a')
f.write("\n-------------------------------------------\n\n{} Scanner started\n".format(datetime.datetime.now()))
f.flush()

for networkID1 in range (1,255+1):
    for networkID2 in range (255):
        for networkID3 in range (255):
            for hostID in range (255):
                ip = str(networkID1) + '.' + str(networkID2) + '.' + str(networkID3) + '.' +str(hostID)
                print(ip)
                response = subprocess.call(['ping', '-n', '1', ip],stdout=subprocess.DEVNULL) # 1 = NO IP FOUND, 0 = IP FOUND
                if response == 0:
                    f.write("{}: ({}) active, Open Ports:\n".format(datetime.datetime.now(),ip))
                    f.flush()
                    port_scan(ip, range(1, 5000), f)
f.close()
