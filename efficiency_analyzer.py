import streamlit as st
import cProfile
import pstats
import ast
import time
import io

def analyze_script(file_content):
    profiler = cProfile.Profile()
    profiler.enable()

    start_time = time.time()
    try:
        exec(file_content, {})
    except Exception as e:
        st.error(f"Execution Error: {e}")
    end_time = time.time()

    profiler.disable()

    stats_stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stats_stream).sort_stats('cumulative')
    stats.print_stats(10)  # Top 10 functions

    total_time = end_time - start_time

    return stats_stream.getvalue(), total_time

def list_functions(file_content):
    tree = ast.parse(file_content)
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    return functions

def main():
    st.set_page_config("Python Script Analyzer", layout="wide")
    st.title("🛠️ Python Script Analyzer")
    st.write("Upload a Python script to analyze its functions and performance!")

    uploaded_file = st.file_uploader("Upload a Python (.py) file", type="py")

    if uploaded_file is not None:
        file_content = uploaded_file.read().decode("utf-8")

        st.subheader("🔍 Function Analysis")
        functions = list_functions(file_content)
        if functions:
            st.success(f"Found {len(functions)} function(s):")
            for func in functions:
                st.write(f"➔ `{func}`")
        else:
            st.warning("No functions found.")

        st.subheader("⚙️ Profiling Report")
        with st.spinner("Analyzing script..."):
            profile_report, total_runtime = analyze_script(file_content)

        st.code(profile_report)

        st.subheader("⏱️ Script Runtime")
        st.info(f"Total execution time: **{total_runtime:.4f} seconds**")

        if total_runtime > 2:
            st.warning("⚡ Suggestion: The script took longer than 2 seconds. Consider optimizing it.")
        else:
            st.success("✅ Good Job! Your script runs efficiently.")

if __name__ == "__main__":
    main()
