#!/usr/bin/env python3
"""TCP relay for Windows Mobile Hotspot in WSL development environments.

Windows Mobile Hotspot isolates devices on 192.168.137.x using a virtual
Wi-Fi Direct adapter that WSL cannot route to directly. Running this relay
on the Windows host bridges port 2302 between WSL and the target device.

Usage:
    python3 tools/wsl_relay.py [REMOTE_HOST] [PORT]
"""
import os
import shutil
import socket
import subprocess
import sys
import threading

DEFAULT_PORT = int(os.environ.get("PORT", 2302))
DEFAULT_BIND = os.environ.get("BIND_ADDR", "0.0.0.0")


def forward(src, dst):
    try:
        while chunk := src.recv(65536):
            dst.sendall(chunk)
    except Exception:
        pass
    try:
        dst.shutdown(socket.SHUT_WR)
    except Exception:
        pass


def handle_client(client, remote_host, remote_port):
    try:
        remote = socket.create_connection((remote_host, remote_port), timeout=10)
    except Exception as e:
        sys.stderr.write(f"Relay connect error to {remote_host}:{remote_port}: {e}\n")
        client.close()
        return

    t1 = threading.Thread(target=forward, args=(client, remote))
    t2 = threading.Thread(target=forward, args=(remote, client))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    client.close()
    remote.close()


def run_relay(remote_host, port, bind_addr):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((bind_addr, port))
    except OSError as e:
        sys.stderr.write(f"Failed to bind to {bind_addr}:{port}: {e}\n")
        sys.exit(1)

    server.listen(16)
    print(f"WSL Hotspot Relay running: {bind_addr}:{port} -> {remote_host}:{port}", flush=True)
    print("Press Ctrl+C to stop.", flush=True)

    try:
        while True:
            client, _ = server.accept()
            threading.Thread(target=handle_client, args=(client, remote_host, port), daemon=True).start()
    except KeyboardInterrupt:
        print("\nStopping relay.")
    finally:
        server.close()


def find_windows_python():
    """Dynamically locate the Windows Python interpreter from within WSL."""
    for candidate in ("python.exe", "py.exe"):
        path = shutil.which(candidate)
        if path:
            return path

    try:
        out = subprocess.check_output(
            ["cmd.exe", "/c", "where python"],
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
        ).decode()
        for line in out.splitlines():
            line = line.strip()
            if line.lower().endswith("python.exe"):
                wsl_path = subprocess.check_output(["wslpath", "-u", line]).decode().strip()
                if os.path.exists(wsl_path):
                    return wsl_path
    except Exception:
        pass

    return None


def discover_hotspot_ip():
    """Attempt to discover a device connected to the Windows Mobile Hotspot."""
    try:
        cmd = ["arp", "-a"] if sys.platform == "win32" else ["cmd.exe", "/c", "arp -a"]
        out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, stdin=subprocess.DEVNULL).decode()
        in_hotspot = False
        candidates = []
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Interface:"):
                in_hotspot = "192.168.137.1" in line
                continue
            if in_hotspot:
                parts = line.split()
                if len(parts) >= 2:
                    ip = parts[0]
                    if ip.startswith("192.168.137.") and not ip.endswith(".1") and not ip.endswith(".255"):
                        candidates.append(ip)
        if len(candidates) == 1:
            return candidates[0]
    except Exception:
        pass
    return None


def resolve_remote_host():
    if len(sys.argv) > 1 and not sys.argv[1].isdigit():
        return sys.argv[1]

    env_host = os.environ.get("REMOTE_HOST") or os.environ.get("Q2_HOST")
    if env_host and env_host != "127.0.0.1" and env_host != "localhost":
        return env_host

    discovered = discover_hotspot_ip()
    if discovered:
        print(f"Auto-detected hotspot device IP: {discovered}", flush=True)
        return discovered

    return None


def main():
    remote_host = resolve_remote_host()
    if not remote_host:
        sys.stderr.write(
            "Error: Target device IP not specified and could not be auto-detected.\n"
            "Usage: python3 tools/wsl_relay.py <REMOTE_HOST> [PORT]\n"
            "   or: export Q2_HOST=<REMOTE_HOST>\n"
        )
        sys.exit(1)

    port = int(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_PORT

    if sys.platform != "win32":
        is_wsl = os.path.exists("/proc/version") and "microsoft" in open("/proc/version").read().lower()
        if is_wsl:
            win_py = find_windows_python()
            if win_py and os.path.exists(win_py):
                print(f"WSL detected: launching relay via Windows host Python ({win_py})...", flush=True)
                sys.exit(subprocess.call([win_py, os.path.abspath(__file__), remote_host, str(port)]))
            else:
                print("Warning: Windows python.exe not found; attempting to bind directly in WSL.")

    run_relay(remote_host, port, DEFAULT_BIND)


if __name__ == "__main__":
    main()
