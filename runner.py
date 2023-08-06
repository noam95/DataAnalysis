import os
import subprocess


def start_streamlit():
    main_script_path = "./main.py"
    streamlit_command = f"streamlit run {main_script_path}"
    # os.system(streamlit_command)
    subprocess.run(streamlit_command, shell=True)


if __name__ == '__main__':
    start_streamlit()
