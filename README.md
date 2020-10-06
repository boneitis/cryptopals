# cryptopals

Here lives my umpteenth attempt to sit still long enough to crank out a few solutions.

Behold __Cryptopals__, [a series of coding challenges in modern cryptography](https://blog.pinboard.in/2013/04/the_matasano_crypto_challenges/). Why spend time cleaning up code when there are horns to toot?

- [ Objectives ](#objectives)
- [ What I Have Learned During the Undertaking ](#learned)
- [ Dues and Doodies ](#doodie)
- [ Remarks and Commentary for Selected Exercises ](#remarks)

_This W is IP. If we're lucky, it might stay that way!_

<a name="objectives"></a>
## Objectives

#### To hone my Python syntaxing for CTF engagements

Where I stand today, my on-the-fly scripting lacks the refinement that resembles handy use of a readily available pocketknife, not to mention other outstanding, pressing tasks to [resolve P-vs-NP](https://www.youtube.com/watch?v=wf-BqAjZb8M&t=12m46s) and refresh my deeply rusted faculties in OOP and Go4 design patterns.

Deeper still, effective scripting ought to feel like a natural extension of one's hands when diving into binaries, mapping web applications, or administering systems in general. I yet remain bogged down by Googling how to zip bytes in a desired manner or correctly create and apply generators.

#### To feed on bite- and byte-sized research in modern applications of cryptography

Also living here is an attempt to keep the mind sharp.

A brief perusal of the Cryptopals problems, alongside a coaxing claim of tractability without the hard requirement for higher math, intimates potential for sweeping transfer of decades' worth of research knowledge to the wandering, prospective undertaker. And, it dares profess to accomplish this in just a handful of exercises, lickety split.

Considering that just about any other technical material put out by Ptacek appears to already be neatly presented in the exercises, I can only suspect some credibility to the claims.

The experience so far, to my best explanation, is of reliving my kindergarten days playing with LEGOs or, my favorite toy set in the classroom, the marble run. I enjoy the opportunity to work on marvelous constructions by direct, hands-on interaction with the raw bits in a playground where everything plays by _my_ rules, and anything that doesn't bend to my will is _my_ own fault.

It is a thoroughly liberating exercise of freedom.

<a name="learned"></a>
## What I Have Learned during the Undertaking

#### That I Must Not Stop doing what I want to do

Reaffirmation from lessons past continues to bring comfort and relief.

While progression hasn't been swift, I find the multifaceted yields already fruitful and many.

I have found every reason to [keep doing](https://www.youtube.com/watch?v=-PdXNRAQ31c&t=49m10s) what I'm doing, and any reason not to has led me only to contradiction.

<a name="doodie"></a>
## Dues and Doodies

To _Sir Psifertex_, I assign the distinction of having [casted the first baited hook](https://www.youtube.com/watch?v=okPWY0FeUoU&t=4m34s) that reeled me in to a culture that inspires my ongoing, longest-running push to buckle down and do what I want to do.

To _Sir geohot_, I look upon, in his light of infamy, as a [relatable](https://www.youtube.com/watch?v=AerjS7PTNYs&t=6m42s) and [timeless](https://www.youtube.com/watch?v=eGl6kpSajag&t=11m16s)... model.

To _dc916_, I am grateful for, aside from a platform serving as an outlet, the camaraderie provided me today and tomorrow. If history has taught me anything, it is that it is unlikely unwise to not count on anything to last. You will otherwise be better self-served by distracting yourself with a few meaningful, shared experiences along the way while you move forward in yearning.

To [the _Space Cowboy_](https://www.youtube.com/watch?v=eo7iwlMFPrM), were it not for whom... I can't even fathom.

And to my _dearest_ reader, I beg your recognition that, while we're a colorful bunch, I'm just a guy.

<a name="remarks"></a>
## Remarks and Commentary for Selected Exercises

#### 12, 14. Byte-at-a-time ECB decryption

The attack vector here is exposed via an injection point into the target plaintext and an oracle that will yield its electronic codebook (ECB) encryption when queried. The data following behind the point of entry can be revealed by easing bytes one at a time across cipher block borders and running a 2<sup>8</sup> dictionary check for each candidate final byte (or tighter still, less an order of magnitude for a printable ASCII target), knowing ahead of time the preceding bytes in the block.

Fossilized footprints along this stretch of road hint to the dangers of an overempowered oracle. Suggestive to the presence of a mentally-ill madman, curious is the omitted detail of the encryption oracle's lack of ability to consume the input (and possibly the threat to my predecessors of a rejected submission) when decrypting beyond the first cipher block. Nevertheless, in my vigilance, I escaped a grave calamity of ignorance to a hidden dimension in the exercise.

The final solution calls for a juggling act wherein the fully-suspended attacker orchestrates, with razor-sharp precision, several loop invariants in tandem to reground him-/herself and summon the correct order of bytes.

Among the invariants to manage are:
 - a byte index within a cipher block, which must be reconciled against...
 - a block index that, absent any mechanism to consume input, triggers a reset of the byte index when incremented,
 - all the while accommodating a blind offset into the entry block

Considering in hindsight the spread of milestones over multiple trials, there is room for a concession after all that mercy may have been mistaken for madness.

Dude's still [mentally ill](https://www.youtube.com/watch?v=iZa_XKpj9X4&t=5m05s), though.

#### 10, 18. Implement CBC & CTR

For quick learning, these exercises instruct you to manually replicate (and pick up on implicit hints for) the constructions on which you're about to mount your attacks. Difficult, they are not, but respite, they provide inbetween the more intense challenges. Their true value comes from the boost in self-confidence upon realizing that [comprehension of](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CBC) these [gorgeous machines](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#CTR), in fact, lies within reach of any curious mind.

What's fascinating is how straightforwardly these augmentations address weaknesses in ECB and provide for theoretically sound bit-shuffling, even in the presence of plaintext repetition.

Further mesmerizing is the insight gleaned from a brief look at counter (CTR) mode and its decoupled keystream after two challenge sets of fixation on pure block ciphers. The undertaker who approaches with [a vague notion of security primitives](https://www.coursera.org/learn/crypto) will be handsomely rewarded with even more profound appreciation for CTR mode's newly realized advantages.

#### 16. CBC bitflipping attacks

Attacks can also be [cheeky and cute](https://www.coursera.org/lecture/crypto/attacking-non-atomic-decryption-mtJS8).

In a cipher block chaining (CBC) construction, even the painstaking effort to reject outright a metacharacter when parsing user-supplied strings can be sidestepped by feeding a dormantly malicious placeholder-letter by which, later on, its corresponding byte in the previous block of the ciphertext (at this point under the attacker's control) during decryption will be XOR-ed to sneak in that restricted character.

#### 17. The CBC padding oracle

#### 21-24. The Mersenne Twister PRNG

### Hash Functions Triple Play

#### 52. Breaking the bigger hash with, quote-unquote, random samples

This exercise has you homebake your own de-fanged Merkle-Damgard hashes, so that you can run solution code within a reasonable timeframe (as well as giving you a closer view of the machinery).

What I took away from the challenge was that I would feel better using a single, longer hash than two shorter, concatenated hashes, because you are bottlenecking your construction to your stronger hash (if they differ in strength).

An auditor or attacker with white box access can attack your smaller hash (if your two hash functions differ in bit-size) to generate a 2^(n/2)-way collision (that is, if it's feasible to collide the hash at all, there is a clever trick to generate a massive number of messages that all collide to the same output), then birthday attack the bigger hash using the messages from that collision-pool. (Importantly, this mention of "n" specifically refers to the bit-size of the larger hash, a.k.a., the bottleneck.)

Although there might be something about it at first glance that makes the messages feel not random enough (in order for the birthday principle to hold), it's far easier to instruct you, dear reader, to just do the exercise in order to grok why it works than for me to figure out how to explain it :)

#### 53. Crashing into the hash chain somewhere along the path

#### 54. Dictating Destiny with the hash diamond
