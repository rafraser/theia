import shutil
import os
import subprocess


def generate_template(
    output_dir: str,
    output_name: str,
    template_name: str,
    variables: list[tuple[str, str]],
) -> None:
    with open(output_dir + "/" + output_name + ".qc", "w") as f:
        for (key, value) in variables:
            f.write(f'$definevariable {key} "{value}"\n')
        f.write(f'$include "{template_name}.qc"\n')


def copy_template_file(
    output_directory: str, template_name: str, template_directory: str = "qc_templates"
) -> None:
    shutil.copy(
        f"{template_directory}/{template_name}.qc",
        f"{output_directory}/{template_name}.qc",
    )


def compile_files(directory: str, files: list[str]):
    for file in files:
        path = os.path.join(directory, file)
        subprocess.call(["sh", "./scripts/compileqc.sh", path])
