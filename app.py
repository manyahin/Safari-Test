# Python 3.8.2

from abc import ABC, abstractmethod
import random

class SafariField:

  def __init__(self, width=10, height=10):
    self.field = []
    self.animals = ('Lion', 'Tiger', 'Wolf', 'Deer')

    self.generate_field(width, height)
    # self.matrix = [[0 for x in range(width)] for y in range(height)]

  def generate_field(self, width, height):
    for h in range(height):
      self.field.append([])
      for _ in range(width):
        random_animal_name = self.get_random_animal_name()
        if random_animal_name == 'Lion':
          self.field[h].append(Lion())
        elif random_animal_name == 'Tiger':
          self.field[h].append(Tiger())
        elif random_animal_name == 'Wolf':
          self.field[h].append(Wolf())
        elif random_animal_name == 'Deer':
          self.field[h].append(Deer())
   
    # todo: tried to make class dinamicly, didn't success
    # todo: check if class exists
    # using polymorphism
    # random_animal = type(random_animal_name, (random_animal_name,), {
    #   "__metaclass__": Animal
    # })

    pass

  def render_field(self):
    print('Safari Field - a danger place')
    for h in range(len(self.field)):
      print()
      for w in range(len(self.field)):
        print(self.field[h][w].symbol, end = ' ')

  def get_random_animal_name(self):
    return random.choice(self.animals)

# using inheritance
class Animal(ABC):
  @property
  @abstractmethod
  def type(self):
    pass

  @property
  def symbol(self):
    return self.type[0]

  def conquere(self):
    print('I am', self.type)

  def get_symbol(self):
    pass

class Lion(Animal):
  type = 'Lion'
    
class Tiger(Animal):
  type = 'Tiger'

class Wolf(Animal):
  type = 'Wolf'  

class Deer(Animal):
  type = 'Deer'


# l = Lion()
# l.conquere()

# print(l.type)

# d = Deer()
# d.conquere()

x = SafariField()
x.render_field()

# print(x.field)

