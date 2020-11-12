""" """

import re
import sys
import logging

from typing import * 
from enum import Enum
from dataclasses import dataclass, field

logging.basicConfig(level=logging.DEBUG)

class TokenType(Enum):
    flag = 1
    argument = 2

@dataclass
class Token:
    t_type: TokenType
    value: str

regex_lexing_pattern = r"-?\S*"


def lex(tokens: str) -> Generator[Token, None, bool]:
    """ Returns the given string as a list of Tokens """

    offset: int = 0
    tokens = re.findall(regex_lexing_pattern, tokens)
    
    for token in tokens[::2]:

        # Token is a flag
        if token.startswith('-'):
            
            # Remove prexix dashes
            while token[offset] == '-':
                offset += 1
            
            token = token[offset:]
                
            yield Token(TokenType.flag, token)

        # Token is an argument
        else:
            yield Token(TokenType.argument, token)


def validate_and_cast(token: str, caster: Union[Callable, List[Callable]]) -> Tuple[int, Any]:
    """ Tries to typecase a given string to a(ny) given type callable,
    returns the success state and the resulting typecast value
    """

    success: bool = False 
    if type(caster) != list:
        caster = [caster]

    for cast in caster:
        try:
            token = cast(token)
            success = True
            break
        except:
            continue

    return (success, token)


def parse(itokens: str, a_args: Dict[str, any]) -> Tuple[bool, Dict[str, Any]]:
    """ """
    
    global tokens
    tokens = list(lex(itokens))

    FAULTY_OUTPUT = (False, dict())

    def eat(tokens: List[Token]) -> Union[Token, None]:
        out = None
        if len(tokens) > 0:
            out = tokens.pop(0)

        return out

    b_args = dict()

    while (token := eat(tokens)) is not None:

        # Token is a flag
        if token.t_type == TokenType.flag:

            # Flag is not a possible option
            if not token.value in a_args:
                logging.error(f"'{token.value}' is not specified as an option")
                return FAULTY_OUTPUT

            # Validate Arguments
            
            ## Flag is a boolean
            if a_args[token.value] == bool:
                b_args[token.value] = True
                continue
            
            ## Flag only takes a single argument
            if a_args[token.value] in (str, int, float):
                new_token = eat(tokens)

                # Expected argument could not be found
                if new_token is None:
                    logging.error(f"Flag: '{token.value}' expected an argument but none were given")
                    return FAULTY_OUTPUT

                success, argument = validate_and_cast(new_token.value, a_args[token.value])
             
                # Given argument cannot be cast to its expected type
                if success is False:
                    logging.error(f"Flag '{token.value}' received argument '{new_token.value}' which could not be cast to its expected type '{a_args[token.value]}'")
                    return FAULTY_OUTPUT

                # Set final argument value for flag
                b_args[token.value] = argument
                
            ## Flag can takes multiple arguments
            elif (wrapper_type := type(a_args[token.value])) in (list, tuple):
        
                # Flag takes explicit arguments
                if wrapper_type == tuple:
                    b_args[token.value] = list()

                    # Find expected arguments
                    for i in range(len(a_args[token.value])):
                        new_token = eat(tokens)

                        # Expected an argument but did not find any
                        if new_token is None or new_token.t_type == TokenType.flag:
                            logging.error(f"Flag '{token.value}' expected {len(a_args[token.value])} arguments but only {i + 1} were found")
                            return FAULTY_OUTPUT

                        success, argument = validate_and_cast(new_token.value, a_args[token.value][i])
                        
                        # Argument can not be cast to expected type
                        if success is False:
                            logging.error(f"Flag '{token.value}' received argument '{new_token.value}' which could not be cast to its expected type '{a_args[token.value]}'")
                            return FAULTY_OUTPUT
                        
                        b_args[token.value].append(argument)
                    
                    # Rewrap found arguments into a tuple 
                    b_args[token.value] = tuple(b_args[token.value])

                # Flag take implicit arguments
                elif wrapper_type == list:
                    b_args[token.value] = list()

                    # Look ahead for arguments fitting criteria
                    while (new_token := eat(tokens)):
                        
                        # No more arguments given to flag
                        if new_token is None or new_token.t_type == TokenType.flag:
                            tokens.insert(0, new_token)
                            logging.info(f"flag '{token.value}' found no more args")
                            break

                        success, argument = validate_and_cast(new_token.value, [int, float, str])
                        
                        # Argument can not be cast to expected type
                        if success is False:
                            logging.error(f"Flag '{token.value}' received argument '{new_token.value}' which could not be cast to its expected type '{a_args[token.value]}'")
                            return FAULTY_OUTPUT

                        b_args[token.value].append(argument)

    
    return b_args

if __name__ == "__main__":
    wanted_args = {
            "foods":str,
            "names": str,
            "files": [str, int],
            "items": (str, int, str, str)
    }
    args = parse("-foods banana -names test guess -files a b c 1 2 3 -items my 2 toy ducks", wanted_args)
    print(args)
