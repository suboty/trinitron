# Lexical Analysis

This directory contains the source code for the **Lexical Analysis** episode.

## What is lexical analysis?

Lexical analysis is the first stage of compilation. 
The lexer reads the source code character by character and groups those characters into **tokens** such as keywords, identifiers, operators, literals, and punctuation.

For example:

```cpp
int result = max(a + b, 42);
```

becomes

```text
[int] [result] [=] [max] [(] [a] [+] [b] [,] [42] [)] [;]
```

During this stage, new identifiers are also recorded in the **symbol table** for use by later stages of the compiler.

This directory contains the Manim source code used to create the animation for this topic.