import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

GRID_SIZE = 5
walls = [(0, 3), (2, 3), (4, 3), (1, 1), (3, 1)]

fig, ax = plt.subplots(figsize=(5, 5))
# — desenha a grade —
for x in range(GRID_SIZE + 1):
    ax.plot([x, x], [0, GRID_SIZE], 'k-')
for y in range(GRID_SIZE + 1):
    ax.plot([0, GRID_SIZE], [y, y], 'k-')

# — pinta as paredes —
for col, row in walls:
    ax.add_patch(Rectangle((col, row), 1, 1, facecolor='#ffcccc', edgecolor='k'))

ax.set_xlim(0, GRID_SIZE)
ax.set_ylim(0, GRID_SIZE)
ax.set_aspect('equal')
ax.set_xticks(range(GRID_SIZE+1))
ax.set_yticks(range(GRID_SIZE+1))
ax.set_title('Maze 5×5 (paredes)')

# **salva o arquivo PNG na raiz do projeto**:
plt.savefig('maze5x5.png', dpi=300, bbox_inches='tight')

# mostra na tela (opcional)
plt.show()
