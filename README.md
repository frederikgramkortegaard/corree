# Rapidy

Simple and lightweight command line argument parser with type validation.

```python
""" Rapidy Usecase Example """
import rapidy

# Declare wanted flags, args and types
declared_args = {
    "age": int,
    "name": str,
    "foods": [str],
    "domain-name":str,
    "likes-cake": bool,
    "IP-PORT":  [str, int]
},

# This would be sys.argv[1:] usually, the parser handles
# both strings as well as lists of strings as input
given_input = "-name johndoe -age 42 --domain-name python.org --likes-cake /
-foods banana pineapple, pizza, oreos, --IP-PORT 192.0.0.1 8080"

# Parse input
success, result = rapidy.parse_args(
    declared_args, given_input
)

# Output Dictionary
>> result
{
    'name': 'johndoe',
    'age': 42,
    'domain-name': 'python.org',
    'likes-cake': True,
    'foods': ['banana', 'pineapple', 'pizza', 'oreos'],
    'IP-PORT': ["192.0.0.1", 8080]
}
```
