# Rapidy

Simple and lightweight command line argument parser with type validation.

## Example
```python
""" Rapidy Usecase Example """
import rapidy

# Declare wanted flags, args and types
declared_args = {
    "age": int,
    "name": str,
    "foods": [str],
    "numbers": [int],
    "domain-name":str,
    "likes-cake": bool,
    "IP-PORT":  [str, int],
},

# This would be sys.argv[1:] usually, the parser handles
# both strings as well as lists of strings as input
given_input = """-name johndoe -age 42 --domain-name python.org --likes-cake /
-foods banana pineapple, pizza, oreos, --IP-PORT 192.0.0.1 8080 -numbers 1 2 3 4"""

# Parse input
success, result = rapidy.parse_args(
    declared_args, given_input
)

# Output Dictionary
>> result
{
    'age': 42,
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