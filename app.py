from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

app = Flask(__name__)

def realizar_scraping(url):
    # Configurar Selenium
    options = webdriver.ChromeOptions()
    #options.add_argument('--headless') # Para ejecución sin ventana visible
    driver = webdriver.Chrome(options=options)

    # Realizar scraping
    driver.get(url)
    time.sleep(2) # Espera para asegurar que la página esté cargada completamente

    # Encuentra los elementos con el tag 'h3' y la clase 'tAxDx'
    nombres_productos = driver.find_elements(By.CSS_SELECTOR, 'h3.tAxDx')
    # Encuentra los elementos con el tag 'span' y las clases 'a8Pemb OFFNJ'
    precios_elementos = driver.find_elements(By.CSS_SELECTOR, 'span.a8Pemb.OFFNJ')
    # Encuentra los elementos con el tag 'div' y las clases 'aULzUe IuHnof'
    tiendas_elementos = driver.find_elements(By.CSS_SELECTOR, 'div.aULzUe.IuHnof')
    # Encuentra los elementos con el tag 'img' dentro de un 'div' con la clase 'ArOc1c'
    imagenes_elementos = driver.find_elements(By.CSS_SELECTOR, 'div.ArOc1c > img')
    # Encuentra los elementos con el tag 'a' dentro de un 'div' con la clase 'mnIHsc'
    enlaces_elementos = driver.find_elements(By.CSS_SELECTOR, 'div.mnIHsc > a')

    productos = []
    i = 0
    j = 0
    while i < len(nombres_productos) and j < len(enlaces_elementos):
        nombre = nombres_productos[i]
        precio = precios_elementos[i]
        tienda = tiendas_elementos[i]
        imagen = imagenes_elementos[i]
        enlace = enlaces_elementos[j] 

       # Acceder al índice correspondiente de enlaces_elementos

        productos.append({
            "nombre": nombre.text,
            "precio": precio.text,
            "tienda": tienda.text,
            "img": imagen.get_attribute('src'),
            "url": enlace.get_attribute('href')
        })

        i += 1
        j += 2

    driver.quit() # Cerrar el navegador después del scraping
    return productos

@app.route('/scraping', methods=['GET'])
def scraping():
    url = "https://www.google.com/search?q=televisor+lg&sca_esv=782705a13c1e22f4&sca_upv=1&biw=1536&bih=730&tbm=shop&sxsrf=ACQVn085P3_BpF36mA_M9du9nZb8wej-PA%3A1714614273530&ei=AfAyZpnUH__7wbkPnuy_6A4&ved=0ahUKEwjZ2Mz16-2FAxX_fTABHR72D-0Q4dUDCAg&uact=5&oq=televisor+lg&gs_lp=Egtwcm9kdWN0cy1jYyIMdGVsZXZpc29yIGxnMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABDIFEAAYgAQyBRAAGIAEMgUQABiABEiZHFCPB1jzF3ABeACQAQCYAZsCoAHOEaoBBjAuMTMuMbgBA8gBAPgBAZgCD6ACkxLCAgQQIxgnwgIKEAAYgAQYQxiKBZgDAIgGAZIHBjEuMTMuMaAHpUk&sclient=products-cc"

    # Realizar scraping utilizando Selenium
    productos = realizar_scraping(url)
    return jsonify(productos)

if __name__ == '__main__':
    app.run(debug=True) 