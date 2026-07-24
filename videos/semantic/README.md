# Semantic Analysis

This directory contains the source code for the **Semantic Analysis** episode.

Source code of this animation is in **episode.py** file.

## What is semantic analysis?

Semantic analysis is the compilation stage that gives meaning to the abstract syntax tree produced by the parser.

The semantic analyzer walks the AST, records declarations in a symbol table, resolves identifiers, verifies function calls, and checks whether expressions use compatible types.

For example, in:

```text
int result = max(a + b, 42);
```

semantic analysis verifies that:

- `result`, `a`, and `b` are valid variables;
- `a` and `b` have types compatible with `+`;
- `max` is a known function;
- the arguments of `max` match its signature;
- the returned value can be assigned to `result`.

After semantic analysis succeeds, the program is ready to be transformed into an intermediate representation.

This directory contains the Manim source code used to create the animation for this topic.
