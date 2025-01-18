#include "tracer.hpp"

int Tracer::indent = 0;
std::chrono::high_resolution_clock::time_point Tracer::operationStartTime =
    std::chrono::high_resolution_clock::now();

std::ofstream& Tracer::getLogFile()
{
    static std::ofstream logFile("Tracer.log");
    return logFile;
}

long long Tracer::get_nanoseconds()
{
    auto now = std::chrono::high_resolution_clock::now();
    return std::chrono::duration_cast<std::chrono::nanoseconds>(
               now - operationStartTime)
        .count();
}

void Tracer::trace(bool enter)
{
    auto& logFile = getLogFile();
    logFile << std::string(indent, ' ');

    logFile << (enter ? "Enter " : "Exit ");

    logFile << (className.empty() ? "" : className + "::") << functionName
            << " at " << get_nanoseconds() << " ns";

    if (!enter)
    {
        auto duration =
            std::chrono::duration_cast<std::chrono::nanoseconds>(
                std::chrono::high_resolution_clock::now() - startTime)
                .count();
        logFile << " (duration: " << duration << " ns)";
    }

    logFile << std::endl;
}
