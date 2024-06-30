import threading
import time
import curses
import random

# Configurações do jogo
LARGURA_TELA = 80
ALTURA_TELA = 24
VELOCIDADE_NAVE = 2
TAXA_RECARGA = 1  # segundos para recarregar um foguete
ESPACO_FOGUETES = 5  # capacidade de foguetes

# Configurações de dificuldade
DIFICULDADES = {
    "facil": {"k": 10, "velocidade": 1, "m": 15, "vitoria": 20},
    "medio": {"k": 7, "velocidade": 2, "m": 10, "vitoria": 50},
    "dificil": {"k": 5, "velocidade": 3, "m": 15, "vitoria": 100}
}

# Ângulos de disparo
ANGULOS_DISPARO = {
    "vertical": "|",
    "diagonal_esquerda": "\\",
    "diagonal_direita": "/",
    "horizontal_esquerda": "__",
    "horizontal_direita": "__"
}

# Classe Nave
class Nave(threading.Thread):
    def __init__(self, tela, x, y, velocidade):
        threading.Thread.__init__(self)
        self.tela = tela
        self.x = x
        self.y = y
        self.velocidade = velocidade
        self.viva = True

    def run(self):
        while self.viva and self.y < ALTURA_TELA - 1:
            self.y += self.velocidade
            time.sleep(1)
        if self.y >= ALTURA_TELA - 1:
            self.viva = False

    def desenhar(self):
        if self.viva:
            with threading.Lock():
                self.tela.addstr(self.y, self.x, 'A')

# Classe Foguete
class Foguete(threading.Thread):
    def __init__(self, tela, x, y, angulo, semaforo, naves):
        threading.Thread.__init__(self)
        self.tela = tela
        self.x = x
        self.y = y
        self.angulo = angulo
        self.semaforo = semaforo
        self.naves = naves
        self.disparando = True

    def run(self):
        while self.disparando and self.y >= 0 and 0 <= self.x < LARGURA_TELA:
            self.mover()
            time.sleep(0.1)
            self.verificar_acerto()

    def mover(self):
        if self.angulo == "|":
            self.y -= 1
        elif self.angulo == "\\":
            self.y -= 1
            self.x -= 1
        elif self.angulo == "/":
            self.y -= 1
            self.x += 1
        elif self.angulo == "__":
            self.x += 1

    def verificar_acerto(self):
        for nave in self.naves:
            if nave.viva and nave.x == self.x and nave.y == self.y:
                nave.viva = False
                self.disparando = False

    def desenhar(self):
        if self.disparando and 0 <= self.x < LARGURA_TELA and 0 <= self.y < ALTURA_TELA:
            with threading.Lock():
                self.tela.addstr(self.y, self.x, '*')

# Função principal do jogo
def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)
    stdscr.timeout(100)

    dificuldade = DIFICULDADES["medio"]
    velocidade_nave = dificuldade["velocidade"]
    max_naves = dificuldade["m"]
    vitoria = dificuldade["vitoria"]

    foguetes = ESPACO_FOGUETES
    naves = []
    foguetes_lancados = []
    naves_abatidas = 0

    def lancar_foguete(x, y, angulo):
        nonlocal foguetes
        if foguetes > 0:
            foguete = Foguete(stdscr, x, y, angulo, semaforo_foguetes, naves)
            foguete.start()
            foguetes_lancados.append(foguete)
            foguetes -= 1

    def recarregar_foguetes():
        nonlocal foguetes
        while foguetes < ESPACO_FOGUETES:
            time.sleep(TAXA_RECARGA)
            foguetes += 1

    semaforo_foguetes = threading.Semaphore(ESPACO_FOGUETES)
    thread_recarga = threading.Thread(target=recarregar_foguetes)
    thread_recarga.start()

    jogador_x = LARGURA_TELA // 2
    jogador_y = ALTURA_TELA - 2
    angulo_disparo = "|"

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"Foguetes: {foguetes}")
        stdscr.addstr(1, 0, f"Naves abatidas: {naves_abatidas}")

        for nave in naves:
            nave.desenhar()

        for foguete in foguetes_lancados:
            foguete.desenhar()

        stdscr.addstr(jogador_y, jogador_x, angulo_disparo)

        key = stdscr.getch()
        if key == curses.KEY_LEFT and jogador_x > 0:
            jogador_x -= 1
        elif key == curses.KEY_RIGHT and jogador_x < LARGURA_TELA - 1:
            jogador_x += 1
        elif key == curses.KEY_UP:
            angulo_disparo = "|"
        elif key == curses.KEY_DOWN:
            angulo_disparo = "__"
        elif key == ord(' '):
            lancar_foguete(jogador_x, jogador_y, angulo_disparo)
        elif key == ord('q'):
            break

        if len(naves) < max_naves and random.random() < 0.1:
            x = random.randint(0, LARGURA_TELA - 1)
            nave = Nave(stdscr, x, 0, velocidade_nave)
            nave.start()
            naves.append(nave)

        naves = [n for n in naves if n.viva]
        foguetes_lancados = [f for f in foguetes_lancados if f.disparando]

        naves_abatidas = max_naves - len(naves)

        if naves_abatidas >= vitoria:
            stdscr.addstr(ALTURA_TELA // 2, LARGURA_TELA // 2 - 5, "VITÓRIA!")
            stdscr.refresh()
            time.sleep(3)
            break
        elif len(naves) >= max_naves // 2:
            stdscr.addstr(ALTURA_TELA // 2, LARGURA_TELA // 2 - 5, "DERROTA!")
            stdscr.refresh()
            time.sleep(3)
            break

        stdscr.refresh()

    thread_recarga.join()

curses.wrapper(main)
