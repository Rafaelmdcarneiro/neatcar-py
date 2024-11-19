# neatcar-py

-> Instale as bibliotecas neat-python e pygame .

Esse script é um exemplo simples de um algoritmo de aprendizado de máquina evolutivo usando a biblioteca NEAT (NeuroEvolution of Augmenting Topologies), que treina redes neurais para controlar carros em uma simulação no PyGame. 

O NEAT é um algoritmo de evolução de redes neurais, onde as redes evoluem ao longo de várias gerações. 

Cada "genoma" representa uma rede neural e a fitness de cada genoma é baseada no desempenho do carro (distância percorrida). 

O objetivo é evoluir uma população de carros para aprender a navegar em um mapa e continuar vivo!

# Ciclo de Vida da Simulação:

Inicialização: Cada carro recebe uma rede neural e começa no mapa.

Simulação: A simulação roda enquanto houver carros vivos, e cada carro é controlado pela sua rede neural. O objetivo é que os carros aprendam a desviar das bordas e percorrer o maior caminho possível.

Evolução: O NEAT evolui as redes ao longo de várias gerações para melhorar o desempenho dos carros.
