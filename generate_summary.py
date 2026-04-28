import os
import subprocess
import tempfile
from datetime import datetime

def main():
    model = "github-copilot/gpt-5-mini"
    
    plan_content = """
    1. Look for any changes since the last commit in the current directory using git.
    2. Ensure a 'summaries' directory exists in the current directory.
    3. Create a summary of the changes in a markdown file under 'summaries/'.
    4. The filename should include the current timestamp.
    """
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as refinement_file:
        refinement_file.write(plan_content.strip())
        refinement_path = refinement_file.name

    try:
        command = [
            "opencode",
            "run",
            "please follow the plan in the provided file:",
            "--file",
            refinement_path,
            "--agent",
            "build",
            "--model",
            model,
            "--dangerously-skip-permissions"
        ]
        
        print(f"Spawning opencode... \nCommand: {' '.join(command)}\n")
        
        subprocess.run(command, cwd=os.getcwd(), check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"opencode exited with error: {e}")
    finally:
        if os.path.exists(refinement_path):
            os.remove(refinement_path)

if __name__ == "__main__":
    main()
