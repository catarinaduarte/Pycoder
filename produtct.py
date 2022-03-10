
from decimal import Decimal as dec
from typing import TextIO

CSV_DEFAULT_DELIM = ','

PRODUCT_TYPES = {
    'AL': 'Alimentação',
    'DL': 'Detergente p/ Loiça',
    'FRL': 'Frutas e Legumes'
}

class Product:
    def __init__(
            self, 
            id_: int,
            name: str,
            type_: str,
            quantity: int,
            price: dec
    ):
        if id_ < 0 or len(str(id_)) != 5:
            raise InvalidProdAttribute(f'Invalid id {id_}.')
        if not name:
            raise InvalidProdAttribute(f'Invalid name {name}.')
        if type_ not in PRODUCT_TYPES:
            raise InvalidProdAttribute(f'Invalid product type {type_}.')
        if quantity < 0:
            raise InvalidProdAttribute(f'Invalid quantity {quantity}.')
        if price < 0:
            raise InvalidProdAttribute(f'Invalid price {price}.')

        self.id = id_
        self.name = name
        self.type = type_
        self.quantity = quantity
        self.price = price
    #:

    @classmethod
    def from_csv(cls, csv_line: str) -> 'Product':
        product_attrs = csv_line.split(CSV_DEFAULT_DELIM)
        return Product(
            id_=int(product_attrs[0].strip()),
            name=product_attrs[1].strip(),
            type_=product_attrs[2].strip(),
            quantity=int(product_attrs[3].strip()),
            price=dec(product_attrs[4].strip()),
        )
    #:

    @property
    def type_name(self):
        return PRODUCT_TYPES[self.type]
    #:

    def __str__(self):
        s = self
        return f'Product {s.name} id: {s.id} price: {s.price}'
    #:

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(id={self.id}, name={self.name}, ...)'
    #:
#:

class InvalidProdAttribute(ValueError):
    pass
#:

class ProductCollection:
    def __init__(self):
        self._prods = {}
    #:

    def append(self, prod: Product):
        if prod.id in self._prods:
            raise DuplicateValue(f'Product with ID {prod.id} already exists.')
        self._prods[prod.id] = prod
    #:

    def search_by_id(self, id_: int) -> Product:
        return self._prods.get(id_)
    #:

    def search(self, filter_fn: int):
        for prod in self._prods.values():
            if filter_fn(prod):
                yield prod
        #:
    #:
    
    def __iter__(self):
        for prod in self._prods.values():
            yield prod
    #:

    def _dump(self):
        for prod in self._prods.values():
            print(prod)
        #:
    #:
#:

class DuplicateValue(Exception):
    pass
#:

def read_products(in_file_path: str):
    prods = ProductCollection()
    with open(in_file_path, 'rt') as in_:
        for line in relevant_lines(in_):
            prods.append(Product.from_csv(line))
        #:
    #:
    return prods
#:

def relevant_lines(csv_file: TextIO):
    for line in csv_file:
        if not line.strip():
            continue
        if line[0] == '#':
            continue
        yield line
    #:
#:

prods = read_products('produtos.csv')

# ITERÁVEL: Objecto a partir do qual tiramos um iterador
#           Na prática, um iterável é um objecto que pode 
#           estar à direita de um ciclo FOR.
#           Se um objecto é iterável em Python, então 
#           conseguimos obter um iterador através da função
#           ITER.
#
# ITERADOR: Objecto que permite obter o próximo elemento de
#           um iterável. Um iterador é também um iterável.
#           Dado um iterador, acedemos ao próximo elemento 
#           (e fazemos avançar o iterador) através da função 
#           NEXT.
#
# GERADOR:  Um objecto criado a partir de uma função que pode ser 
#           parada ("pause") e retomada a partir do ponto onde 
#           ficou. Ou seja, um gerador tem "memória". Um gerador 
#           é também um iterador.
#           Qualquer função com a palavra-reservada YIELD é 
#           um gerador.
# 
#       ITERÁVEL
#          ^
#          |
#       ITERADOR
#          ^
#          |
#       GERADOR


def exec_menu():
    # L - Listar Produtos
    # A - Adicionar Produto
    # G - Guardar
    # S - Sair
    pass