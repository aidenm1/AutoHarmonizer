import music21 as mus
import random
import copy

lengthofsolo = int(input("How many bars would you like the melody?"))
melody = mus.stream.Stream()
key = mus.key.Key(input("What key would you like the melody in?"))
pitches = key.pitches[0 : len(key.pitches) - 1]
notelengths = [0.5, 0.5, 0.5, 1, 1, 2]
pitches.append(pitches[0])
pitches.append(pitches[1])
pitches.append(pitches[2])
pitches.append(pitches[4])
pitches.append(pitches[5])
measure1 = mus.stream.Measure()
randomnumber = -1
restornot = 0
for z in range(0, lengthofsolo - 1):
    measure = mus.stream.Measure()
    measurelength = 0
    measurenotelengths = []
    while (measurelength != 4):
        while (measurelength <=3.5):
            randomchoicelength = random.choice(notelengths)
            measurenotelengths.append(randomchoicelength)
            measurelength += randomchoicelength
        if (measurelength != 4):
            measurelength = 0
            measurenotelengths = []
    for i in measurenotelengths:
        if randomnumber != -1:
            if (str(pitches[randomnumber])) == (str(pitches[1])):
                randomnumber = 0
            elif (str(pitches[randomnumber])) == (str(pitches[3])):
                randomnumber = 2
            elif (str(pitches[randomnumber])) == (str(pitches[5])):
                randomnumber = 4
            elif (str(pitches[randomnumber])) == (str(pitches[6])):
                randomnumber = 1000
            else:
                randomnumber = random.randint(0, len(pitches) - 1)
        else:
            randomnumber = 0
        if randomnumber != 1000:
            if restornot != 7:
                measure.append(mus.note.Note(pitches[randomnumber], quarterLength=i))
            else:
                measure.append(mus.note.Rest(quarterLength=i))
        else:
            measure.append(mus.note.Note(pitches[0].transpose(12), quarterLength=i))
            randomnumber = 0
        restornot = random.randint(0, 7)
    if z == 0:
        measure1 = copy.deepcopy(measure)
    if z % 4 == 0:
        measure = copy.deepcopy(measure1)
    melody.append(measure)
measure = mus.stream.Measure()
measure.append(mus.note.Note(pitches[0], quarterLength = 4))
melody.append(measure)
melody.append(mus.meter.TimeSignature('4/4'))

melody.show()
melody.write(fmt = 'midi', fp = 'random3.mid')