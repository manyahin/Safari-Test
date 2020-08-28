#!/usr/bin/python

from abc import ABC, abstractmethod
import random
import copy
import sys

if sys.version_info[0] < 3 or sys.version_info[1] < 6:
  print('Required Python version 3.6 or higher')
  sys.exit()

# Python has recursion limit, so big field will not work with that algorithm
# print('Recursion limit:', sys.getrecursionlimit())


class Safari:
  def __init__(self, height=10, width=10):
    self.size = {"height": height, "width": width}
    self.matrix = []
    self.animals = ('Lion', 'Tiger', 'Wolf', 'Deer')

    self.generate()
    print('Board at start:')
    self.render()

  def generate(self):
    for h in range(self.size['height']):
      self.matrix.append([])
      for w in range(self.size['width']):
        animal_type = self.get_random_animal_type()
        animal = self.make_animal(animal_type)
        animal.position = {'y': h, 'x': w}

        self.matrix[h].append(animal)

  def render(self):
    for h in range(len(self.matrix)):
      print()  # new line
      for w in range(len(self.matrix[h])):
        print(self.matrix[h][w].symbol, end=' ')

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

  def get_random_cell(self):
    y = random.randrange(self.size['height'])
    x = random.randrange(self.size['width'])
    print(f'\n\nChosen cell: [{y + 1}, {x + 1}]: {self.matrix[y][x].symbol}')
    return self.matrix[y][x]

  def get_neighbors(self, animal):
    neighbors = []
    relatives = [
        {'y': -1, 'x':  0},  # up
        {'y': -1, 'x':  1},  # upRight
        {'y':  0, 'x':  1},  # right
        {'y':  1, 'x':  1},  # downRight
        {'y':  1, 'x':  0},  # down
        {'y':  1, 'x': -1},  # downLeft
        {'y':  0, 'x': -1},  # left
        {'y': -1, 'x': -1},  # upLeft
    ]

    for r in relatives:
      try:
        y = animal.position['y'] - r['y']
        x = animal.position['x'] - r['x']

        # prevent negative indexes because Python allow it by default
        if x < 0 or y < 0:
          raise IndexError('Negative indexes not allowed')

        neighbor = self.matrix[y][x]
        neighbors.append(neighbor)
      except IndexError:
        # out of border, do nothing
        pass

    return neighbors

  def live(self):
    blessed_animal = self.get_random_cell()
    blessed_animal.conquer()
    pass


# using inheritance
class Animal(ABC):
  def __init__(self, field):
    self.field = field
    self.position = {"y": 0, "x": 0}
    '''
        the counter with an amount of required iterations to do
        use Python language property that reference to object is the same for cloned objects
        thus this counter will be the same for all copied objects of the same animal
        '''
    self.steps_todo = {'count': 1}

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
    '''
    1. move the animal out of the cell
    2. get neighboars and check which of them can be beated
    3. copy the animal to possible cells
    4. execute the same logic for other cells with the animal (recursion)
    '''
    # move the animal out of the cell
    self.field.matrix[self.position['y']
                      ][self.position['x']] = Nobody(self.field)
    self.steps_todo['count'] -= 1

    neighbors = self.field.get_neighbors(self)
    animal_copies = []

    for n in neighbors:
      if n.type in self.beat:
        self.steps_todo['count'] += 1

        # copy the predator to next cells
        animal_copy = copy.copy(self)
        animal_copy.position = {'x': n.position['x'], 'y': n.position['y']}
        animal_copies.append(animal_copy)

        # update field with new position of animals
        self.field.matrix[n.position['y']][n.position['x']] = animal_copy

    # check if there is more available cells to discover
    if not self.steps_todo['count']:
      print('\nBoard after conquer:')
      self.field.render()
    else:
      for a in animal_copies:
        a.conquer()


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
  beat = ()  # poor deer


class Nobody(Animal):
  # dummy animal to fill the board with dead bodies
  type = '-'
  beat = ()


def main():
  safari = Safari()
  safari.live()


if __name__ == "__main__":
  main()
