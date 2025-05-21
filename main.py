
import tkinter as tk
import pygame
import requests
import json

# Configurações da API Perplexity
API_KEY = ""
API_URL = "https://api.perplexity.ai/chat/completions"

# Configuração inicial do jogo
def iniciar_jogo():
    sistema_prompt = """
    Você é um mestre de RPG experiente narrando uma aventura de fantasia medieval baseado em Dungeons & Dragons. 
    O jogador tem a opção de montar o seu personagem antes de começar o jogo, como classe, arma, nome e habilidade especial. 
    Mantenha a narrativa envolvente, descreva cenários detalhados e faça perguntas sobre as ações do jogador.
    O jogo deve ter elementos de exploração, combate e mistério. 
    Sempre ofereça opções de ação, mas permita liberdade criativa.
    Use um estilo dramático e mantenha o ritmo da história.
    Mantenha o contexto da narrativa da história.
    as classes disponiveis são: Guerreiro: Versátil e mestre em armas, especialista em combate corpo a corpo.|Bárbaro: Guerreiro selvagem que luta com fúria bruta e pouca armadura.|Paladino: Guerreiro sagrado que usa poderes divinos para proteger e curar.|Cavaleiro: Combatente honrado, geralmente montado, com código de conduta.|Monge: Mestre em artes marciais, rápido, disciplinado e centrado.|Mago: Usuário de magia arcana estudada, poderoso mas fisicamente frágil.|Feiticeiro: Canaliza magia inata, geralmente com linhagem mágica.|Bruxo: Faz pacto com entidades para obter poder mágico sombrio.|Clérigo: Servo divino que cura, protege e luta em nome de um deus.|Druida: Guardião da natureza que usa magias naturais e se transforma em animais.|Ladino: Mestre da furtividade, armadilhas, truques e ataques precisos.|Bardo: Usuário de música mágica, versátil no combate e na diplomacia.|Patrulheiro: Caçador e rastreador do mato, excelente com arco e natureza.|Caçador de Recompensas: Especialista em caçar alvos específicos, furtivo e letal.|Ninja: Combatente veloz e furtivo, mestre em ataques surpresa.|Assassino: Perito em eliminar alvos rapidamente, usa venenos e táticas furtivas.|Artífice: Inventor mágico que usa engenhocas, armadilhas e itens mágicos.|Alquimista: Mestre de poções, explosivos e transmutações químicas.|Oráculo: Canal espiritual com visões do futuro, poderes únicos e maldições.|Xamã: Mediador entre espíritos e o mundo físico, usa magias tribais.|Invocador: Conjura e controla criaturas mágicas para lutar por ele.|Psíquico: Usa o poder da mente para controlar, manipular ou prever.|Necromante: Controla mortos-vivos e usa magias sombrias de morte.|Samurai: Guerreiro disciplinado com estilo de combate focado e honra.|Pirata: Combatente ágil do mar, usa táticas sujas e armas exóticas.|Gunslinger: Especialista em armas de fogo, rápido e letal a distância.
    """

    historico = [{"role": "system", "content": sistema_prompt}]

    primeira_mensagem = "Olá jogador! Bem-vindo ao mundo de Dungeons & Pythons. Vamos montar seu personagem!\n\n" \
                        "Por favor, me diga as seguintes informações:\n\n*Nome do seu personagem:\n*Classe que você gostaria de jogar (guerreiro, mago, ladrão, etc.)\n" \
                        "*Arma que você deseja usar\n*Uma habilidade especial que você gostaria de ter."
    #historico.append({"role": "assistant", "content": primeira_mensagem})

    atualizar_interface(primeira_mensagem)
    return historico

def perguntar_ia(historico, mensagem_jogador):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    historico_temp = historico + [{"role": "user", "content": mensagem_jogador}]

    print(historico_temp)

    data = {
        "model": "sonar",
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
                historico.append({"role": "system", "content": conteudo_resposta})
                return conteudo_resposta
            else:
                return "Erro na API: Resposta inesperada do modelo."
        else:
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

    top_text.config(state='normal')
    top_text.insert(tk.END, "\nJogador: " + user_input + "\n")
    top_text.config(state='disabled')
    bottom_text.delete("1.0", tk.END)

    resposta_ia = perguntar_ia(historico, user_input)
    atualizar_interface(resposta_ia)

def limpar():
    bottom_text.delete("1.0", tk.END)

# Configuração da janela principal
root = tk.Tk()
root.title("Dungeons & Pythons")

historico = None

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

bottom_text.bind("<Return>", lambda event: (enviar(), "break"))

enviar_btn = tk.Button(button_frame, text="Enviar", command=enviar, width=12)
enviar_btn.pack(side=tk.LEFT, padx=(0, 5))

limpar_btn = tk.Button(button_frame, text="Limpar", command=limpar, width=12)
limpar_btn.pack(side=tk.LEFT)

musica_var = tk.BooleanVar(value=True)
checkbox = tk.Checkbutton(root, text="Ativar musica", variable=musica_var)
checkbox.pack(pady=(0, 10), anchor='w', padx=10)

pygame.mixer.init()

historico = iniciar_jogo()

def toggle_music():
    if musica_var.get():
        pygame.mixer.music.load("audio/theme.wav")
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()

musica_var.trace_add("write", lambda *args: toggle_music())
toggle_music()

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
