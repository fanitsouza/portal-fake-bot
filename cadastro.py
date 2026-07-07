import time
from pathlib import Path
import pandas as pd

from botcity.web import WebBot, Browser, By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# Configurações
INDEX_HTML = Path(r"C:\Users\Turma02\Desktop\HO7\portal_fake\index.html")
CSV_PATH = Path(r"C:\Users\Turma02\Desktop\HO7\cadastros_portal_fake_20.csv")
QTDE = None
DELAY = 0.5


def carregar_usuarios(csv_path):
    df = pd.read_csv(csv_path, dtype=str)
    return df.to_dict(orient="records")


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
        ec.presence_of_element_located((By.CSS_SELECTOR, "#btnNovo"))
    )


def cadastrar_usuario(bot, usuario):
    bot.find_element("#btnNovo", By.CSS_SELECTOR).click()
    time.sleep(DELAY)

    campos = [
        ("f_nome", "nome"),
        ("f_sobrenome", "sobrenome"),
        ("f_cpf", "cpf"),
        ("f_telefone", "telefone"),
        ("f_email", "email"),
        ("f_nascimento", "nascimento"),
        ("f_endereco", "endereco"),
        ("f_observacao", "observacao"),
    ]

    for campo_id, coluna in campos:
        campo = bot.find_element(f"#{campo_id}", By.CSS_SELECTOR)
        campo.clear()
        campo.send_keys(str(usuario[coluna]))

    Select(
        bot.find_element("#f_status", By.CSS_SELECTOR)
    ).select_by_value(usuario["status"])

    bot.find_element("#btnSalvar", By.CSS_SELECTOR).click()
    time.sleep(DELAY)


def cadastrar_usuarios(bot, usuarios, qtd=None):
    lista = usuarios[:qtd] if qtd else usuarios

    for i, usuario in enumerate(lista, start=1):
        print(f"Cadastrando {i}/{len(lista)}: {usuario['nome']} {usuario['sobrenome']}")
        cadastrar_usuario(bot, usuario)

    print("Cadastros concluídos.")


def main():
    usuarios = carregar_usuarios(CSV_PATH)
    bot = iniciar_bot()

    try:
        abrir_portal(bot, INDEX_HTML)
        cadastrar_usuarios(bot, usuarios, QTDE)
        time.sleep(3)
    finally:
        bot.stop_browser()


if __name__ == "__main__":
    main()