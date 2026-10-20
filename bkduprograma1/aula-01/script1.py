import tkinter as tk
import random
import math

# =========================
# CONFIGURAÇÕES
# =========================
TAMANHO = 28
COLUNAS = 19
LINHAS = 21
LARGURA = COLUNAS * TAMANHO
ALTURA = LINHAS * TAMANHO + 60

# # = parede
# . = comida
# P = jogador
# G = fantasma
MAPA = [
    "###################",
    "#........#........#",
    "#.###.###.###.###.#",
    "#.................#",
    "#.###.#.#####.#.###",
    "#.....#...#...#...#",
    "#####.### # ###.###".replace(" ", ""),
    "    #.#       #.#  ".replace(" ", "#"),
    "#####.# ### # #.###",
    "#.....# #GGG# #...#",
    "#.##### #GGG# #####",
    "#.........P.........",
    "###################",
    "#........#........#",
    "#.###.###.###.###.#",
    "#...#........#...#",
    "###.#.#####.#.###.#",
    "#.....#...#...#....#",
    "#.###.###.###.###.#",
    "#.................#",
    "###################"
]

# Corrige o tamanho do mapa caso necessário
MAPA = [linha[:COLUNAS].ljust(COLUNAS, "#") for linha in MAPA[:LINHAS]]

# =========================
# JANELA
# =========================
janela = tk.Tk()
janela.title("PAC-MAN - Python")
janela.resizable(False, False)
janela.configure(bg="black")

canvas = tk.Canvas(
    janela,
    width=LARGURA,
    height=ALTURA,
    bg="black",
    highlightthickness=0
)
canvas.pack()

# =========================
# VARIÁVEIS
# =========================
pontuacao = 0
vidas = 3
fim_de_jogo = False
pausado = False

jogador = [1, 1]
direcao = [0, 0]
proxima_direcao = [0, 0]

fantasmas = [
    {"pos": [9, 8], "cor": "red", "dir": [0, -1]},
    {"pos": [9, 9], "cor": "pink", "dir": [0, 1]},
    {"pos": [9, 10], "cor": "cyan", "dir": [1, 0]},
]

comidas = set()

# =========================
# CRIAR COMIDAS
# =========================
for y in range(LINHAS):
    for x in range(COLUNAS):
        if MAPA[y][x] == ".":
            comidas.add((x, y))

# =========================
# FUNÇÕES
# =========================
def parede(x, y):
    if x < 0 or x >= COLUNAS or y < 0 or y >= LINHAS:
        return True
    return MAPA[y][x] == "#"


def desenhar():
    canvas.delete("all")

    # Labirinto
    for y in range(LINHAS):
        for x in range(COLUNAS):
            if parede(x, y):
                canvas.create_rectangle(
                    x * TAMANHO,
                    y * TAMANHO,
                    (x + 1) * TAMANHO,
                    (y + 1) * TAMANHO,
                    fill="#1515ff",
                    outline="#3030ff"
                )

    # Comidas
    for x, y in comidas:
        cx = x * TAMANHO + TAMANHO // 2
        cy = y * TAMANHO + TAMANHO // 2

        canvas.create_oval(
            cx - 3, cy - 3,
            cx + 3, cy + 3,
            fill="white",
            outline=""
        )

    # Jogador
    x, y = jogador
    cx = x * TAMANHO + TAMANHO // 2
    cy = y * TAMANHO + TAMANHO // 2

    canvas.create_arc(
        cx - 11,
        cy - 11,
        cx + 11,
        cy + 11,
        start=35,
        extent=290,
        fill="yellow",
        outline="yellow"
    )

    # Fantasmas
    for fantasma in fantasmas:
        x, y = fantasma["pos"]

        cx = x * TAMANHO + TAMANHO // 2
        cy = y * TAMANHO + TAMANHO // 2

        cor = fantasma["cor"]

        canvas.create_oval(
            cx - 11,
            cy - 11,
            cx + 11,
            cy + 10,
            fill=cor,
            outline=""
        )

        canvas.create_rectangle(
            cx - 11,
            cy,
            cx + 11,
            cy + 10,
            fill=cor,
            outline=""
        )

        # Olhos
        canvas.create_oval(
            cx - 7, cy - 5,
            cx - 2, cy + 1,
            fill="white",
            outline=""
        )

        canvas.create_oval(
            cx + 2, cy - 5,
            cx + 7, cy + 1,
            fill="white",
            outline=""
        )

        canvas.create_oval(
            cx - 5, cy - 3,
            cx - 2, cy,
            fill="black",
            outline=""
        )

        canvas.create_oval(
            cx + 2, cy - 3,
            cx + 5, cy,
            fill="black",
            outline=""
        )

    # HUD
    canvas.create_rectangle(
        0,
        LINHAS * TAMANHO,
        LARGURA,
        ALTURA,
        fill="black",
        outline=""
    )

    canvas.create_text(
        10,
        LINHAS * TAMANHO + 30,
        text=f"PONTOS: {pontuacao}",
        fill="white",
        font=("Arial", 15, "bold"),
        anchor="w"
    )

    canvas.create_text(
        LARGURA - 10,
        LINHAS * TAMANHO + 30,
        text=f"VIDAS: {vidas}",
        fill="yellow",
        font=("Arial", 15, "bold"),
        anchor="e"
    )


def pode_mover(pos, direcao):
    novo_x = pos[0] + direcao[0]
    novo_y = pos[1] + direcao[1]

    return not parede(novo_x, novo_y)


def mover_jogador():
    global pontuacao

    if pode_mover(jogador, proxima_direcao):
        direcao[0] = proxima_direcao[0]
        direcao[1] = proxima_direcao[1]

    if pode_mover(jogador, direcao):
        jogador[0] += direcao[0]
        jogador[1] += direcao[1]

    pos = (jogador[0], jogador[1])

    if pos in comidas:
        comidas.remove(pos)
        pontuacao += 10

    # Verifica vitória
    if len(comidas) == 0:
        vencer()


def mover_fantasmas():
    for fantasma in fantasmas:

        opcoes = []

        direcoes = [
            [1, 0],
            [-1, 0],
            [0, 1],
            [0, -1]
        ]

        for d in direcoes:
            if pode_mover(fantasma["pos"], d):
                opcoes.append(d)

        if not opcoes:
            continue

        # Evita ficar voltando imediatamente
        inversa = [
            -fantasma["dir"][0],
            -fantasma["dir"][1]
        ]

        melhores = [
            d for d in opcoes
            if d != inversa
        ]

        if not melhores:
            melhores = opcoes

        # Às vezes persegue o jogador
        if random.random() < 0.65:
            melhores.sort(
                key=lambda d:
                abs(
                    fantasma["pos"][0] + d[0] - jogador[0]
                )
                +
                abs(
                    fantasma["pos"][1] + d[1] - jogador[1]
                )
            )

            escolha = melhores[0]
        else:
            escolha = random.choice(melhores)

        fantasma["dir"] = escolha

        fantasma["pos"][0] += escolha[0]
        fantasma["pos"][1] += escolha[1]


def verificar_colisao():
    global vidas, fim_de_jogo

    for fantasma in fantasmas:
        if fantasma["pos"] == jogador:
            vidas -= 1

            if vidas <= 0:
                perder()
            else:
                reiniciar_posicoes()

            return


def reiniciar_posicoes():
    jogador[0] = 1
    jogador[1] = 1

    direcao[0] = 0
    direcao[1] = 0

    proxima_direcao[0] = 0
    proxima_direcao[1] = 0

    fantasmas[0]["pos"] = [9, 8]
    fantasmas[1]["pos"] = [9, 9]
    fantasmas[2]["pos"] = [9, 10]

    desenhar()


def vencer():
    global fim_de_jogo

    fim_de_jogo = True

    desenhar()

    canvas.create_rectangle(
        50,
        200,
        LARGURA - 50,
        330,
        fill="black",
        outline="yellow",
        width=4
    )

    canvas.create_text(
        LARGURA // 2,
        235,
        text="VOCÊ VENCEU!",
        fill="yellow",
        font=("Arial", 32, "bold")
    )

    canvas.create_text(
        LARGURA // 2,
        280,
        text=f"Pontuação: {pontuacao}",
        fill="white",
        font=("Arial", 20, "bold")
    )

    canvas.create_text(
        LARGURA // 2,
        315,
        text="Pressione ENTER para jogar novamente",
        fill="cyan",
        font=("Arial", 13)
    )


def perder():
    global fim_de_jogo

    fim_de_jogo = True

    desenhar()

    canvas.create_rectangle(
        50,
        200,
        LARGURA - 50,
        330,
        fill="black",
        outline="red",
        width=4
    )

    canvas.create_text(
        LARGURA // 2,
        235,
        text="GAME OVER",
        fill="red",
        font=("Arial", 34, "bold")
    )

    canvas.create_text(
        LARGURA // 2,
        280,
        text=f"Pontuação: {pontuacao}",
        fill="white",
        font=("Arial", 20, "bold")
    )

    canvas.create_text(
        LARGURA // 2,
        315,
        text="Pressione ENTER para tentar novamente",
        fill="yellow",
        font=("Arial", 13)
    )


def reiniciar_jogo():
    global pontuacao, vidas, fim_de_jogo

    pontuacao = 0
    vidas = 3
    fim_de_jogo = False

    comidas.clear()

    for y in range(LINHAS):
        for x in range(COLUNAS):
            if MAPA[y][x] == ".":
                comidas.add((x, y))

    reiniciar_posicoes()
    desenhar()


def tecla(evento):
    tecla = evento.keysym.lower()

    if tecla == "up" or tecla == "w":
        proxima_direcao[0] = 0
        proxima_direcao[1] = -1

    elif tecla == "down" or tecla == "s":
        proxima_direcao[0] = 0
        proxima_direcao[1] = 1

    elif tecla == "left" or tecla == "a":
        proxima_direcao[0] = -1
        proxima_direcao[1] = 0

    elif tecla == "right" or tecla == "d":
        proxima_direcao[0] = 1
        proxima_direcao[1] = 0

    elif tecla == "return" and fim_de_jogo:
        reiniciar_jogo()


def jogo():
    if not fim_de_jogo:
        mover_jogador()
        mover_fantasmas()
        verificar_colisao()
        desenhar()

    janela.after(150, jogo)


# =========================
# INICIAR
# =========================
janela.bind("<KeyPress>", tecla)

desenhar()
jogo()

janela.mainloop()