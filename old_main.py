import tkinter as tk
import pygame
import requests
import json

# Configurações da API Perplexity
API_KEY = "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"  # Obtenha em: https://pplx.ai/
API_URL = "https://api.perplexity.ai/chat/completions"

# Configuração inicial do jogo
def iniciar_jogo():
    sistema_prompt = """
    Você é um mestre de RPG experiente narrando uma aventura de fantasia medieval. 
    O jogador está controlando um guerreiro humano chamado Arthas. 
    Mantenha a narrativa envolvente, descreva cenários detalhados e faça perguntas sobre as ações do jogador.
    O jogo deve ter elementos de exploração, combate e mistério. 
    Sempre ofereça opções de ação, mas permita liberdade criativa.
    Use um estilo dramático e mantenha o ritmo da história.
    """
    
    historico = [{"role": "system", "content": sistema_prompt}]
    
    primeira_mensagem = "Você acorda em uma masmorra escura e úmida. A luz fraca entra por uma grade no alto das paredes de pedra. O que você faz?"
    historico.append({"role": "assistant", "content": primeira_mensagem})
    
    atualizar_interface(primeira_mensagem)
    return historico

def perguntar_ia(historico, mensagem_jogador):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    historico_temp = historico + [{"role": "user", "content": mensagem_jogador}]

    data = {
        "model": "sonar",  # modelo correto
        "messages": historico_temp,
        "max_tokens": 1000,
        "temperature": 0.7
    }

    try:
        resposta = requests.post(API_URL, headers=headers, json=data)
        resposta_json = resposta.json()

        if resposta.status_code == 200 and "choices" in resposta_json and resposta_json["choices"]:
            conteudo_resposta = resposta_json["choices"][0].get("message", {}).get("content", "")
            if conteudo_resposta:
                historico.append({"role": "assistant", "content": conteudo_resposta})
                return conteudo_resposta
            else:
                return "Erro na API: Resposta inesperada do modelo."
        else:
            # Mostra mensagem de erro detalhada
            return f"Erro na API: {resposta_json}"
    except Exception as e:
        return f"Erro na conexão: {str(e)}"

def atualizar_interface(texto):
    top_text.config(state='normal')
    top_text.insert(tk.END, "\nMestre: " + texto + "\n")
    top_text.see(tk.END)
    top_text.config(state='disabled')

def enviar():
    user_input = bottom_text.get("1.0", tk.END).strip()
    if not user_input:
        return
    
    # Atualiza a interface do usuário
    top_text.config(state='normal')
    top_text.insert(tk.END, "\nJogador: " + user_input + "\n")
    top_text.config(state='disabled')
    bottom_text.delete("1.0", tk.END)
    
    # Processa a resposta da IA
    resposta_ia = perguntar_ia(historico, user_input)
    atualizar_interface(resposta_ia)

def limpar():
    bottom_text.delete("1.0", tk.END)

# Configuração da janela principal
root = tk.Tk()
root.title("Dungeons & Pythons")

# Variável global para o histórico
historico = None  # será inicializado após a criação dos widgets

# Elementos da interface
title_label = tk.Label(
    root,
    text="Dungeons & Pythons",
    font=("Helvetica", 18, "bold"),
    anchor="center"
)
title_label.pack(pady=(20, 0))

top_text = tk.Text(root, height=8, width=40, state='disabled', wrap='word')
top_text.pack(padx=10, pady=(10, 5), fill='both', expand=True)

bottom_text = tk.Text(root, height=2, width=40, wrap='word')
bottom_text.pack(padx=10, pady=(0, 10), fill='x')

button_frame = tk.Frame(root)
button_frame.pack(pady=(0, 10), fill='x')

enviar_btn = tk.Button(button_frame, text="Enviar", command=enviar, width=12)
enviar_btn.pack(side=tk.LEFT, padx=(0, 5))

limpar_btn = tk.Button(button_frame, text="Limpar", command=limpar, width=12)
limpar_btn.pack(side=tk.LEFT)

# Configuração de música
musica_var = tk.BooleanVar(value=True)
checkbox = tk.Checkbutton(root, text="Ativar musica", variable=musica_var)
checkbox.pack(pady=(0, 10), anchor='w', padx=10)

pygame.mixer.init()

# Inicializa o histórico após os widgets necessários existirem
historico = iniciar_jogo()

def toggle_music():
    if musica_var.get():
        pygame.mixer.music.load("audio/theme.wav")
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

musica_var.trace_add("write", lambda *args: toggle_music())
toggle_music()

# Configurações visuais
root.geometry("640x480")
root.minsize(640, 480)
root.configure(bg="#593818")

title_label.config(bg="#593818", fg="#ffffff")
top_text.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
bottom_text.config(bg="#ffffff", fg="#000000", insertbackground="#000000")
button_frame.config(bg="#593818")
enviar_btn.config(bg="#3d2812", fg="#ffffff", activebackground="#7a4f2a", activeforeground="#ffffff")
limpar_btn.config(bg="#3d2812", fg="#ffffff", activebackground="#7a4f2a", activeforeground="#ffffff")
checkbox.config(bg="#593818", fg="#ffffff", selectcolor="#593818", activebackground="#593818", activeforeground="#ffffff")

root.mainloop()
