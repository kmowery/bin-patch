import itertools

def readall(f):
  f.seek(0,0)
  buf = "enter the while loop"
  contents = []
  while(len(buf) > 0):
    buf = f.read()
    contents += buf
  return contents

class FileWrapper:
  def __init__(self, filename, mode, blocksize=None):
    self.filename = filename
    self.f = open(filename, mode)
    self.blocksize = blocksize
    self.filedata = None

    if blocksize is None:
      # Reads the whole file and closes the file
      n = self.data()

  def __len__(self):
    if self.filedata is not None:
      return len(self.filedata)
    else:
      loc = self.f.tell()
      # find end of file
      self.f.seek(0,2)
      # get size of file
      size = self.f.tell()
      # go back to where we were
      self.f.seek(loc,0)
      return size

  def tell(self):
    if self.f is not None:
      return self.f.tell()
    else:
      return -1

  def seek(self, n, pos=0):
    if self.f is not None:
      self.f.seek(n, pos)

  # return all of the file's data
  def data(self):
    if self.filedata is None:
      self.filedata = readall(self.f)
      self.f.close()
      self.f = None
    return self.filedata

  def read(self, n):
    buf = self.f.read(n)
    return buf


class HexByteWrapper(FileWrapper):
  def __init__(self, hexcontent):
    self.hexcontent = hexcontent
    if len(self.hexcontent)%2 != 0:
      raise Exception("HexByteWrapper must have an integer number of bytes")
    self.bytes = [chr(int(a+b, 16)) for a,b in
        itertools.izip(itertools.islice(hexcontent, 0, None, 2),
                       itertools.islice(hexcontent, 1, None, 2))]
    self.readloc = 0

  def __len__(self):
    return len(self.hexcontent)/2

  def data(self):
    return "".join(self.bytes)

  def read(self, n):
    buf = self.bytes[self.readloc:self.readloc+n]
    self.readloc = min(len(self.bytes), self.readloc+n)
    return buf

  def tell(self):
    return self.readloc

  def seek(self, n, pos):
    if pos == 0:
      self.readloc = n
    if pos == 1:
      self.readloc += n
    if pos == 2:
      self.readloc = len(self.bytes) - n

if __name__ == "__main__":
  fw = FileWrapper("file_wrapper.py", 'r')
  print len(fw)

  hbw = HexByteWrapper("414141")
  print hbw.read(2)

