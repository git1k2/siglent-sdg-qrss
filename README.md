# siglent-qrss
Proof of concept for transmitting QRSS FSKCW with a Siglent Function / 
Arbitrary Waveform Generator. Tested with Siglent SDG-1032X instructions.

My 0 dBm signal into an endfed sloper antenna was received from a few 
hundred kilometers to 3000 km away!

## Usage

First, generate the arbitrary gate waveform. 
- Edit, and run `morse_csv.py`. This will output `output.csv`. 
- Rename this file to something useful, for example `callsign.csv`.
- For example callsign.csv becomes waveform 'callsign' in the SDG.

Load callsign.csv into EasyWaveX and upload it to the generator:

![Alt text](/screenshots/easywavex-call.png?raw=true "trigger waveform")

- Connect an HF antenna to channel 1.
- Connect channel 2 to to aux input on the back of the instrument.
- Connect a 10 MHz reference.
- Edit the 'wave' variable in `sdg.sh`
- Configure the frequency.
- Install lxi-tools (Ubuntu): snap install lxi-tools
- Find your device, update 'address' variable below: lxi discover
- Find wave name:   lxi scpi -a <IP address> "STL? USER"
- Run `sdg.sh`