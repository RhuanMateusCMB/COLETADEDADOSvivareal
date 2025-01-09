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
    options.add_argument('--disable-blink-features=AutomationControlled')

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)  # Aumentado para 30 segundos

    try:
        url = "https://www.vivareal.com.br/venda/ceara/eusebio/lote-terreno_residencial/"
        logger.info(f"Acessando URL: {url}")
        driver.get(url)
        
        # Espera inicial mais longa
        time.sleep(20)
        logger.info("Página carregada")

        # Tenta diferentes seletores para encontrar os imóveis
        selectors_to_try = [
            'article.property-card',  # Novo possível seletor
            'div[data-type="property"]',  # Seletor antigo
            'div.property-card',  # Alternativa
            'div.results-list article'  # Outra alternativa
        ]

        for selector in selectors_to_try:
            logger.info(f"Tentando seletor: {selector}")
            properties = driver.find_elements(By.CSS_SELECTOR, selector)
            logger.info(f"Elementos encontrados com {selector}: {len(properties)}")

        # Procura elementos específicos na página
        logger.info("Procurando elementos específicos...")
        specific_elements = [
            ('.results-list', 'Lista de resultados'),
            ('.results-summary', 'Resumo de resultados'),
            ('.js-card-list', 'Lista de cards'),
            ('article', 'Articles'),
            ('.property-card', 'Cards de propriedade')
        ]

        for selector, name in specific_elements:
            elements = driver.find_elements(By.CSS_SELECTOR, selector)
            logger.info(f"{name} encontrados: {len(elements)}")

        # Captura e loga a estrutura da página
        logger.info("Estrutura do DOM principal:")
        main_content = driver.find_element(By.TAG_NAME, 'main')
        logger.info(main_content.get_attribute('outerHTML'))

        # Verifica se há algum elemento de loading ou bloqueio
        loading_elements = driver.find_elements(By.CSS_SELECTOR, '[class*="loading"], [class*="block"]')
        if loading_elements:
            logger.info("Elementos de loading/bloqueio encontrados:")
            for elem in loading_elements:
                logger.info(f"Classe: {elem.get_attribute('class')}")

    except Exception as e:
        logger.error(f"Erro durante o teste: {str(e)}")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    test_selectors()
