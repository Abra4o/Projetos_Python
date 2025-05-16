import yt_dlp
import whisper
import os
import re

# Função para limpar os sinais do nome do arquivo
def limparNomeArquivo(nome):
    return re.sub(r'[<>:"/\\|?*]', '_', nome)

# Link do video
link = input(str('Digite o link do vídeo do Youtube aqui: '))

# Extrai as informações do vídeo para pegar o titulo
with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
    info_dict = ydl.extract_info(link, download=False)
    video_title = info_dict.get('title', 'audio')
    nome_limpo = limparNomeArquivo(video_title)

# Definir opções de download
ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl':f'audios/{nome_limpo}.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'quiet': False,
}

# Baixar o audio do vídeo
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link])


# Trancrição do Audio
model = whisper.load_model("base")
audio_path = f'audios/{nome_limpo}.mp3'
result = model.transcribe(audio_path)

texto_transcrito = result["text"]
with open('transcricao.txt', "w", encoding="utf-8")as arquivo:
    arquivo.write(texto_transcrito)