import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
CHAVE_API_GEMINI = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=CHAVE_API_GEMINI)
modelo = "gemini-2.5-flash"

def carrega(nome_do_arquivo):
  try:
    # 1. Adicionado encoding="utf-8" para o Windows não travar se o CSV tiver nomes com acento (ex: João, Márcia)
    with open(nome_do_arquivo, "r", encoding="utf-8") as arquivo:
      dados = arquivo.read()
      return dados
  except IOError as e:
    print(f"Erro: {e}") 

prompt_sistema = """
Identifique o perfil de compra para cada cliente a seguir.

O formato de saída deve ser:

cliente - descreva o perfil do cliente em 3 palavras
"""

# 2. Invertida a barra de "\" para "/" para resolver o erro "invalid escape sequence \l"
prompt_usuario = carrega("dados/lista_de_compras_100_clientes.csv")

modelo_flash = genai.GenerativeModel(f"models/{modelo}")
qtd_tokens = modelo_flash.count_tokens(prompt_usuario)

LIMITE_TOKENS = 3000
# sair de um modelo para outro
#if qtd_tokens.total_tokens >= LIMITE_TOKENS:
#   modelo = "gemini-2.5-pro"

print(f"O modelo selecionado foi: {modelo}")

llm = genai.GenerativeModel(
  model_name= modelo,
  system_instruction = prompt_sistema
)

resposta = llm.generate_content(prompt_usuario)
print(f"Resposta: {resposta.text}")