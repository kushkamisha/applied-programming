import math


"""
За один прохід з послідовності довільних цілих чисел (додатні, від'ємні, нуль)
вибрати три числа, добуток яких є максимально можливим.

Технічні вимоги.
  Вхід   Текстовий файл, у першому рядку - кількість n цілих чисел (2 < n < 108),
         у наступних n рядках - цілі числа.
  Вихід  Три числа у довільному порядку та добуток. Якщо розв'язків декілька -
         вивести будь-який.
"""


def insert(arr, x, order="descending"):
  """
  Inserts element in the correct position in sorted array
  (in the descending/ascending order of absolute values)
  """
  arr.append(x)
  i = len(arr) - 1

  if order == "descending":
    while (i != 0 and abs(arr[i]) > abs(arr[i - 1])):
      arr[i], arr[i - 1] = arr[i - 1], arr[i]
      i -= 1
  else:
    while (i != 0 and abs(arr[i]) < abs(arr[i - 1])):
      arr[i], arr[i - 1] = arr[i - 1], arr[i]
      i -= 1
  return arr


def iterate_file(filename):
  greatest = []
  smallest = []
  a_positive = None

  with open("input/{}".format(filename), "r") as f:
    n = int(f.readline().replace("\n", ""))
    lines = 0

    for line in f:
      lines += 1
      x = int(line.replace("\n", ""))

      if a_positive is None:
        # collect the smallest by absolute value
        if len(smallest) < 3:
          smallest = insert(smallest, x, "ascending") # in the correct position
        else:
          if abs(smallest[-1]) > abs(x):
            smallest.pop()
            smallest = insert(smallest, x, "ascending")

      if a_positive is None and x > 0:
        a_positive = x

      # collect the greatest by absolute values
      if len(greatest) < 3:
        greatest = insert(greatest, x) # in the correct position
      elif abs(greatest[-1]) < abs(x):
        greatest.pop()
        greatest = insert(greatest, x)

  if lines != int(n):
    raise Exception("The number of elements is not {}".format(n))

  # print("Greatest", greatest)
  # print("Smallest", smallest)
  # print("A positive", a_positive)

  return greatest, smallest, a_positive


def display_answer(answer):
  print("\nЧисла, що дають максимальний добуток: {}, {} та {}".format(*answer))
  print("Максимальним добутком є {}\n".format(math.prod(answer)))


def greatest_product(filename):
  greatest, smallest, a_positive = iterate_file(filename)
  mask = list(map(lambda x: x > 0, greatest))

  answer = []
  if(sum(mask) >= 3):
    # at least 3 positive numbers
    # print("3 greatest positive from greatest")
    answer = greatest[:3]
  elif (sum(mask) == 0):
    if a_positive is None:
      # print("just a smallest array")
      answer = smallest[:3]
    else:
      # print("a_positive and 2 greatest from greatest")
      answer = [a_positive, greatest[0], greatest[1]]
  elif ((len(mask) - sum(mask)) % 2 == 0):
    # even number of negative numbers
    # print("2 greatest negative + 1 greatest positive from greatest")
    neg_limit = 2
    pos_limit = 1
    for x in greatest:
      if x > 0 and pos_limit > 0:
        answer.append(x)
        pos_limit -= 1
      elif neg_limit > 0:
        answer.append(x)
        neg_limit -= 1
  else:
    print("unknown case")

  display_answer(answer)


if __name__ == "__main__":
  # filename = "neg-except-one.txt"
  # filename = "all-negatives.txt"
  filename = "random.txt"
  # filename = "positives.txt"
  # filename  = "neg-and-zero.txt"

  greatest_product(filename)
