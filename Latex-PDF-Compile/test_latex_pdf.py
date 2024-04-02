import unittest
import subprocess
import time
from unittest.mock import patch
# from LatexToPDF import compile_latex_to_pdf

def compile_latex_to_pdf(file_name):
    start_time = time.time()

    latex_file_path = f"{file_name}.tex"
    output_pdf_path = f"{file_name}.pdf"

    try:
        subprocess.run(["pdflatex", "-interaction=nonstopmode", latex_file_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to compile LaTeX file. Error: {e}")
        return False
    else:
        print(f"Compilation successful. PDF saved as {output_pdf_path}.")

        end_time = time.time()
        print("\nExecution time:", end_time - start_time)
        return True

class TestLatexCompilationWithTiming(unittest.TestCase):

    def test_compile_with_timing(self):
        # Setup: Ensure you have a small, valid .tex file named 'TestFile.tex'
        file_name = "TestFile"  # Use a real, small LaTeX file for this test

        start_time = time.time()
        result = compile_latex_to_pdf(file_name)
        end_time = time.time()

        self.assertTrue(result, "The LaTeX file should compile successfully.")
        runtime = end_time - start_time
        print(f"Compilation time: {runtime:.2f} seconds.")

        # Optionally, assert on runtime if you have a maximum allowed time
        max_allowed_time = 10  # seconds, adjust as needed
        self.assertTrue(runtime < max_allowed_time, f"Compilation should take less than {max_allowed_time} seconds.")

if __name__ == '__main__':
    unittest.main()
