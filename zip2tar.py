#!/usr/bin/env python3

# Copyright (c) 2019 SUSE LLC.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import argparse
import os
import stat
import sys
import tarfile
import time
import zipfile


def zip2tar(zip_file: str, tar_file: str, subdir=None):
    zf = zipfile.ZipFile(zip_file)
    tf = tarfile.open(tar_file, "w:gz")
    files_count = len(zf.infolist())
    last_percent_reported = 0

    for i, zip_info in enumerate(zf.infolist()):
        filename = zip_info.filename
        if subdir:
            filename = os.path.join(subdir, filename)
        filemode = zip_info.external_attr >> 16

        tar_info = tarfile.TarInfo(name=filename)
        tar_info.mode = filemode
        tar_info.size = zip_info.file_size
        tf.addfile(
            tarinfo=tar_info,
            fileobj=zf.open(zip_info.filename)
        )

        percent = int(i * 100 / files_count)
        progress = int(i * 50 / files_count)

        if last_percent_reported == percent:
            continue

        sys.stdout.write("\r[%s%s] %d%%" %
                         ('=' * progress, ' ' * (50-progress), percent))
        sys.stdout.flush()

    print()
    tf.close()
    zf.close()
            

def main():
    parser = argparse.ArgumentParser("Convert zip to tar archives")
    parser.add_argument("zip_file", type=str,
                        help="file name of the zip archive")
    parser.add_argument("--output-file", dest="tar_file", type=str,
                        help="output file name for the tar archive")
    parser.add_argument("--subdir", dest="subdir", type=str,
                        help="subdirectory to create inside the tar archive")
    args = parser.parse_args()

    tar_file = args.tar_file
    if tar_file is None:
        tar_file = os.path.splitext(args.zip_file)[0] + ".tar.gz"

    zip2tar(args.zip_file, tar_file, subdir=args.subdir)


if __name__ == "__main__":
    main()
