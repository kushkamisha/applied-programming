# filename = "neg-except-one.txt"
# filename = "all-negatives.txt"
# filename = "random.txt"
filename = "positives.txt"

with open("input/{}".format(filename), "r") as f:
  arr = f.readlines()

arr = list(map(lambda x: int(x.replace("\n", "")), arr))
n = arr.pop(0)

if len(arr) != int(n):
  raise Exception("The number of elements is not {}".format(n))

print("The number of elements is", n)
print("Array", arr)

# Process

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

greatest = [] # should contain at least one positive number if such exists
smallest = []
a_positive = None

for x in arr:
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

print("Greatest", greatest)
print("Smallest", smallest)
print("A positive", a_positive)

mask = list(map(lambda x: x > 0, greatest))

if(sum(mask) >= 3):
  # at least 3 positive numbers
  print("3 greatest positive from greatest")
  print(greatest[:3])
elif (sum(mask) == 0):
  if a_positive is None:
    print("just a smallest array")
    print(smallest[:3])
  else:
    print("a_positive and 2 greatest from greatest")
    print(a_positive, greatest[0], greatest[1])
elif ((len(mask) - sum(mask)) % 2 == 0):
  # even number of negative numbers
  print("2 greatest negative + 1 greatest positive from greatest")
  neg_limit = 2
  pos_limit = 1
  answer = []
  for x in greatest:
    if x > 0 and pos_limit > 0:
      answer.append(x)
      pos_limit -= 1
    elif neg_limit > 0:
      answer.append(x)
      neg_limit -= 1
  print(answer)
else:
  print("unknown case")
