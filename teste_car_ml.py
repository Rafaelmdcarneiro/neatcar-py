import math
import random
import sys
import os
import neat
import pygame

LARGURA = 1920
ALTURA = 1080
TAMANHO_CARRO_X = 25  
TAMANHO_CARRO_Y = 25
COR_BORDA = (255, 255, 255, 255)  
geracao_atual = 0  

class Carro:
    def __init__(self):
        self.sprite = pygame.image.load('carro.png').convert() 
        self.sprite = pygame.transform.scale(self.sprite, (TAMANHO_CARRO_X, TAMANHO_CARRO_Y))
        self.sprite_rotacionado = self.sprite 
        self.posicao = [880, 920] 
        self.angulo = 0
        self.velocidade = 0
        self.velocidade_definida = False 
        self.centro = [self.posicao[0] + TAMANHO_CARRO_X / 2, self.posicao[1] + TAMANHO_CARRO_Y / 2]  
        self.sensores = []  
        self.sensores_desenho = []  
        self.vivo = True  
        self.distancia = 0  
        self.tempo = 0  

    def desenhar(self, tela):
        tela.blit(self.sprite_rotacionado, self.posicao)  
        self.desenhar_sensores(tela) 

    def desenhar_sensores(self, tela):
        for sensor in self.sensores:
            posicao = sensor[0]
            pygame.draw.line(tela, (0, 255, 0), self.centro, posicao, 1)
            pygame.draw.circle(tela, (0, 255, 0), posicao, 5)

    def verificar_colisao(self, mapa_jogo):
        self.vivo = True
        for ponto in self.cantos:
            if mapa_jogo.get_at((int(ponto[0]), int(ponto[1]))) == COR_BORDA:
                self.vivo = False
                break

    def verificar_sensor(self, grau, mapa_jogo):
        comprimento = 0
        x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grau))) * comprimento)
        y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grau))) * comprimento)
        try:
            while not mapa_jogo.get_at((x, y)) == COR_BORDA and comprimento < 300:
                comprimento += 1
                x = int(self.centro[0] + math.cos(math.radians(360 - (self.angulo + grau))) * comprimento)
                y = int(self.centro[1] + math.sin(math.radians(360 - (self.angulo + grau))) * comprimento)
            dist = int(math.sqrt(math.pow(x - self.centro[0], 2) + math.pow(y - self.centro[1], 2)))
            self.sensores.append([(x, y), dist])
        except Exception as err:
            print(f'ERRO PIXEL FORA DO INDEX: {err}')
            
        
    def atualizar(self, mapa_jogo):
        if not self.velocidade_definida:
            self.velocidade = 10
            self.velocidade_definida = True
            
        self.sprite_rotacionado = self.rotacionar_centro(self.sprite, self.angulo)
        self.posicao[0] += math.cos(math.radians(360 - self.angulo)) * self.velocidade
        self.posicao[0] = max(self.posicao[0], 20)
        self.posicao[0] = min(self.posicao[0], LARGURA - 120)
        self.distancia += self.velocidade
        self.tempo += 1
        self.posicao[1] += math.sin(math.radians(360 - self.angulo)) * self.velocidade
        self.posicao[1] = max(self.posicao[1], 20)
        self.posicao[1] = min(self.posicao[1], LARGURA - 120)
        self.centro = [int(self.posicao[0]) + TAMANHO_CARRO_X / 2, int(self.posicao[1]) + TAMANHO_CARRO_Y / 2]
        comprimento = 0.5 * TAMANHO_CARRO_X
        canto_superior_esquerdo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 30))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 30))) * comprimento]
        canto_superior_direito = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 150))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 150))) * comprimento]
        canto_inferior_esquerdo = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 210))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 210))) * comprimento]
        canto_inferior_direito = [self.centro[0] + math.cos(math.radians(360 - (self.angulo + 330))) * comprimento, self.centro[1] + math.sin(math.radians(360 - (self.angulo + 330))) * comprimento]
        self.cantos = [canto_superior_esquerdo, canto_superior_direito, canto_inferior_esquerdo, canto_inferior_direito]
        self.verificar_colisao(mapa_jogo)
        self.sensores.clear()
        for d in range(-90, 120, 45):
            self.verificar_sensor(d, mapa_jogo)

    def obter_dados(self):
        sensores = self.sensores
        valores_retorno = [0, 0, 0, 0, 0]
        for i, sensor in enumerate(sensores):
            valores_retorno[i] = int(sensor[1] / 30)
        return valores_retorno

    def esta_vivo(self):
        return self.vivo

    def obter_recompensa(self):
        return self.distancia / (TAMANHO_CARRO_X / 2)

    def rotacionar_centro(self, imagem, angulo):
        retangulo = imagem.get_rect()
        imagem_rotacionada = pygame.transform.rotate(imagem, angulo)
        retangulo_rotacionado = retangulo.copy()
        retangulo_rotacionado.center = imagem_rotacionada.get_rect().center
        imagem_rotacionada = imagem_rotacionada.subsurface(retangulo_rotacionado).copy()
        return imagem_rotacionada

def executar_simulacao(genomas, config):
    redes = []
    carros = []
    pygame.init()
    tela = pygame.display.set_mode((LARGURA, ALTURA), pygame.WINDOWMAXIMIZED)
    
    for _, genoma in genomas:
        rede = neat.nn.FeedForwardNetwork.create(genoma, config)
        redes.append(rede)
        genoma.fitness = 0
        carros.append(Carro())
        
    relogio = pygame.time.Clock()
    fonte_geracao = pygame.font.SysFont("Arial", 30)
    fonte_vivos = pygame.font.SysFont("Arial", 20)
    
    mapa_jogo = pygame.image.load('pista1.png').convert()
    global geracao_atual
    geracao_atual += 1
    contador = 0

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit(0)

        for i, carro in enumerate(carros):
            saida = redes[i].activate(carro.obter_dados())
            escolha = saida.index(max(saida))
            if escolha == 0:
                carro.angulo += 10
            elif escolha == 1:
                carro.angulo -= 10 
            elif escolha == 2:
                if carro.velocidade - 2 >= 12:
                    carro.velocidade -= 2  
            else:
                carro.velocidade += 2

        vivos = 0
        for i, carro in enumerate(carros):
            if carro.esta_vivo():
                vivos += 1
                carro.atualizar(mapa_jogo)
                genomas[i][1].fitness += carro.obter_recompensa()

        if vivos == 0:
            break

        contador += 1
        if contador == 9999 * 99999:
            break

        tela.blit(mapa_jogo, (0, 0))
        for carro in carros:
            if carro.esta_vivo():
                carro.desenhar(tela)

        texto = fonte_geracao.render(f"Geração: {geracao_atual}", True, (0, 0, 0))
        rect_texto = texto.get_rect()
        rect_texto.center = (100, 60)
        tela.blit(texto, rect_texto)

        texto = fonte_vivos.render(f"Carros Vivos: {vivos}", True, (0, 0, 0))
        rect_texto = texto.get_rect()
        rect_texto.center = (100, 100)
        tela.blit(texto, rect_texto)

        pygame.display.flip()
        relogio.tick(60)  


if __name__ == "__main__":
    caminho_config = "config.txt"
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        caminho_config
    )
    populacao = neat.Population(config)
    populacao.add_reporter(neat.StdOutReporter(True))
    estatisticas = neat.StatisticsReporter()
    populacao.add_reporter(estatisticas)
    populacao.run(executar_simulacao, 100)

