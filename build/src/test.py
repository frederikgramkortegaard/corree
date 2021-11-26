import corree


xargs = {
    "name": str,
    "age": (int)
}


s, r = corree.parse("--name frederik", xargs)
print(s, r)
