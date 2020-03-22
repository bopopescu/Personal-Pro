import requests
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup

titulares = []
url = 'https://www.pagina12.com.ar/'
p12 = requests.get(url)

s = BeautifulSoup(p12.text,'lxml')

titulo = s.find('title').get_text()
secciones = s.find('ul', attrs={'class':'hot-sections'}).find_all('li')

links = [seccion.a.get('href') for seccion in secciones]
all_requests = [BeautifulSoup(requests.get(enlace).text,'lxml') for enlace in links]
list_requests = [req.find('ul', attrs={'class':'article-list'}).find_all('h2') for req in all_requests]


for pestaña in list_requests:
    for contenedores in pestaña:
        titulares.append(contenedores.a.get('href'))

        
print(f'Se obtuvieron un total de {len(titulares)} titulares de la página [{titulo}]\n')
    
    
#Función para obtener la información de cada artículo
def obtener_info (s_nota):
    
    contenido = {}

    #Extraemos el titulo
    titulo_nota = s_nota.find('h1', attrs={'class':'article-title'})

    if titulo_nota: contenido['Titulo'] = titulo_nota.get_text()
    else: contenido['Titulo'] = None


    #Extraer la fecha del articulo 
    fecha_articulo = s_nota.find('span', attrs={'pubdate':"pubdate"})

    if fecha_articulo: contenido['Fecha'] = fecha_articulo.get('datetime')
    else: contenido['Fecha'] = None


    #Extraer la volanta
    volanta = s_nota.find('h2', attrs={'class':'article-prefix'})

    if volanta: contenido['Volanta'] = volanta.get_text()
    else: contenido['Volanta'] = None


    #Extraer el copete
    copete = s_nota.find('div', attrs={'class':'article-summary'})

    if copete: contenido['Copete'] = copete.get_text()
    else: contenido['Copete'] = None


    #Epígrafe
    epigrafe = s_nota.find('span', attrs={'class':'article-main-media-text-image'})

    if epigrafe: contenido['Epigrafe'] = epigrafe.get_text()
    else: contenido['Epigrafe'] = None


    #Imagen
    media = s_nota.find('div', attrs={'class':'article-main-media-image'})

    if media: 
        imagenes = media.find_all('img')

        if len(imagenes) == 0:
            print('No se encontraron imagenes')

        else:
            imagen = imagenes[-1]
            img_src = imagen.get('data-src')

            try:
                img_req = requests.get(img_src)
                if img_req.status_code == 200:
                    contenido['Imagen'] = img_req.content
                else:
                    contenido['Imagen'] = None
            except:
                print('No se pudo obtener la imagen')

    if all(value == None for value in contenido.values()):
        print(f'La página\n\n\t{url_nota}\n\nNo tiene la estructura adecuada para este scraper')

    return contenido


#Función para procesar cada una de las urls

def scrape_nota(url):
    
    try:
        nota = requests.get(url)
    except Exception as e:
        print('Error scrapeando URL ',url)
        print(e)
        return None
    
    if nota.status_code != 200:
        print(f'Error obteniendo nota {url}')
        print(f'Status Code = {nota.status_code}')
        return None
    
    s_nota = BeautifulSoup(nota.text,'lxml')
    contenido = obtener_info(s_nota)
    contenido['Url'] = url
    
    return contenido


#Creación de una lista con los diccionarios creados en las funciones donde se almacena la información

result = []
for titular in tqdm(titulares, desc='Scraping: '):
    result.append(scrape_nota(titular))
    

#Creamos y exportamos el dataframe
df = pd.DataFrame(result)
df.to_csv('Notas Pagina12.csv')
print('Dataframe guardado')
