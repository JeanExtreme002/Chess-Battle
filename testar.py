from core import *

b = Board()
b.imprimir()
print()

p = Pawn.Pawn(Color.White,1,1)
p.move((2, 2), b.pecas)
b.imprimir()
