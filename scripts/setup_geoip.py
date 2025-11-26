#!/usr/bin/env python
"""
Setup helper to prepare GeoIP directory and optionally download GeoLite2-City.mmdb
If MAXMIND_LICENSE_KEY env var is set, the script will attempt to download and extract the DB.
"""
import os
import sys
import tarfile
import shutil
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
GEOIP_DIR = BASE_DIR / 'geoip'
GEOIP_DIR.mkdir(parents=True, exist_ok=True)


def download_geolite2(license_key: str) -> bool:
    """Attempt to download GeoLite2-City using MaxMind license key."""
    import urllib.request
    import tempfile

    url = f"https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City&license_key={license_key}&suffix=tar.gz"
    print(f"Downloading GeoLite2-City from MaxMind (this may take a while)...")
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".tar.gz") as tmpf:
            urllib.request.urlretrieve(url, tmpf.name)
            tmp_path = tmpf.name

        # extract mmdb
        with tarfile.open(tmp_path, "r:gz") as tar:
            # find the mmdb file inside archive
            mmdb_member = None
            for member in tar.getmembers():
                if member.name.endswith("GeoLite2-City.mmdb"):
                    mmdb_member = member
                    break
            if not mmdb_member:
                print("Could not find GeoLite2-City.mmdb inside archive.")
                return False
            tar.extract(mmdb_member, path=GEOIP_DIR)
            extracted_path = GEOIP_DIR / mmdb_member.name
            # move to GEOIP_DIR root
            final_path = GEOIP_DIR / "GeoLite2-City.mmdb"
            shutil.move(str(extracted_path), str(final_path))
            # cleanup nested directories if any
            # remove temp file
        os.remove(tmp_path)
        print(f"GeoLite2-City.mmdb downloaded to {final_path}")
        return True
    except Exception as e:
        print(f"Error downloading GeoLite2: {e}")
        return False


def main():
    license_key = os.getenv("MAXMIND_LICENSE_KEY", "")
    if not license_key:
        print("MAXMIND_LICENSE_KEY not set. Created geoip directory at:", GEOIP_DIR)
        print("If you provide a MaxMind license key as MAXMIND_LICENSE_KEY env var, this script can download GeoLite2-City automatically.")
        return

    ok = download_geolite2(license_key)
    if not ok:
        print("Automatic download failed. Please download GeoLite2-City manually and place GeoLite2-City.mmdb inside:", GEOIP_DIR)


if __name__ == "__main__":
    main()


