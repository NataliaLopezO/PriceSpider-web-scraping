from flask import Flask, jsonify, request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

app = Flask(__name__)

def realizar_scraping(nombre_producto):
    # Configurar Selenium
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    # Abrir Google
    driver.get("https://www.google.com/")
    time.sleep(2) 

    # Encontrar el cuadro de búsqueda y escribir el nombre del producto
    search_box = driver.find_element(By.XPATH, '//textarea[@title="Buscar"]')
    search_box.send_keys(nombre_producto)

    # Presionar Enter para realizar la búsqueda
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

    # Encontrar el enlace de "Shopping" y hacer clic en él
    shopping_links = driver.find_elements(By.CSS_SELECTOR, 'a.LatpMc.nPDzT.T3FoJb')
    for link in shopping_links:
        if "Shopping" in link.text:
            link.click()
            break
    time.sleep(2) 

    # Encuentra los elementos 
    nombres_productos = driver.find_elements(By.CSS_SELECTOR, 'h3.tAxDx')
    precios_elementos = driver.find_elements(By.CSS_SELECTOR, 'span.a8Pemb.OFFNJ')
    tiendas_elementos = driver.find_elements(By.CSS_SELECTOR, 'div.aULzUe.IuHnof')
    imagenes_elementos = driver.find_elements(By.CSS_SELECTOR, 'div.ArOc1c > img')
    enlaces_elementos = driver.find_elements(By.CSS_SELECTOR, 'div.mnIHsc > a')

    productos = []
    i = 0
    j = 0
    while i < 10 and j < 20:
        nombre = nombres_productos[i]
        precio = precios_elementos[i]
        tienda = tiendas_elementos[i]
        imagen = imagenes_elementos[i]
        enlace = enlaces_elementos[j]
        
        productos.append({
            "nombre": nombre.text,
            "precio": precio.text,
            "tienda": tienda.text,
            "img": imagen.get_attribute('src'),
            "url": enlace.get_attribute('href')
        })
        i += 1
        j += 2

    driver.quit() 
    return productos


@app.route('/scraping', methods=['POST'])
def scraping():
    data = request.json
    nombre_producto = data.get('nombre_producto')
    if not nombre_producto:
        return jsonify({"error": "Se necesita proporcionar el nombre del producto en el cuerpo de la solicitud"}), 400

    # Realizar scraping utilizando Selenium
    productos = realizar_scraping(nombre_producto)
    return jsonify(productos)

if __name__ == '__main__':
    app.run(debug=True)