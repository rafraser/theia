import argparse, os, subprocess
from source.qc_templater import generate_template, copy_template_file, compile_files


def font_file_to_name(file: str):
    pass


def main(args):
    charset = args.charset
    output = args.output
    fontname = "roboto"

    # Make output dir if not exists
    os.makedirs(output, exist_ok=True)

    # Generate SMDs
    process = subprocess.run(
        ["blender", "--python", "./blender/letter_gen.py", "--", output]
    )

    # Generate QCs
    for char in charset:
        variables = [
            ("basePath", f"alphabet/{fontname}/large_{char}.mdl"),
            ("smd", f"{char}.smd"),
        ]
        generate_template(output, f"large_{char}", "letter_base", variables)

        variables = [
            ("basePath", f"alphabet/{fontname}/small_{char}.mdl"),
            ("smd", f"{char}.smd"),
        ]
        generate_template(output, f"small_{char}", "letter_base_small", variables)

    # Copy templates
    copy_template_file(output, "letter_base")
    copy_template_file(output, "letter_base_small")

    # Compile QCs
    compile_files(output, [f"large_{c}" for c in charset])
    compile_files(output, [f"small_{c}" for c in charset])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--charset", default="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    parser.add_argument("--font", default="C:\\Windows\\Fonts\\Roboto-Bold.ttf")
    args = parser.parse_args()
    main(args)
