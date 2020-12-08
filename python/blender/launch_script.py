import subprocess


def launch_script(script_path: str, script_args: list[str], background: bool = True):
    """Launch a given Python script in Blender
    This will require

    Args:
        script_path (str): Python script to execute
        script_args (list[str]): Additional arguments to pass to the script
        background (bool, optional): Should the script run in the background?. Defaults to True.
    """
    base_args = ["blender", "--python", script_path]
    if background:
        base_args.append("--background")
    subprocess.run(base_args + ["--"] + script_args)
