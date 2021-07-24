#!/bin/bash

# SDG IP address
address="192.0.2.1"

# Frequency in Herz.
# You need a amateur radio license to transmit into an antenna!
freq="7039900"
#freq="14096900"
#freq="28125700"

# FSK shift in Hz
shift="4"

# Amplitude in Vpp, see: http://wera.cen.uni-hamburg.de/DBM.shtml
ampl=0.632 # 0 dBm

# Gate waveform name
wave="call"

# Duration of 1 transmission (keep it < 10 min)
period="360"

trap ctrl_c INT
stty -echoctl # hide ^C

send() {
	lxi scpi -a "${address}"  "$1"
}

ctrl_c() {
	echo "Ctrl-C pressed, switching off outputs."
	send "C1:OUTP OFF"
	send "C2:OUTP OFF"
	echo "Goodbye."
	exit
}

# Print identification
send "*IDN?"

# Turn off output channel 1 and 2
send "C1:OUTP OFF"
send "C2:OUTP OFF"
    
# Enable external 10 MHz clock input
send "ROSC EXT"

# Configure output load channel 1 and 2
send "C1:OUTP LOAD,50"
send "C2:OUTP LOAD,50"

# Enable screen saver
send "SCSV 1"

configure_fsk() {
    # Disable wave combine
    send "C1:CMBN OFF"
    send "C2:CMBN OFF"
 
    # Configure wave channel 1
    send "C1:BSWV WVTP,SINE,FRQ,${freq},AMP,${ampl},OFST,0,PHSE,0"
    
    # Load Arb wave channel 2
    send "C2:ARWV NAME,${wave}"
    send "c2:BSWV PERI,${period},AMP,5,OFST,2.5,PHSE,0"
    
    # Modulation channel 1
    send "C1:MDWV FSK"
    send "C1:MDWV STATE,ON"
    send "C1:MDWV FSK,SRC,EXT"
    send "C1:MDWV FSK,HFRQ,$(( freq + shift ))"

    }

wait_for_minute() {
	if [ "$1" = "0" ]; then
		next="$(date --date='10 min' +%H:%M:%S| cut -b 1-4)$1:$2"
	else
		next="$(date +%H:%M:%S| cut -b 1-4)$1:$2"
	fi
	echo "Next TX at:   $next"
	current_epoch=$(date +%s.%N)
	target_epoch=$(date -d "$next" +%s.%N)
	sleep_seconds=$(echo "$target_epoch - $current_epoch"|bc)
	sleep "$sleep_seconds"
}

# Loop
while true
do
	configure_fsk
	echo "======================================"
        echo "Next TX freq: ${freq} Hz, ampl: ${ampl} Vpp"
	# Start at every 10th minute
	wait_for_minute 0 00

	echo "$(date) - TX ON"
	# Turn on sig gen.
	send "C1:MDWV STATE,ON"
	send "C2:OUTP ON"
	send "C1:OUTP ON"
	sleep "${period}"	# After this period the whole message is sent.

	# Turn off sig gen.
	send "C1:OUTP OFF"
	send "C2:OUTP OFF"
	send "C1:MDWV STATE,OFF"
	echo "$(date) - TX OFF"

done

