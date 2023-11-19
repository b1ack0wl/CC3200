#!/usr/bin/python3
import argparse
import os

def extract_fs(args, contents):
  is_formatted = 0
  if (contents[2] == ord("L")) and contents[3] == ord("S"):
    flash_begin = 4
    filename_table = 0x774
    filenames = 0x974
    size_1 = (contents[0]) + (contents[1] << 8)
    is_formatted = 1
  if (contents[0x1002] == ord("L")) and (contents[0x1003] == ord("S")) and ((contents[0x1000]) + (contents[0x1001] << 8) > size_1):
    flash_begin = 0x1004
    filename_table = 0x1774
    filenames = 0x1974
    is_formatted = 1
  if is_formatted == 0:
    print("[💔] Filesystem is invalid or not formatted 😞")
    return False
  offset = 0
  for i in range(0, 0x98+1):
    if contents[flash_begin + offset] == 0xff:
      offset += 4
      continue
    if contents[flash_begin + offset + 3] & 0x40 == 0:
      fail_safe = "Yes"
      block_size = contents[flash_begin + offset + 1]
      total_block_size = block_size << 1
    else:
      fail_safe = "No"
      block_size = contents[flash_begin + offset + 1]
      total_block_size = block_size
    file_index = contents[flash_begin + offset]
    start = contents[flash_begin + offset + 2] + ((contents[flash_begin + offset + 3] & 0x3f) << 8)
    filename_offset = contents[filename_table + offset] + (contents[filename_table + offset + 1] << 8)
    filename_len =  contents[filename_table + offset + 2] + (contents[filename_table + offset + 3] << 8)
    decoded_filename = contents[filenames + filename_offset: filenames + filename_offset + filename_len].decode("UTF-8")
    data_offset = start << 12
    len = block_size * 4096
    outfile = os.path.join(os.getcwd(), args.outdir, decoded_filename.replace('/','_'))
    print(f"[🔔] Filename: \"{decoded_filename}\"")
    print(f"[📖] File index: 0x{file_index:02X}")
    print(f"[📏] Len: 0x{len:08X}")
    print(f"[🏁] Start: 0x{start:08X}")
    print(f"[🟦] Block Size: 0x{block_size:08X}")
    print(f"[🦺] Fail Safe: \"{fail_safe}\"")
    print(f"[💯] Total_Block_Size: 0x{total_block_size:08X}")
    print(f"[💾] Creating File \"{outfile}\"")
    print("------------------")
    open(outfile, "wb").write(contents[data_offset:data_offset+len+1])
    offset += 4
  return True

def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument('image', type=str, help="Path to the CC3200 SPI image.")
  parser.add_argument('--outdir', type=str, help="Path to where the extracted files will be saved to.", required=True)
  return parser.parse_args()

def main():
  args = parse_args()
  try:
    contents = open(args.image, "rb").read()
  except:
    print(f"[💔] Unable to open file \"{args.image}\" 😞")
    return
  if (os.path.isdir(args.outdir) != True):
     print(f"[💔] Output Directory \"{args.outdir}\" does not exist 😞")
     return
  if (extract_fs(args, contents) == False):
    return

if __name__ == "__main__":
  print(">> 🦉 CC3200 Filesystem Extractor v0.1 🦉 << ")
  print(">> by: b1ack0wl <<\n")
  main()
  print("✨   [fin]   ✨")