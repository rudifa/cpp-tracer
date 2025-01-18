# cpp-tracer

A C++ project.

Contains the class `Tracer` that can be used to trace the execution of a program.

Function `bank_demo` is a simple example of how to use `class Tracer`.

### build cmake files

```
cpp-tracer % mkdir -p build && cd build
build % cmake ..
```

### build the `cpp-tracer` application with cmake

```
build % make
build % cmake --build . # same as make
```

### run the `cpp-tracer` application

```
cpp-tracer % build/cpp-tracer
`
```

This will update the file `build/Tracer.log`.
