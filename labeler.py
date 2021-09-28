import base64
import json
import hashlib

"""
TODO: 
1. Validate other files write out exactly as they're in.
   A. Compare the MD5 hashes of the original file vs the read file of the encrypted data
   B. 
2. Add read-file support
"""


class Labeler:

    __slots__ = ['file_name','security_level','compartments','file_data','binary_file_data','md5_origin']

    def __init__(self):
        self.file_name = ""
        self.security_level = ""
        self.compartments = ""
        self.file_data = ""
        self.binary_file_data = b""
        self.md5_origin = ""

    def structure(self):
        """ Defines the json structure"""
        structure = {
            "version":1,
            "label": {
              "classification":  self.security_level,
              "compartments" :   self.compartments,
            },
            "file": self.file_name,
            "meta": {
                "original_hash": self.md5_origin,  #for de-encoding validation
                "meta_meta_hash": "Not Implemented", #for validating the headers created here
            },
            "data": self.file_data,
        }
        return structure
    
    def labeled_file_name(self):
        if type(self.file_name) is not str:
            raise TypeError("file name must be string")
        return self.file_name + ".mclf"

    def load_file_data(self):
        with open(self.file_name, "rb") as f:
            self.binary_file_data = f.read()
        self.file_data = base64.b64encode(self.binary_file_data).decode("utf-8")
        self.md5_origin = hashlib.md5(self.binary_file_data).hexdigest()
    
    # I hate this function, and the design of the class. It sets attributes, but functions don't necessarily
    # return stuff. This seems like bad design. But the point of all this to show the end result, not have good code
    def write_json(self):
        self.load_file_data()
        new_file = self.labeled_file_name()
        with open(new_file, "w") as f:
            f.write(json.dumps(self.structure(),indent=2))
        return 1

    def read_file(self):
        """
        I think this should walk over whatever structure is defined in the version. Eventually the versions might
        define different structures, and this particular function should be agnostic to the structure.
        For the moment that design consideration isn't necessary. 
        """
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