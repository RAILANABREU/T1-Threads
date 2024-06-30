import tkinter as tk
from threading import Thread, Lock
import random
import time

lancador_0_cima = [
    "   ||   ",
    "___++___",
]

lancador_135_cima = [
    "   \\    ",
    "___++___",
]

lancador_45_cima = [
    "   / /   ",
    "___++___",
]

lancador_90_direita = [
    "   >>   ",
    "___++___",

]

lancador_90_esquerda = [
    "   <<   ",
    "___++___",

]

nave = [
"     __/)     (\__     ",
"  ,-'~~(   _   )~~`-.  ",
" /      \/'_`\/      \ ",
"|       /_(_)_\       |",
"|     _(/(\_/)\)_     |",
"|    / // \ / \\ \    |",
 "\  | ``  / \ ''  |  / ",
 " \  )   /   \   (  /  ",
 "  )/   /     \   \(   ",
 "  '    `-`-'-'    `   ",

]

foguetes = ["*"]



# Parâmetros de dificuldade
dificuldade = {
    'facil': {'n_foguetes': 20, 'velocidade_naves': 5, 'qtd_naves': 10},
    'medio': {'n_foguetes': 15, 'velocidade_naves': 3, 'qtd_naves': 15},
    'dificil': {'n_foguetes': 10, 'velocidade_naves': 1, 'qtd_naves': 20}
}

# Configuração inicial
config = dificuldade['medio']
n_foguetes = config['n_foguetes']
velocidade_naves = config['velocidade_naves']
qtd_naves = config['qtd_naves']

# Inicialização de variáveis globais
foguetes_disponiveis = n_foguetes
foguetes_disparados = []
naves = []
mutex = Lock()

# Inicialização da interface do jogo
root = tk.Tk()
root.title("Jogo de Defesa de Naves")
canvas = tk.Canvas(root, width=800, height=600, bg='black')
canvas.pack()

# Mostrador de foguetes disponíveis
label_foguetes = tk.Label(root, text=f"Foguetes Disponíveis: {foguetes_disponiveis}", fg='white', bg='black')
label_foguetes.pack()

# Configuração inicial do lançador
lancador_pos = 400
direcao_lancador = 'vertical'

def atualizar_mostrador_foguetes():
    label_foguetes.config(text=f"Foguetes Disponíveis: {foguetes_disponiveis}")

# Função para criar a interface do jogo
def criar_interface():
    global canvas, lancador_pos, direcao_lancador
    canvas.delete("all")
    # Canhão representado como um retângulo
    canhao_repres = {
        'vertical': "||",
        'esquerda': "<<",
        'direita': ">>",
        'diagonal_esquerda': "\\",
        'diagonal_direita': "//"
    }
    # Desenhar o lançador
    canvas.create_rectangle(lancador_pos - 10, 580, lancador_pos + 10, 600, fill='white')
    # Desenhar a ponta do lançador
    canvas.create_text(lancador_pos, 570, text=canhao_repres[direcao_lancador], font=('Courier', 12), fill='white')
    root.update()

def agendar_atualizacao():
    global foguetes_disparados, naves
    canvas.delete("all")
    # Desenhar o lançador
    canhao_repres = {
        'vertical': "||",
        'esquerda': "<<",
        'direita': ">>",
        'diagonal_esquerda': "\\",
        'diagonal_direita': "//"
    }
    canvas.create_rectangle(lancador_pos - 10, 580, lancador_pos + 10, 600, fill='white')
    canvas.create_text(lancador_pos, 570, text=canhao_repres[direcao_lancador], font=('Courier', 12), fill='white')
    # Desenhar os foguetes disparados
    for foguete in foguetes_disparados:
        foguete.desenhar(canvas)
    # Desenhar as naves
    for nave in naves:
        nave.desenhar(canvas)
    root.update()

def atualizar_interface():
    root.after(50, agendar_atualizacao)

# Classe para representar as naves
class Nave:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.viva = True

    def mover(self):
        self.y += velocidade_naves

    def desenhar(self, canvas):
        if self.viva:
            canvas.create_rectangle(self.x - 10, self.y - 10, self.x + 10, self.y + 10, fill='blue')

# Função para gerar naves de forma aleatória
def gerar_naves_aleatoriamente():
    global naves
    while len(naves) < qtd_naves:
        time.sleep(random.randint(1, 5))  # Intervalo aleatório entre 1 e 5 segundos
        with mutex:
            x = random.randint(20, 780)
            naves.append(Nave(x))

# Classe para representar os foguetes
class Foguete:
    def __init__(self, x, y, direcao):
        self.x = x
        self.y = y
        self.direcao = direcao
        self.ativo = True
        self.representacao = self.escolher_representacao(direcao)

    def mover(self):
        if self.direcao == 'vertical':
            self.y -= 10
        elif self.direcao == 'diagonal_esquerda':
            self.x -= 7
            self.y -= 7
        elif self.direcao == 'diagonal_direita':
            self.x += 7
            self.y -= 7
        elif self.direcao == 'esquerda':
            self.x -= 10
        elif self.direcao == 'direita':
            self.x += 10
        if self.y < 0 or self.x < 0 or self.x > 800:
            self.ativo = False

    def escolher_representacao(self, direcao):
        if direcao == 'vertical':
            return "     | |\n__+ +__"
        elif direcao == 'diagonal_esquerda':
            return "     \\ \n__+ +__"
        elif direcao == 'diagonal_direita':
            return "     / /\n__+ +__"
        elif direcao == 'esquerda':
            return "    <<\n__+ +__"
        elif direcao == 'direita':
            return "    >>\n__+ +__"

    def desenhar(self, canvas):
        if self.ativo:
            canvas.create_text(self.x, self.y, text=self.representacao, font=('Courier', 10), fill='red')

# Função para disparar foguetes
def disparar_foguete():
    global foguetes_disponiveis, foguetes_disparados, lancador_pos, direcao_lancador, mutex
    with mutex:
        if foguetes_disponiveis > 0:
            foguetes_disponiveis -= 1
            foguete = Foguete(lancador_pos, 580, direcao_lancador)
            foguetes_disparados.append(foguete)
            atualizar_mostrador_foguetes()

# Função para capturar e processar as entradas do jogador
def mover_lancador(event):
    global lancador_pos, direcao_lancador
    if event.keysym == 'Left' and lancador_pos > 20:
        lancador_pos -= 20
    elif event.keysym == 'Right' and lancador_pos < 780:
        lancador_pos += 20
    elif event.keysym == 'Up':
        direcao_lancador = 'vertical'
    elif event.keysym == 'Down':
        direcao_lancador = 'vertical'
    elif event.keysym == 'a':
        direcao_lancador = 'esquerda'
    elif event.keysym == 'd':
        direcao_lancador = 'direita'
    elif event.keysym == 'q':
        direcao_lancador = 'diagonal_esquerda'
    elif event.keysym == 'e':
        direcao_lancador = 'diagonal_direita'
    criar_interface()

def disparar(event):
    if event.keysym == 'space':
        disparar_foguete()

# Bind das teclas
root.bind('<Key>', mover_lancador)
root.bind('<space>', disparar)

# Função para mover foguetes em uma thread
def mover_foguetes():
    global foguetes_disparados
    while True:
        with mutex:
            for foguete in foguetes_disparados:
                foguete.mover()
                if not foguete.ativo:
                    foguetes_disparados.remove(foguete)
        atualizar_interface()
        time.sleep(0.05)

# Função para mover naves em uma thread
def mover_naves():
    global naves
    while True:
        with mutex:
            for nave in naves:
                nave.mover()
                if nave.y > 600:
                    naves.remove(nave)
        atualizar_interface()
        time.sleep(0.1)

# Função para verificar colisões entre foguetes e naves
def verificar_colisoes():
    global foguetes_disparados, naves
    while True:
        with mutex:
            for foguete in foguetes_disparados:
                for nave in naves:
                    if (nave.x - 10 < foguete.x < nave.x + 10) and (nave.y - 10 < foguete.y < nave.y + 10) and nave.viva:
                        nave.viva = False
                        foguete.ativo = False
                        naves.remove(nave)
                        foguetes_disparados.remove(foguete)
        time.sleep(0.05)

# Função para verificar condições de vitória ou derrota
def verificar_condicoes():
    while True:
        with mutex:
            naves_vivas = [nave for nave in naves if nave.viva]
            if len(naves_vivas) <= qtd_naves / 2:
                print("Vitória do jogador!")
                break
            elif len(naves) > qtd_naves / 2:
                print("Derrota do jogador!")
                break
        time.sleep(1)

# Função principal que executa o loop do jogo
def loop_principal():
    threads = []
    threads.append(Thread(target=mover_foguetes, daemon=True))
    threads.append(Thread(target=mover_naves, daemon=True))
    threads.append(Thread(target=verificar_colisoes, daemon=True))
    threads.append(Thread(target=verificar_condicoes, daemon=True))
    threads.append(Thread(target=gerar_naves_aleatoriamente, daemon=True))
    
    for thread in threads:
        thread.start()

# Inicializar e executar o jogo
def iniciar_jogo():
    criar_interface()
    root.after(100, loop_principal)

if __name__ == "__main__":
    iniciar_jogo()
    root.mainloop()
 