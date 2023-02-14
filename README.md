# Quarzo
Quarzo: a Quarto engine, developed in Python with minimax, alpha-beta pruning and iterative deepening.

##Instructions
Import the quarzo module with the line:
```python
from quarzo import QuarzoMiniMax
from quarzo import QuarzoMonteCarlo
```

They can be used with the Quarto class as follows:
```python
 game = quarto.Quarto()
 game.set_players((QuarzoMiniMax(game), QuarzoMonteCarlo(game)))
```
