from uuid import uuid4
from random import randint
import io
import zipfile


XML_FILE_COUNT = 100
ZIP_FILE_COUNT = 50

XML_FILE_NAMES = [f"{i}.xml" for i in range(XML_FILE_COUNT)]
ZIP_FILE_NAMES = [f"{i}.zip" for i in range(ZIP_FILE_COUNT)]


def get_random_xml() -> str:
    uid = str(uuid4())
    level = randint(0, 100)
    objects = []
    for i in range(randint(0, 10)):
        objects.append(f"<object name='{str(uuid4())}'/>")

    objects = "\n".join(objects)
    return f"""
<root>
    <var name='id' value='{uid}'/>
    <var name='level' value='{level}'/>
    <objects>
      {objects}
    </objects>
</root>
"""


def create_zip_file(name: str):
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a") as zip_file:
        for xml_file_name in XML_FILE_NAMES:
            zip_file.writestr(xml_file_name, get_random_xml())

    with open(name, "wb") as f:
        f.write(zip_buffer.getvalue())


if __name__ == "__main__":
    [create_zip_file(name) for name in ZIP_FILE_NAMES]
