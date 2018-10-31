# -*- coding: utf-8 -*-

"""Algoritmos para o Problema de localização de ponto

"""
from . import slab

# cada entrada deve ter:
#  [ 'nome-do-modulo', 'nome-da-funcao', 'nome do algoritmo' ]
children = [ 
    ( 'slab', 'SlabDecomposition', 'Slab Decomposition' ) 
]

#children = algorithms

#__all__ = [ 'graham', 'gift' ]
__all__ = [a[0] for a in children]
