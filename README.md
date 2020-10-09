# Rapidy

Simple and lightweight command line argument parser.

```python
""" Rapidy Usecase Example """
import rapidy

# Declare wanted flags, args and types
declared_args = {
    "name": [str],
    "foods": [str, str],
    "age": [int],
    "domain-name": [str],
    "likes-cake": bool,
},

# This would be sys.argv[1:] usually
given_input = "-name johndoe -age 42 --domain-name python.org --likes-cake -foods banana pineapple"

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
    'foods': ['banana', 'pineapple']
}
```
