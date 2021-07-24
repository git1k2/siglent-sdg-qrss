# siglent-qrss
Proof of concept for transmitting QRSS FSKCW with a Siglent Function / 
Arbitrary Waveform Generator. Tested with Siglent SDG-1032X.

My HF 0 dBm (1 mW) signal into an endfed sloper antenna was received from a few 
hundred kilometers to 3000 km away! Note: You'll need an amateur radio license!

- [QRSS info](https://swharden.com/blog/2020-10-03-new-age-of-qrss/)
- [QRSS Plus, grabbers](https://swharden.com/qrss/plus/)

## Usage
###Generate the arbitrary gate waveform 
- Edit, and run `morse_csv.py`. This will output `output.csv`. 
- Rename this file to something useful, for example `callsign.csv`.
- For example callsign.csv becomes waveform 'callsign' in the SDG.
- Load `callsign.csv` into EasyWaveX and upload it to the generator:

![Alt text](/screenshots/easywavex-call.png?raw=true "trigger waveform")

###Connect the instrument
- Connect an HF antenna to channel 1.
- Connect channel 2 to aux input on the back of the instrument.
- Connect a 10 MHz reference.

###Run the sdg.sh script
- Install lxi-tools (Ubuntu): `snap install lxi-tools`
- Find your device: `lxi discover`
- Get waveform name: `lxi scpi -a <IP address> "STL? USER"`
- Edit the variables in `sdg.sh`
  - `address`: SDG IP address
  - `freq`: frequency in Herz.
  - `ampl`: amplitude in Vpp.
  - `wave`: waveform name.

- Run `sdg.sh`