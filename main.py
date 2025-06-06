
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pygame # <-- Suporte para música de fundo
import requests # <-- Requesito para a API Perplexity
import json
import os

# Configurações da API Perplexity
API_KEY = ""
API_URL = "https://api.perplexity.ai/chat/completions"

# Configuração inicial do jogo
def iniciar_jogo():
    sistema_prompt = """
    Você é um mestre de RPG experiente narrando uma aventura de fantasia medieval baseado em Dungeons & Dragons. 
    O jogador já criou o seu personagem , como classe, arma, nome e habilidade especial. 
    Mantenha a narrativa envolvente, descreva cenários detalhados e faça perguntas sobre as ações do jogador.
    O jogo deve ter elementos de exploração, combate e mistério. 
    Sempre ofereça opções de ação, mas permita liberdade criativa.
    Use um estilo dramático e mantenha o ritmo da história.
    Mantenha o contexto da narrativa da história.
    O jogador pode escolher entre as seguintes classes: Guerreiro: Versátil e mestre em armas, especialista em combate corpo a corpo.|Bárbaro: Guerreiro selvagem que luta com fúria bruta e pouca armadura.|Paladino: Guerreiro sagrado que usa poderes divinos para proteger e curar.|Cavaleiro: Combatente honrado, geralmente montado, com código de conduta.|Monge: Mestre em artes marciais, rápido, disciplinado e centrado.|Mago: Usuário de magia arcana estudada, poderoso mas fisicamente frágil.|Feiticeiro: Canaliza magia inata, geralmente com linhagem mágica.|Bruxo: Faz pacto com entidades para obter poder mágico sombrio.|Clérigo: Servo divino que cura, protege e luta em nome de um deus.|Druida: Guardião da natureza que usa magias naturais e se transforma em animais.|Ladino: Mestre da furtividade, armadilhas, truques e ataques precisos.|Bardo: Usuário de música mágica, versátil no combate e na diplomacia.|Patrulheiro: Caçador e rastreador do mato, excelente com arco e natureza.|Caçador de Recompensas: Especialista em caçar alvos específicos, furtivo e letal.|Ninja: Combatente veloz e furtivo, mestre em ataques surpresa.|Assassino: Perito em eliminar alvos rapidamente, usa venenos e táticas furtivas.|Artífice: Inventor mágico que usa engenhocas, armadilhas e itens mágicos.|Alquimista: Mestre de poções, explosivos e transmutações químicas.|Oráculo: Canal espiritual com visões do futuro, poderes únicos e maldições.|Xamã: Mediador entre espíritos e o mundo físico, usa magias tribais.|Invocador: Conjura e controla criaturas mágicas para lutar por ele.|Psíquico: Usa o poder da mente para controlar, manipular ou prever.|Necromante: Controla mortos-vivos e usa magias sombrias de morte.|Samurai: Guerreiro disciplinado com estilo de combate focado e honra.|Pirata: Combatente ágil do mar, usa táticas sujas e armas exóticas.|Gunslinger: Especialista em armas de fogo, rápido e letal a distância.
    """

    historico = [{"role": "system", "content": sistema_prompt}]

    # Carregar personagem salvo, se existir

    if os.path.exists("personagem_salvo.json"):
        try:
            with open("personagem_salvo.json", "r", encoding="utf-8") as f:
                dados = json.load(f)
                personagem_info.update({
                    "nome": dados.get("nome", "-"),
                    "classe": dados.get("classe", "-"),
                    "arma": dados.get("arma", "-"),
                    "habilidade": dados.get("habilidade", "-")
                })
                # Atualiza status
                hp_var.set(dados.get("hp", 100))
                mp_var.set(dados.get("mp", 50))
                xp_var.set(dados.get("xp", 0))
                atualizar_info_personagem()

            primeira_mensagem = "Olá jogador! Bem-vindo de volta ao mundo de Dungeons & Pythons. Vamos continuar sua aventura!\n\n"
            atualizar_interface(primeira_mensagem)
        except Exception as e:
            print(f"Erro ao carregar personagem salvo: {e}")
    else:
        primeira_mensagem = "Olá jogador! Bem-vindo ao mundo de Dungeons & Pythons. Vamos montar seu personagem!\n\n" \
                            "Por favor, escolha Personagem no menu acima e escolha Criar Personagem.\n" \
                            "Depois disso, você poderá começar a aventura!\n\n"
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

def definir_icone():
    try:
        icone = tk.PhotoImage(file="img/logo.png")
        root.iconphoto(False, icone)
    except Exception as e:
        print(f"Erro ao definir ícone: {e}")

# Janela de criação de personagem
personagem_info = {}

def janela_personagem():
    janela = tk.Toplevel(root)
    janela.title("Criação de Personagem")
    janela.geometry("300x320")

    nome_label = tk.Label(janela, text="Nome do Personagem:")
    nome_label.pack(pady=(10, 0))
    nome_entry = tk.Entry(janela)
    nome_entry.pack(pady=(0, 10))

    classe_label = tk.Label(janela, text="Classe:")
    classe_label.pack(pady=(10, 0))
    classeEscolhida = tk.StringVar()
    classes = (
        'Guerreiro',
        'Bárbaro',
        'Paladino',
        'Cavaleiro',
        'Monge',
        'Mago',
        'Feiticeiro',
        'Bruxo',
        'Clérigo',
        'Druida',
        'Ladino',
        'Bardo',
        'Patrulheiro',
        'Caçador de Recompensas',
        'Ninja',
        'Assassino',
        'Artífice',
        'Alquimista',
        'Oráculo',
        'Xamã',
        'Invocador',
        'Psíquico',
        'Necromante',
        'Samurai',
        'Pirata',
        'Gunslinger',
    )
    classeEscolhida.set(classes[0])
    classesCombo = ttk.Combobox(janela, width=27, textvariable=classeEscolhida, values=classes)
    classesCombo.current(0)
    classesCombo.pack(pady=(0, 10))

    arma_label = tk.Label(janela, text="Arma:")
    arma_label.pack(pady=(10, 0))
    armaEscolhida = tk.StringVar()
    armasList = (
        ' Espada Longa ' ,
        ' Espada Curta ' ,
        ' Machado de Guerra ' ,
        ' Martelo de Guerra ' ,
        ' Lança ' ,
        ' Adagas ' ,
        ' Katanas ' ,
        ' Bastão ' ,
        ' Besta ' ,
        ' Fundas ' ,
        ' Mosquete ' ,
        ' Rifle Arcano ' ,
        ' Pistolas Duplas ' ,
        ' Cajado Arcano ' ,
        ' Orbe Mágico ' ,
        ' Chicote ' ,
        ' Foice Sombria ' ,
        ' Manoplas Encantadas ' ,
        ' Lâmina de Energia ' ,
    )
    armaEscolhida.set(armasList[0])
    armaCombo = ttk.Combobox(janela, width=27, textvariable=armaEscolhida, values=armasList)
    armaCombo.current(0)
    armaCombo.pack(pady=(0, 10))

    habilidade_label = tk.Label(janela, text="Habilidade Especial:")
    habilidade_label.pack(pady=(10, 0))
    habilidadeEscolhida = tk.StringVar()
    habilidadesList = (
        ' Golpe Crítico ' ,
        ' Furtividade ' ,
        ' Magia Arcana ' ,
        ' Regeneração ' ,
        ' Escudo Mágico ' ,
        ' Invocação ' ,
        ' Metamorfose ' ,
        ' Aura Divina ' ,
        ' Teletransporte ' ,
        ' Ataque Sombrio ' ,
        ' Fúria Bárbara ' ,
        ' Agilidade Felina ' ,
        ' Controle Elemental ' ,
        ' Maldição ' ,
        ' Visão Mística ' ,
        ' Manipulação Mental ' ,
        ' Disparo Preciso ' ,
        ' Golpe Fantasma ' ,
        ' Domínio das Sombras ' ,
        ' Inspiração de Bardo ' ,
        ' Resiliência ' ,
        ' Maestria Marcial ' ,
        ' Explosão Arcana ' ,
        ' Defesa Absoluta ' ,
        ' Ritual de Cura ' ,
        ' Dança da Lâmina ' ,
        ' Golpe Relâmpago ' ,
        ' Invocação Espiritual ' ,
        ' Proteção Ancestral ' ,
        ' Fogo Infernal ' ,
        ' Controle Temporal ' ,
        ' Veneno Mortal ' ,
        ' Ilusão Perfeita ' ,
        ' Voz Encantadora ' ,
        ' Domínio do Caos ' ,
        ' Concentração Suprema ' ,
        ' Armadura Viva ' ,
    )
    classeEscolhida.set(habilidadesList[0])
    habilidadeCombo = ttk.Combobox(janela, width=27, textvariable=habilidadeEscolhida, values=habilidadesList)
    habilidadeCombo.current(0)
    habilidadeCombo.pack(pady=(0, 10))

    def criar_personagem():
        nome = nome_entry.get()
        classe = classeEscolhida.get()
        arma = armaEscolhida.get()
        habilidade = habilidadeEscolhida.get()

        if not (nome and classe and arma and habilidade):
            atualizar_interface("Por favor, preencha todos os campos.")
            return

        global personagem_info
        personagem_info = {
            "nome": nome,
            "classe": classe,
            "arma": arma,
            "habilidade": habilidade
        }

        mensagem_criacao = f"Seu personagem {nome} é um(a) {classe} que usa uma {arma} e tem a habilidade especial {habilidade}."
        atualizar_interface(mensagem_criacao)
        atualizar_info_personagem()
        janela.destroy()

    criar_btn = tk.Button(janela, text="Criar Personagem", command=criar_personagem)
    criar_btn.pack(pady=(10, 0))

# Configuração da janela principal
root = tk.Tk()
root.title("Dungeons & Pythons")

definir_icone()

historico = None

title_label = tk.Label(
    root,
    text="Dungeons & Pythons",
    font=("Helvetica", 18, "bold"),
    anchor="center"
)
title_label.pack(pady=(20, 0))

menubar = tk.Menu(root)
root.config(menu=menubar)

menu_menu = tk.Menu(menubar, tearoff=0)
menu_menu.add_command(label="Sair", command=root.quit)
menubar.add_cascade(label="Menu", menu=menu_menu)

personagem_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Personagem", menu=personagem_menu)
personagem_menu.add_command(label="Criar Personagem", command=janela_personagem)

sobre_menu = tk.Menu(menubar, tearoff=0)
menubar.add_cascade(label="Sobre", menu=sobre_menu)

# Frame principal para dividir a área de texto e o painel de informações
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=(10, 5), fill='both', expand=True)

# Área de texto (narrativa)
top_text = tk.Text(main_frame, height=8, width=40, state='disabled', wrap='word')
top_text.pack(side=tk.LEFT, fill='both', expand=True)

# Painel de informações do personagem
info_frame = tk.Frame(main_frame, width=200, bg="#eee")
info_frame.pack(side=tk.RIGHT, fill='y', padx=(10, 0))

# Labels para informações do personagem
nome_var = tk.StringVar(value="Nome: -")
classe_var = tk.StringVar(value="Classe: -")
arma_var = tk.StringVar(value="Arma: -")
habilidade_var = tk.StringVar(value="Habilidade: -")

tk.Label(info_frame, textvariable=nome_var, anchor='w', bg="#eee").pack(fill='x', pady=(5,0))
tk.Label(info_frame, textvariable=classe_var, anchor='w', bg="#eee").pack(fill='x')
tk.Label(info_frame, textvariable=arma_var, anchor='w', bg="#eee").pack(fill='x')
tk.Label(info_frame, textvariable=habilidade_var, anchor='w', bg="#eee").pack(fill='x')

# Função para atualizar painel de informações
def atualizar_info_personagem():
    nome_var.set(f"Nome: {personagem_info.get('nome', '-')}")
    classe_var.set(f"Classe: {personagem_info.get('classe', '-')}")
    arma_var.set(f"Arma: {personagem_info.get('arma', '-')}")
    habilidade_var.set(f"Habilidade: {personagem_info.get('habilidade', '-')}")
    hp_var.set(100)
    mp_var.set(50)
    xp_var.set(0)

    # Salvar informações do personagem e status em um arquivo JSON
    dados = {
        "nome": personagem_info.get('nome', '-'),
        "classe": personagem_info.get('classe', '-'),
        "arma": personagem_info.get('arma', '-'),
        "habilidade": personagem_info.get('habilidade', '-'),
        "hp": hp_var.get(),
        "mp": mp_var.get(),
        "xp": xp_var.get()
    }
    try:
        with open("personagem_salvo.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Erro ao salvar personagem: {e}")

# Barras de status (HP, MP, XP)
def criar_barra_status(parent, texto, var):
    frame = tk.Frame(parent, bg="#eee")
    frame.pack(fill='x', pady=(10,0))
    tk.Label(frame, text=texto, bg="#eee").pack(anchor='w')
    barra = ttk.Progressbar(frame, orient='horizontal', length=120, mode='determinate', variable=var, maximum=100)
    barra.pack(fill='x', padx=5)
    return barra

hp_var = tk.IntVar(value=0)
mp_var = tk.IntVar(value=0)
xp_var = tk.IntVar(value=0)

hp_bar = criar_barra_status(info_frame, "HP", hp_var)
mp_bar = criar_barra_status(info_frame, "MP", mp_var)
xp_bar = criar_barra_status(info_frame, "XP", xp_var)

# Atualizar barras de status (exemplo de função, pode ser chamada conforme o jogo evolui)
def atualizar_status(hp=None, mp=None, xp=None):
    if hp is not None:
        hp_var.set(hp)
    if mp is not None:
        mp_var.set(mp)
    if xp is not None:
        xp_var.set(xp)

# Main

def solicitar_api_key():
    def confirmar():
        key = entry.get().strip()
        if not key:
            messagebox.showerror("Erro", "A chave da API não pode ser vazia.")
            root.destroy()
        else:
            global API_KEY
            API_KEY = key
            janela.destroy()

    import tkinter.messagebox
    janela = tk.Toplevel(root)
    janela.title("API Key Perplexity")
    janela.geometry("350x120")
    janela.grab_set()
    janela.resizable(False, False)
    tk.Label(janela, text="Informe sua API Key do Perplexity:").pack(pady=(15, 5))
    entry = tk.Entry(janela, width=40)
    entry.pack(pady=(0, 10))
    entry.focus_set()
    btn = tk.Button(janela, text="Ok", command=confirmar, width=10)
    btn.pack(pady=(0, 10))
    janela.protocol("WM_DELETE_WINDOW", lambda: (messagebox.showerror("Erro", "A chave da API é obrigatória."), root.destroy()))
    root.wait_window(janela)

solicitar_api_key()

bottom_text = tk.Text(root, height=2, width=40, wrap='word')
bottom_text.pack(padx=10, pady=(0, 10), fill='x')

button_frame = tk.Frame(root)
button_frame.pack(pady=(0, 10), fill='x')

bottom_text.bind("<Return>", lambda event: (enviar(), "break")) 

enviar_btn = tk.Button(button_frame, text="Enviar", command=enviar, width=12)
enviar_btn.pack(side=tk.LEFT, padx=(0, 5))

limpar_btn = tk.Button(button_frame, text="Limpar", command=limpar, width=12)
limpar_btn.pack(side=tk.LEFT)

musica_var = tk.BooleanVar(value=False)
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

# Manter o programa em execução
root.mainloop()
