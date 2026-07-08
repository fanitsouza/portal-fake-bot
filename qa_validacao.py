# qa_validacao.py
# Módulo de testes e validação de qualidade do Portal Fake

import time
from pathlib import Path
import pandas as pd

from botcity.web import WebBot, Browser, By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from exportacao import exportar_dados


# Configurações
INDEX_HTML = Path(r"C:\Users\Turma02\Desktop\HO7\portal_fake\index.html")
CSV_PATH = Path(r"C:\Users\Turma02\Desktop\HO7\cadastros_portal_fake_20.csv")
DELAY = 0.5


def iniciar_bot():
    bot = WebBot()
    bot.headless = False
    bot.browser = Browser.CHROME
    bot.driver_path = ChromeDriverManager().install()
    bot.start_browser()
    return bot


def abrir_portal(bot):
    url = "file:///" + str(INDEX_HTML).replace("\\", "/")
    bot.browse(url)

    WebDriverWait(bot.driver, 10).until(
        ec.presence_of_element_located((By.CSS_SELECTOR, "#btnNovo"))
    )


def executar_teste(nome_teste, funcao):
    try:
        funcao()
        print(f"[OK] {nome_teste}")
    except AssertionError as erro:
        print(f"[FALHA] {nome_teste} - {erro}")
    except Exception as erro:
        print(f"[ERRO] {nome_teste} - {erro}")


def teste_csv_existe():
    assert CSV_PATH.exists(), "Arquivo CSV não foi encontrado."


def teste_colunas_csv():
    df = pd.read_csv(CSV_PATH, dtype=str)

    colunas_esperadas = [
        "nome",
        "sobrenome",
        "cpf",
        "telefone",
        "email",
        "nascimento",
        "endereco",
        "observacao",
        "status"
    ]

    for coluna in colunas_esperadas:
        assert coluna in df.columns, f"Coluna ausente no CSV: {coluna}"


def teste_portal_abre(bot):
    abrir_portal(bot)

    bot.find_element("#btnNovo", By.CSS_SELECTOR)
    bot.find_element("#filtro", By.CSS_SELECTOR)
    bot.find_element("#btnPesquisar", By.CSS_SELECTOR)


def cadastrar_usuario_teste(bot):
    bot.find_element("#btnNovo", By.CSS_SELECTOR).click()
    time.sleep(DELAY)

    usuario = {
        "nome": "Teste",
        "sobrenome": "Qualidade",
        "cpf": "98765432109",
        "telefone": "92999999999",
        "email": "teste.qualidade@email.com",
        "nascimento": "2000-01-01",
        "endereco": "Rua de Teste",
        "observacao": "Usuário criado para teste de QA",
        "status": "ATIVO"
    }

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

    for campo_id, chave in campos:
        campo = bot.find_element(f"#{campo_id}", By.CSS_SELECTOR)
        campo.clear()
        campo.send_keys(usuario[chave])

    Select(
        bot.find_element("#f_status", By.CSS_SELECTOR)
    ).select_by_value(usuario["status"])

    bot.find_element("#btnSalvar", By.CSS_SELECTOR).click()
    time.sleep(DELAY)

    return usuario


def consultar_usuario_teste(bot, nome):
    campo = bot.find_element("#filtro", By.CSS_SELECTOR)
    campo.clear()
    campo.send_keys(nome)

    bot.find_element("#btnPesquisar", By.CSS_SELECTOR).click()
    time.sleep(DELAY)

    texto_pagina = bot.driver.find_element(By.TAG_NAME, "body").text

    return nome.lower() in texto_pagina.lower()


def teste_cadastro_e_consulta(bot):
    usuario = cadastrar_usuario_teste(bot)

    encontrado = consultar_usuario_teste(bot, usuario["nome"])

    assert encontrado, "Usuário cadastrado não foi encontrado na consulta."


def teste_exportacao():
    resultado = exportar_dados()

    assert resultado is True, "Função de exportação não retornou sucesso."


def main():
    print("Iniciando testes de qualidade do Portal Fake...\n")

    executar_teste("Verificar se o arquivo CSV existe", teste_csv_existe)
    executar_teste("Verificar colunas do arquivo CSV", teste_colunas_csv)
    executar_teste("Verificar função de exportação", teste_exportacao)

    bot = iniciar_bot()

    try:
        executar_teste("Verificar se o Portal Fake abre corretamente", lambda: teste_portal_abre(bot))
        executar_teste("Testar cadastro e consulta de usuário", lambda: teste_cadastro_e_consulta(bot))

        time.sleep(3)

    finally:
        bot.stop_browser()

    print("\nTestes finalizados.")


if __name__ == "__main__":
    main()