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

    # Encuentra los elementos con el tag 'h2' y la clase 'ui-search-item__title'
    nombres_productos = driver.find_elements(By.CSS_SELECTOR, 'h2.ui-search-item__title')
    nombres = []

    for i, nombre in enumerate(nombres_productos):
        if i == 5:  # Detener el bucle después de los primeros 5 nombres
            break
        nombres.append(nombre.text)

    driver.quit() # Cerrar el navegador después del scraping
    return nombres

@app.route('/scraping', methods=['GET'])
def scraping():
    url = "https://listado.mercadolibre.com.co/televisor-lg#D[A:televisor%20lg]"
    # Realizar scraping utilizando Selenium
    datos = realizar_scraping(url)
    return jsonify({'datos': datos})

if __name__ == '__main__':
    app.run(debug=True)