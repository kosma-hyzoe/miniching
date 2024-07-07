## miniching

A customizable CLI I Ching tool.

## How to run miniching?

1. Make sure `python3` is installed. The project was developed on Python 3.10.6.
   Older versions should also work, but were not tested.
2. Download or clone this repo.
3. Modify `config.py` as needed.
4. Execute `minching/mcng`.

I recommend adding the repo to your `$PATH` variable.

Use `mcng -h` to see the options:

```
usage: mcng [-h] [-z] [-r] [-s] [-q QUERY] [-e EXCERPT] [-t TIMESTAMP] [-p HISTORY_PATH] [-a] [-l--print-last]

options:
  -h, --help            show this help message and exit
  -z, --zhu-xi          use the modified Zhu Xi evaluation method instead of the classic 'read all changing lines' method
  -r, --reading         get full reading, not just the 'hex:lines -> hex' style result
  -s, --skip-history    don't write to history, even if -p flag was provided
  -q QUERY, --query QUERY
                        provide a query instead of the default prompt or posix redirects
  -e EXCERPT, --excerpt EXCERPT
                        provide an excerpt using the '64' /'61:1,2' formator the 3 coin sum notation where '788688' -> 23:3
  -t TIMESTAMP, --timestamp TIMESTAMP
                        provide a timestamp, any format
  -p HISTORY_PATH, --history-path HISTORY_PATH
                        provide an alternative history path, file or directory path
  -a, --asci-hex        use ascii symbols to mirror the hexagram next to their numbers
  -l--print-last        print the last history record, can be combined with -r and -p.will ignore -t, -e and -q flags
```

You can add some shell functions/aliases to fit your needs, i.e.:

```bash
# for the Zhu Xi method enthusiasts
alias mcng="mcng --zhu-xi"

# Always use custom path and print full reading
alias mcng="mcng -p ~/documents/personal -r"

# Unfortunately, to page the reading and see your query input while
# NOT writing your embarrassing queries to shell history, you need to get hacky
alias pcng="mcng >/dev/null; mcng -l -r"
```

## What is I Ching?

An ancient divination and wisdom book, easily one of, if not the most
influential chinese text. Think jungian dream generator and Bible
studies for the cool kids or a less woo-woo Tarot.

### Isn't it still a bit esoteric and weird?

**It probably is.** I hope that mentioning Jung makes it digestible enough for
an average western intellectual. Here's his I Ching foreword at
[carljungdepthpsychologysite.blog](https://carljungdepthpsychologysite.blog/2020/02/03/foreword-to-the-i-ching-by-carl-gustav-jung/)

### How does I Ching divination work?

The user writes down a query (usually a question) and gets a result with one
of the divination methods - usually tossing 3 coins, described below, or
arranging yarrow stalks.

The main part of the text consists of 64 hexagrams.
Their signs consist of six lines - yin ("unbroken") and yang ("broken") ones.

When tossing coins, each coin is assigned a value of 3 (usually "heads") or
2 (usually "tails"). A 7 or 8 gets you a "young", unchanging, yin or yang,
a 9 or 6 gets you  an "old" yin or yang and produce changing lines.

The result to a query can either be a static hexagram, (i.e. 3 : ䷂) or a
hexagram transition if one or more changing lines apply
(i.e. '3 -> 27 : ䷂ -> ䷚', with changing lines 5 and 6th).
The user should now read all the relevant text using their  preferred
evaluation method.

*This is of course nothing but a major oversimplification.*

## Credits and references

I know the Zu Xhi evaluation method that `miniching` thanks to
[biroco.com](https://www.biroco.com/yijing/basics.htm).

The `iching_reference.json` file is the classic
Richard Wilhelm's and Cary F. Baynes' translation.
I modified the one I found on [this dkloke's repo](https://github.com/dkloke/I-Ching-ref/blob/master/iChing.json).

## Recommended sources for an in-depth study

* [Wikipedia](https://en.wikipedia.org/wiki/I_Ching)
* [Biroco](https://www.biroco.com/yijing/index.htm)
* [The Gnostic Book Of Changes](https://www.jamesdekorne.com/GBCh/GBCh.htm)
