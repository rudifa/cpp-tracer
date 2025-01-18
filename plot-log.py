#!/usr/bin/env python3

import matplotlib.pyplot as plt
import re
import sys
from typing import Dict, List, Tuple
import numpy as np


class FunctionCallGraph:
    def __init__(self, log_file: str):
        self.log_file = log_file
        self.functions: Dict[str, List[Tuple[int, str]]] = {}

    def parse_log_file(self):
        pattern = r'(Enter|Exit) (.*?) at (\d+) ns(?:\s+\(duration: (\d+) ns\))?'
        with open(self.log_file, 'r') as f:
            for line in f:
                match = re.search(pattern, line)
                if match:
                    event_type, func_name, timestamp = match.group(
                        1), match.group(2), int(match.group(3))
                    if func_name not in self.functions:
                        self.functions[func_name] = []
                    self.functions[func_name].append(
                        (timestamp, event_type.lower()))

    def plot_graph(self):
        _, ax = plt.subplots(figsize=(12, 6))
        colors = self._generate_colors()
        stack_levels = {func: i for i, func in enumerate(self.functions)}

        max_stack_depth, functions_at_levels = self._plot_function_lines(
            ax, colors, stack_levels)
        self._set_plot_properties(
            ax, max_stack_depth, functions_at_levels, colors, stack_levels)
        plt.show()

    def _generate_colors(self) -> List[Tuple[float, float, float, float]]:
        return plt.cm.rainbow(np.linspace(0, 1, len(self.functions)))

    def _plot_function_lines(self, ax: plt.Axes, colors: List[Tuple[float, float, float, float]],
                             stack_levels: Dict[str, int]) -> Tuple[int, Dict[int, List[str]]]:
        func_stack: List[Tuple[str, int, int]] = []
        all_events = [(time, event_type, func_name)
                      for func_name, events in self.functions.items()
                      for time, event_type in events]
        all_events.sort(key=lambda x: x[0])
        max_stack_depth = 0
        functions_at_levels: Dict[int, List[str]] = {}

        for i, (time, event_type, func_name) in enumerate(all_events):
            color = colors[stack_levels[func_name]]
            if event_type == 'enter':
                current_level = len(func_stack)
                self._draw_enter_event(ax, func_name, time, color, func_stack)
                max_stack_depth = max(max_stack_depth, len(func_stack))

                if current_level not in functions_at_levels:
                    functions_at_levels[current_level] = []
                if func_name not in functions_at_levels[current_level]:
                    functions_at_levels[current_level].append(func_name)

            elif event_type == 'exit':
                self._draw_exit_event(ax, func_name, time, color, func_stack)

            if func_stack:
                next_time = all_events[i+1][0] if i + \
                    1 < len(all_events) else time
                top_func, _, top_level = func_stack[-1]
                top_color = colors[stack_levels[top_func]]
                ax.plot([time, next_time], [top_level, top_level],
                        color=top_color, linewidth=1)

        self._draw_full_width_lines(ax, stack_levels)
        return max_stack_depth, functions_at_levels

    def _draw_enter_event(self, ax: plt.Axes, func_name: str, time: int, color: Tuple[float, float, float, float],
                          func_stack: List[Tuple[str, int, int]]):
        current_level = len(func_stack)
        ax.plot([time, time], [current_level, current_level + 1],
                color=color, linewidth=1)
        func_stack.append((func_name, time, current_level + 1))

    def _draw_exit_event(self, ax: plt.Axes, func_name: str, time: int, color: Tuple[float, float, float, float],
                         func_stack: List[Tuple[str, int, int]]):
        for k in range(len(func_stack) - 1, -1, -1):
            if func_stack[k][0] == func_name:
                _, _, enter_level = func_stack.pop(k)
                current_level = func_stack[-1][2] if func_stack else 0
                ax.plot([time, time], [enter_level, current_level],
                        color=color, linewidth=1)
                break

    def _draw_full_width_lines(self, ax: plt.Axes, stack_levels: Dict[str, int]):
        for func_name in self.functions.keys():
            level = stack_levels[func_name] + 1
            ax.axhline(y=level, xmin=0.0, xmax=1,
                       color='gray', linewidth=1, alpha=0.3)

        ax.set_xlim(left=0)

    def _set_plot_properties(self, ax: plt.Axes, max_stack_depth: int,
                             functions_at_levels: Dict[int, List[str]],
                             colors: List[Tuple[float, float, float, float]],
                             stack_levels: Dict[str, int]):
        ax.set_yticks([])
        ax.spines['left'].set_visible(True)

        for level, functions in functions_at_levels.items():
            y_pos = level + 1
            x_pos = 0.01
            for func_name in functions:
                color = colors[stack_levels[func_name]]
                text = ax.text(x_pos, y_pos, func_name, color=color,
                               ha='left', va='bottom', fontweight='bold',
                               transform=ax.get_yaxis_transform())

                bbox = text.get_window_extent(
                    renderer=ax.figure.canvas.get_renderer())
                x_pos += bbox.width / ax.figure.dpi / ax.figure.get_figwidth() + 0.01

        ax.set_xlabel('Time (ns)')
        ax.set_title('Function Call Graph')
        ax.set_ylim(0, max_stack_depth + 1)
        plt.subplots_adjust(left=0.025, right=0.975, top=0.95, bottom=0.1)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python plot-log.py <log_file_path>')
        sys.exit(1)

    log_file = sys.argv[1]
    graph = FunctionCallGraph(log_file)
    graph.parse_log_file()
    graph.plot_graph()
