""" """


cases = [
    (
        {
            "names": [list],
        },
        "-names [john, doe]",
        True,
    ),
    (
        {
            "name": [str],
            "foods": [str, str],
            "age": [int],
            "domain-name": [str],
            "likes-cake": bool,
        },
        "-name johndoe -age 42 --domain-name python.org --likes-cake -foods banana pineapple",
        True,
    ),
    (
        {
            "name": [str],
            "foods": [str, str],
            "age": [int],
            "domain-name": [str],
            "likes-cake": bool,
        },
        "--name johndoe   -age 42 --domain-name python.org --likes-cake -foods banana pineapple",
        True,
    ),
    (
        {
            "name": [str],
            "foods": [str, str],
            "age": [int],
            "domain-name": [str],
            "likes-cake": bool,
        },
        "-name johndoe   -age 42 --domain-name python.org --likes-cake -foods banana",
        False,
    ),
    (
        {
            "name": [str],
            "foods": [str, str],
            "age": [int],
            "domain-name": [str],
            "likes-cake": bool,
        },
        "-name johndoe   -age 42 --domain-name --likes-cake -foods banana pineapple",
        False,
    ),
    (
        {
            "name": [str],
            "foods": [str, str],
            "age": [int],
            "domain-name": [str],
            "likes-cake": bool,
        },
        "-name johndoe   -age 42 --domain-name python.org --likes-cake True -foods banana pineapple",
        False,
    ),
    (
        {
            "name": [str],
            "foods": [str, str],
            "age": [int],
            "domain-name": [str],
            "likes-cake": bool,
        },
        "-name johndoe   -age notanint --domain-name python.org --likes-cake -foods banana pineapple",
        False,
    ),
    (
        {
            "name": [str],
            "foods": [str, str],
            "age": [int],
            "domain-name": [str],
            "likes-cake": bool,
        },
        "--help",
        False,
    ),
    (
        {
            "name": [list],
        },
        "-name [hello]",
        True,
    ),
    (
        {
            "name": [list],
        },
        "-name [hello, world]",
        True,
    ),
]
