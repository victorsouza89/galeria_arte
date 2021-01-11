#!/usr/bin/env python
# -*- coding: utf-8 -*-

#imports do programa
import turtle
import random
import datetime

#variáveis globais
posCamera = -1210						#define a posição inicial da câmera como central
ultimoRefresh = datetime.datetime.now()	#variavel utilizada para atualizar a tela
fps = 25								#fps utilizado pelo programa para imprimir as imagens na tela

#abaixo define configurações iniciais do ambiente
cenario = turtle.Turtle()					#cria uma tartaruga para o backround móvel
#cenario.tracer(0, 0)						#configura tartaruga para não atualizar sem o metodo update
cenario.penup()								#evita que o background desenhe na tela
cenario.screen.setup(1000, 600)				#define tamanho de tela
cenario.screen.addshape("sprites/hall.gif")	#cadastra "hall.gif" como shape
cenario.shape("sprites/hall.gif")			#define background como "hall.gif"
cenario.goto(posCamera, 0)					#movimenta background para posição inicial

#define classe para personagens da simulação
class Visitante:
	"""
	a função __init__ é executada ao incializar um objeto
	recebe o nome do personagem para identificar sua sprite
	cria a tartaruga desse personagem e salva sua aparência
	"""
	def __init__(self, nome):
		#abaixo cria tartaruga e a esconde
		self.turtle = turtle.Turtle()
		self.turtle.penup()
		self.turtle.hideturtle()
		self.escondido = True

		self.sprites = dict()							#cria um dicionário para guardar endereços das sprites do personagem
		main = "sprites/visitantes/" + nome + "/"		#endereço base de onde ficam os arquivos
		
		#abaixo preenche o dicionário com os endereços
		for d in ['up', 'down', 'right', 'left']:
			self.sprites[d] = []						#cria lista das imagens de cada movimento
			self.sprites[d].append(main + d + "/0.gif")	#adiciona a primeira imagem ao registro
			self.sprites[d].append(main + d + "/1.gif")	#adiciona a segunda imagem ao registro

			#abaixo registra sprites do personagem
			cenario.screen.addshape(self.sprites[d][0])	
			cenario.screen.addshape(self.sprites[d][1])

	"""
	atualizaSprite atualiza o desenho de cada passo do personagem
	recebe a direção em que ele se movimenta
	"""
	def atualizaSprite(self, direction):
		#se o pesonagem está se movendo em alguma direção troca sua sprite
		if direction:
			if self.turtle.shape() == self.sprites[direction][0]:
				self.turtle.shape(self.sprites[direction][1])
			else:
				self.turtle.shape(self.sprites[direction][0])

			#salva o momento da atualização
			self.ultimaAtualizacao = datetime.datetime.now()

	"""
	a função mostra exibe o personagem no ponto de entrada como se ele estivesse entrando no museu
	"""
	def mostra(self):
		#define aleatoriamente dentro de intervalos os pontos da tela por onde circulará o personagem
		self.eixoY = random.randint(-140, -130)
		self.pontoEntrada = random.randint(1520, 1540)
		self.pontoSaida = random.randint(-1550, -1530)

		#define aleatoriamente dentro de intervalo parâmetro de atualização que controla a velocidade da caminhada do visitante
		self.taxaAtualizacao = random.randint(100000, 200000)

		#define posição como a inicial
		self.pos = [self.pontoEntrada, 100]
		#inicia personagem andando para 'baixo'
		self.atualizaSprite('down')
		
		#atualiza posição relativa à câmera
		self.atualizaPosicao(None)		

		#exibe o visitante na tela
		self.turtle.showturtle()
		self.escondido = False

		#define o personagem como não visualizando nenhuma obra
		self.apreciandoArte = False
		self.tempoRecuo = None
		self.entrou = False

		#cria lista para inserir os pontos de parada
		self.parada = []

		#corre a lista com os pontos de cada obra
		for q in quadros:
			#tem 70% de chance de parar
			if random.randint(0, 10) > 3:
				#adiciona um ponto de parada
				self.parada.append(q + random.randint(-15, 15))

	"""
	a função atualizaPosicao movimenta o personagem e corrige onde irá exibí-lo com base no posicionamento da câmera
	recebe a direção para a qual ele está se movimentando ('left', 'right', 'up' ou 'down')
	"""
	def atualizaPosicao(self, direction):
		#declara abaixo posCamera nesse escopo
		global posCamera

		#salva status atual de movimentação
		self.movimentoAtual = direction

		#atualiza imagem exibida do personagem
		self.atualizaSprite(direction)

		#movimenta o personagem na direção desejada
		if direction == 'down':
			self.pos[1] -= 3
		if direction == 'up':
			self.pos[1] += 3
		if direction == 'right':
			self.pos[0] += 5
		if direction == 'left':
			self.pos[0] -= 5
		
		#gera a posição absoluta do personagem com base na posição relativa e posição da câmera
		pos = (self.pos[0] + posCamera, self.pos[1])

		#move o personagem
		self.turtle.goto(pos)

	"""
	a função defineDirecao retorna a movimentação do personagem com base na posição
	retorna a direção definida
	"""
	def defineDirecao (self):
		#testa se está no final do corredor
		if self.pos[0] > self.pontoSaida:
			#se está no corredor testa se acabou de entrar
			if self.pos[1] > self.eixoY and not self.entrou:
				#se entrou agora vai em direção à galeria
				return 'down'
			
			#confirma que o personagem entrou
			self.entrou = True

			#testa se está olhando alguma obra
			if not self.apreciandoArte:
				#se não está olhando
				try:
					#se chegou no próximo ponto de parada
					if self.pos[0] < max(self.parada):
						#testa se já parou
						if self.tempoRecuo:
							#testa se já deve parar
							if self.tempoRecuo < datetime.datetime.now():
								#caso já deva parar determina tempo de contemplação
								self.tempoContemplacao = datetime.datetime.now() + datetime.timedelta(0, random.randint(5, 15))
								#reinicia tempo de recuo
								self.tempoRecuo = None
								self.apreciandoArte = True
								#remove essa parada para os próximas testes
								self.parada.remove(max(self.parada))
						else:
							#caso esteja andando determina o tempo para parar
							self.tempoRecuo = datetime.datetime.now() + datetime.timedelta(0, 2)
						return 'up'
				except:
					None
				return 'left'
			elif self.tempoContemplacao < datetime.datetime.now():
				#se acabou de olhar
				if self.tempoRecuo:
					#testa se já voltou ao corredor
					if self.tempoRecuo < datetime.datetime.now():
						#se já voltou ao corredor reinicia variáveis
						self.tempoRecuo = None
						self.apreciandoArte = False
				else:
					#define tempo para voltar ao corredor
					self.tempoRecuo = datetime.datetime.now() + datetime.timedelta(0, 2)
				return 'down'
			else:
				return None

		else:
			#se está no final do corredor sai
			if self.pos[1] < -450:
				#se está fora da tela esconde a tartaruga
				self.turtle.hideturtle()
				#define como escondido o personagem
				self.escondido = True
			
			return 'down'


"""
função para "mover a camera"
toma direction como variável para definir entre esquerda e direita (-1 = direita, 1 = esquerda)
utiliza-se da variável posCamera, global, como um offset para todos os elementos da tela
desloca então os objetos mostrados no eixo x, dando a impressão de movimento da camera
"""
def moveCamera (direction):
	global posCamera				#declara posCamera nesse escopo
	posCamera += direction*5		#muda posCamera
	if abs(posCamera) > 1210:
		posCamera -= direction*5	#se posCamera está saindo da tela anula movimento

	#abaixo corrige a posição de todos os visitantes
	for v in visitantes:
		if not v.escondido:
			v.atualizaPosicao(None)
	

#define abaixa as teclas que movem a camera durante a execução
cenario.screen.onkey(lambda : moveCamera(-1), "Right")
cenario.screen.onkey(lambda : moveCamera(1), "Left")
cenario.screen.listen()	#inicia monitoramento das teclas

#cria lista dos nomes dos personagens a ser criados
nomes = ['adenor', 'alfredo', 'amanda', 'augusto', 'charles', 'gertrudes', 'marcos', 'monique']
visitantes = []		#cria lista para os objetos de cada visitante
for n in nomes:
	visitantes.append(Visitante(n))	#insere na lista cada visitante como objeto da classe Visitante

#cria a lista da posição dos quadros no corredor
quadros = [1255, 1030, 800, 600 , 380, 230, 60, -180, -400, -600. -730, -930, -1110, -1300]

#loop principal do programa
while 1:
	cenario.goto(posCamera, 0)	#movimenta background

	#zera variável que conta número de personagens no museu
	personagensCriados = 0
	#corre todos os personagens cadastrados
	for v in visitantes:
		#checa se o personagem não está já aparecendo
		if not v.escondido:
			#incrementa a contagem
			personagensCriados += 1
			#se já é momento de atualizar a imagem do visitante em questão
			if v.ultimaAtualizacao + datetime.timedelta(0, 0, v.taxaAtualizacao) < datetime.datetime.now():
				#atualiza posição e desenho do personagem
				v.atualizaPosicao(v.defineDirecao())

	if ultimoRefresh + datetime.timedelta(0, 0, 1000000/fps) < datetime.datetime.now():
		#se não está "lotado" o museu
		if personagensCriados <= 5:
			#cria novo personagem (possibilidade de acontecer varia de acordo com os que já estão presentes)
			if random.randint(0, 500*personagensCriados) == 0:
				#escolhe um visitante para entrar no museu
				v = random.choice(visitantes)

				#se ele já não está, entra
				if v.escondido:
					v.mostra()

		#atualiza tela e salva momento de atualização
		ultimoRefresh = datetime.datetime.now()
		cenario.screen.update()
