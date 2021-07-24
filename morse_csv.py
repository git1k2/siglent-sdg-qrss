import math

""""
Timing source: https://morsecode.world/international/timing.html
The timing in Morse code is based around the length of one "dit" (or "dot" if you like).
From the dit length we can derive the length of a "dah" (or "dash") and the various pauses:
  * Dit: 1 unit
  * Dah: 3 units
  * Intra-character space (the gap between dits and dahs within a character): 1 unit
  * Inter-character space (the gap between the characters of a word): 3 units
  * Word space (the gap between two words): 7 units
"""

# Points in waveform
points = 16384

# Trigger voltage
low=0.000000
high=5.000000

# Morse timing
dit = 1
dah = 3
# intra-character between character elements
ic = 1
# intra-character between characters of a word
iw = 3
# word space
ws = 7

# Morse characters.
# Source: https://www.itu.int/dms_pubrec/itu-r/rec/m/R-REC-M.1677-1-200910-I!!PDF-E.pdf
morse = {
    "a": [dit, dah],
    "b": [dah, dit, dit, dit],
    "c": [dah, dit, dah, dit],
    "d": [dah, dit, dit],
    "e": [dit],
    "f": [dit, dit, dah, dit],
    "g": [dah, dah, dit],
    "h": [dit, dit, dit, dit],
    "i": [dit, dit],
    "j": [dit, dah, dah, dah],
    "k": [dah, dit, dah],
    "l": [dit, dah, dit, dit],
    "m": [dah, dah],
    "n": [dah, dit],
    "o": [dah, dah, dah],
    "p": [dit, dah, dah, dit],
    "q": [dah, dah, dit, dah],
    "r": [dit, dah, dit],
    "s": [dit, dit, dit],
    "t": [dah],
    "u": [dit, dit, dah],
    "v": [dit, dit, dit, dah],
    "w": [dit, dah, dah],
    "x": [dah, dit, dit, dah],
    "y": [dah, dit, dah, dah],
    "z": [dah, dah, dit, dit],
    "1": [dit, dah, dah, dah, dah],
    "2": [dit, dit, dah, dah, dah],
    "3": [dit, dit, dit, dah, dah],
    "4": [dit, dit, dit, dit, dah],
    "5": [dit, dit, dit, dit, dit],
    "6": [dah, dit, dit, dit, dit],
    "7": [dah, dah, dit, dit, dit],
    "8": [dah, dah, dah, dit, dit],
    "9": [dah, dah, dah, dah, dit],
    "0": [dah, dah, dah, dah, dah],
    " ": [ws],
}


def intersperse(seq, value):
    res = [value] * (2 * len(seq) - 1)
    res[::2] = seq
    return res


def gen_csv(text=None):
    count = 0
    concat_lists = []

    for character in text:
        # Add space between elements of a character
        interspersed = intersperse(morse[character], ic)
        concat_lists.append(interspersed)

    # Add space between characters of a word
    concat_lists2 = []
    for idx, i in enumerate(concat_lists):
        concat_lists2.append(i)

        # check if this element is a word space, don't append iw
        if len(i) == 1 and i[0] == 7:
            pass
        else:
            # check if next element is a wordspace
            next = idx + 1
            if next in concat_lists:
                if len(concat_lists[next]) == 1 and concat_lists[next] == 7:
                    pass
            else:
                concat_lists2.append(iw)

    all_elements = []
    for element in concat_lists2:
        if isinstance(element, int):
            all_elements.append(element)
        elif isinstance(element,list):
            for i in element:
                all_elements.append(i)
    for i in all_elements:
        count += i

    unit = math.floor(points / count)

    volt = high
    count = 1
    output = []
    for element in all_elements:
        # reset volt to low on word space:
        if element == ws:
            volt = low
        for point in range(unit * element):
            output.append(f"{count},{volt}")
            count += 1

        if volt == high:
            volt = low
        else:
            volt = high
    return output


def main():
    # Add text below, for example your callsign
    text = " call ".lower()
    output = gen_csv(text=text)

    header = f"""data length,{points}
frequency,1000.000000
amp,{high}
offset,{high / 2}
phase,0.000000







xpos,value
"""

    with open('output.csv', 'w') as file:
        file.write(header)
        for item in output:
            file.write(item + '\n')


if __name__ == "__main__":
    main()
