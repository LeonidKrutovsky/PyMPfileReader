from io import BytesIO
from typing import List, Tuple
import zipfile
import xml.etree.ElementTree as et
import multiprocessing as mp
import time
import csv

from part1 import ZIP_FILE_NAMES


def parse_xml(xml: str) -> Tuple[str, int, List[str]]:
    root = et.fromstring(xml)
    id = ""
    level = None
    objects = []
    for item in root:
        if item.tag == "var":
            if item.attrib["name"] == "id":
                id = item.attrib["value"]
            elif item.attrib["name"] == "level":
                level = item.attrib["value"]
        elif item.tag == "objects":
            objects = [obj.attrib["name"] for obj in item]

    return id, level, objects


def load_zip_file(zip_name: str) -> zipfile.ZipFile:
    zip_file = None
    with open(zip_name, "rb") as fp:
        buf = BytesIO(fp.read())
    zip_file = zipfile.ZipFile(buf)

    return [parse_xml(zip_file.read(name)) for name in zip_file.namelist()]


if __name__ == "__main__":
    pool = mp.Pool()

    start = time.time()

    results = pool.map(load_zip_file, ZIP_FILE_NAMES)

    with open("out1.csv", "w", newline="") as csvfile1, open(
        "out2.csv", "w", newline=""
    ) as csvfile2:
        csv_writer1 = csv.writer(csvfile1, delimiter=" ")
        csv_writer2 = csv.writer(csvfile2, delimiter=" ")
        for result in results:
            for value in result:
                id = value[0]
                level = value[1]
                objects = value[2]
                csv_writer1.writerow([id, level])
                for obj in objects:
                    csv_writer2.writerow([id, obj])

    print(f"Elapsed = {time.time() - start}")
