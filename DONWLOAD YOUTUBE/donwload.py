import yt_dlp
import os

def baixar_video(url, qualidade):
    """Função que baixa o vídeo do YouTube com a qualidade escolhida pelo usuário."""
    
    opcoes = {}

    if qualidade == "1":
        opcoes = {'format': 'bestvideo+bestaudio/best'}  # Melhor qualidade disponível
    elif qualidade == "2":
        opcoes = {'format': 'worstvideo+worstaudio/worst'}  # Qualidade mais baixa (economiza espaço)
    elif qualidade == "3":
        opcoes = {
            'format': 'bestaudio',  # Baixa o melhor áudio disponível
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',  # Qualidade do MP3
            }]
        }

    opcoes['outtmpl'] = os.path.join(os.getcwd(), '%(title)s.%(ext)s')  # Salvar na pasta atual

    with yt_dlp.YoutubeDL(opcoes) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    while True:
        print("\n=== YouTube Downloader ===")
        link = input("Digite o link do vídeo (ou 'sair' para fechar): ").strip()

        if link.lower() == "sair":
            print("Saindo do programa...")
            break

        print("\nEscolha a qualidade do download:")
        print("1 - Melhor qualidade (vídeo e áudio)")
        print("2 - Qualidade média (menor resolução)")
        print("3 - Apenas áudio (MP3)")

        escolha = input("Digite o número da opção desejada: ").strip()

        if escolha in ["1", "2", "3"]:
            print("\nBaixando... Aguarde!")
            baixar_video(link, escolha)
            print("✅ Download concluído!\n")
        else:
            print("❌ Opção inválida. Tente novamente.")
