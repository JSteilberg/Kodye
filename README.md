# HHacks2017

![kanye-logo](https://user-images.githubusercontent.com/26828467/31050514-0586d2fc-a61a-11e7-9ea7-34bccde69576.png)

## What is Kodye?

Hands-free coding! Have you ever wanted to code while driving? For the first time ever, now you can, with Kodye. Using Kodye, you can hum or whistle at your computer, and your tones will be translated into instructions for the computer to follow.

Kodye maps eight different tones to the eight different instructions of [Brainfuck](https://en.wikipedia.org/wiki/Brainfuck). Kodye's syntax is as follows:

* C4: Increment the byte at the data pointer.
* C#4: Decrement the byte at the data pointer.
* D4: Decrement the data pointer (to point to the next cell to the left).
* E4: Increment the data pointer (to point to the next cell to the right).
* F4: If the byte at the data pointer is zero, then instead of moving the instruction pointer forward to the next command, jump it forward to the command after the matching G4 command.
* G4: If the byte at the data pointer is nonzero, then instead of moving the instruction pointer forward to the next command, jump it back to the command after the matching F4 command.
* A4: Output the byte at the data pointer.
* B4: Accept one byte of input, storing its value in the byte at the data pointer.

Kodye is implemented in Python. Usage is `python kodye.py [name of output file]` on pc. Usage on mac is `python kodye-mac.py [name of output file]` . Both versions will stop recording on keypress.
