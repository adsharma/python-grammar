Some experimental changes to python-3.13+ grammar

These changes seek to implement structural pattern matching in a way
that's compatible with other compiled languages such as Rust, C++ (proposed)
and borgo (a language that compiles to golang)

Uses [pegen](https://github.com/we-like-parsers/pegen). Has instructions on
installation and how to parse the test cases.

You'll need to pick up https://github.com/we-like-parsers/pegen/pull/111
