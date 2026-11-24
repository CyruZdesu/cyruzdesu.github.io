# Note for File IO
## open the file:
```
fin = open('FileName', Mode)    
[Mode: r, w, a, defaulted as r]
```
* r: read only. If the file is not found, the programme will return a FileNoyFoundError.
* w: rewrite. Create a file if the file does not exist. Or rewrite the existed file with the same name.
* a: append. Create a file if the file does not exist. If the file has existed, continue writing the content following the existing text
* remember to close the file by **fin.close()** to avoid waste of memory
* Enclose the filename in quotation marks '' to convert it to a string.
* you need a variable to store the file in the programme process

```
with open('Filename', Mode) as ShortName:
```
* automatically close the file even if some errors exist.
* Enclose the filename in quotation marks '' to convert it to a string.

## read the file:
```
lines = fin.read([length])     
[length: defaulted as the length of the entire text]

e.g. 
OI.text: 
123
456
programme:
    with open('OI.txt') as fin:
    lines = fin.read(4)
    print(lines)
Output:
123
|-->(the placeholder is here)
```
* read the in-file and return a string to **lines**, which keep all the information in the in-file, including \n \t...
* **space, \n** are treated as 1-length characters

```
line = fin.readline()
lines = fin.readlines()
```
* read the in-file till the next '\n' character. Next time **readline()** is called, it will continue reading where it stoped before. It returns a **string**.
* **readlines()** reads all the text in one go and stores them in a **list** (named lines as shown)
* After reading to the end, reading again gives `''` — the pointer is at the end, the file is not empty! Use `fin.seek(0)` to jump back to the start, or re-open the file. (jump to the place before index 0)

```
for line in fin:
    text = line.strip().split([split-sign])
    if len(text) < 2: 
        continue
    else:
        ...
```
* This is a commonly used structure to read the in-file and avoid empty lines.
* **for ... in ...** does not mean that **fin** is a list. This loop can be applied to any iterable object.

## write the file
```
with open('Filename', 'w') as f:
    f.write('paper: 3.3 kg\n')
    f.write('plastic: 1.2 kg\n')    # won't clean the text in the same file-operation

with open('out.txt', 'a') as f:      # append instead of rewrite
    f.write('glass: 3.0 kg\n')
```
* **write()** function does not automatically wrap to the next line. Add **\n** each time you want a new line.
* **write()** function only recieves **string**, no ~~int, float~~, or you can use the formatted output to write the number as follows
```
f.write(str(3.3) + '\n') # or
kg = 3.3
f.write(f'paper: {kg:.1f} kg\n')
```

## String helpers: strip / split / splitlines / repr

| Tool | What it does |
| ---  | --- |
| `strip()`  | removes whitespace (`\n`, `\t`, spaces) from the **two ends only**, never the middle |
| `split()`  | cuts a line into a **list** of fields; `split()` splits on any whitespace, `split(',')` splits on commas |
| `splitlines()`  | `read().splitlines()` gives a list of lines **without** `\n` |
| `repr()` | returns an exact description string so invisible characters become visible; changes nothing |

* With a bare `split()`, `strip()` is optional (bare `split()` ignores leading/trailing whitespace anyway).
* With `split(',')`, `strip()` matters — otherwise the last field keeps its `\n`, e.g. `'2.5\n'`.
*  `repr()`'s returned description is a new string in which the one newline character appears as **two printable characters** (backslash + n); the original string is untouched.



---

[← Back to Home](/)
