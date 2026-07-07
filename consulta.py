import time
from pathlib import Path

from botcity.web import WebBot, Browser, By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Configurações
INDEX_HTML = Path(r"C:\Users\Turma02\Desktop\HO7\portal_fake\index.html")
DELAY = 0.5


def iniciar_bot():
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()
    bot.start_browser()
    return bot


def abrir_portal(bot, url_portal):
    url = "file:///" + str(url_portal).replace("\\", "/")
    bot.browse(url)

    WebDriverWait(bot.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "#filtro"))
    )


def consultar_usuario(bot, nome):
    campo = bot.find_element("#filtro", By.CSS_SELECTOR)
    campo.clear()
    campo.send_keys(nome)

    bot.find_element("#btnPesquisar", By.CSS_SELECTOR).click()
    time.sleep(DELAY)

    linhas = bot.find_elements("tbody tr", By.CSS_SELECTOR)

    if linhas:
        print(f"Usuário '{nome}' encontrado.")
    else:
        print(f"Usuário '{nome}' não encontrado.")


def main():
    bot = iniciar_bot()

    try:
        abrir_portal(bot, INDEX_HTML)

        consultar_usuario(bot, "Maria")
        consultar_usuario(bot, "João")
        consultar_usuario(bot, "Fernanda")

        time.sleep(3)

    finally:
        bot.stop_browser()


if __name__ == "__main__":
    main()