import os
import subprocess
import sys
import webbrowser

from src.config import EnvironmentalVariableNames as EnvVar, get_env


def main():

    # Getting path to python executable (full path of deployed python on Windows)
    executable = sys.executable

    # Open browser tab. May temporarily display error until streamlit server is started.
    webbrowser.open("http://localhost:8501")

    # Run streamlit server
    path_to_main = os.path.join(
        get_env(EnvVar.EMPORIO_VESTIARIO_DASHBOARD_WORKING_DIR), "src", "Home.py"
    )
    result = subprocess.run(
        f"{executable} -m streamlit run {path_to_main} --server.headless=true --global.developmentMode=false",
        shell=True,
        capture_output=True,
        text=True,
    )

    # These are printed only when server is stopped.
    # NOTE: you have to manually stop streamlit server killing process.
    print(result.stdout)
    print(result.stderr)


if __name__ == "__main__":
    main()