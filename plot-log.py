#! python

import matplotlib.pyplot as plt
import re
import sys


class FunctionCallGraph:
    def __init__(self, log_file):
        self.log_file = log_file
        self.functions = {}

    def parse_log_file(self):
        with open(self.log_file, 'r') as f:
            log_lines = f.readlines()

        for line in log_lines:
            match = re.search(r'Enter (.*) at (\d+) ns', line)
            if match:
                func_name = match.group(1)
                timestamp = int(match.group(2))
                if func_name not in self.functions:
                    self.functions[func_name] = []
                self.functions[func_name].append((timestamp, 'enter'))
            match = re.search(
                r'Exit (.*) at (\d+) ns \(duration: (\d+) ns\)', line)
            if match:
                func_name = match.group(1)
                timestamp = int(match.group(2))
                duration = int(match.group(3))
                if func_name not in self.functions:
                    self.functions[func_name] = []
                self.functions[func_name].append((timestamp, 'exit'))

    def plot_graph(self):
        _, ax = plt.subplots(figsize=(12, 6))
        colors = self._generate_colors()
        stack_levels = {func: i for i, func in enumerate(self.functions)}

        max_stack_depth, functions_at_levels = self._plot_function_lines(
            ax, colors, stack_levels)
        self._set_plot_properties(
            ax, max_stack_depth, functions_at_levels, colors, stack_levels)
        plt.show()

    def _generate_colors(self):
        return plt.cm.rainbow([i / len(self.functions) for i in range(len(self.functions))])

    def _plot_function_lines(self, ax, colors, stack_levels):
        func_stack = []
        all_events = []
        max_stack_depth = 0
        functions_at_levels = {}

        # Collect all events and sort them by timestamp
        for func_name, events in self.functions.items():
            for time, event_type in events:
                all_events.append((time, event_type, func_name))
        all_events.sort(key=lambda x: x[0])

        print(f'_plot_function_lines: all_events: {all_events}')

        for i, (time, event_type, func_name) in enumerate(all_events):
            color = colors[stack_levels[func_name]]
            if event_type == 'enter':
                current_level = len(func_stack)
                self._draw_enter_event(ax, func_name, time, color, func_stack)
                max_stack_depth = max(max_stack_depth, len(func_stack))

                # Add function to the current level
                if current_level not in functions_at_levels:
                    functions_at_levels[current_level] = []
                if func_name not in functions_at_levels[current_level]:
                    functions_at_levels[current_level].append(func_name)

            elif event_type == 'exit':
                self._draw_exit_event(ax, func_name, time, color, func_stack)

            # Draw top of stack line to the next event or to the end
            if func_stack:
                next_time = all_events[i+1][0] if i + \
                    1 < len(all_events) else time
                top_func, _, top_level = func_stack[-1]
                top_color = colors[stack_levels[top_func]]
                ax.plot([time, next_time], [top_level, top_level],
                        color=top_color, linewidth=1)
                print(f'Drawing top of stack for {
                    top_func} from {time} to {next_time}')

        self._draw_full_width_lines(ax, colors, stack_levels)
        return max_stack_depth, functions_at_levels

    def _draw_enter_event(self, ax, func_name, time, color, func_stack):
        current_level = len(func_stack)
        ax.plot([time, time], [current_level, current_level + 1],
                color=color, linewidth=1)
        func_stack.append((func_name, time, current_level + 1))
        print(f'_handle_enter_event for {
              func_name} with func_stack {func_stack} at time {time}')

    def _draw_exit_event(self, ax, func_name, time, color, func_stack):
        for k in range(len(func_stack) - 1, -1, -1):
            if func_stack[k][0] == func_name:
                _, enter_time, enter_level = func_stack.pop(k)
                current_level = func_stack[-1][2] if func_stack else 0
                ax.plot([time, time], [enter_level, current_level],
                        color=color, linewidth=1)
                print(f'_handle_exit_event for {
                      func_name} with func_stack {func_stack} at time {time}')
                break

    def _draw_top_of_stack(self, ax, func_stack, colors, stack_levels, time):
        if func_stack:
            top_func, top_time, top_level = func_stack[-1]
            ax.plot([top_time, time], [top_level, top_level],
                    color=colors[stack_levels[top_func]], linewidth=1)
            print(f'_draw_top_of_stack for {top_func} at {
                  top_level} from func_stack {func_stack}')

    def _draw_full_width_lines(self, ax, colors, stack_levels):
        for func_name in self.functions.keys():
            level = stack_levels[func_name] + 1
            ax.axhline(y=level, xmin=0.0, xmax=1,
                       color='gray', linewidth=1, alpha=0.3)
            print(f'_draw_full_width_lines for {func_name} at level {level}')

        ax.set_xlim(left=0)

    def _set_plot_properties(self, ax, max_stack_depth, functions_at_levels, colors, stack_levels):
        # Remove y-ticks but keep the left spine
        ax.set_yticks([])
        ax.spines['left'].set_visible(True)

        # Add colored function names as text
        for level, functions in functions_at_levels.items():
            y_pos = level + 1  # +1 to align with the function lines
            x_pos = 0.01  # Start position for text
            for func_name in functions:
                color = colors[stack_levels[func_name]]
                text = ax.text(x_pos, y_pos, func_name, color=color,
                               ha='left', va='bottom', fontweight='bold',
                               transform=ax.get_yaxis_transform())

                # Move x_pos for the next function name
                bbox = text.get_window_extent(
                    renderer=ax.figure.canvas.get_renderer())
                x_pos += bbox.width / ax.figure.dpi / \
                    ax.figure.get_figwidth() + 0.01  # Add a small gap

        ax.set_xlabel('Time (ns)')
        ax.set_title('Function Call Graph')

        # Set the y-limit (vertical range) for the plot
        ax.set_ylim(0, max_stack_depth + 1)

        # Add a small left margin for the function names
        plt.subplots_adjust(left=0.025, right=0.975, top=0.95, bottom=0.1)

    def _rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % tuple(int(x * 255) for x in rgb[:3])


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python function_call_graph.py <log_file_path>')
        sys.exit(1)

    log_file = sys.argv[1]
    graph = FunctionCallGraph(log_file)
    graph.parse_log_file()
    graph.plot_graph()
