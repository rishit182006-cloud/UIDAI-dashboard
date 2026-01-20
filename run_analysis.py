# This script saves the output to a file to avoid terminal truncation
import subprocess

result = subprocess.run(
    ['python', '-u', 'detailed_coverage_analysis.py'],
    capture_output=True,
    text=True,
    encoding='utf-8'
)

with open('analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(result.stdout)
    if result.stderr:
        f.write("\n\nERRORS:\n" + result.stderr)

print("Analysis complete! Report saved to analysis_report.txt")
print(f"Exit code: {result.returncode}")
