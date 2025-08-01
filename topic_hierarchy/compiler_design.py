compiler_design = {
    "Introduction to Compilers": [
        "What is a compiler?",
        "Phases of a compiler",
        "Difference between compiler, interpreter, assembler",
        "Languages: source language, target language",
    ],

    "Lexical Analysis": [
        "Role of lexical analyzer",
        "Tokens, Lexemes, Patterns",
        "Regular expressions & Finite Automata (DFA/NFA)",
        "Lexical Errors",
        "Lexical analyzer generators (e.g., Lex, Flex)",
    ],

    "Syntax Analysis (Parsing)": [
        "Context-Free Grammar (CFG)",
        "Parse Trees and Derivations",
        "Top-Down Parsing: Recursive Descent, LL(1)",
        "Bottom-Up Parsing: Shift Reduce, LR, SLR, LALR",
        "FIRST and FOLLOW sets",
        "Parser generators (e.g., YACC, Bison)",
    ],

    "Semantic Analysis": [
        "Syntax-directed definitions",
        "Syntax-directed translation",
        "Type checking and type inference",
        "Type systems and declarations",
        "Symbol Table construction",
    ],

    "Intermediate Code Generation": [
        "Intermediate Representations: Three Address Code, Quadruples, Triples",
        "Translation of expressions and control flow",
        "Backpatching",
        "Intermediate code for procedures",
    ],

    "Code Optimization": [
        "Introduction to code optimization",
        "Local vs Global optimization",
        "Control Flow Graph (CFG)",
        "Data flow analysis",
        "Common Subexpression Elimination, Dead Code Elimination",
        "Loop optimizations (Unrolling, Invariant Code Motion)",
    ],

    "Target Code Generation": [
        "Issues in code generation",
        "Instruction selection",
        "Register allocation and assignment",
        "Peephole optimization",
        "Stack management",
    ],

    "Error Handling": [
        "Types of errors: Lexical, Syntactic, Semantic",
        "Error recovery strategies: Panic Mode, Phrase Level, Error productions",
    ],

    "Symbol Table Management": [
        "Data structures for symbol table",
        "Operations: insert, lookup, scope handling",
        "Hash tables, Tries",
    ],

    "Compiler Construction Tools": [
        "Lex and Yacc / Flex and Bison",
        "ANTLR",
        "LLVM",
        "GCC Compiler Internals",
    ],

    "Advanced Topics (Optional)": [
        "JIT Compilation (e.g., JVM, CLR)",
        "Garbage Collection Techniques",
        "Bootstrapping a Compiler",
        "Cross Compilers",
        "Interpreters vs Compilers Internals",
    ]
}
