import yt_dlp
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import sys

# Função para verificar e instalar dependências automaticamente
def instalar_dependencias():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "yt-dlp"])
        subprocess.check_call([sys.executable, "-m", "pip", "install", "customtkinter"])
    except Exception as e:
        messagebox.showerror("Erro", f"❌ Não foi possível instalar as dependências: {str(e)}")

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
ctk.CTkButton(app, text="Instalar Dependências", command=instalar_dependencias).pack(pady=10)

# Rodar a aplicação
app.mainloop()