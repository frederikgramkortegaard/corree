# Corree

## "Ask and you shall receive" - style command-line argument parser. 



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
    'likes-cake': True,''''
    'IP-PORT': ["192.0.0.1", 8080]
}
