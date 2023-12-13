import re
from typing import Iterable, Pattern, Tuple
from .errors import CommandError

CMD_PATTERN = re.compile(r'\b(?:ls|cat|get|put|h)\b')
LS_PATTERN = re.compile(r'^ls(?: (\d+))?$')
CAT_PATTERN = re.compile(r'^cat ([a-zA-Z0-9_.-]+)$')
GET_PATTERN = re.compile(r'^get ([a-zA-Z0-9_.\-*]+)$')
PUT_PATTERN = re.compile(r'^put(?: (.+))?$')

type ValidCommand = Tuple[str, str]
type EmptyCommand = Tuple[None, None]

def match_command_name(template: str) -> re.Match:
    """
    Matchs the names of the command in template.
    :returns: re.Match
    """
    return CMD_PATTERN.match(template)

def match_command_args(template: str, patterns: Iterable[Pattern]) -> re.Match | None:
    """
    Matchs the args of the command in template.
    :returns: re.Match
    """
    for pattern in patterns:
        if args := pattern.match(template):
            return args
        
    return None

def match_command(template: str, patterns: Iterable[Pattern]) -> ValidCommand | EmptyCommand:
    """
    Matchs all arguments in a template.
    :returns: re.Match
    """
    cmd = match_command_name(template)
    if not cmd:
        print(CommandError(f'{template} is not a valid command.\n'))
        
    if (argsless_cmd := cmd.group(0)) == 'h':
        return argsless_cmd, None
    
    args = match_command_args(template, patterns)
    if args:
        match = args.group(1)
        return cmd.group(0), match if match else None
    
    return None, None

class FTPCommand:    
    def __init__(self, template: str) -> None:
        self.__parse_template(template)
    
    def __parse_template(self, template: str) -> None:
        self.__cmd, self.__args = match_command(template, 
            (LS_PATTERN, CAT_PATTERN, GET_PATTERN, PUT_PATTERN)
        )
        
    def is_help(self) -> bool:
        return self.__cmd == 'h'
    
    def is_ls(self) -> bool:
        return self.__cmd == 'ls'
    
    def is_cat(self) -> bool:
        return self.__cmd == 'cat'
    
    def is_get(self) -> bool:
        return self.__cmd == 'get'
    
    def is_put(self) -> bool:
        return self.__cmd == 'put'

    @property    
    def cmd(self) -> str:
        return self.__cmd
    
    @property
    def args(self) -> str:
        return self.__args
    
    def __bool__(self) -> bool:
        return bool(self.__cmd)
        
    def __repr__(self) -> str:
        return f'FTPCommand(cmd={self.__cmd}, args={self.__args})'