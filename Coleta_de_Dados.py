from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_selectors():
    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        url = "https://www.vivareal.com.br/venda/ceara/eusebio/lote-terreno_residencial/"
        logger.info(f"Acessando URL: {url}")
        driver.get(url)
        
        # Espera inicial
        time.sleep(10)
        logger.info("Página carregada")

        # Verifica classe do container principal
        logger.info("Procurando container principal...")
        containers = driver.find_elements(By.CSS_SELECTOR, '[data-type]')
        logger.info(f"Classes encontradas nos containers: {[c.get_attribute('class') for c in containers]}")
        
        # Verifica propriedades dos imóveis
        logger.info("Procurando elementos de imóveis...")
        properties = driver.find_elements(By.CSS_SELECTOR, '[data-type="property"]')
        logger.info(f"Número de propriedades encontradas: {len(properties)}")
        
        if properties:
            first_property = properties[0]
            logger.info("Analisando primeira propriedade...")
            
            # Imprime toda a estrutura HTML da primeira propriedade
            html = first_property.get_attribute('outerHTML')
            logger.info(f"HTML da primeira propriedade:\n{html}")
            
            # Testa diferentes seletores
            selectors = {
                'título': 'span.property-card__title',
                'preço': 'div.property-card__price',
                'área': 'span.property-card__detail-area',
                'endereço': 'span.property-card__address',
                'link': 'a.property-card__content-link'
            }
            
            for name, selector in selectors.items():
                try:
                    element = first_property.find_element(By.CSS_SELECTOR, selector)
                    logger.info(f"{name} encontrado: {element.text}")
                except Exception as e:
                    logger.error(f"Erro ao encontrar {name}: {str(e)}")

    except Exception as e:
        logger.error(f"Erro durante o teste: {str(e)}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_selectors()
