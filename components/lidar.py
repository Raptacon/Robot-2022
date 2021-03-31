import logging as log
from wpilib import SerialPort

class Lidar:
    compatString = ["testBoard"]
    dist = 0

    MXPserial: SerialPort

    bufferArray = bytearray(18)

    def on_enable(self):
        self.read()

    def checkAndRead(self, packet):
        """
        Checks the lidar and reads the output
        sample packet:([0x59,0x59,0x59,0x0, 0x10, 0x45,0xB8, 0x7, 0x1F])
        The first 2 bytes are the indicators of the start of the packet.
        The last byte is the checksum.
        """
        full = False
        self.packArr = packet
        x=0 #An index
        checksumin=0
        begin=0
        for i in self.packArr[:-1]:
            if i==89 and self.packArr[x+1]==89: #Look for the two indicators
                checksumin=x+8
                begin=x
                tot = sum(self.packArr[begin:checksumin])
                tot=(0x00FF & tot)
                if checksumin<len(self.packArr) and tot==self.packArr[checksumin]:
                    self.packArr = self.packArr[begin:checksumin]
                    full = True #Say that the packet now contains a full 9 byte packet
                    break #break to avoid errors
                elif tot != self.packArr[checksumin]:
                    log.error("Checksum does not match")
                elif checksumin>=len(self.packArr):
                    log.error('The index: '+str(checksumin)+' was out of range: '+str(len(self.packArr)-1))
            x += 1

        if not full:
            log.info('Lidar failed to find a packet')

        if full:
            # Indices 2 and 3 are the locations of the distance data
            strengthLow = self.packArr[2]
            strengthHigh = self.packArr[3]
            # Add strengthLow to strengthHigh, by shifting strengthHigh to the left.
            strength = strengthLow | (strengthHigh << 8)
            return strength
        else:
            log.info('The packet is not full, so lidar cannot find distance')
            return 0

    def getDist(self):
        return self.dist

    def execute(self):
        self.read()
        self.dist = self.checkAndRead(self.bufferArray)
        if self.dist == 0:
            print("Lidar failed to read dist")

    def read(self):
        self.MXPserial.read(self.bufferArray)
