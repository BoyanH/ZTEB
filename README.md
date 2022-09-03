# ZTEB -- ZTEB is Tony's Electronic Birthday-Card


## Getting Started

```shell
$ pip install zteb
$ zteb unwrap
```

## Background Story

Nedelcho Petrov and me, being the great friends that we are, 
were brainstorming ideas for Tony's (Anton Karakochev) birthday present at the very last moment.
Inbetween of trying to find a rather unique and satisfying present and entertaining ourselves,
as, did I say, great friends, we considered everything from a set of fresh winter tyres to mount
a car onto to some bitcoins (or infinitesimal fractions thereof) to be locked for good as a nice (?) 
investment for the next twenty years. I thought about this for a while on my own, but concluded that even
though such an investment could probably be sufficient to buy a new car, it would be a shame if there
are no tyres to mount it on. I took the idea a bit further (or behind) and decided
to lock a simple birthday card in an electronic time capsule of some sort, so it could only be read 
after three days. This would make for some present and prevent Tony from realising what kind of friends
he has, or at least in our presence.

## About the Project

**ZTEB** provides a simple command line interface to create a sort of electronic time capsules, the
content of which can only be retrieved after a specified amount of time. 
The functionality is based on the paper 
[Time-lock puzzles and timed-release Crypto](http://people.csail.mit.edu/rivest/RivestShamirWagner-timelock.pdf)
by Rivest, Shamir and Wagner and relies on encrypting the contents of the capsule
and only exposing information on how to retrieve the encryption key with 
significant computational effort. In case our current beliefs on 
complexity classes (P/NP) and prime number factorization techniques are correct,
a fixed amount of iterations is required to solve the puzzle.
The time it takes to perform a single iteration, however, can vary greatly
between various machines and algorithm implementations, the average naturally decreasing
as more powerful CPUs are produced. This implementation can create a capsule which
takes approximately the specified amount of time to open on the current machine, 
running the same operating system, running the current code, 
on the same Python interpreter, using the same... 

### CLI

#### Creating a time capsule

```
Usage: zteb wrap [OPTIONS] CARD OUTPUT

  Wrap an electronic birthday-card.

Options:
  -w, --wrapper-text PATH  Optional path to file containing wrapper text. This
                           is shown while unwrapping the card.
  -d, --duration DELTA     Desired amount of time for the unwrapping to take
                           in the format of pandas.Timedelta.
  --help                   Show this message and exit.
```

Example
```shell
$ zteb wrap amazing-capsule-contents.txt capsule.zteb -d 13:37:00
```


#### Opening a time capsule

```
Usage: zteb unwrap [OPTIONS]

  Unwrap an electronic birthday-card.

Options:
  -c, --card PATH         Path to a wrapped birthday-card. If not specified,
                          the built-incard for Tony's birthday is being
                          unwrapped.
  -o, --output-file PATH  Path to file to store card message to.
  -s, --silent            Suppress all stdout output.
  --help                  Show this message and exit.

```

Example
```shell
$ zteb unwrap -c capsule.zteb
```
