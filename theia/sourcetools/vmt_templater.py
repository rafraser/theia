import subprocess


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