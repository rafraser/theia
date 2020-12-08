import argparse, os, subprocess, time

from blender.launch_script import launch_script
from source.qc_templater import generate_template, copy_template_file, compile_files


def main(args):
    charset = args.charset
    output = args.output
    fontname = args.fontname

    # Start timing
    start_time = time.time()

    # Make output dir if not exists
    os.makedirs(output, exist_ok=True)

    # Generate SMDs in Blender
    launch_script(
        "./python/blender/letter_gen.py",
        [
            output,
            "--font",
            args.font,
            "--quality",
            str(args.quality),
            "--extrude",
            str(args.extrude),
            "--characters",
            args.charset,
        ],
    )

    # Generate QCs
    for char in charset:
        variables = [
            ("basePath", f"alphabet/{fontname}/large_{char}.mdl"),
            ("smd", f"{char}.smd"),
            ("collision_smd", f"{char}_collision.smd"),
        ]
        generate_template(output, f"large_{char}", "letter_base", variables)

        variables = [
            ("basePath", f"alphabet/{fontname}/small_{char}.mdl"),
            ("smd", f"{char}.smd"),
            ("collision_smd", f"{char}_collision.smd"),
        ]
        generate_template(output, f"small_{char}", "letter_base_small", variables)

    # Copy templates
    copy_template_file(output, "letter_base")
    copy_template_file(output, "letter_base")

    # Compile QCs
    compile_files(output, [f"large_{c}" for c in charset])
    compile_files(output, [f"small_{c}" for c in charset])

    # Done!
    print("Compiled succesfully!")
    print(f"Elapsed time: {round(time.time() - start_time, 2)} seconds")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("output")
    parser.add_argument("--charset", default="ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890")
    parser.add_argument("--font", default="C:\\Windows\\Fonts\\Roboto-Bold.ttf")
    parser.add_argument("--fontname", default="roboto")
    parser.add_argument("--quality", default=4)
    parser.add_argument("--extrude", default=0.05)
    args = parser.parse_args()
    main(args)
