import os
import subprocess


def get_temperature():
    return os.popen("vcgencmd measure_temp").readline().replace("temp=", "").strip()


def get_cpu_usage():
    return (
        subprocess.getoutput("top -bn1 | grep 'Cpu(s)' | awk '{print $2 + $4}'") + "%"
    )


def get_system_uptime():
    return subprocess.getoutput("uptime -p").replace("up ", "")


def get_ram_usage():
    return subprocess.getoutput("free -m | awk 'NR==2{printf \"%sMB / %sMB\", $3, $2}'")


def get_disk_usage():
    return subprocess.getoutput("df -h / | awk 'NR==2 {print $3 \" / \" $2}'")


def get_network_info():
    return {
        "ip_address": subprocess.getoutput("hostname -I | awk '{print $1}'"),
        "wifi_ssid": subprocess.getoutput("iwgetid -r"),
    }
