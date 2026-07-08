import time

import cadastro
import consulta
import exportacao


def executar_cadastro(bot):
    """
    Executa o módulo de cadastro de usuários.
    """
    print("\n[INÍCIO] Executando módulo de cadastro...")

    usuarios = cadastro.carregar_usuarios(cadastro.CSV_PATH)
    cadastro.abrir_portal(bot, cadastro.INDEX_HTML)
    cadastro.cadastrar_usuarios(bot, usuarios, cadastro.QTDE)

    print("[FIM] Módulo de cadastro concluído.")


def executar_consulta(bot):
    """
    Executa o módulo de consulta de usuários.
    """
    print("\n[INÍCIO] Executando módulo de consulta...")

    consulta.abrir_portal(bot, consulta.INDEX_HTML)

    consulta.consultar_usuario(bot, "Maria")
    consulta.consultar_usuario(bot, "João")
    consulta.consultar_usuario(bot, "Fernanda")

    print("[FIM] Módulo de consulta concluído.")


def executar_exportacao():
    """
    Executa o módulo de exportação de dados.
    """
    print("\n[INÍCIO] Executando módulo de exportação...")

    exportacao.exportar_dados()

    print("[FIM] Módulo de exportação concluído.")


def main():
    """
    Função principal responsável por orquestrar o fluxo completo do RPA.
    """
    print("==========================================")
    print("INICIANDO ORQUESTRADOR RPA - PORTAL FAKE")
    print("==========================================")

    bot = cadastro.iniciar_bot()

    try:
        executar_cadastro(bot)
        executar_consulta(bot)
        executar_exportacao()

        print("\n==========================================")
        print("PROCESSO RPA FINALIZADO COM SUCESSO")
        print("==========================================")

        time.sleep(3)

    except Exception as erro:
        print("\n[ERRO] Ocorreu uma falha durante a execução do RPA.")
        print(f"Detalhes do erro: {erro}")

    finally:
        bot.stop_browser()
        print("\nNavegador encerrado.")


if __name__ == "__main__":
    main()