# cryptopals

Here lives my umpteenth attempt to sit still long enough to crank out a few solutions. Behold __Cryptopals__, [a series of coding challenges in modern cryptography](https://blog.pinboard.in/2013/04/the_matasano_crypto_challenges/). Why spend time cleaning up code when there are horns to toot?

- [ Objectives ](#objectives)
- [ Things I Have Learned so Far During the Undertaking ](#learned)
- [ Dues and Doodies ](#doodie)
- [ Remarks and Commentary for Selected Exercises ](#remarks)

_This writeup is a WIP. The present headlines are expected to be exhaustively final._

<a name="objectives"></a>
## Objectives

#### To hone my Python syntaxing for engagement in CTFs

Where I stand today, my on-the-fly scripting lacks the refinement that resembles handy use of a readily available pocketknife, not to mention other outstanding tasks to [resolve P-vs-NP](https://www.youtube.com/watch?v=wf-BqAjZb8M&t=12m46s) and refresh my deeply rusted faculties in OOP and Go4 design patterns.

Deeper still, effective practice of scripting ought to feel like a natural extension of one's hands when diving into binaries, mapping web applications, and administering systems in general. I yet remain bogged down by Googling how to zip bytes in a desired manner or correctly create and apply generators.

#### To feed on bite- and byte-sized research in modern applications of cryptography

Also living here is an attempt at keeping the mind sharp.

A brief perusal of the Cryptopals problems, alongside a coaxing claim of tractability without a hard requirement for higher mathematics, intimates potential for sweeping transfer of decades' worth of research knowledge to the wandering, prospective undertaker in just a handful of exercises, lickety split. This is especially so, noting that just about any other content put out by Ptacek I look for has turned out to already be neatly presented in the exercises.

So far, the experience I can best compare this to is reliving my kindergarten days playing with building blocks or, my favorite toy set in the classroom, the marble run. I get to work on incredibly marvelous constructions through direct, hands-on interaction with the raw bits in a safe environment graciously provided for by Ptacek, et al. Everything plays by _my_ rules, and if something doesn't work correctly, it is _my_ own fault. It is a thoroughly liberating exercise of freedom.

While progress hasn't been swift, I find the yields already fruitful, and I see no reason to stop now. 

<a name="learned"></a>
## Things I Have Learned so Far during the Undertaking

#### The simplicity of the augmentative constructions built on top of the base encryption schemes

#### The significance of the oracle construct in cryptography

No claims are made regarding the attack oracle's relationship to the random oracle or generalized oracle machine in algorithmic analysis, and pay no mind to my having withdrawn from that advanced algorithms session a few years back. Do hush for a moment as I sweep them under the rug.

The oracle as it concerns me provides a service, computational or otherwise, that can be leveraged to mount attacks on the target system. It can be queried as much as desired, if its definition (and your computational resources for a local implementation) allows for it. When provided the particular parameters it requests to process a query, it will yield a usually very specific piece of information.

It serves to model a realistic trait or exhibited behavior of a live computer system that performs services probably more useful than those provided by a machine that only communicates, once, through the ultimately secure, one-time pad under a single key.

#### That I Must Not Stop doing what I want to do

<a name="doodie"></a>
## Dues and Doodies

To _Sir Psifertex_, I assign the distinction of having [casted the first baited hook](https://www.youtube.com/watch?v=okPWY0FeUoU&t=4m34s) that reeled me in to a culture that inspires my ongoing, longest-running push to buckle down and do what I want to do.

To _Sir geohot_, I look upon, in his light of infamy, as a [relatable](https://www.youtube.com/watch?v=AerjS7PTNYs&t=6m42s) and [timeless](https://www.youtube.com/watch?v=eGl6kpSajag&t=11m16s)... model.

To _dc916_, I am grateful for, aside from a platform serving as an outlet, the camaraderie provided me today and tomorrow. If history has taught me anything, it is that it is unlikely unwise to not count on anything to last. You will be better self-served by distracting yourself with a few meaningful, shared experiences along the way while you move forward in yearning.

And to my _dearest_ reader, I beg your recognition that, while we're a colorful bunch, I'm just a guy.

<a name="remarks"></a>
## Remarks and Commentary for Selected Exercises

#### 12, 14. Byte-at-a-time ECB decryption

#### 10, 18. Implement CBC & CTR

For quick learning, these exercises instruct you to manually replicate (and thus pick up on implicit hints for) the constructions on which you're about to mount your attacks. Difficult, they are not, but respite, they provide inbetween the more intense challenges. Their true value comes from the boost in self-confidence upon realizing that [comprehension of](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC) these [gorgeous machines](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CTR), in fact, lies within reach of any curious mind.

What's fascinating is how straightforwardly these augmentations address weaknesses in ECB and provide for theoretically sound bit-shuffling, even in the presence of plaintext repetition.

Further mesmerizing is the insight gleaned from a brief look at counter (CTR) mode and its decoupled keystream after two sets of fixation on pure block ciphers. The undertaker who otherwise enters with [a vague notion of security primitives](https://www.coursera.org/learn/crypto) will be handsomely rewarded with even more profound appreciation for CTR mode's newly realized advantages.

#### 16. CBC bitflipping attacks

Attacks can also be [cheeky and cute](https://www.coursera.org/lecture/crypto/attacking-non-atomic-decryption-mtJS8).

In a cipher block chaining (CBC) construction, even the painstaking effort to reject outright a metacharacter when parsing user-supplied strings can be sidestepped by providing a dormantly malicious placeholder-letter by which, later on, its corresponding byte in the previous block of the ciphertext (at this point under the attacker's arbitrary control) during decryption will be XOR-ed to sneak in that restricted character.

It bewilders me to imagine the extent of session hijacks, unintended shopping cart discounts, and disproportionate withdrawals accomplished by this silly attack.

#### 17. The CBC padding oracle

#### 21-24 The Mersenne Twister PRNG
