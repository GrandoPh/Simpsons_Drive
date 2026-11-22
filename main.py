import os
import random
import pygame
from Recursos.funcoes import inicializarBancoDeDados, limpar_tela, aguarde, escreverDados, maior_pontuador
from Recursos.trabalho import falar_texto, calcular_dificuldade


os.system("color 0E")
limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada, horaJogada = maior_pontuador()

print("=========================================")
print("      SIMPSONS DRIVE - SPRINGFIELD       ")
print("=========================================")
aguarde(1)

nome = input("Informe o Nome do Competidor: ")
if nome == "":
    print("Nome vazio! Usando nome padrao: Homer")
    nome = "Homer"

print("Preparando o carro para " + nome + "...")
aguarde(1)

# Requisito 19: Biblioteca pyttsx3
falar_texto("Bem-vindo a Springfield, " + nome)

pygame.init()

# Requisito 8: Tamanho da tela configurado para 1000x700 pixels
tamanho = (1000, 700)
pygame.display.set_caption("Simpsons Drive - Corrida em Springfield")
icone = pygame.image.load("bases/icone.png")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode(tamanho)

# Cores basicas
branco = (255, 255, 255)
preto = (0, 0, 0)
amarelo = (255, 222, 45)
azul_escuro = (25, 45, 95)
vermelho = (220, 40, 40)
cinza_claro = (230, 230, 230)

# Carregando imagens da pasta bases/ (Requisitos 2 e 10)
fundo = pygame.image.load("bases/background.png")
fundoDead = pygame.image.load("bases/backgroundDead.png")
fundoStart = pygame.image.load("bases/backgroundStart.png")

homer = pygame.image.load("bases/homer_carro.png")
homer = pygame.transform.scale(homer, (80, 130))

carroPolicia = pygame.image.load("bases/carro_policia.png")
carroPolicia = pygame.transform.scale(carroPolicia, (80, 130))

carroRoxo = pygame.image.load("bases/carro_inimigo.png")
carroRoxo = pygame.transform.scale(carroRoxo, (80, 130))

dirigivelDuff = pygame.image.load("bases/decoracao_duff.png")
dirigivelDuff = pygame.transform.scale(dirigivelDuff, (120, 60))

# Carregando sons da pasta bases/
buzinaSound = pygame.mixer.Sound("bases/buzina.wav")
batidaSound = pygame.mixer.Sound("bases/batida.wav")
pygame.mixer.music.load("bases/trilha.wav")

# Fontes
fonteTitulo = pygame.font.SysFont("comicsans", 34, bold=True)
fonteMenu = pygame.font.SysFont("comicsans", 22)
fontePequena = pygame.font.SysFont("comicsans", 16)
fontePause = pygame.font.SysFont("comicsans", 64, bold=True)

def jogar():
    # Requisito 13: O personagem se move SOMENTE no eixo X (Esquerda e Direita)
    posicaoXPersona = 460
    posicaoYPersona = 530
    movimentoXPersona = 0
    velocidadeMovPersona = 8

    # Carro inimigo 1 (Policia - Faixa da Esquerda)
    posicaoXInimigo1 = random.randint(240, 410)
    posicaoYInimigo1 = -140
    velocidadeInimigo1 = 6

    # Carro inimigo 2 (Carro Roxo - Faixa da Direita)
    posicaoXInimigo2 = random.randint(510, 680)
    posicaoYInimigo2 = -480
    velocidadeInimigo2 = 5

    # Faixas brancas animadas do asfalto
    faixaY = 0

    # Requisito 14: Objeto decorativo que se movimenta de forma randomica sem interagir com o jogador
    posicaoXDecoracao = random.randint(50, 800)
    posicaoYDecoracao = random.randint(25, 110)
    velocidadeXDecoracao = 2
    velocidadeYDecoracao = 1

    # Requisito 16: Circulo amarelo (Sol) em um dos cantos da tela que pulsa lentamente
    raioSol = 38
    crescendoSol = True

    pontos = 0
    pausado = False
    dificuldade = 18

    pygame.mixer.music.play(-1)

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                # Requisito 20: Ao pressionar ESC fecha o jogo completamente
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                # Requisito 11: Ao pressionar Espaco (Space) pausa e despausa o jogo
                elif evento.key == pygame.K_SPACE:
                    if pausado == False:
                        pausado = True
                        pygame.mixer.music.pause()
                    else:
                        pausado = False
                        pygame.mixer.music.unpause()
                # Requisito 13: Movimento apenas no eixo X
                elif evento.key == pygame.K_RIGHT:
                    movimentoXPersona = velocidadeMovPersona
                elif evento.key == pygame.K_LEFT:
                    movimentoXPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYUP:
                if evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT:
                    movimentoXPersona = 0

        if pausado == False:
            # Atribuicao aumentada (+=) e limites do asfalto com if e elif
            posicaoXPersona += movimentoXPersona
            if posicaoXPersona < 235:
                posicaoXPersona = 235
            elif posicaoXPersona > 685:
                posicaoXPersona = 685

            # Atualiza movimentacao das faixas da pista
            faixaY += int(velocidadeInimigo1)
            if faixaY >= 100:
                faixaY = 0

            # Atualiza Carro Inimigo 1 (Faixa da Esquerda)
            posicaoYInimigo1 += velocidadeInimigo1
            if posicaoYInimigo1 > 700:
                pygame.mixer.Sound.play(buzinaSound)
                posicaoYInimigo1 = -140
                posicaoXInimigo1 = random.randint(240, 410)
                pontos += 1
                velocidadeInimigo1 += 0.3

            # Atualiza Carro Inimigo 2 (Faixa da Direita)
            posicaoYInimigo2 += velocidadeInimigo2
            if posicaoYInimigo2 > 700:
                pygame.mixer.Sound.play(buzinaSound)
                posicaoYInimigo2 = -180
                posicaoXInimigo2 = random.randint(510, 680)
                pontos += 1
                velocidadeInimigo2 += 0.3

            # Atualiza Objeto Decorativo Randomico (Requisito 14)
            posicaoXDecoracao += velocidadeXDecoracao
            posicaoYDecoracao += velocidadeYDecoracao
            if posicaoXDecoracao < 20 or posicaoXDecoracao > 850:
                velocidadeXDecoracao = -velocidadeXDecoracao
            if posicaoYDecoracao < 15 or posicaoYDecoracao > 130:
                velocidadeYDecoracao = -velocidadeYDecoracao
            if random.randint(1, 90) == 1:
                velocidadeXDecoracao = random.randint(-2, 2)
                velocidadeYDecoracao = random.randint(-1, 1)

            # Atualiza pulso lento do Sol Amarelo (Requisito 16)
            if crescendoSol == True:
                raioSol += 0.25
                if raioSol >= 48:
                    crescendoSol = False
            else:
                raioSol -= 0.25
                if raioSol <= 32:
                    crescendoSol = True

        # Desenho do cenario
        tela.fill(branco)
        tela.blit(fundo, (0, 0))

        # Desenha faixas tracejadas brancas no meio do asfalto
        y_linha = faixaY - 100
        while y_linha < 700:
            pygame.draw.rect(tela, branco, (495, y_linha, 10, 50))
            y_linha += 100

        # Requisito 16: Circulo amarelo (Sol) pulsando no canto superior esquerdo
        pygame.draw.circle(tela, amarelo, (70, 65), int(raioSol))

        # Requisito 14: Objeto decorativo randomico (Dirigivel Duff)
        tela.blit(dirigivelDuff, (posicaoXDecoracao, posicaoYDecoracao))

        # Desenha carros inimigos e o carro do Homer
        tela.blit(carroPolicia, (posicaoXInimigo1, int(posicaoYInimigo1)))
        tela.blit(carroRoxo, (posicaoXInimigo2, int(posicaoYInimigo2)))
        tela.blit(homer, (posicaoXPersona, posicaoYPersona))

        # Placar e nivel (Requisito 7)
        nivel_atual = calcular_dificuldade(pontos)
        textoPontos = fonteMenu.render("Pontos: " + str(pontos), True, branco)
        textoNivel = fontePequena.render(nivel_atual, True, amarelo)
        tela.blit(textoPontos, (820, 15))
        tela.blit(textoNivel, (240, 12))

        # Requisito 12: Mensagem discreta na tela
        textoPauseAviso = fontePequena.render("Press Space to Pause Game", True, cinza_claro)
        tela.blit(textoPauseAviso, (15, 670))

        # Requisito 11: Exibe "PAUSE" no centro da tela quando pausado
        if pausado == True:
            textoPauseCentro = fontePause.render("PAUSE", True, amarelo)
            tela.blit(textoPauseCentro, (395, 300))

        # Verificacao de colisao igual a base da aula do Prof. Marcos
        if pausado == False:
            pixelsPersonaX = list(range(int(posicaoXPersona), int(posicaoXPersona) + 80))
            pixelsPersonaY = list(range(int(posicaoYPersona), int(posicaoYPersona) + 130))

            # Colisao com Carro 1
            pixelsInimigo1X = list(range(int(posicaoXInimigo1), int(posicaoXInimigo1) + 80))
            pixelsInimigo1Y = list(range(int(posicaoYInimigo1), int(posicaoYInimigo1) + 130))
            if len(list(set(pixelsInimigo1Y).intersection(set(pixelsPersonaY)))) > dificuldade:
                if len(list(set(pixelsInimigo1X).intersection(set(pixelsPersonaX)))) > dificuldade:
                    escreverDados(nome, pontos)
                    dead(pontos)

            # Colisao com Carro 2
            pixelsInimigo2X = list(range(int(posicaoXInimigo2), int(posicaoXInimigo2) + 80))
            pixelsInimigo2Y = list(range(int(posicaoYInimigo2), int(posicaoYInimigo2) + 130))
            if len(list(set(pixelsInimigo2Y).intersection(set(pixelsPersonaY)))) > dificuldade:
                if len(list(set(pixelsInimigo2X).intersection(set(pixelsPersonaX)))) > dificuldade:
                    escreverDados(nome, pontos)
                    dead(pontos)

        pygame.display.update()
        relogio.tick(60)

def dead(pontos_partida):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(batidaSound)
    falar_texto("Doh! Fim de jogo! Voce fez " + str(pontos_partida) + " pontos.")

    # Atualiza o maior pontuador apos salvar no log.dat (Requisito 18)
    nome_top, pontos_top, data_top, hora_top = maior_pontuador()

    larguraButtonStart = 240
    alturaButtonStart = 50

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                # Requisito 20: ESC fecha o jogo completamente
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 230
                    alturaButtonStart = 45
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 240
                    alturaButtonStart = 50
                    jogar()

        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))

        tituloDead = fonteTitulo.render("D'OH! VOCE BATEU O CARRO!", True, amarelo)
        tela.blit(tituloDead, (255, 160))

        textoSuaPontuacao = fonteMenu.render("Sua Pontuacao: " + str(pontos_partida) + " pontos", True, branco)
        tela.blit(textoSuaPontuacao, (350, 230))

        # Requisito 18: Mostrar o competidor com maior numero de pontos na tela de morte
        textoRecordeTitulo = fonteMenu.render("RECORDE DE SPRINGFIELD (MAIOR PONTUADOR):", True, amarelo)
        tela.blit(textoRecordeTitulo, (230, 300))

        textoRecordeDados = fonteMenu.render(
            nome_top + " - " + str(pontos_top) + " pts (" + data_top + " as " + hora_top + ")",
            True,
            branco
        )
        tela.blit(textoRecordeDados, (250, 340))

        startButton = pygame.draw.rect(tela, amarelo, (380, 430, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Jogar Novamente", True, preto)
        tela.blit(startTexto, (410, 440))

        textoEsc = fontePequena.render("Pressione ESC ou clique no X para sair", True, branco)
        tela.blit(textoEsc, (365, 520))

        pygame.display.update()
        relogio.tick(60)

def start():
    # Requisito 9: Tela de boas-vindas com nome, mecanica, recorde (data e hora) e UM UNICO BOTAO (sem botao fechar)
    nome_top, pontos_top, data_top, hora_top = maior_pontuador()
    larguraButtonStart = 240
    alturaButtonStart = 55

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                # Requisito 20: ESC fecha o jogo completamente
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 230
                    alturaButtonStart = 50
            elif evento.type == pygame.MOUSEBUTTONUP:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 240
                    alturaButtonStart = 55
                    jogar()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))

        # Saudacao com o nome do jogador
        tituloBemVindo = fonteTitulo.render("Bem-vindo, " + nome + "!", True, azul_escuro)
        tela.blit(tituloBemVindo, (200, 170))

        # Explicacao rapida da mecanica do jogo
        textoMec1 = fonteMenu.render("Ajude o Homer a dirigir pelo asfalto de Springfield!", True, preto)
        textoMec2 = fonteMenu.render("Use as setas ESQUERDA e DIREITA para desviar dos carros.", True, preto)
        textoMec3 = fonteMenu.render("Aperte ESPACO para pausar e ESC para sair.", True, preto)
        tela.blit(textoMec1, (200, 235))
        tela.blit(textoMec2, (200, 270))
        tela.blit(textoMec3, (200, 305))

        # Maior pontuador, data e hora
        textoRecorde = fonteMenu.render(
            "Recorde: " + nome_top + " | " + str(pontos_top) + " pts | " + data_top + " " + hora_top,
            True,
            vermelho
        )
        tela.blit(textoRecorde, (200, 365))

        # Unico botao para iniciar a partida (sem botao de fechar interno)
        startButton = pygame.draw.rect(tela, azul_escuro, (380, 445, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Partida", True, branco)
        tela.blit(startTexto, (425, 458))

        pygame.display.update()
        relogio.tick(60)

start()
