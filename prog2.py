"""Calculate input length; treat missing input as an empty string."""
try:
    n = input()
except EOFError:
    n = ""

print("Length:", len(n))
print("New information 2")