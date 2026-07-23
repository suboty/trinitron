# Syntax Analysis

This directory contains the source code for the **Syntax Analysis** episode.

## What is syntax analysis?

Syntax analysis is the second stage of compilation.

The parser reads the stream of tokens produced by the lexer and checks whether they follow the grammar of the programming language.

For example:

```text
[int] [result] [=] [max] [(] [a] [+] [b] [,] [42] [)] [;]
```

is transformed into an **Abstract Syntax Tree**, or AST:

```text
Declaration
├── Type: int
└── Assignment
    ├── Identifier: result
    └── Call
        ├── Function: max
        ├── Binary Expression: +
        │   ├── Identifier: a
        │   └── Identifier: b
        └── Number: 42
```

During this stage, the parser processes tokens from left to right, enters nested grammar rules recursively, and returns completed subtrees as each construct is recognized.

The resulting AST represents the structure of the program and is used by later compilation stages.

This directory contains the Manim source code used to create the animation for this topic.