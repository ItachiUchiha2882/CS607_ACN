import argparse 
import sys
import random
import copy
import statistics
import math

# Create a command-line argument parser
parser = argparse.ArgumentParser() 
parser.add_argument("-N", help = "number of input and output ports")  # N = 8 # Number of ports
parser.add_argument("-B", help = "size of buffer")  # B = 4 
parser.add_argument("-p", help = "probability")  # p = 0.5
parser.add_argument("-queue", help = "INQ | KOUQ | ISLIP")  # queue = INQ
parser.add_argument("-K", help = "max K packets queued per output port")  # K = 1
parser.add_argument("-out", help = "output file")  # outputfile = "output.txt"
parser.add_argument("-T", help = "max simulation time")    # T = 10000

# Parse the command-line arguments
args = parser.parse_args() 

# Check if the correct number of arguments are provided
if(len(sys.argv) != 15):
    print("Usage: python3 200010004.py -N <switchportcount> -B <buffersize> -p <packetgenprob> -queue <INQ | KONQ | ISLIP> -K <knockout> -out <outputfile> -T <maxtimeslots>")
    exit()

# Extract values from command-line arguments
N = int(args.N) 
B = int(args.B) 
p = float(args.p) 
queue = str(args.queue) 
K = float(args.K) 
knockout = int(K*N)
outputfile = str(args.out) 
T = int(args.T) 

# Packet class to store the packet information
class Packet:  # 
    def __init__(self, frm, to, timestamp):
        self.frm = frm 
        self.to = to
        self.timestamp = timestamp
        self.delay = 0
    def display(self): 
        return (self.frm, self.timestamp, self.to)

# Alogithm selection based on the queue type

# Input Queue (INQ) Algorithm
if queue == 'INQ':
    print("*** INQ Algorithm ***")
    InputPort = [[] for i in range(N)]  
    OutputPort = [None for i in range(N)]  
    packets = []  
    generated_count = 0 
    transfer_count = 0  
    total_delay = 0  
    
    for _ in range(T):
        # Generate the Packet for Ports
        for i in range(N):
            r = int(random.random() * N)
            for h in range(r):
                x = random.random()
                if x < p and len(InputPort[i]) < B:
                    packet = Packet(i, int(random.random() * N), _ + (random.random()/10))
                    InputPort[i].append(packet)
                    generated_count += 1
                break

        # Calculate how many Input ports want to send packet to ouput port
        packetToOutputport = [[] for i in range(N)]
        for i in range(N):
            for j in range(len(InputPort[i])):
                packetToOutputport[InputPort[i][j].to].append(InputPort[i][j])
        
        # Packet Scheduling
        for i in range(N):
            size = len(packetToOutputport[i])
            if size > 0:
                if size == 1:
                    packet = copy.deepcopy(packetToOutputport[i][0])
                    packet.delay = int(_) - int(packet.timestamp)
                    OutputPort[i] = packet
                    InputPort[packet.frm].remove(packetToOutputport[i][0])
                    del packetToOutputport[i][0]
                else:
                    index = int(len(packetToOutputport[i]) * random.random())
                    packet = copy.deepcopy(packetToOutputport[i][index])
                    packet.delay = int(_) - int(packet.timestamp)
                    OutputPort[i] = (packet)
                    InputPort[packet.frm].remove(packetToOutputport[i][index])
                    del packetToOutputport[i][index]

        # Transfer the packets
        for i in range(N):
            if OutputPort[i] is not None:
                transfer_count += 1
                packets.append(OutputPort[i].delay)
                total_delay += OutputPort[i].delay
            OutputPort[i] = None

    # Write results to an output file
    file1 = open(outputfile, "a")
    # file1.write('N\tP\tQtype\tAvg PD\t\t\tStd. Dev of PD\t\tAvg LU'+ '\n')
    file1.write(str(N) + '\t' + str(p) + '\t' + queue + '\t' + str(total_delay/transfer_count) + '\t\t\t' + str((total_delay/transfer_count)/math.sqrt(N)) + '\t\t' + str(transfer_count/(N*T))+ '\n')
    file1.close()

    # Print the results
    print('N\tP\tQtype\tAvg PD\t\t\tStd. Dev of PD\t\tAvg.LU')
    print(str(N) + '\t' + str(p) + '\t' + queue + '\t' + str(total_delay/transfer_count) + '\t' + str((total_delay/transfer_count)/math.sqrt(N)) + '\t' + str(transfer_count/(N*T)))

# K Output Queue (KOUQ) Algorithm
if queue == 'KOUQ':
    print("*** KOUQ Algorithm ***")
    packets = []
    generated_count = 0
    transfer_count = 0
    dropped_count = 0
    total_delay = 0
    OutputPort = [[] for i in range(N)]

    for _ in range(T):
        packetsToSend = [[] for i in range(N)]
        # Generate the Packet for Ports
        for i in range(N):
            x = random.random()
            r = int(random.random() * N)
            for h in range(r):
                if x < p:
                    packet = Packet(i, int(random.random() * N), _ + (random.random()/10))
                    if len(packetsToSend[packet.to]) < B:
                        packetsToSend[packet.to].append(packet)
                        generated_count += 1
                break
                
        # Packet Scheduling
        for i in range(N):
            if len(packetsToSend[i]) > 0:
                if len(packetsToSend[i]) == 1 and len(OutputPort[i]) < knockout:
                    packet = copy.deepcopy(packetsToSend[i][0])
                    OutputPort[i].append(packet)
                elif len(packetsToSend[i]) > 1 and len(packetsToSend[i]) <= (knockout - len(OutputPort[i])):
                    for each in packetsToSend[i]:
                        packet = copy.deepcopy(each)
                        OutputPort[i].append(packet)
                else:
                    space_left = knockout - len(OutputPort[i]) 
                    dropped_count += len(packetsToSend[i]) - space_left
                    random_space_left = [int(len(packetsToSend[i])*random.random()) for i in range(space_left)]
                    for each in random_space_left:
                        packet = copy.deepcopy(packetsToSend[i][each])
                        OutputPort[i].append(packet)
                packetsToSend[i] = []

        # Transfer
        for i in range(N):
            if len(OutputPort[i]) > 0:
                delay = int(_) - int(OutputPort[i][-1].timestamp)
                total_delay += delay
                transfer_count += 1
                packets.append(delay)
                OutputPort[i].remove(OutputPort[i][-1])

    link_uti = transfer_count/(N*T)
    # Write results to an output file
    file1 = open(outputfile, "a")
    # file1.write('N\tP\tQtype\tAvg PD\t\t\tStd. Dev of PD\t\tAvg LU'+ '\n')
    file1.write(str(N) + '\t' + str(p) + '\t' + queue + '\t' + str(total_delay/transfer_count) + '\t\t\t' + str((total_delay/transfer_count)/math.sqrt(N)) + '\t\t' + str(link_uti)+ '\n')
    file1.close()

    # Print the results
    print('N\tP\tQtype\tAvg PD\t\t\tStd. Dev of PD\t\tAvg LU')
    print(str(N) + '\t' + str(p) + '\t' + queue + '\t' + str(total_delay/transfer_count) + '\t' + str((total_delay/transfer_count)/math.sqrt(N)) + '\t' + str(link_uti))

# ISLIP Algorithm
if queue == 'ISLIP':
    print("*** ISLIP Algorithm ***")
    generated_count = 0
    InputPort = [[] for i in range(N)]
    OutputPort = [None for i in range(N)]
    request = [ [ 0 for i in range(N) ] for j in range(N) ]
    lastUsedPort= [ -1 for i in range(N) ]
    delaylist = []

    def grant(out_port, portUsed):
        for i in range(lastUsedPort[out_port] + 1, N):
            if(request[i][out_port] == 1 and portUsed[i] == 0):
                portUsed[i] = 1
                return i

        for i in range(0, lastUsedPort[out_port] + 1):
            if(request[i][out_port] == 1 and portUsed[i] == 0):
                portUsed[i] = 1
                return i
        
        return -1

    def schedule_packets(InputPort,t, portUsed, delay, generated_count):
        global delaylist
        
        # Grant Phase, input ports get mapped to required output ports in a round-robin fashion where last used port have lowest priority
        for out_port in range(N):
            lastUsedPort[out_port] = grant(out_port, portUsed)

        # Accept phase
        for out_port in range(N):
            in_port = lastUsedPort[out_port]
            if in_port != -1:
                # Remove request
                request[in_port][out_port] = 0
                generated_count = generated_count - 1
                delaylist.append(delay)
        return generated_count

    sum_delay = 0
    for t in range(T):
        # Generate the Packet for Ports
        generated = 0
        InputPort = [[] for i in range(N)]
        for inPort in range(N):
            x = random.random()
            r = int(random.random() * N)
            for h in range(r):
                if x < p and len(InputPort[inPort]) < B:
                    outPort = int(random.random() * N)
                    packet = Packet(inPort, outPort , t )
                    InputPort[inPort].append(packet)
                    generated += 1
                    request[inPort][outPort] = 1
                break
        generated_count += generated
        # Scheduling of the traffic
        portUsed = [ 0 for i in range(N) ]
        delay = 0
        while generated > 0:
            generated = schedule_packets(InputPort,t, portUsed, delay, generated)
            delay = delay + 1
        sum_delay += delay

    # Write results to an output file
    file1 = open(outputfile, "a")
    # file1.write('N\tP\tQtype\tAvg PD\t\t\tStd. Dev of PD\t\tAvg LU\n')
    file1.write(str(N) + '\t' + str(p) + '\t' + queue + '\t' + str(sum(delaylist)/len(delaylist)) + '\t\t\t' + str((sum(delaylist)/len(delaylist))/math.sqrt(N)) + '\t\t' + str(generated_count/(N*sum_delay)) + '\n')
    file1.close()

    # Print the results
    print('N\tP\tQtype\tAvg PD\t\t\tStd. Dev of PD\t\tAvg LU')
    print(str(N) + '\t' + str(p) + '\t' + queue + '\t' + str(sum(delaylist)/len(delaylist)) + '\t' + str((sum(delaylist)/len(delaylist))/math.sqrt(N)) + '\t' + str(generated_count/(N*T)))
    