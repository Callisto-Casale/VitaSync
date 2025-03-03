# import subprocess
# import app.database.database_logic as database_logic


def scan_network():
    return 0
    # """Scans the local network using arp-scan and updates the database."""
    # try:
    #     output = subprocess.run(["sudo", "arp-scan", "--localnet"], capture_output=True, text=True)
    #     lines = output.stdout.split("\n")

    #     for line in lines[2:]:
    #         parts = line.split()
    #         if len(parts) >= 3:
    #             ip, mac, hostname = parts[0], parts[1], parts[2] if len(parts) > 2 else "Unknown"
    #             database_logic.update_device(mac, ip, hostname)

    #     database_logic.disconnect_old_devices()

    #     return 1

    # except Exception as e:
    #     print(f"error {e}")
    #     return {"error": e}
