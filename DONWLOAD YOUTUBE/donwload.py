import yt_dlp
import os
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Função para baixar o vídeo
def baixar_video(url, qualidade):
    """Baixa o vídeo do YouTube com base na qualidade escolhida."""
    opcoes = {
        'outtmpl': os.path.join(os.getcwd(), '%(title)s.%(ext)s')
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
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            ydl.download([url])
        messagebox.showinfo("Sucesso", "✅ Download concluído com sucesso!")
    except Exception as e:
        messagebox.showerror("Erro", f"❌ Ocorreu um erro: {str(e)}")

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

    baixar_video(url, qualidade)

# Configuração da interface gráfica
app = ctk.CTk()
app.title("YouTube Downloader")
app.geometry("500x350")

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

# Botões de Ações
ctk.CTkButton(app, text="Escolher Pasta de Saída", command=escolher_pasta).pack(pady=5)
ctk.CTkButton(app, text="Iniciar Download", command=iniciar_download).pack(pady=10)

app.mainloop()