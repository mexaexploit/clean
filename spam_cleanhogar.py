from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import os
import time

# Cargamos el archivo txt con los números de teléfono
with open('numeros.txt', 'r') as file:
    lista_numero = [line.strip() for line in file]

# Establecemos el límite diario de mensajes
limite_diario = 20

# Definimos el nombre del archivo de progreso
archivo_progreso = 'progreso.txt'

# Creamos el archivo de progreso si es que no existe
if os.path.exists(archivo_progreso):
    with open(archivo_progreso, 'r') as file:
        ultimo_envio = int(file.read())
else:
    ultimo_envio = 0

# Iniciamos el contador de envíos
contador_envios = 0

# Configuración de chromedriver
chromedriver_path = 'chromedriver.exe'
service = Service(chromedriver_path)
print("chromedriver encontrado")

driver = webdriver.Chrome(service=service)
print("Se inició chromedriver")

# Abrimos WhatsApp Web
driver.get("https://web.whatsapp.com")
time.sleep(25)

input("Esperando a que el usuario escanee el QR y presione enter...")

# Bucle for para enviar mensajes a los números en la lista
for i in range(ultimo_envio, len(lista_numero)):
    if contador_envios >= limite_diario:
        print("Se alcanzó el límite diario, inténtalo mañana.")
        break
    
    # Obtenemos el número de teléfono actual
    numero_telefono = lista_numero[i]

    try:
        # Buscamos el contacto o número en WhatsApp
        search_box_contacto = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box_contacto.click()
        time.sleep(5)
        search_box_contacto.send_keys(numero_telefono)
        search_box_contacto.send_keys(Keys.ENTER)
        time.sleep(10)
        print(f"Se ingresó el número de teléfono: {numero_telefono}")

        # Enviamos el mensaje
        search_box_enviar = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
        mensaje = f"Hola, ¿Quieres recibir el año nuevo con un hogar impecable? Aprovecha nuestras promociones de diciembre y deja tu hogar reluciente. ¡Contáctanos para más información!"
        search_box_enviar.send_keys(mensaje)
        search_box_enviar.send_keys(Keys.ENTER)
        time.sleep(10)
        print(f"Se envió el mensaje a {numero_telefono}")

        # Incrementamos el contador de envíos
        contador_envios += 1

    except Exception as e:
        print(f"Ocurrió un error al enviar el mensaje a {numero_telefono}: {str(e)}")

# Guardamos el progreso
with open(archivo_progreso, 'w') as file:
    file.write(str(ultimo_envio + contador_envios))

print("Envíos del día completados.")