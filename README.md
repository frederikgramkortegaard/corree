# corree
Command-line arguments in an _**"Ask and you shall receive"**_ fashion.

Pythons standard [argparser](https://docs.python.org/3/library/argparse.html) isn't very pretty, nor is it short, compact or to the point.  This tool is meant to fill the gap between "quick-and-dirty" and overly complex. 


However simple it is, this parser _does_ support type validation. Combine this with an easy-to-use system for specifying the number and types of arguments expected for a flag and you get a suprisingly powerful tool.

---

:notebook_with_decorative_cover: note: _the notion of raising exceptions is not one that is used here.  The "success" flag returned by _parse_args_ is to be used to validate proper responses_


## Example
