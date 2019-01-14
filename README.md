# cryptopals

Here lives my umpteenth attempt to sit still long enough to crank out a few solutions. Behold Cryptopals, [a series of coding challenges in modern cryptography](https://blog.pinboard.in/2013/04/the_matasano_crypto_challenges/). Why spend time cleaning up code when there are horns to toot?

This writeup is a WIP. The present headlines are expected to be exhaustively final.

## Objectives

#### To hone my Python syntaxing for engagement in CTFs

To _Sir Psifertex_, I award the distinction of having [casted the first baited hook](https://www.youtube.com/watch?v=okPWY0FeUoU&t=4m34s) that reeled me in to a culture that inspires my ongoing, longest-running push to buckle down and do what I want to do.

To _Sir geohot_, I look upon, in his light of infamy, as a [relatable](https://www.youtube.com/watch?v=AerjS7PTNYs&t=6m42s) and [timeless](https://www.youtube.com/watch?v=eGl6kpSajag&t=11m16s)... model.

Where I stand today, my on-the-fly scripting lacks the refinement that resembles handy use of a readily available pocketknife, not to mention other outstanding tasks to [resolve P-vs-NP](https://www.youtube.com/watch?v=wf-BqAjZb8M&t=12m46s) and refresh my deeply rusted faculties in OOP and Go4 design patterns.

Deeper still, the effective practice of Bash and Python scripting ought to feel like a natural extension of one's hands when diving into binaries, mapping web applications, and administering systems in general. I yet remain bogged down by Googling how to zip bytes in a desired manner or correctly create and apply generators.

#### To feed on bite- and byte-sized research in modern applications of cryptography

I find that the body is easily kept sharp with half-conscious nutritional intake, balanced gym workouts, and physical work.

The stimulation and cultivation of intellectual curiosity in a technical discipline of personal interest represents my attempt to keep the mind sharp.

## Things I Have Learned so Far during the Undertaking

#### The significance of the oracle construct in cryptography

#### The simplicity of the augmentative constructions built on top of the base encryption schemes

#### That I Must Not Stop doing what I want to do

## Dues and Doodies

To dc916, I am thankful for providing me today and tomorrow, aside from a platform as my outlet, friendships and fellowship. If history has taught me anything, it is that it is unlikely unwise to not count on anything to last. You will be better self-served by distracting yourself with a few meaningful, shared experiences along the way while you move forward in yearning.

And to my dear reader, I beg your recognition that, while we're a colorful bunch, I'm just a guy.

## Remarks and Commentary for Selected Exercises

#### 12, 14. Byte-at-a-time ECB decryption

#### 10, 18. Implement CBC & CTR

For quick learning, these exercises instruct you to manually replicate (and thus pick up on implicit hints for) the constructions on which you're about to mount your attacks. Difficult, they are not, but respite, they provide inbetween the more intense challenges. The biggest value they provide comes as a boost in self-confidence from the realization that comprehension of these [gorgeous machines](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC) is, in fact, [relatively simple](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CTR) and within reach of any curious mind.

Of fascinating note is how straightforward these overlying augmentations are in order to address the problems that arise from repeated plaintext blocks under a given key, despite having an underlying encryption algorithm with proven primitive security properties.

Even more amazing is, after two sets of fixation on CBC-mode constructions, the decoupled keystream of counter (CTR) mode and its newly realized advantages that envelop much more than the deceptively simplified problem description lets on.

#### 16. CBC bitflipping attacks

Attacks can also be [cheeky and cute](https://www.coursera.org/lecture/crypto/attacking-non-atomic-decryption-mtJS8).

In a cipher block chaining (CBC) construction, even the painstaking effort to reject outright a metacharacter when parsing user-supplied strings can be sidestepped by providing a dormantly malicious placeholder-plaintext-letter by which, later on, its corresponding byte in the previous ciphertext (at this point under the attacker's arbitrary control) during decryption will be XOR-ed to sneak in that restricted character.

It bewilders me to imagine the extent of session hijacks, unintended shopping cart discounts, and disproportionate withdrawals accomplished by this silly attack.

#### 17. The CBC padding oracle

#### 21-24 The Mersenne Twister PRNG
