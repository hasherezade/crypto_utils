quick_aes
--
This tiny tool is meant to provide fast AES encryption of strings and files.
It can be used in cases when you don't want to send message via open text but you have no time to prepare more sophiasticated encryption methods (GPG etc).
<br/><br/>
DISCLAIMER: <br/>
This tools is provided AS IS and I am not responsible for any consequences of using it. If you notice any bug, please let me know and it will be fixed ASAP.
<br/>
This tool is intended to be minimalistic. It does not provide a secure way of sharing AES keys, only provides AES encryption. It is your reponsibility to share your key securely with the second party.
<br/>
How to use:
-
1) To encrypt a message:

<pre>
./quick_aes.py 
Password: 
Enter a message:
This is my test message that is going to be encrypted and saved in Base64!
---
CivtrN5BtxgHcFzDHx2Eqn/W48Wp4dobb75dXt9nC+2zfqIKdyzYG6uSCXyxOeV2rAoy2kjhkKCjFgBKAkI6yXgAb6VCWOY+4pgHt/+7ucH9EWY2hY7YeHNdUKvSplQn
---
</pre>
Now you can copy the Base64 text, paste it and send wherever you like.

2) To decrypt a message:<br/>
use a parameter <b>--decode</b> and paste the encrypted text in Base64
<pre>
./quick_aes.py --decode
Password: 
Enter a message:
CivtrN5BtxgHcFzDHx2Eqn/W48Wp4dobb75dXt9nC+2zfqIKdyzYG6uSCXyxOeV2rAoy2kjhkKCjFgBKAkI6yXgAb6VCWOY+4pgHt/+7ucH9EWY2hY7YeHNdUKvSplQn
---
This is my test message that is going to be encrypted and saved in Base64!
---
</pre>
3) To encrypt a file<br/>
Use a parameter <b>--infile</b> [filename]
<pre>
./quick_aes.py --infile file2png.py 
Password: 
[OK] Output: enc_file2png.txt
</pre>
4) To decrypt a file:<br/>
Use a parameters <b>--infile</b> [filename] <b>--decode</b> <b>--oext</b> [output_extension]
<pre>
./quick_aes.py --infile enc_file2png.txt --decode --oext py
Password: 
[OK] Output: dec_enc_file2png.py
</pre>

