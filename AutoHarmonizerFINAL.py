import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import filedialog
import music21 as mus
import copy
import random
import time
from music21 import converter, midi, instrument, stream, note

def exitButton(self):
    window.destroy()


comboChoice = ""


def checkCombo(self):
    global comboChoice
    comboChoice = varBox.get()

keyChoice = ""
def checkKey(self):
    global keyChoice
    keyChoice = keyBox.get()

melodyCheck = False


def checkMelody():
    global melodyCheck
    melodyCheck = sysCheck.get()


selectInv = 1


def selectInversion():
    global selectInv
    selectInv = v0.get()


selectDrum = 1


def selectDrums():
    global selectDrum
    selectDrum = v1.get()


filename = ""


def browseFiles():
    global filename
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File", filetypes=(("Midi Files", ".mid"),
                                                                                            ("all files", "*.*")))
    label_file_explorer.configure(text="File Opened:" + filename)


window = Tk()
window.title("AutoHarmonizer")
window.geometry("800x600")
window.config(background="white")
label_file_explorer = Label(window, text="File Explorer", width=100, height=5, fg="blue")
button_explore = Button(window, text="Browse Files", command=browseFiles)
button_exit = Button(window, text="Confirm Selections")
button_exit.bind('<Button-1>', exitButton)
label_file_explorer.place(x=30, y=275)
button_explore.place(x=345, y=275)
button_exit.place(x=325, y=375)
v0 = IntVar()
v0.set(1)
r1 = Radiobutton(window, text="No Inversions", variable=v0, value=1, command=selectInversion)
r2 = Radiobutton(window, text="Inversions", variable=v0, value=2, command=selectInversion)
r1.place(x=30, y=20)
r2.place(x=130, y=20)
v1 = IntVar()
v1.set(1)
r3 = Radiobutton(window, text="No Drums", variable=v1, value=1, command=selectDrums)
r4 = Radiobutton(window, text="Drums", variable=v1, value=2, command=selectDrums)
r3.place(x=30, y=60)
r4.place(x=110, y=60)
sysCheck = BooleanVar()
check = Checkbutton(window, text="Auto-Generate Melody ", variable=sysCheck, command=checkMelody, onvalue=True,
                    offvalue=False, height=5, width=20)
check.place(x=550, y=10)
variety = ("None", "Some", "A Lot")
varLabel = Label(window, text="Musical Variety", width=15, height=1, fg="blue", bg="white")
varLabel.place(x=300, y=10)
varBox = Combobox(window, values=variety)
varBox.bind("<<ComboboxSelected>>", checkCombo)
varBox.place(x=300, y=30)
measureLabel = Label(window, text="Measures", width=10, height=1, bg="white", fg="blue")
measureLabel.place(x=550, y=105)
curval = StringVar(value=0)
measureCount = Spinbox(window, from_=1, to=100, textvariable=curval)

measureCount.place(x=550, y=125)
keyArr = ("C", "C#", "Db", "D", "Eb", "E", "Fb", "F", "F#", "Gb", "G", "G#", "Ab", "A", "A#", "Bb", "B", "Cb")
keyLabel = Label(window, text="Musical Key", width=15, height=1, fg="blue", bg="white")
keyLabel.place(x=550, y=160)
keyBox = Combobox(window, values=keyArr)
keyBox.bind("<<ComboboxSelected>>", checkKey)
keyBox.place(x=550, y=180)
window.mainloop()

if melodyCheck:
  lengthofsolo = int(curval.get())
  melody = mus.stream.Stream()
  key = mus.key.Key(keyChoice)

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
      if z % 8 == 0:
          measure = copy.deepcopy(measure1)
      melody.append(measure)
  measure = mus.stream.Measure()
  measure.append(mus.note.Note(pitches[0], quarterLength = 4))
  melody.append(measure)
  melody.append(mus.meter.TimeSignature('4/4'))

  melody.show()
  time = time.ctime()
  name = ''
  for i in time:
    if i == ' ' or i == ':':
        name += '_'
    else:
        name += i
  melody.write(fmt = 'midi', fp = 'output_'+name+'.mid')
  filename = 'output_'+name+'.mid'

def threefourdrum(song, numMeasures, extraMeasure, length):
  lengthofsolo = numMeasures

  snarePart = stream.Part()
  # Bug in music21 requires us to use instrument.BassDrum in order for the snare drum to be heard in musescore
  snareDrum = instrument.BassDrum()
  snarePart.insert(snareDrum)
  for i in range(0, lengthofsolo):
    snareMeasures = [threesnaremeasure1, threesnaremeasure2, threesnaremeasure3, threesnaremeasure4]
    snarePart.insert(random.choice(snareMeasures)())

  bassPart = stream.Part()
  bassDrum = instrument.BassDrum()
  bassPart.insert(bassDrum)
  for i in range(0, lengthofsolo):
    bassMeasures = [threebassmeasure1, threebassmeasure2, threebassmeasure3, threebassmeasure4]
    bassPart.insert(random.choice(bassMeasures)())

  hiHatPart = stream.Part()
  hiHat = instrument.HiHatCymbal()
  hiHatPart.insert(hiHat)
  for i in range(0, lengthofsolo):
    hatMeasures = [threehatmeasure1, threehatmeasure2, threehatmeasure3, threehatmeasure4]
    hiHatPart.insert(random.choice(hatMeasures)())

  if extraMeasure:

    measure = stream.Measure()
    rest = mus.note.Rest()
    rest.duration.quarterLength = length
    measure.insert(rest)
    snarePart.insert(measure)
    bassPart.insert(measure)
    hiHatPart.insert(measure)

  song.append(snarePart)
  song.append(bassPart)
  song.append(hiHatPart)
  return song

def threesnaremeasure1():
    snareMeasure = stream.Measure()
    snareMeasure.append(note.Note(40, quarterLength = 0.75))
    snareMeasure.append(note.Note(40, quarterLength = 1.75))
    snareMeasure.append(note.Note(40, quarterLength = 0.5))
    return snareMeasure

def threesnaremeasure2():
    snareMeasure = stream.Measure()
    snareMeasure.append(note.Rest())
    snareMeasure.append(note.Note(40))
    snareMeasure.append(note.Note(40))
    return snareMeasure

def threesnaremeasure3():
    snareMeasure = stream.Measure()
    snareMeasure.append(note.Note(40, quarterLength = 1.5))
    snareMeasure.append(note.Note(40, quarterLength = 1.5))
    return snareMeasure

def threesnaremeasure4():
    snareMeasure = stream.Measure()
    snareMeasure.append(note.Note(40, quarterLength = 0.5))
    snareMeasure.append(note.Note(40))
    snareMeasure.append(note.Note(40, quarterLength = 1.5))
    return snareMeasure

def threebassmeasure1():
    bassMeasure = stream.Measure()
    bassMeasure.append(note.Note(35, quarterLength = 3))
    return bassMeasure

def threebassmeasure2():
    bassMeasure = stream.Measure()
    bassMeasure.append(note.Note(35, quarterLength = 1.5))
    bassMeasure.append(note.Note(35, quarterLength=1.5))
    return bassMeasure

def threebassmeasure3():
    bassMeasure = stream.Measure()
    bassMeasure.append(note.Note(35, quarterLength = 2))
    bassMeasure.append(note.Note(35))
    return bassMeasure

def threebassmeasure4():
    bassMeasure = stream.Measure()
    bassMeasure.append(note.Note(35))
    bassMeasure.append(note.Note(35))
    bassMeasure.append(note.Note(35))
    return bassMeasure

def threehatmeasure1():
    hatMeasure = stream.Measure()
    hatMeasure.append(note.Note(42, quarterLength = 0.75))
    hatMeasure.append(note.Note(42, quarterLength=0.75))
    hatMeasure.append(note.Note(42, quarterLength=0.75))
    hatMeasure.append(note.Note(42, quarterLength=0.75))
    return hatMeasure

def threehatmeasure2():
    hatMeasure = stream.Measure()
    hatMeasure.append(note.Note(42, quarterLength = 0.5))
    hatMeasure.append(note.Note(42, quarterLength = 1.75))
    hatMeasure.append(note.Note(42, quarterLength = 0.75))
    return hatMeasure

def threehatmeasure3():
    hatMeasure = stream.Measure()
    hatMeasure.append(note.Note(42, quarterLength = 2))
    hatMeasure.append(note.Note(42, quarterLength = 0.75))
    hatMeasure.append(note.Note(42, quarterLength=0.25))
    return hatMeasure

def threehatmeasure4():
    hatMeasure = stream.Measure()
    hatMeasure.append(note.Note(42, quarterLength = 0.5))
    hatMeasure.append(note.Note(42, quarterLength = 1.5))
    hatMeasure.append(note.Note(42))
    return hatMeasure

def fourfourdrum(song, numMeasures, extraMeasure, length):
  lengthofsolo = numMeasures

  snarePart = stream.Part()
  # Bug in music21 requires us to use instrument.BassDrum in order for the snare drum to be heard in musescore
  snareDrum = instrument.BassDrum()
  snarePart.insert(snareDrum)
  for i in range(0, lengthofsolo):
    snareMeasures = [foursnaremeasure1, foursnaremeasure2, foursnaremeasure3]
    snarePart.insert(random.choice(snareMeasures)())

  bassPart = stream.Part()
  bassDrum = instrument.BassDrum()
  bassPart.insert(bassDrum)
  for i in range(0, lengthofsolo):
    bassMeasures = [fourbassmeasure1, fourbassmeasure2, fourbassmeasure3, fourbassmeasure4]
    bassPart.insert(random.choice(bassMeasures)())

  hiHatPart = stream.Part()
  hiHat = instrument.HiHatCymbal()
  hiHatPart.insert(hiHat)
  for i in range(0, lengthofsolo):
    hatMeasures = [fourhatmeasure1, fourhatmeasure2, fourhatmeasure3, fourhatmeasure4]
    hiHatPart.insert(random.choice(hatMeasures)())

  if extraMeasure:

    measure = stream.Measure()
    rest = mus.note.Rest()
    rest.duration.quarterLength = length
    measure.insert(rest)
    snarePart.insert(measure)
    bassPart.insert(measure)
    hiHatPart.insert(measure)

  song.append(snarePart)
  song.append(bassPart)
  song.append(hiHatPart)
  return song



def fourbassmeasure1():
  bassMeasure = stream.Measure()
  bassMeasure.append(note.Note(35, quarterLength=0.75))
  bassMeasure.append(note.Note(35, quarterLength=0.75))
  bassMeasure.append(note.Note(35, quarterLength=1.5))
  bassMeasure.append(note.Note(35, quarterLength=1))
  return bassMeasure


def fourbassmeasure2():
  bassMeasure = stream.Measure()
  bassMeasure.append(note.Note(35, quarterLength=2))
  bassMeasure.append(note.Note(35, quarterLength=2))
  return bassMeasure


def fourbassmeasure3():
  bassMeasure = stream.Measure()
  bassMeasure.append(note.Note(35, quarterLength=1.5))
  bassMeasure.append(note.Note(35, quarterLength=1))
  bassMeasure.append(note.Note(35, quarterLength=1.5))
  return bassMeasure


def fourbassmeasure4():
  bassMeasure = stream.Measure()
  bassMeasure.append(note.Note(35, quarterLength=1))
  bassMeasure.append(note.Note(35, quarterLength=0.5))
  bassMeasure.append(note.Note(35, quarterLength=1.75))
  bassMeasure.append(note.Note(35, quarterLength=0.75))
  return bassMeasure


def foursnaremeasure1():
  snareMeasure = stream.Measure()
  snareMeasure.append(note.Rest())
  snareMeasure.append(note.Note(40, quarterLength=2))
  snareMeasure.append(note.Note(40, quarterLength=1))
  return snareMeasure


def foursnaremeasure2():
  snareMeasure = stream.Measure()
  snareMeasure.append(note.Rest(0.5))
  snareMeasure.append(note.Note(40, quarterLength=0.5))
  snareMeasure.append(note.Note(40, quarterLength=2))
  snareMeasure.append(note.Note(40, quarterLength=0.5))
  return snareMeasure


def foursnaremeasure3():
  snareMeasure = stream.Measure()
  snareMeasure.append(note.Note(40, quarterLength=0.5))
  snareMeasure.append(note.Note(40, quarterLength=1.5))
  snareMeasure.append(note.Note(40, quarterLength=0.5))
  snareMeasure.append(note.Note(40, quarterLength=1.5))
  return snareMeasure


def fourhatmeasure1():
  hatMeasure = stream.Measure()
  hatMeasure.append(note.Note(42, quarterLength=1.5))
  hatMeasure.append(note.Note(42, quarterLength=0.75))
  hatMeasure.append(note.Note(42, quarterLength=1))
  hatMeasure.append(note.Note(42, quarterLength=0.75))
  return hatMeasure


def fourhatmeasure2():
  hatMeasure = stream.Measure()
  hatMeasure.append(note.Note(42, quarterLength=2))
  hatMeasure.append(note.Note(42, quarterLength=0.5))
  hatMeasure.append(note.Note(42, quarterLength=1.5))
  return hatMeasure


def fourhatmeasure3():
  hatMeasure = stream.Measure()
  hatMeasure.append(note.Note(42, quarterLength=0.5))
  hatMeasure.append(note.Note(42, quarterLength=1.75))
  hatMeasure.append(note.Note(42, quarterLength=1.25))
  hatMeasure.append(note.Note(42, quarterLength=0.5))
  return hatMeasure


def fourhatmeasure4():
  hatMeasure = stream.Measure()
  hatMeasure.append(note.Note(42, quarterLength=1.75))
  hatMeasure.append(note.Note(42, quarterLength=0.5))
  hatMeasure.append(note.Note(42, quarterLength=0.75))
  hatMeasure.append(note.Note(42))
  return hatMeasure






mf1 = mus.midi.MidiFile()
mf1.open(filename)
mf1.read()
mf1.close()
s1 = mus.midi.translate.midiFileToStream(mf1)

key = s1.analyze('key')

noteToNum = {}

pitchNew = key.pitches[0 : len(key.pitches) - 1]
chords = []
chordsMajor = []
chordsMinor = []

for i in range(7):
  noteToNum[pitchNew[i].name] = i
  a = mus.note.Note(pitchNew[i])
  b = a.transpose(3)
  c = b.transpose(4)
  chord = mus.chord.Chord([a, b, c])
  chordsMinor.append(chord)

for i in range(7):
  a = mus.note.Note(pitchNew[i])
  b = a.transpose(4)
  c = b.transpose(3)
  chord = mus.chord.Chord([a, b, c])
  chordsMajor.append(chord)
for i in range(7):
  a = mus.note.Note(pitchNew[i])
  b = mus.note.Note(pitchNew[(i + 2) % 7])
  if i + 2 >= len(key.pitches) - 1:
    b = b.transpose(12)
  c = mus.note.Note(pitchNew[(i + 4) % 7])
  if i + 4 >= len(key.pitches) - 1:
    c = c.transpose(12)
  chord = mus.chord.Chord([a, b, c])
  chords.append(chord)
  #chord.show()

if key.mode == 'minor':
  progressions = [[2, 3, 4, 5, 6, 7], [5, 7], [4, 6], [1, 2, 5, 7], [1, 6], [2, 4], [1]]
else:
  progressions = [[2, 3, 4, 5, 6, 7], [5, 7], [4, 6], [1, 2, 5, 7], [1, 6], [2, 4], [1]]
prev = 0
prevChord = copy.copy(chords[0])
p2 = mus.stream.Part()
s2 = mus.stream.Stream()

timeSignature = s1.recurse().getElementsByClass(mus.meter.TimeSignature)[0]
s2.append(timeSignature)

i = 1
while len(s1.measure(i).pitches) > 0:
  matches = [0, 0, 0, 0, 0, 0, 0]
  freqDict = {}
  reach = [False, False, False, False, False, False, False]
  for j in progressions[prev]:
    reach[j - 1] = True

  for j in key.pitches:
    freqDict[j.name] = 0
  volume = 0
  num = 0
  notes = set(())

  for j in s1.measure(i).recurse().getElementsByClass(mus.note.Note):
    num += 1
    volume += j.volume.cachedRealized
    notes.add(j.name)

    if j.name in freqDict:
      freqDict[j.name] += 1
  for j in s1.measure(i).recurse().getElementsByClass(mus.chord.Chord):
    num += 1
    volume += j.volume.cachedRealized
    for k in j.pitches:
      notes.add(k.name)

      if k.name in freqDict:
        freqDict[k.name] += 1

  for j in range(7):
    for pitch in chords[j].pitches:
      if pitch.name in freqDict and freqDict[pitch.name] > 0:
        matches[j] += 1
  max = 0
  bestChoice = 0
  for j in range(7):
    if matches[j] > max:
      max = matches[j]
      bestChoice = j
  ops = []
  for j in notes:
    if not j in noteToNum:
        for pitch in key.pitches:
            if pitch.ps == mus.pitch.Pitch(j).ps:
                j = pitch.name
                break
    ops.append(j)
  list = []
  progressionList = []
  for j in range(7):
    if matches[j] == max:
      list.append(j)
    if i > 0:
      if matches[j] == max and reach[j]:
        progressionList.append(j)

  if len(notes) <= 2:
    choice = random.randint(0, len(ops) - 1)
    chord = copy.copy(chords[noteToNum[ops[choice]]])
    prev = noteToNum[ops[choice]]
  elif comboChoice == 'None':
    prev = bestChoice
    chord = copy.deepcopy(chords[bestChoice])
  else:
    if len(progressionList) < 2 or comboChoice == 'A Lot':
      choice = random.randint(0, len(list) - 1)
      chord = copy.deepcopy(chords[list[choice]])
      prev = list[choice]
    else:
      choice = random.randint(0, len(progressionList) - 1)
      chord = copy.deepcopy(chords[progressionList[choice]])
      prev = progressionList[choice]


  best = 100
  if i > 1 and selectInv == 2:
    for inversion in range(3):
      curr = 0
      if inversion == 0:
        currChord = copy.deepcopy(chord)
      if inversion == 1:
        currChord = mus.chord.Chord([copy.deepcopy(chord.notes[1]), copy.deepcopy(chord.notes[2]), copy.deepcopy(chord.notes[0]).transpose(12)])
      elif inversion == 2:
        currChord = mus.chord.Chord([copy.deepcopy(chord.notes[2]), copy.deepcopy(chord.notes[0]).transpose(12), copy.deepcopy(chord.notes[1]).transpose(12)])

      for j in range(3):
        interval = mus.interval.Interval(prevChord.notes[j], currChord.notes[j])
        curr += abs(interval.semitones)
      if curr < best:
        best = curr
        chord = currChord
  chord.duration.quarterLength = s1.measure(i).duration.quarterLength

  if num != 0:
    volume /= num
  if volume < 0.1:
    volume = 0.16

  chord.volume.velocityScalar = volume
  prevChord = copy.deepcopy(chord)
  s2.append(chord)

  i += 1

extraMeasure = False
length = 0
if i == len(s1.recurse().getElementsByClass(mus.stream.Measure)):
  extraMeasure = True
  rest = mus.note.Rest()
  rest.duration.quarterLength = s1.measure(i).duration.quarterLength
  length = s1.measure(i).duration.quarterLength
  s2.append(rest)

p2.insert(s2)
s1.insert(s2)

if selectDrum == 2:
    if str(s1.recurse().getElementsByClass(mus.meter.TimeSignature)[0]) == '<music21.meter.TimeSignature 4/4>':
        s1 = fourfourdrum(s1, i - 1, extraMeasure, length)
    elif str(s1.recurse().getElementsByClass(mus.meter.TimeSignature)[0]) == '<music21.meter.TimeSignature 3/4>':
        s1 = threefourdrum(s1, i - 1, extraMeasure, length)
s1.show()
