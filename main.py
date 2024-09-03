import telebot
from PIL import Image
import os

# Substitua 'YOUR_API_KEY' pelo seu token do Bot do Telegram
API_KEY = '7026407192:AAHJnf4CG_riFN0V1aM_qNv_U_vUTa-HI-A'
bot = telebot.TeleBot(API_KEY)

# Variável para armazenar a imagem atual
current_image = None

# Comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Olá! Eu sou o Shitbot. Você pode me enviar perguntas ou imagens.")

# Comando /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Use /start para começar. Você pode enviar mensagens de texto ou imagens, e eu vou tentar responder.")

# Comando /info
@bot.message_handler(commands=['info'])
def send_info(message):
    bot.reply_to(message, "Eu sou um bot de exemplo criado para interagir com você!")

# Tratamento de mensagens de texto
@bot.message_handler(content_types=['text'])
def handle_text(message):
    global current_image
    user_message = message.text.lower()

    if 'olá' in user_message or 'oi' in user_message:
        bot.reply_to(message, "Olá! Como posso ajudar você hoje?")
    elif 'tudo bem' in user_message:
        bot.reply_to(message, "Estou bem, obrigado! E com você?")
    elif 'quem é você' in user_message:
        bot.reply_to(message, "Eu sou o Shitbot, seu bot de exemplo!")
    else:
        if current_image:
            # Responder com análise fictícia da imagem
            bot.reply_to(message, f"Eu recebi sua mensagem: '{user_message}'. Estou analisando a imagem.")
        else:
            bot.reply_to(message, "Desculpe, eu não entendi. Tente perguntar outra coisa ou envie uma imagem para analisar!")

# Tratamento de imagens
@bot.message_handler(content_types=['photo'])
def handle_image(message):
    global current_image

    try:
        # Baixar a imagem enviada
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        
        # Verificar se o diretório para salvar a imagem existe
        image_path = "received_image.jpg"
        if not os.path.exists(os.path.dirname(image_path)):
            os.makedirs(os.path.dirname(image_path))

        # Salvar a imagem em disco
        with open(image_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        # Carregar a imagem com PIL
        current_image = Image.open(image_path)
        bot.reply_to(message, "Imagem recebida! Agora você pode me fazer perguntas sobre ela.")
    
    except Exception as e:
        bot.reply_to(message, f"Desculpe, ocorreu um erro ao processar a imagem: {str(e)}")

# Iniciar o bot
bot.polling()

