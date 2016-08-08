import gzip, struct, os, sys
import data_structures

"""
The ideas, and parts of the program, are taken from Mark Summerfield's very good book:
Programming in Python 3 - A Complete Introduction to the Python Language
"""

MAGIC = b"CS\x00\x00"
FORMAT_VERSION = b"\x00"
GZIP_MAGIC = b"\x1F\x8B"

def clean(text):
    """
    cleans the text for use as a filename without whitespace or punctuation
    :param text:
    :return: a cleaned version of text for use as a filename
    """
    newText = ""
    for char in text:
        if char not in ' #%&()\<>*?/$!\'":@+`|=':
            newText += char
    return newText


def encrypt(text):

    cipher = ""
    for char in text:
        code = ord(char) << 2
        cipher += chr(code)
    return cipher

def decrypt(text):
    plain = ""
    for char in text:
        code = ord(char) >> 2
        plain += chr(code)
    return plain

def saveCollection(collection):

    def pack_string(string):
        data = string.encode("utf8")
        format = "<H{0}s".format(len(data))
        return struct.pack(format, len(data), data)

    filename = "../collections/" + clean(collection.name()) + ".col"

    fh = None
    try:
        fh = gzip.open(filename, "wb")
        fh.write(MAGIC)
        fh.write(FORMAT_VERSION)
        data = bytearray()
        data.extend(pack_string(collection.name()))
        data.extend(pack_string(collection.author()))
        for puzzle in collection.puzzles():
            data.extend(pack_string(puzzle.title()))
            data.extend(pack_string(puzzle.puzzleCode()))
            data.extend(pack_string(puzzle.citationCode()))
            data.extend(pack_string(puzzle.puzzleSolution()))
            data.extend(pack_string(puzzle.citationSolution()))
            for hint in puzzle.hints():
                data.extend(pack_string(hint))
            data.extend(pack_string("***EOH***"))       # the End of Hints marker
        data.extend(pack_string("***EOP***"))           # the End of Puzzles marker
        fh.write(data)

    except EnvironmentError as err:             #figure out how to check for file already existing
        print("{0}: export error: {1}".format(
            os.path.basename(sys.argv[0]), err))
        return False
    finally:
        if fh is not None:
            fh.close()

def readCollection(filename):

    print("Got to readCollection()")

    def unpack_string(fh, eof_is_error=True):
        uint16 = struct.Struct("<H")
        length_data = fh.read(uint16.size)
        if not length_data:
            if eof_is_error:
                raise ValueError("missing or corrupt string size")
            return None
        length = uint16.unpack(length_data)[0]
        if length == 0:
            return ""
        data = fh.read(length)
        if not data or len(data) != length:
            raise ValueError("missing or corrupt string")
        format = "<{0}s".format(length)
        return struct.unpack(format, data)[0].decode("utf8")

    fh = None
    try:
        print("before the try")
        fh = gzip.open(filename, "rb")
        print("before reading MAGIC")
        magic = fh.read(len(MAGIC))
        if magic != MAGIC:
            raise ValueError("invalid .aib file format")
        print("before reading FORMAT_VERSION")
        version = fh.read(len(FORMAT_VERSION))
        if version > FORMAT_VERSION:
            raise ValueError("unrecognized .aib file version")

        collection = data_structures.Collection()
        collection.setName(unpack_string(fh))
        collection.setAuthor(unpack_string(fh))
        # Get the set of puzzles until the End of Puzzle marker is found
        puzzles = []
        while True:
            title = unpack_string(fh)
            print(title)
            if title == "***EOP***":
                break
            puzzle = data_structures.Puzzle()
            puzzle.setTitle(title)
            puzzle.setPuzzleCode(unpack_string(fh))
            print(puzzle.puzzleCode())
            puzzle.setCitationCode(unpack_string(fh))
            puzzle.setPuzzleSolution(unpack_string(fh))
            puzzle.setCitationSolution(unpack_string(fh))
            # Get the set of hints, in any, until the End of Hints marker is found
            hints = []
            while True:
                hint = unpack_string(fh)
                if hint == "***EOH***":
                    break
                hints.append(hint)
            puzzle.setHints(hints)
            puzzles.append(puzzle)
        collection.setPuzzles(puzzles)
        return collection


    except:
        pass

    finally:
        if fh is not None:
            fh.close()


