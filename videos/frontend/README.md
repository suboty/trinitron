# Compiler Frontend

This directory contains the source code for the **Frontend** episode.

Source code of this animation is in **episode.py** file.

The compiler frontend is responsible for understanding your source code.

It consists of three main stages:

* **Lexical Analysis** — converts a stream of characters into tokens.
* **Syntax Analysis** — transforms tokens into an Abstract Syntax Tree (AST).
* **Semantic Analysis** — resolves identifiers, checks types, and verifies that the program follows the language's semantic rules.

The result of the frontend is a validated program representation that can be passed to the compiler backend for optimization and code generation.

This directory contains the Manim animations used to visualize how these stages work.