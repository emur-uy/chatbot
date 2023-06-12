import psycopg2
from psycopg2 import sql
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

def make_request(url):
    # Make a GET request to the URL
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to make request to {url}, status code: {response.status_code}")
        return None
    return response.content

def parse_html(content):
    # Parse the HTML content using BeautifulSoup
    return BeautifulSoup(content, "html.parser")

def extract_text(soup):
    # Extract and clean up the text from the parsed HTML
    body_text = soup.body.get_text()
    cleaned_text = ' '.join(body_text.split())
    return cleaned_text

def insert_into_db(url, data):
    # Create a connection to the database using the URL from the environment variables
    db_url = os.getenv('SQLALCHEMY_DATABASE_URL')
    connection = psycopg2.connect(db_url)
    cursor = connection.cursor()

    # Prepare the INSERT statement with an ON CONFLICT DO UPDATE clause
    insert = sql.SQL(
        """
        INSERT INTO information (url, data, created_at) 
        VALUES (%s, %s, %s) 
        ON CONFLICT (url) DO UPDATE 
        SET data = %s, updated_at = %s
        """
    )

    # Execute the INSERT statement
    cursor.execute(insert, (url, data, datetime.now(), data, datetime.now()))

    # Commit the transaction
    connection.commit()

    # Close the cursor and the connection
    cursor.close()
    connection.close()


def scrape_website(urls):
    # Scrape and insert data for each URL
    for url in urls:
        content = make_request(url)
        if not content:
            continue

        soup = parse_html(content)

        text = extract_text(soup)

        print(f"URL: {url}")
        print(text)

        insert_into_db(url, text)


if __name__ == "__main__":
    urls = ["https://brujulaem.uy/sitio/em/que-es", 
                "https://brujulaem.uy/sitio/em/que-sucede", 
                "https://brujulaem.uy/sitio/em/sintomas", 
                "https://brujulaem.uy/sitio/em/diagnostico", 
                "https://brujulaem.uy/sitio/em/tipos", 
                "https://brujulaem.uy/sitio/em/tratamiento",
                "https://brujulaem.uy/sitio/em/mi-vida",
                "https://brujulaem.uy/sitio/em/recibir_la_noticia",
                "https://brujulaem.uy/sitio/em/aceptar_mi_nueva_realidad",
                "https://brujulaem.uy/sitio/em/vivir_con_em",
                "https://brujulaem.uy/sitio/em/servicios-de-salud",
                "https://brujulaem.uy/sitio/em/especialistas",
                "https://brujulaem.uy/sitio/em/otros_especialistas",
                "https://brujulaem.uy/sitio/em/tratamiento_permanente",
                "https://brujulaem.uy/sitio/em/medicacion_neurologo",
                "https://brujulaem.uy/sitio/em/acceso_a_medicacion",
                "https://brujulaem.uy/sitio/em/costo_medicacion",
                "https://brujulaem.uy/sitio/em/acceso_a_tratamientos",
                "https://brujulaem.uy/sitio/em/tramites_acceder_tratamiento",
                "https://brujulaem.uy/sitio/em/sistema_de_acceso",
                "https://brujulaem.uy/sitio/em/plazos",
                "https://brujulaem.uy/sitio/em/formularios",
                "https://brujulaem.uy/sitio/em/servicios_sociales_comunitarios",
                "https://brujulaem.uy/sitio/em/rehabilitacion",
                "https://brujulaem.uy/sitio/em/rehabilitacion_cognitiva",
                "https://brujulaem.uy/sitio/em/rehabilitacion_fisica",
                "https://brujulaem.uy/sitio/em/apoyo_psicologico",
                "https://brujulaem.uy/sitio/em/tratamientos_complementarios"]
    scrape_website(urls)
