import base64
import json

"""
TODO: 
1. Validate other files write out exactly as they're in.
   A. Compare the MD5 hashes of the original file vs the read file of the encrypted data
   B. 
2. Add read-file support
"""


class Labeler:

    __slots__ = ['file_name','security_level','compartments','file_data',]

    def __init__(self):
        self.file_name = ""
        self.security_level = ""
        self.compartments = ""
        self.file_data = ""

    def structure(self):
        """ Defines the json structure"""
        structure = {
            "version":1,
            "label": {
              "classification":  self.security_level,
              "compartments" :   self.compartments,
            },
            "file": self.file_name,
            "meta": "",
            "data": self.file_data,
        }
        return structure
    
    def labeled_file_name(self):
        if type(self.file_name) is not str:
            raise TypeError("file name must be string")
        return self.file_name + ".mclf"

    def load_file_data(self):
        with open(self.file_name, "rb") as f:
            file_data = f.read()
        return file_data
    
    def write_json(self):
        file_data = self.load_file_data()
        new_file = self.labeled_file_name()
        with open(new_file, "w") as f:
            b64_file = base64.b64encode(file_data).decode("utf-8")
            self.file_data = b64_file
            f.write(json.dumps(self.structure(),indent=2))
        return 1

    def read_file(self):
        with open(self.labeled_file_name(), "r") as f:
            file_data = json.loads(f.read())
        encoded = file_data['data']
        decoded = base64.b64decode(encoded)
        return decoded
    
    # below this line should be moved into a test file
    def test_write(self, decoded):
        test_file_name = "test_" + self.file_name
        with open(test_file_name, "wb") as test_file:
            test_file.write(decoded)
        return 1

FILE = "t.txt"

if __name__ == "__main__":
    l = Labeler()
    l.file_name = FILE
    l.security_level = "proprietary"
    l.compartments = ["HR","CEO"]
    l.write_json()
    decoded = l.read_file()
    l.test_write(decoded)