import socket
import time
import math

SOCKET_PATH = "/tmp/qtest.sock"

# -----------------------------
# Configuración de señales
# -----------------------------
PERIODO = 4.0      # segundos por ciclo completo
MUESTRAS = 20      # submuestras por período PDM
dt = PERIODO / MUESTRAS

GPIO4 = 4          # senoidal PDM
GPIO17 = 17        # cuadrada

# Registros GPIO Raspberry Pi 
GPSET0 = 0x3F20001C
GPCLR0 = 0x3F200028


def enviar_comando(sock, cmd):
    sock.sendall((cmd + "\n").encode())
    return sock.recv(1024).decode().strip()


def set_gpio(sock, pin, valor):
    """Pone un GPIO en HIGH o LOW."""
    reg = GPSET0 if valor else GPCLR0
    mask = (1 << pin)
    cmd = f"writel 0x{reg:08x} 0x{mask:08x}"
    enviar_comando(sock, cmd)


def senoidal_pdm(t):
    """
    Genera una senoide aproximada usando PDM.
    La densidad de pulsos HIGH sigue el valor de la senoide.
    """
    fase = (t % PERIODO) / PERIODO

    # Senoidal normalizada [0,1]
    valor = (math.sin(2 * math.pi * fase) + 1) / 2

    # Índice de submuestra dentro del período
    muestra_idx = int(fase * MUESTRAS)

    # Umbral progresivo
    umbral = muestra_idx / MUESTRAS

    return 1 if valor > umbral else 0


def cuadrada(t):
    """Señal cuadrada 50% duty."""
    fase = t % PERIODO
    return 1 if fase < (PERIODO / 2) else 0


with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
    sock.connect(SOCKET_PATH)

    print("Conectado a qtest.")
    print(f"GPIO4  -> senoidal PDM")
    print(f"GPIO17 -> cuadrada")
    print(f"Periodo = {PERIODO}s")
    print(f"Submuestras PDM = {MUESTRAS}")
    print("-" * 50)

    inicio = time.monotonic()
    siguiente_tick = inicio

    try:
        while True:
            t = time.monotonic() - inicio

            val_pdm = senoidal_pdm(t)
            val_cua = cuadrada(t)

            set_gpio(sock, GPIO4, val_pdm)
            set_gpio(sock, GPIO17, val_cua)

            print(
                f"t={t:6.2f}s | "
                f"GPIO4(PDM)={val_pdm} | "
                f"GPIO17(CUA)={val_cua}"
            )

            siguiente_tick += dt
            sleep_time = siguiente_tick - time.monotonic()

            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\nDeteniendo señales...")

    finally:
        # Apagar GPIOs al salir
        set_gpio(sock, GPIO4, 0)
        set_gpio(sock, GPIO17, 0)
        print("GPIOs apagados.")
