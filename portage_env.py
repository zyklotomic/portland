import subprocess

EPREFIX = subprocess.check_output(["portageq", "envvar", "EPREFIX"]).decode().strip()

ETC = EPREFIX + "/etc"
VARDBPKG = EPREFIX + "/var/db/pkg"
USE_DESC = EPREFIX + "/usr/portage/profiles/use.desc"
USE_LOCAL_DESC = EPREFIX + "/usr/portage/profiles/use.local.desc"
EMERGE_LOG_DIR = EPREFIX + "/var/log/emerge.log"
EBUILD_TREE = EPREFIX + "/usr/portage"
