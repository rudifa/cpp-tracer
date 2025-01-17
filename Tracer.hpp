#pragma once

#include <iostream>
#include <string>

class Tracer
{
public:
    Tracer(const std::string& name);
    ~Tracer();

private:
    std::string name;
};


Tracer::Tracer(const std::string& name) : name(name) {
    std::cout << "Enter " << name << std::endl;
}

Tracer::~Tracer() {
    std::cout << "Exit " << name << std::endl;
}
