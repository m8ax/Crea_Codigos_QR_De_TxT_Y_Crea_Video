# M8AX - Crea Video De Un Fichero De Texto, Cada Linea 1 QR = 1 FRAME, A 1 Fps...

import qrcode
import glob
import cv2
import os
import time

def barra_progreso_amarillat(progreso, total, tiembarra, n):
    porcen = 100 * (progreso / float(total))
    pseg = n / (time.time() - tiembarra)
    segrestante = 0
    if porcen > 0:
        segrestante = (100 * (tiembarra - time.time()) / porcen) - (
            tiembarra - time.time()
        )
    barra = "█" * int(porcen) + "-" * (100 - int(porcen))
    print(
        f"\r\033[38;2;{255};{255};{0}m|{barra}| - ETA - {segahms(segrestante*-1)} - {pseg:.2f} Qr-Ln/Seg - {porcen:.2f}%      ",
        end="\r\033[0m",
    )

def barra_progreso_amarilla(progreso, total, tiembarra):
    porcen = 100 * (progreso / float(total))
    segrestante = 0
    if porcen > 0:
        segrestante = (100 * (tiembarra - time.time()) / porcen) - (
            tiembarra - time.time()
        )
    barra = "█" * int(porcen) + "-" * (100 - int(porcen))
    print(
        f"\r\033[38;2;{255};{255};{0}m|{barra}| - ETA - {segahms(segrestante*-1)} - {porcen:.2f}%      ",
        end="\r\033[0m",
    )

def segahms(segundos):
    horas = int(segundos / 60 / 60)
    segundos -= horas * 60 * 60
    minutos = int(segundos / 60)
    segundos -= minutos * 60
    return f"{horas}h:{minutos}m:{int(segundos)}s"

print(f"\nComenzando...\n")
a = time.time()
n = 0

with open("Texto.TxT", "r", encoding="utf-8") as file:
    lineas = file.readlines()
    totallineas = len(lineas)
    for linea in lineas:
        data = linea
        if len(data) != 0:
            qr = qrcode.QRCode(version=7, box_size=45, border=1)
            qr.add_data(data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="#FF0000", back_color="black")
            img.save("img-0000" + str(n) + ".png")
            data = ""
        n = n + 1
        barra_progreso_amarillat(n, totallineas, a, n)
    file.close()
barra_progreso_amarillat(totallineas, totallineas, a, n)

b = time.time()
framesize = ((2115), (2115))
print("\n")
outv = cv2.VideoWriter(
    "VideoTexto-QR.Mp4", cv2.VideoWriter_fourcc(*"h265"), 1, framesize
)
print("\n")
nn = 0

for filename in sorted(glob.glob("*.png"), key=os.path.getmtime):
    imgv = cv2.imread(filename)
    outv.write(imgv)
    nn = nn + 1
    barra_progreso_amarilla(nn, len(glob.glob("*.png")), b)

barra_progreso_amarilla(len(glob.glob("*.png")), len(glob.glob("*.png")), b)
print("\n")
print(*sorted(glob.glob("*.png"), key=os.path.getmtime), sep="\n")
outv.release()
print("\n... Video Realizado Correctamente ...\n")
print(
    f"Tiempo Total De Proceso - {segahms((time.time()-a))} A {round(n/(time.time()-a),3)} QR Codes = Líneas De Texto, Por Segundo..."
)