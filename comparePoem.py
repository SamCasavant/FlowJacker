import measurePoem
import pylyrics3
import math

def getFlow(poem):
	stanzas = poem.split("\n\n")
	stanzas = [measurePoem.tokenize(stanza) for stanza in stanzas]
	print(stanzas)
	stress_struct = []
	scheme = []
	for stanza in stanzas:
		for line in stanza:
			stress_struct.append(measurePoem.getStressStruct(line))

		scheme.append(measurePoem.rhyme_scheme(stanza))

	return(stress_struct, scheme)


def compare(poem1, poem2):
	poem1_flow = getFlow(poem1)
	poem2_flow = getFlow(poem2)
	line_scores = []
	stress_scores = []
	for index, line1 in enumerate(poem1_flow[0]):
		try:
			line2 = poem2_flow[0][index]
		except IndexError:
			break
		length1 = len(line1)
		length2 = len(line2)
		variance = math.fabs(length2-length1)
		if variance == 0:
			line_scores.append(100)
		else:
			uncertainty = line1.count('X') + line2.count('X')
			if variance < 3*uncertainty:
				line_scores.append(100)
			elif variance < 3*uncertainty + 1:
				line_scores.append(50)
			elif variance < 3*uncertainty + 2:
				line_scores.append(25)
			else:
				line_scores.append(0)
		matches = 0
		total = 0
		for index2, stress1 in enumerate(line1):
			try:
				stress2 = line2[index2]
			except IndexError:
				break
			if stress1 == line2[index2]:
				matches += 1
			elif stress1 == '*' or line2[index2] == '*':
				matches += 1
			total +=1
		stress_scores.append(matches*100 / total)
	rhyme_scores = []
	for index, stanza1 in enumerate(poem1_flow[1]):
		try:
			stanza2 = poem2_flow[1][index]
		except IndexError:
			break
		matches = 0
		total = 0
		for index2, rhyme1 in enumerate(stanza1):
			try:
				rhyme2 = stanza2[index2]
			except IndexError:
				break
			if rhyme1 == line2[index2]:
				matches += 1
			elif rhyme1 == 'X' or line2[index2] == 'X':
				matches += .5
			total +=1
		rhyme_scores.append(matches*100 / total)

	return(line_scores, stress_scores, rhyme_scores)

poem1 = """
Amazing grace! How sweet the sound
That saved a wretch like me!
I once was lost, but now am found;
Was blind, but now I see.

’Twas grace that taught my heart to fear,
And grace my fears relieved;
How precious did that grace appear
The hour I first believed.

Through many dangers, toils and snares,
I have already come;
’Tis grace hath brought me safe thus far,
And grace will lead me home.

The Lord has promised good to me,
His Word my hope secures;
He will my Shield and Portion be,
As long as life endures.

Yea, when this flesh and heart shall fail,
And mortal life shall cease,
I shall possess, within the veil,
A life of joy and peace.

The earth shall soon dissolve like snow,
The sun forbear to shine;
But God, who called me here below,
Will be forever mine.

When we’ve been there ten thousand years,
Bright shining as the sun,
We’ve no less days to sing God’s praise
Than when we’d first begun."""

poem2 = """
Just sit right back and you'll hear a tale,
A tale of a fateful trip
That started from this tropic port
Aboard this tiny ship.

The mate was a mighty sailing man,
The skipper brave and sure.
Five passengers set sail that day
For a three hour tour, a three hour tour.

The weather started getting rough,
The tiny ship was tossed,
If not for the courage of the fearless crew
The Minnow would be lost, the Minnow would be lost.

The ship set ground on the shore of this uncharted desert isle
With Gilligan
The Skipper too,
A millionaire and his wife,
A movie star
The Professor and Mary Ann,
Here on Gilligan's Isle.

So this is the tale of our castaways,
They're here for a long, long time,
They'll have to make the best of things,
It's an uphill climb.

The first mate and his Skipper too,
Will do their very best,
To make the others comfortable,
In their tropic island nest.

No phone, no lights, no motor car,
Not a single luxury,
Like Robinson Crusoe,
It's primitive as can be.

So join us here each week my friend,
You're sure to get a smile,
From seven stranded castaways,
Here on "Gilligan's Isle."
"""

print([sum(l)/len(l) for l in compare(poem1, poem2)])