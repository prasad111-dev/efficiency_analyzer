import time
import cProfile
import pstats
import ast


def analyze_script(script_path):
    print(f"\nAnalyzing {script_path}...\n")

    # Profile the entire script
    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.time()
    exec(open(script_path).read(), {})
    end_time = time.time()

    profiler.disable()

    # Save profile stats
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')

    print("\n--- Profiling Report ---")
    stats.print_stats(10)  # Top 10 functions

    total_time = end_time - start_time
    print(f"\n⏱ Total Runtime: {total_time:.4f} seconds")

    if total_time > 2:
        print("\n⚡ Suggestion: The script took longer than 2 seconds to run. You may want to optimize it.")
    else:
        print("\n✅ Good Job: Your script runs efficiently!")


def list_functions(script_path):
    with open(script_path, "r") as file:
        tree = ast.parse(file.read(), filename=script_path)

    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions


def main():
    script_path = input("Enter the path of the Python script to analyze: ").strip()

    try:
        functions = list_functions(script_path)
        if functions:
            print("\nFound Functions:")
            for func in functions:
                print(f"  ➔ {func}")
        else:
            print("\nNo functions found in the script.")

        analyze_script(script_path)

    except Exception as e:
        print(f"\n❌ Error analyzing script: {e}")


if __name__ == "__main__":
    main()
