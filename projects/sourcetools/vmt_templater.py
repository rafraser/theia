import subprocess, re


def convert_to_vtf(infile: str, format: str = "dxt5", pause: bool = False):
    """Use VTFCmd to convert a single input image into a VTF
    VTFCmd.exe must exist at the root level for this to work

    Args:
        infile (str): Input image file
        format (str, optional): VTF format mode. Defaults to "dxt5".
        pause (bool, optional): Whether to wait for conversion before continuing. Defaults to False.
    """
    args = ["./vtfcmd/VTFCmd.exe", "-file", infile, "-format", format, "-silent"]
    sp = subprocess.Popen(args)
    if pause:
        sp.wait()


def convert_folder_to_vtf(
    indir: str, outdir: str, format: str = "dxt5", pause: bool = False
):
    """Use VTFCmd to convert a single input image into a VTF
    VTFCmd.exe must exist at the root level for this to work

    Args:
        indir (str): Input directory. This will only convert .png images.
        outdir (str): Output directory
        format (str, optional): VTF format mode. Defaults to "dxt5".
        pause (bool, optional): Whether to wait for conversion before continuing. Defaults to False.
    """
    search = indir + "\*.png"
    args = [
        "./vtfcmd/VTFCmd.exe",
        "-folder",
        search,
        "-output",
        outdir,
        "-format",
        format,
        "-silent",
    ]

    sp = subprocess.Popen(args)
    if pause:
        sp.wait()


def generate_vmt(template: str, outdir: str, path: str, name: str, options: dict = {}):
    """Generate a .vmt from a template

    This will replace certain variables in the VMT as required
    {{ x }} will be replaced with options[x]

    Args:
        template (str): Name of the template to use
        outdir (str): Output directory
        path (str): Material path
        name (str): Material name
        options (dict, optional): Dictionary of options to use for variable replacement. Defaults to {}.
    """
    material_path = f"{path}/{name}"
    pattern = re.compile(r"{{ (.*) }}")
    options["path"] = material_path

    with open(f"templates/vmt/{template}.vmt") as infile:
        with open(f"{outdir}/{material_path}.vmt", "w") as outfile:
            line = infile.read()
            if match := re.search(pattern, line):
                line = line.replace(match.group(0), options.get(match.group(1), ""))
            outfile.write(line)
