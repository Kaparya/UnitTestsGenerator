
def print_metrics(metrics):
    """
    Prints the metrics of the generated tests in a formatted table.

    Args:
        metrics (list): A list of lists containing the metrics for each test file.
                        Each inner list should contain: [file_name, total_complexity, total_tests].
    """
    if not metrics:
        print("No tests were generated.")
        return

    print(f"{'File Name':<80}  {'Complexity':<10}   {'Tests':<5}")
    print("-" * 100)
    
    final_metric = 0
    
    for file_name, total_complexity, total_tests in metrics:
        print(f"{file_name:<80}| {total_complexity:<10} | {total_tests:<5}")
        final_metric += total_tests / total_complexity
    
    print("=" * 100)
    cur_str = f"Total files processed: {len(metrics)}"
    print(f"{cur_str:<37} |")
    cur_str = f"Final metric (tests/complexity): {min(final_metric / len(metrics), 1):.2f}"
    print(f"{cur_str:<37} |")
    print ('=' * 39)
    