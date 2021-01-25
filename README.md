# Agent0_minotauro_RL

## Sobre o projeto:

O projeto Agent0_minotauro permite explorar a interação entre um agente e um ambiente.

### Ambiente

O ambiente consiste num tabuleiro retangular de casas quadradas, que podem conter obstáculos ou objetivos. Para se movimentar neste ambiente, o agente pode deslocar-se em relação à direção (north, south, east, west).

A interação entre o agente e o ambiente é comandada através de um cliente e acontece no servidor.

Foi utilizado o Agent0_minotauro_RL para o desenvolvimento do Agent RL Base.

### Agent RL Base

O agente RL tem como propósito mostrar a política selecionada pelo agente após ter explorado o mundo de forma aleatória, para obter essa política calcula-se  os caminhos que irão retornar uma maior recompensa. Essas recompensas irão ser guardadas numa tabela (Q-Learning table) que terá as rewards de cada direção (norte, sul, este e oeste) de cada posição no mundo. 

### Grupo 4:
 
 Henrique Moniz 20182446
 Leonardo Branco 20182157
 Tiago Rolo 20182770
