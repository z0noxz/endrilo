#!/usr/bin/env python3
import array, base64, getopt, gzip, hashlib, random, sys, traceback, os

help_notes = """
  Endrilo 0.2
  -----------------------------
  Created by: z0noxz
  https://github.com/z0noxz/endrilo

  Description:
  This script encodes and decodes text, files or piping, by counting bits in succession.
  More features included password encryption and compression.

  Usage: (python) endrilo.py [options]

  Options:
    --help                Show this help message and exit

    Mandatory:
      Pick one of the options below

      --encode=TEXT         Specify the text to be encoded
      --encode-file=PATH    Encode a file instead of a string
      --encode-pipe         Reads the pipe for data to encode
      --decode=TEXT         Specify the text to be decoded
      --decode-file=PATH    Decode a file instead of a string
      --decode-pipe         Reads the pipe for data to decode
  
    Optional:
      --password=PASSWD     Specify a password for encryption
      --gzip                zip or unzip data
"""
bin_oct = [ [False, False, False], [True, False, False], [False, True, False], [True, True, False], [False, False, True], [True, False, True], [False, True, True], [True, True, True] ]

class Print(object):
	
	@staticmethod
	def text(text = "", continuous = False):
		if continuous:			
			sys.stdout.write("  " + text)
			sys.stdout.flush()
		else:
			print("  " + text)
		return len(text)
		
	@staticmethod
	def info(text = "", continuous = False): return Print.text("\033[94m[i]\033[0m " + text, continuous)
		
	@staticmethod
	def warning(text = "", continuous = False): return Print.text("\033[96m[!]\033[0m " + text, continuous)
		
	@staticmethod
	def status(text = "", continuous = False): return Print.text("\033[94m[*]\033[0m " + text, continuous)
		
	@staticmethod
	def error(text = "", continuous = False): return Print.text("\033[91m[-]\033[0m " + text, continuous)
		
	@staticmethod
	def success(text = "", continuous = False): return Print.text("\033[92m[+]\033[0m " + text, continuous)
		
	@staticmethod
	def color(text = "", color = 91, continuous = False): return Print.text("\033[" + str(color) + "m" + text + "\033[0m", continuous)


def boolarray(data):
	holder = []
	
	for x in data:
		for i in range(8):
			holder.append(True if ((x >> i) & 1) else False)
	return holder

def passxor(data, passwd):
	_passwd = bytearray()
	_passwd.extend(hashlib.sha512(passwd.encode("utf-8")).digest())
	
	random.seed(str(_passwd))

	if len(_passwd) > len(data):
		for i in range(len(_passwd)):
			data[(i % len(data))] = data[(i % len(data))] ^ random.getrandbits(8)
	else:
		for i in range(len(data)):
			data[i] = data[i] ^ random.getrandbits(8)

	return data

def encode(data, passwd = ""):
	global bin_oct

	data = bytearray(data)
	holder = bytearray()
	bits = []
	count = 0

	for i in range(0, (8 * len(data))):		
		if (((data[int(i / 8)] & (1 << (i % 8))) != 0) != ((len(bits) / 3) % 2 != 0)):			
			while count > 7:
				bits.extend(bin_oct[7])
				bits.extend(bin_oct[0])
				count -= 7				
			bits.extend(bin_oct[count])
			count = 0
		
		if (i + 1 == (8 * len(data))):
			bits.extend(bin_oct[count + 1])
			bits.extend([False for x in range(0, (8 - len(bits) % 8))])
		
		count += 1

	for i in range(0, len(bits), 8):
		holder.extend([ord(chr(sum(v<<x for x, v in enumerate(bits[i:][:8]))))])

	return (passxor(holder, passwd) if len(passwd) > 0 else holder)

def decode(data, passwd = ""):
	global bin_oct

	data = bytearray(data)
	holder = bytearray()
	bits = []
	array = boolarray(passxor(data, passwd) if len(passwd) > 0 else data)
	array.extend([False for x in range(0, (3 - len(array) % 3))])

	for i in range(0, int(len(array) / 3)):
		bits.extend([(True if i % 2 != 0 else False) for x in range(0, bin_oct.index(array[(i * 3):][:3]))])

	for i in range(0, len(bits), 8):
		holder.extend([ord(chr(sum(v<<x for x, v in enumerate(bits[i:][:8]))))])

	return holder

def main(argv):
	global help_notes
	
	_ag = {
		"password" 	: "",
		"gzip"		: False
	}
	_ag_c = 0	

	try:
		opts, args = getopt.getopt(argv, "",
		[
			"help",
				
			# Mandatory
			"encode=",
			"encode-file=",
			"encode-pipe",
			"decode=",
			"decode-file=",
			"decode-pipe",
			
			# Optional
			"password=",
			"gzip",
		])
	except getopt.GetoptError as e:
		Print.error(str(e))
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("--help"):
			print(help_notes)
			sys.exit()
		elif opt in ("--encode"): 
			_ag["encode"] = arg
			_ag_c += 1
		elif opt in ("--encode-file"): 
			_ag["encode-file"] = arg
			_ag_c += 1
		elif opt in ("--encode-pipe"):
			if not os.isatty(sys.stdin.fileno()):
				_ag["encode"] = sys.stdin.read()
				_ag_c += 1
		elif opt in ("--decode"): 
			_ag["decode"] = arg
			_ag_c += 1
		elif opt in ("--decode-file"): 
			_ag["decode-file"] = arg
			_ag_c += 1
		elif opt in ("--decode-pipe"):
			if not os.isatty(sys.stdin.fileno()):
				_ag["decode"] = sys.stdin.read()
				_ag_c += 1
		elif opt in ("--password"): 
			_ag["password"] = arg
		elif opt in ("--gzip"): 
			_ag["gzip"] = True
	
	if (_ag_c > 1):
		Print.error("Only one command is allowed")
		sys.exit(2)

	elif (_ag_c == 0):
		Print.error("No command was given")
		sys.exit(2)		
	
	try:
		data = bytearray()
			
		if ("encode" in _ag) or ("encode-file" in _ag):
			
			# Read input data
			if ("encode-file" in _ag): data.extend(open(_ag["encode-file"]).read().encode("utf-8"))
			else: data.extend(_ag["encode"].encode("utf-8"))
			
			# Encode data
			data = encode(data, _ag["password"])
			
			# Zip data
			if (_ag["gzip"]):
				data = gzip.compress(data)
			
			# Base64 encode
			data = base64.b64encode(data)

		elif ("decode" in _ag) or ("decode-file" in _ag):
			
			# Read input data
			if ("decode-file" in _ag): data.extend(open(_ag["decode-file"]).read().encode("utf-8"))
			else: data.extend(_ag["decode"].encode("utf-8"))
			
			# Base64 decode
			data = base64.b64decode(data)
			
			# Unzip data
			if (_ag["gzip"]):
				data = gzip.decompress(data)
			
			# Decode data
			data = decode(data, _ag["password"])
		
		# Print output
		print(data.decode("utf-8"))

	except Exception as e:
		Print.error("Rethink what you just did...")
		for line in str(traceback.format_exc()).split("\n"):
			Print.color(line)

if __name__ == "__main__": main(sys.argv[1:])