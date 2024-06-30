import tkinter as tk
from tkinter import messagebox
from threading import Thread, Lock
import random
import time

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
pontos = 0
jogo_ativo = True

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

# Desenho da área de recarga
recarregar_x = 50
recarregar_y = 570
recarregar_width = 60
recarregar_height = 30

def atualizar_mostrador_foguetes():
    label_foguetes.config(text=f"Foguetes Disponíveis: {foguetes_disponiveis}")

# Desenhos dos objetos
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
    "     __/)     (\\__     ",
    "  ,-'~~(   _   )~~`-.  ",
    " /      \\'_`\\/      \\ ",
    "|       /_(_)_\\       |",
    "|     _(/(\\_/\\)_     |",
    "|    / // \\ / \\\\ \\    |",
    " \\  | ``  / \\ ''  |  / ",
    "  \\  )   /   \\   (  /  ",
    "   )/   /     \\   \\(   ",
    "   '    `-`-'-'    `   ",
]

foguete = ["*"]

# Classe para representar os foguetes
class Foguete:
    def __init__(self, x, y, direcao):
        self.x = x
        self.y = y
        self.direcao = direcao
        self.ativo = True

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

    def desenhar(self, canvas):
        if self.ativo:
            canvas.create_text(self.x, self.y, text=foguete[0], font=('Courier', 52), fill='red')


class Nave:
    def __init__(self, x):
        self.x = x
        self.y = 0
        self.viva = True

    def mover(self):
        self.y += velocidade_naves

    def desenhar(self, canvas):
        if self.viva:
            for i, line in enumerate(nave):
                canvas.create_text(self.x, self.y + i * 8, text=line, font=('Courier', 8), fill='blue')

def criar_interface():
    global canvas, lancador_pos, direcao_lancador
    canvas.delete("all")
    # Desenhar área de recarga
    canvas.create_rectangle(recarregar_x, recarregar_y, recarregar_x + recarregar_width, recarregar_y + recarregar_height, fill='green')
    canvas.create_text(recarregar_x + recarregar_width/2, recarregar_y + recarregar_height/2, text='RECARREGAR', font=('Courier', 8), fill='white')
    # Canhão representado como um retângulo
    if direcao_lancador == 'vertical':
        representacao = lancador_0_cima
    elif direcao_lancador == 'diagonal_esquerda':
        representacao = lancador_135_cima
    elif direcao_lancador == 'diagonal_direita':
        representacao = lancador_45_cima
    elif direcao_lancador == 'esquerda':
        representacao = lancador_90_esquerda
    elif direcao_lancador == 'direita':
        representacao = lancador_90_direita

    for i, line in enumerate(representacao):
        canvas.create_text(lancador_pos, 580 + i * 10, text=line, font=('Courier', 12), fill='white')
    root.update()

def verificar_recarga():
    global foguetes_disponiveis
    if (lancador_pos >= recarregar_x and lancador_pos <= recarregar_x + recarregar_width):
        foguetes_disponiveis = n_foguetes
        atualizar_mostrador_foguetes()

def agendar_atualizacao():
    global foguetes_disparados, naves
    if jogo_ativo:
        canvas.delete("all")
        criar_interface()
        # Desenhar os foguetes disparados
        for foguete in foguetes_disparados:
            foguete.desenhar(canvas)
        # Desenhar as naves
        for nave in naves:
            nave.desenhar(canvas)
        root.update()

def atualizar_interface():
    root.after(50, agendar_atualizacao)

# Função para gerar naves de forma aleatória
def gerar_naves_aleatoriamente():
    global naves
    while jogo_ativo and len(naves) < qtd_naves:
        time.sleep(random.randint(1, 5))  # Intervalo aleatório entre 1 e 5 segundos
        with mutex:
            x = random.randint(20, 780)
            naves.append(Nave(x))

# Função para disparar foguetes
def disparar_foguete():
    global foguetes_disponiveis, foguetes_disparados, lancador_pos, direcao_lancador, mutex
    with mutex:
        if foguetes_disponiveis > 0 and jogo_ativo:
            foguetes_disponiveis -= 1
            foguete = Foguete(lancador_pos, 580, direcao_lancador)
            foguetes_disparados.append(foguete)
            atualizar_mostrador_foguetes()

# Função para capturar e processar as entradas do jogador
def mover_lancador(event):
    global lancador_pos, direcao_lancador
    if not jogo_ativo:
        return

    if event.keysym == 'Left':
        if direcao_lancador == 'vertical':
            direcao_lancador = 'diagonal_esquerda'
        elif direcao_lancador == 'diagonal_esquerda':
            direcao_lancador = 'esquerda'
        elif direcao_lancador == 'direita':
            direcao_lancador = 'diagonal_direita'
        elif direcao_lancador == 'diagonal_direita':
            direcao_lancador = 'vertical'
        elif direcao_lancador == 'esquerda':
            if lancador_pos > 20:
                lancador_pos -= 20

    elif event.keysym == 'Right':
        if direcao_lancador == 'vertical':
            direcao_lancador = 'diagonal_direita'
        elif direcao_lancador == 'diagonal_direita':
            direcao_lancador = 'direita'
        elif direcao_lancador == 'esquerda':
            direcao_lancador = 'diagonal_esquerda'
        elif direcao_lancador == 'diagonal_esquerda':
            direcao_lancador = 'vertical'
        elif direcao_lancador == 'direita':
            if lancador_pos < 780:
                lancador_pos += 20

    elif event.keysym == 'Up':
        direcao_lancador = 'vertical'

    verificar_recarga()
    criar_interface()



def disparar(event):
    if event.keysym == 'space':
        disparar_foguete()

# Bind das teclas
root.bind('<Left>', mover_lancador)
root.bind('<Right>', mover_lancador)
root.bind('<Up>', mover_lancador)
root.bind('<Down>', mover_lancador)

root.bind('<space>', disparar)

# Função para mover foguetes em uma thread
def mover_foguetes():
    global foguetes_disparados
    while jogo_ativo:
        with mutex:
            for foguete in foguetes_disparados:
                foguete.mover()
                if not foguete.ativo:
                    foguetes_disparados.remove(foguete)
        atualizar_interface()
        time.sleep(0.05)

# Função para mover naves em uma thread
def mover_naves():
    global naves, pontos, jogo_ativo
    while jogo_ativo:
        with mutex:
            for nave in naves:
                nave.mover()
                if nave.y > 600:
                    naves.remove(nave)
                    pontos -= 1
        atualizar_interface()
        time.sleep(0.1)

# Função para verificar colisões entre foguetes e naves
def verificar_colisoes():
    global foguetes_disparados, naves, pontos, jogo_ativo
    while jogo_ativo:
        with mutex:
            for foguete in foguetes_disparados:
                for nave in naves:
                    if nave.viva and (nave.x - 50 < foguete.x < nave.x + 50) and (nave.y - 50 < foguete.y < nave.y + 50):
                        nave.viva = False
                        foguete.ativo = False
                        naves.remove(nave)
                        foguetes_disparados.remove(foguete)
                        pontos += 1
                        break
        time.sleep(0.05)

# Função para mostrar mensagem de vitória ou derrota
def mostrar_mensagem(resultado):
    if resultado == 'vitoria':
        messagebox.showinfo("Fim de Jogo", "Você ganhou!")
    else:
        messagebox.showinfo("Fim de Jogo", "Você perdeu!")

# Função para verificar condições de vitória ou derrota
def verificar_condicoes():
    global jogo_ativo
    while jogo_ativo:
        with mutex:
            naves_vivas = [nave for nave in naves if nave.viva]
            if pontos >= qtd_naves // 2:
                jogo_ativo = False
                root.after(0, mostrar_mensagem, 'vitoria')
            elif len(naves_vivas) > qtd_naves // 2:
                jogo_ativo = False
                root.after(0, mostrar_mensagem, 'derrota')
        time.sleep(1)
    root.quit()

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
