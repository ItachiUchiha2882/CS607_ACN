## Directory Structure

- 200010004.py : Main program file
- output.txt : Output file
- report.pdf : Report of the program
- script.sh : Script to run the program with default values
- readme.md : Readme file

## Instructions to run the program

- First navigate to the directory where the program is present.
- Then run the following command to compile the program
 
```
python3 200010004.py -N <switchportcount> -B <buffersize> -p <packetgenprob> -queue <INQ | KONQ | ISLIP> -K <knockout> -out <outputfile> -T <maxtimeslots>"
```

We have to replace the values in <> with the values we want to run the program with and script to run as default values
```
./script.sh
```

## Output Format

Output will be displayed and written in file provided in command line arguement as follows

N       P       Qtype   Avg PD                  Std. Dev of PD          Avg.LU
8       0.5     INQ     0.34332897504405663     0.12138512321573969     0.439775
8       0.5     KOUQ    0.32873779756807675     0.1162263629463588      0.437925
8       0.5     ISLIP   0.19334285714285715     0.0683570226898481      0.4375

Where, 

N : Number of Input and Output Port

P : Packet Generation Probability

Qtype : INQ or KOUQ or ISLIP

AvgPD : Average packet delay

	-- AvgPktDelay = (TotalDelay * 1.0) / (PacketTransmitted * 1.0)

Std. Dev of PD : Standard Deviation of Packet Delay

	-- StdDevPacketDelay = AvgPktDelay / sqrt(PacketTransmitted * 1.0)

Avg LU : Average Link Utilization

	-- AvgLinkUtilization = (PacketTransmitted * 1.0) / ((maxtimeslots * 1.0) * (NumberofPorts * 1.0))

A detailed report is also generated in the same directory as report.pdf