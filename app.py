# required Python 3.8.2

from abc import ABC, abstractmethod
import random

class SafariField:
  def __init__(self, height=10, width=10):
    self.size = {"height": height, "width": width}
    self.field = []
    self.animals = ('Lion', 'Tiger', 'Wolf', 'Deer')

    self.generate()

  def generate(self):
    for h in range(self.size['height']):
      self.field.append([])
      for w in range(self.size['width']):
        animal_type = self.get_random_animal_type()
        animal = self.make_animal(animal_type)
        animal.position = {'x': w, 'y': h}

        self.field[h].append(animal)

  def render(self):
    print('Safari Field - a danger place')
    # todo: print field at start
    for h in range(len(self.field)):
      print() # new line
      for w in range(len(self.field)):
        print(self.field[h][w].symbol, end = ' ')

  def get_random_animal_type(self):
    return random.choice(self.animals)

  def make_animal(self, animal_type):
    if animal_type == 'Lion':
      return Lion(self)
    elif animal_type == 'Tiger':
      return Tiger(self)
    elif animal_type == 'Wolf':
      return Wolf(self)
    elif animal_type == 'Deer':
      return Deer(self)

    # todo: tried to make class dinamicly using polymorphism, didn't success
    # random_animal = type(random_animal_name, (random_animal_name,), {
    #   "__metaclass__": Animal
    # })
  
  def get_random_cell(self):
    x = random.randrange(self.size['width'])
    y = random.randrange(self.size['height'])
    return self.field[x][y]

  # todo: start_fight, theriocide 
  def start_conquer(self):
    print('start')
    blessed_animal = self.get_random_cell()
    blessed_animal.conquer()
    pass

  def get_neighbors(self, animal):
    neighbors = []
    # todo: change to objects to easy understand
    relatives = [
      # y,  x
      [-1,  0], # up
      [-1,  0], # up
      [-1,  1], # upRight
      [ 0,  1], # right
      [ 1,  1], # downRight
      [ 1,  0], # down
      [ 1, -1], # downLeft
      [ 0, -1], # left
      [-1, -1], # upLeft
    ]

    for r in relatives:
      try:
        neighbor = self.field[animal.position["y"] - r[0]][animal.position["x"] - r[1]]
        neighbors.append(neighbor)
      except IndexError:
        pass

    return neighbors


# using inheritance
class Animal(ABC):
  def __init__(self, field):
    self.field = field
    self.position = {"x": 0, "y": 0}

  @property
  @abstractmethod
  def type(self):
    pass

  @property
  def symbol(self):
    return self.type[0]

  @property
  @abstractmethod
  def beat(self):
    pass

  def conquer(self):
    # get fields around
    '''
    1. attach field to each animal
       get cells around
       run conqure on each of them
    2. fill animals with around fields
    3. make static method for fields to find them
    '''
    print('I am', self.type)

    # move itself out
    # todo: should I move if no beat nobody?
    self.field.field[self.position['y']][self.position['x']] = Nobody(self.field)

    neighbors = self.field.get_neighbors(self)

    for n in neighbors:
      if n.type in self.beat:
        print('i win', n.type)
        # move animal to next cell
        self.field.field[n.position['y']][n.position['x']] = self
        self.field.field[n.position['y']][n.position['x']].conquer()

    # todo: if am I deer?
    if not neighbors:
      self.field.render()


class Lion(Animal):
  type = 'Lion'
  beat = ('Tiger', 'Wolf', 'Deer')
    
class Tiger(Animal):
  type = 'Tiger'
  beat = ('Wolf', 'Deer')

class Wolf(Animal):
  type = 'Wolf'
  beat = ('Deer')

class Deer(Animal):
  type = 'Deer'
  beat = () # poor deer

class Nobody(Animal):
  type = '-'
  beat = ()


def main():
  field = SafariField()
  field.render()
  field.start_conquer()


if __name__ == "__main__":
  main()
