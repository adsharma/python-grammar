from collections import namedtuple
from enum import IntEnum
import re
import sys
import token as token_module


class TokenError(Exception):
    """Exception raised for tokenization errors."""

    pass


# Token type constants matching Python's token module
ENDMARKER = token_module.ENDMARKER
NAME = token_module.NAME
NUMBER = token_module.NUMBER
STRING = token_module.STRING
NEWLINE = token_module.NEWLINE
INDENT = token_module.INDENT
DEDENT = token_module.DEDENT
ERRORTOKEN = token_module.ERRORTOKEN
COMMENT = token_module.COMMENT
OP = token_module.OP


def clean_tokens(tokens):
    """Remove redundant DEDENT NEWLINE INDENT sequences."""
    i = 0
    while i < len(tokens):
        # Check for DEDENT NEWLINE INDENT sequence
        if (
            i + 2 < len(tokens)
            and tokens[i].type == TokenType.DEDENT
            and tokens[i + 1].type == TokenType.NEWLINE
            and tokens[i + 2].type == TokenType.INDENT
        ):
            # Skip DEDENT and INDENT, yield NEWLINE
            yield tokens[i + 1]
            i += 3
        else:
            yield tokens[i]
            i += 1


def _generate_tokens(source_lines):
    """Generate tokens from source lines."""
    source = "".join(source_lines)

    # Combine multiple types of whitespace/indentation handling
    tokenizer = _PythonTokenizer(source)
    tokens = clean_tokens(list(tokenizer.tokenize()))

    return tokens


def tokenize(readline):
    """
    Tokenize a source stream using a readline function.

    Args:
        readline: A function that returns a line of source code or empty string

    Returns:
        A list of token tuples (type, string, start, end, line)
    """
    source_lines = []
    while True:
        line = readline()
        if not line:
            break
        source_lines.append(line)

    return _generate_tokens(source_lines)


def generate_tokens(readline):
    """Generator version of tokenize for streaming tokens."""
    source_lines = []
    while True:
        line = readline()
        if not line:
            break
        source_lines.append(line)

    return _generate_tokens(source_lines)


class TokenType(IntEnum):
    ENDMARKER = 0
    NAME = 1
    NUMBER = 2
    STRING = 3
    NEWLINE = 4
    INDENT = 5
    DEDENT = 6
    OP = 7
    ERRORTOKEN = 8
    COMMENT = 9


# Simplified TokenInfo to match original tokenize module
TokenInfo = namedtuple("TokenInfo", ["type", "string", "start", "end", "line"])


class _PythonTokenizer:
    PATTERNS = [
        (TokenType.NUMBER, r"[0-9]+(?:\.[0-9]*)?(?:[eE][+-]?[0-9]+)?"),
        (TokenType.STRING, r'(["\'])(?:(?=(\\?))\2.)*?\1'),
        (TokenType.NAME, r"[a-zA-Z_][a-zA-Z0-9_]*"),
        (TokenType.OP, r"[():[\]{},.;:@]"),
        (TokenType.NEWLINE, r"\n"),
        (TokenType.COMMENT, r"#.*"),
    ]

    def __init__(self, source):
        self.source = source
        self.lines = source.split("\n")
        self.line_num = 0
        self.indent_stack = [0]
        self.current_line = ""

    def tokenize(self):
        while self.line_num < len(self.lines):
            self.current_line = self.lines[self.line_num]

            # Indentation handling
            indent_match = re.match(r"^\s*", self.current_line)
            current_indent = len(indent_match.group(0))

            # Generate INDENT tokens
            if current_indent > self.indent_stack[-1]:
                self.indent_stack.append(current_indent)
                yield TokenInfo(TokenType.INDENT, "", (0, 0), (0, 0), "")

            # Generate DEDENT tokens
            while current_indent < self.indent_stack[-1]:
                self.indent_stack.pop()
                yield TokenInfo(TokenType.DEDENT, "", (0, 0), (0, 0), "")

            # Tokenize line
            line_tokens = list(self._tokenize_line())

            if line_tokens:
                yield from line_tokens

            self.line_num += 1

        # Handle remaining dedents
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            yield TokenInfo(TokenType.DEDENT, "", (0, 0), (0, 0), "")

        # Final ENDMARKER token
        yield TokenInfo(TokenType.ENDMARKER, "", (0, 0), (0, 0), "")

    def _tokenize_line(self):
        pos = 0

        while pos < len(self.current_line):
            # First skip all whitespace
            whitespace_match = re.match(r"\s+", self.current_line[pos:])
            if whitespace_match:
                pos += len(whitespace_match.group(0))
                continue

            # Then try matching patterns
            for token_type, pattern in [(t, re.compile(p)) for t, p in self.PATTERNS]:
                match = pattern.match(self.current_line[pos:])
                if match:
                    token_value = match.group(0)
                    pos += len(token_value)
                    yield TokenInfo(
                        token_type,
                        token_value,
                        (0, 0),
                        (0, 0),
                        self.current_line[pos - len(token_value) :],
                    )
                    break
            else:
                # If no match, error token
                pos += 1
                yield TokenInfo(
                    TokenType.ERRORTOKEN,
                    self.current_line[pos - 1],
                    (0, 0),
                    (0, 0),
                    self.current_line[pos - 1],
                )

        # Newline at end of line
        yield TokenInfo(TokenType.NEWLINE, "", (0, 0), (0, 0), "")


def generate_tokens(readline):
    """Tokenize a source reading Python code as unicode strings.

    This has the same API as tokenize(), except that it expects the *readline*
    callable to return str objects instead of bytes.
    """
    return _generate_tokens([l for l in readline()])


# Convenience function to tokenize source code directly
def tokenize_source(source_code):
    """Tokenize source code string directly."""
    return list(_generate_tokens([source_code]))


if __name__ == "__main__":
    for x in tokenize_source(sys.stdin.read()):
        print(x)
