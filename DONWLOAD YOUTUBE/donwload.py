import yt_dlp
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import sys
import shutil
import platform
import urllib.request
import zipfile
import subprocess

# Função para instalar dependências automaticamente
def instalar_dependencias():
    try:
       
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    except Exception as e:
        messagebox.showerror("Erro", f"❌ Não foi possível instalar as dependências: {str(e)}")

# Função para instalar o FFmpeg via terminal
def instalar_ffmpeg():
    """Detecta e instala o FFmpeg automaticamente no sistema."""
    if shutil.which("ffmpeg") is not None:
         # Comando para rodar o FFmpeg (exemplo de conversão de vídeo)
        command = ['ffmpeg', '-i', 'entrada.mp4', 'saida.mp4']
        # Executando o comando em segundo plano
        subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ FFmpeg já está instalado.")
        return

    system = platform.system()

    try:
        if system == "Windows":
            # Instalação no Windows
            print("⬇️ Baixando e instalando o FFmpeg para Windows...")
            ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
            ffmpeg_zip = "ffmpeg.zip"
            urllib.request.urlretrieve(ffmpeg_url, ffmpeg_zip)

            with zipfile.ZipFile(ffmpeg_zip, "r") as zip_ref:
                zip_ref.extractall("ffmpeg_temp")

            bin_path = os.path.join("ffmpeg_temp", "ffmpeg-2023-essentials_build", "bin")
            if os.path.exists(bin_path):
                os.environ["PATH"] += os.pathsep + os.path.abspath(bin_path)
                print("✅ FFmpeg instalado com sucesso no PATH do sistema!")
            else:
                raise FileNotFoundError("Arquivos do FFmpeg não encontrados após a extração.")

            # Limpa arquivos temporários
            os.remove(ffmpeg_zip)
            shutil.rmtree("ffmpeg_temp")

        elif system == "Linux":
            # Instalação no Linux
            print("⬇️ Instalando o FFmpeg no Linux via gerenciador de pacotes...")
            subprocess.check_call(["sudo", "apt-get", "update"])
            subprocess.check_call(["sudo", "apt-get", "install", "-y", "ffmpeg"])
            print("✅ FFmpeg instalado com sucesso no Linux!")

        elif system == "Darwin":  # macOS
            # Instalação no macOS
            print("⬇️ Instalando o FFmpeg no macOS via Homebrew...")
            subprocess.check_call(["brew", "install", "ffmpeg"])
            print("✅ FFmpeg instalado com sucesso no macOS!")

        else:
            raise OSError("Sistema operacional não suportado para instalação automática do FFmpeg.")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao instalar o FFmpeg: {e}")

# Função para exibir a barra de progresso
def atualizar_progresso(dado):
    """Atualiza barra de progresso durante o download."""
    if dado['status'] == 'downloading':
        porcentagem = dado.get('downloaded_bytes', 0) / dado.get('total_bytes', 1)
        pbar.set(porcentagem)
        app.update_idletasks()  # Atualizar a interface em tempo real

# Função para baixar o vídeo
def baixar_video(url, qualidade):
    """Baixa o vídeo do YouTube com base na qualidade escolhida."""
    global barra_progresso  # Referência global para a barra de progresso
    opcoes = {
        'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s'),
        'progress_hooks': [atualizar_progresso]  # Hook para barra de progresso
    }

    if qualidade == "Alta (Melhor Qualidade)":
        opcoes['format'] = 'bestvideo+bestaudio/best'
    elif qualidade == "Média (Qualidade Média)":
        opcoes['format'] = 'worstvideo+worstaudio/worst'
    elif qualidade == "Apenas Áudio (MP3)":
        opcoes['format'] = 'bestaudio'
        opcoes['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]

    try:
        # Criar a barra de progresso ao iniciar o download
        barra_progresso.pack(pady=5)
        app.update_idletasks()

        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])

        messagebox.showinfo("Sucesso", "✅ Download concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ Ocorreu um erro: {str(e)}")
    finally:
        # Esconder a barra de progresso ao concluir ou falhar no download
        barra_progresso.pack_forget()

# Função para escolher pasta de saída
def escolher_pasta():
    pasta = filedialog.askdirectory()
    if pasta:
        os.chdir(pasta)
        messagebox.showinfo("Pasta Selecionada", f"Pasta de saída alterada para: {pasta}")

# Função para iniciar o download
def iniciar_download():
    url = entrada_url.get().strip()
    qualidade = qualidade_var.get()

    if not url:
        messagebox.showwarning("Aviso", "Por favor, insira o link do vídeo.")
        return

    if not qualidade:
        messagebox.showwarning("Aviso", "Por favor, selecione a qualidade.")
        return

    pbar.set(0)  # Zerar barra de progresso
    baixar_video(url, qualidade)

# Configuração da interface gráfica
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("500x400")

# Opções de tema
ctk.set_appearance_mode("System")  # Padrão do sistema (claro/escuro)
ctk.set_default_color_theme("blue")  # Tema padrão (azul)

# Título e Entrada do URL
ctk.CTkLabel(app, text="YouTube Downloader", font=("Arial", 20)).pack(pady=10)
ctk.CTkLabel(app, text="Digite o link do vídeo:").pack(pady=5)
entrada_url = ctk.CTkEntry(app, width=400)
entrada_url.pack(pady=5)

# Menu de Qualidade
ctk.CTkLabel(app, text="Escolha a qualidade do vídeo:").pack(pady=5)
qualidade_var = ctk.StringVar(value="Alta (Melhor Qualidade)")
qualidade_menu = ctk.CTkOptionMenu(app, variable=qualidade_var, values=[
    "Alta (Melhor Qualidade)",
    "Média (Qualidade Média)",
    "Apenas Áudio (MP3)"
])
qualidade_menu.pack(pady=5)

# Barra de Progresso (inicialmente invisível)
pbar = ctk.DoubleVar(value=0)
barra_progresso = ctk.CTkProgressBar(app, variable=pbar, width=400)

# Botões de Ações
ctk.CTkButton(app, text="Escolher Pasta de Saída", command=escolher_pasta).pack(pady=5)
ctk.CTkButton(app, text="Iniciar Download", command=iniciar_download).pack(pady=10)
ctk.CTkButton(app, text="Instalar Dependências", command=instalar_dependencias).pack(pady=5)

# Verifica e instala o FFmpeg no início
instalar_ffmpeg()

# Rodar a aplicação
app.mainloop()