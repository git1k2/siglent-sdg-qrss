# siglent-qrss
Proof of concept for transmitting QRSS FSKCW with a Siglent Function / 
Arbitrary Waveform Generator.

## Usage

First, generate the arbitrary gate waveform. 
- Edit, and run `morse_csv.py`. This will output `output.csv`. 
- Rename this file to something useful, for example `callsign.csv`.

Load the CSV into EasyWaveX.
![Alt text](/screenshots/easywavex-call.png?raw=true "trigger waveform")