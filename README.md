Endrilo: This script encodes and decodes text, files or piping, by counting bits in succession.
===============================================================================================

Contact
-------
* Author: z0noxz
* Source: https://github.com/z0noxz/endrilo
* Email: z0noxz@mail.com

Description
-----------
This script encodes and decodes text, files or piping, by counting bits in succession. More features include password encryption and compression.

By itself counting bits in succession isn't a particularly safe way of ciphering data, so besides that the data will also get XORed with a password based seed randomizer. 

How to use
----------

Install it:

	git clone https://github.com/z0noxz/endrilo
	cd endrilo
	sudo ./setup.py install

Encode your message in any of the following ways:

	endrilo --encode "my secret message"
	echo -n "my secret message" | endrilo --encode-pipe
	endrilo --encode-file my-secret-file
	cat my-secret-file | endrilo --encode-pipe

Decode your message in any of the following ways:

	endrilo --decode "SBQloiNpSSJFk6IlibRkjhJFSSJFWqQlVCYliRQ="
	echo -n "SBQloiNpSSJFk6IlibRkjhJFSSJFWqQlVCYliRQ=" | endrilo --decode-pipe
	endrilo --decode-file my-encoded-file
	cat my-encoded-file | endrilo --decode-pipe

A password can be specified to enhance security:

	endrilo --encode "my secret message" --password "lamepassword"
	endrilo --decode "MDiXIdE17GRFxehlGVd0A4BIOvk5BqwLOJA1rig=" --password "lamepassword"

Compression can be used for smaller storage:

	endrilo --encode "my secret message" --password "lamepassword" --gzip
	endrilo --decode "H4sIABxvglgC/zOwmK540fRNiuvRF6mS4SXMDR5WPy3Z1nBbTDBdpwEACDQlwB0AAAA=" --password "lamepassword" --gzip