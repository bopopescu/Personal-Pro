import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(executable_path = '/Users/drarn/Documents/Code/Study/BigData/WebScraping/chromedriver', options = options)

url = 'https://www.latam.com/es_co/apps/personas/booking?fecha1_dia=13&fecha1_anomes=2020-03&fecha2_dia=21&fecha2_anomes=2020-03&from_city2=CTG&to_city2=BOG&auAvailability=1&ida_vuelta=ida_vuelta&vuelos_origen=Bogot%C3%A1&from_city1=BOG&vuelos_destino=Cartagena%20de%20Indias&to_city1=CTG&flex=1&vuelos_fecha_salida_ddmmaaaa=13/03/2020&vuelos_fecha_regreso_ddmmaaaa=21/03/2020&cabina=Y&nadults=1&nchildren=0&ninfants=0&cod_promo=&stopover_outbound_days=0&stopover_inbound_days=0#/'
if requests.get(url).status_code == 200:
    driver.get(url)
    

def obtenerInfo(indices, precios):
    
    lista_escalas = driver.find_elements_by_xpath('//span[@class="sc-hzDkRC ehGSeR"]')
    lista_esperas = driver.find_elements_by_xpath('//span[@class="sc-cvbbAY kxLrTU"]')
    
    total_viajes = []
    tiempo = True

    for idx,escalas in enumerate(lista_escalas):
        
        datos_viaje = {}
        datos_viaje['Indice']=indices
        datos_viaje['Ciudad']=escalas.find_element_by_xpath('.//abbr').text
        datos_viaje['Hora']=escalas.find_element_by_xpath('.//time').text
        datos_viaje['Aeropuerto']=escalas.find_element_by_xpath('.//span[@class="sc-csuQGl ktjiAI"]').text
        
        if idx == 0 or idx == len(lista_escalas):
            datos_viaje['Tiempo'] = ''
        else:
            datos_viaje['Tiempo'] = lista_esperas[idx-1].find_element_by_xpath('.//time').get_attribute('datetime')
        
        datos_viaje['Precio'] = precios[indices-1]
        total_viajes.append(datos_viaje)

    return total_viajes

driver.implicitly_wait(100)

lista_botones = driver.find_elements_by_xpath('//div[@class="flight-summary-stops-description"]/button')
lista_precios = driver.find_elements_by_xpath('//section[@class="container flight-list"]//span[@class="price"]/span[@class="value"]')

vuelos_precios = [precio.text for precio in lista_precios]

vuelos_data= []

for indices, boton in enumerate(lista_botones):
    
    boton.click()
    
    driver.implicitly_wait(15)
    
    vuelos_data.append(obtenerInfo(indices+1,vuelos_precios))
    
    cerrar = driver.find_element_by_xpath('//div[@class="modal-header sc-dnqmqq cGfTsx"]/button[@class="close"]')
    
    cerrar.click()
    
    driver.implicitly_wait(15)
    
driver.close()

    
df = pd.DataFrame(vuelos_data[0])

for i in range(1,len(vuelos_data)):
    df = df.append(vuelos_data[i])
    
df = df.set_index('Indice')
df.to_csv('VuelosLatam.csv')