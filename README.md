# Rapidy

Simple and lightweight command line argument parser with type validation.

## Example
```python
""" Corree Usecase Example """
import corree

# Declare wanted flags, args and types
declared_args = {
    "age": float,
    "name": str,
    "foods": [str],
    "numbers": [int],
    "domain-name":str,
    "likes-cake": bool,
    "IP-PORT":  [str, int],
},

# This would be sys.argv[1:] usually, the parser handles
# both strings as well as lists of strings as input
given_input = """-name johndoe -age 42.2 --domain-name python.org --likes-cake /
-foods banana pineapple pizza oreos --IP-PORT 192.0.0.1 8080 -numbers 1 2 3 4"""

# Parse input
success, result = corree.parse_args(
    declared_args, given_input
)

# Output
>> success, result
True,
{
    'age': 42.2,
    'name': 'johndoe',
    'foods': ['banana', 'pineapple', 'pizza', 'oreos'],
    'numbers': [1, 2, 3, 4],
    'domain-name': 'python.org',
    'likes-cake': True,
    'IP-PORT': ["192.0.0.1", 8080]
}
```

## Specifying number of arguments
```python
one_name: str # represents a single str argument for the flag
inf_names: [str] # means infinite arguments of type str
two_names: [str, str] # means exactly two args of type str
IP-PORT: [str, int] # means a single str and a single int argument
```

## Unspecified Arguments

If a flag was not given any arguments, its value in the resulting output arguments dictionary would be an empty initialiser of its type.

### Examples

```python
# Declare wanted flags, args and types
declared_args = {
    "age": int,
    "names":  [str],
},

# This would be sys.argv[1:] usually, the parser handles
# both strings as well as lists of strings as input
given_input = ""

# Parse input
success, result = rapidy.parse_args(
    declared_args, given_input
)

# Output
>> success, result
True,
{
    'age': None,
    'names': []
}

"""
If a flag **explicitly** takes a number of arguments and none were given,
the resulting value in the output dictionary
would be an empty list, however the _success_
bool would be set to false
"""

# Declare wanted flags, args and types
declared_args = {
    "names":  [str, str],
},

# This would be sys.argv[1:] usually, the parser handles
# both strings as well as lists of strings as input
given_input = ""

# Parse input
success, result = rapidy.parse_args(
    declared_args, given_input
)

# Output
>> success, result
False,
{
    'names': []
}
```
