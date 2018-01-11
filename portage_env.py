import subprocess

EPREFIX = subprocess.check_output(["portageq", "envvar", "EPREFIX"]).decode().strip()
ETC = EPREFIX + "/etc"
VARDBPKG = EPREFIX + "/var/db/pkg"
