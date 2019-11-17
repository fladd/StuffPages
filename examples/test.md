title: 10 years of Expyriment 🎉
author: Florian Krause
author_link: https//www.floriankrause.org
date: October 30, 2019

**Today marks [Expyriment](https://expyriment.org)'s 10th anniversary!** We are very excited about this and would like to take the opportunity to look back on the last 10 years, introduce the [0.10 anniversary release](https://github.com/expyriment/expyriment/releases/tag/v0.10.0), and contemplate a bit about what is coming up next.

[![expyriment_logo](https://www.expyriment.org/images/expyriment_logo.png)](http://expyriment.org)

## "Initial upload, start of project"

It all began when I started my PhD position - supervised by [Oliver Lindemann](http://www.cognitive-psychology.eu/lindemann/) - at the Donders Institute in Nijmegen, The Netherlands. I had just finished my Master's project during which I was using specialised commercial software for implementing my behavioural and fMRI tasks, and I was convinced that there had to be a better way to do this. Oliver, who used to programme his experiments in Delphi, agreed. Since I was already a big Python fan back then, and had written some crude Pygame code to present visual stimuli and collect button press responses, I suggested to Oliver that it might be beneficial to extend this into a more comprehensive framework to facilitate implementing our planned studies. Oliver agreed again, we started coding, and after four intense weeks, not only did we have something that worked for us, but something we believed could be helpful for others as well. And so, on October 30, 2009 - exactly 10 years ago - we made the very first Expyriment code publicly available at our back then [Google Code repository](https://code.google.com/archive/p/expyriment/) with a rather unspectacular commit message:

> Initial upload, start of project

Approximately one year later, we packaged everything into a first (alpha) release and spread it around colleagues. The throughout positive feedback encouraged us to continue working on the project and after several further releases, in 2014 we decided to introduce Expyriment to a wider scientific audience by writing a [method article](https://doi.org/10.3758/s13428-013-0390-6) (Krause & Lindemann, 2014[^1]). In the same year we also followed the rest of the open source community in moving our code to a [GitHub repository](https://github.com/expyriment/expyriment) (where it still is today), and we released a first proof-of-concept [version for Android](https://github.com/expyriment/expyriment-android-runtime/releases/tag/v0.1.0). As Expyriment matured, it also turned into an integral part of other open source projects, most notably [OpenSesame](https://osdoc.cogsci.nl/) (Mathôt, Schreij & Theeuwes, 2012[^2]) and [TrajTracker](https://trajtracker.wixsite.com/trajtracker). In the following years then, with me having started a Postdoc in Maastricht, The Netherlands, and Oliver working at the University of Potsdam, Germany, it became a bit quieter around Expyriment. Nevertheless, we continuously fixed bugs, implemented new features, and even managed to be the first Python-based experimental software to have an official [release with Python 3 support](https://github.com/expyriment/expyriment/releases/tag/v0.9.0).

## 0.10 anniversary release; Expyriment stash

More recently, working in the same country again (Oliver at Erasmus University Rotterdam, me at the Donders Institute again) has surely facilitated collaborating on Expyriment, and so we are happy to celebrate today with a brand new [Expyriment 0.10](https://github.com/expyriment/expyriment/releases/tag/v0.10.0) release. Besides fixing several bugs, we also included a variety of new features. For instance, a new `misc.Colour` class makes handling colours more convenient by allowing to create them from either RGB, HSV or HSL tuples, Hex triplets, or even [colour names](https://www.w3schools.com/colors/colors_names.asp), and providing a way to seemingly convert between these different formats. The `io.TextInput` class now supports unicode characters by default and has a new setting for right-to-left text. All visual stimuli now have methods to get and set their position in polar coordinates. The keyboard can now also be checked for key-up events. The command line interface is now also available as the system command `expyriment`. And there are [many more changes](https://docs.expyriment.org/Changelog.html).

The probably biggest novelty in this release, however, is the addition of the new [Expyriment stash](http://stash.expyriment.org), a central place for additional Expyriment resources, such as plugins ("extras"), examples and other tools. All of which can be downloaded and installed automatically from within Expyriment itself when needed. But we didn't just move all our current additional resources into the stash to keep the core library lightweight. No. We are also hoping that the stash can become a hub for future contributions from the open science community that enrich it with a colourful variety of Expyriment plugins, tools and full example scripts for specific equipment and different experimental paradigms.

## Expyriment 1.0, Pygame 2 and Python 3

To end this article, I would like to share with you some of our thoughts on Expyriment's future. Even though currently only one of us (Oliver) has managed to find a _permanent_ position in Academia, we are both very committed to continue working on and supporting Expyriment.

The next planned major release will be 1.0 and will have some big changes. First of all, we will switch to the new [Pygame 2](https://www.pygame.org/news/2018/11/where-we-are-up-to-with-pygame-2-and-1-9-5), which we expect to be released very soon. Based on [SDL2](https://www.libsdl.org/index.php), this new version will bring many modern and much requested features, such as HiDPI, display scaling, multiple displays, and multitouch support. With SDL2 officially supporting Android and iOS, we are also hoping to be able to offer better mobile support for Expyriment somewhere along the line. Next, we will focus exclusively on Python 3, meaning that we will join the Python Software Foundation in [dropping Python 2 support](https://www.python.org/dev/peps/pep-0373/). Other changes we are currently discussing include implementing a new audio system (with hopefully shorter and more stable latencies), as well as providing sub-millisecond timing accuracy (up to 1 microsecond) throughout Expyriment.

Last but not least, we are also considering to explore potential funding options specifically for Expyriment development. So, if you are aware of a research grant that we qualify to apply for, please let us know! 🙂

```python
#!/usr/bin/env python

"""Summary of module.

Description of module.
Can contain multiple lines.

"""

__author__ = 'Name Surname <Email address>'
__version__ = '0.0.0'
__revision__ = '0000000'
__date__ = 'Mon Jan 01 00:00:00 2000 +0000'


# Imports
import package
import package.module
import package.module as mymodule
from package import module
from package import module as mymodule
from package import Class
from package import Class as MyClass
from package import module1, module2, Class1, Class2


# Variables
my_global_variable = "use underscores if needed"
print_ = "avoid collision with keywords"
MY_CONSTANT = 3.1415

# Functions
def my_function(a, b=""):
    """Summary of function.

    Description of function.
    Can contain multiple lines.

    Parameters:
    -----------
    a : int
        A variable.
    b : str, optional
        Another variable.

    Returns:
    --------
    rtn : int
        Sum of a and length of b.

    """

    try:
        return a + len(b)
    except Exception:
        return None


# Classes
class MyClass(ParentClass):
    """Summary of class.

    Description of class.
    Can contain multiple lines.

    """

    class_variable = "a class variable"
    another_class_variabel = "another one"

    @staticmethod
    def static_method(*args):
        """Summary of static method.

        Description of static method.
        Can contain multiple lines.

        Parameters:
        -----------
        args* : list
            A list of arguments.

        """

        pass

    @classmethod
    def class_method(cls, *args):
        """Summary of class method

        Description of class method.
        Can contain multiple lines.

        Parameters:
        -----------
        args* : list
            A list of arguments.

        """

        pass

    def __init__(self, *args):
        """Summary of constructor.

        Description of constructor.
        Can contain multiple lines.


        Parameters:
        -----------
        args* : list
            A list of arguments.

        """

        ParentClass.__init__(self, *args)

        self.arg1 = "public argument"
        self._arg2 = "non-public argument"
        self.__arg3 = "non-public argument, avoids collision with subclasses"

    @property
    def arg2(self):
        """Getter for arg2."""

        return self._arg2

    @arg2.setter
    def arg2(self, value):
        """Setter for arg2."""

        self._arg2 = value

    def instance_method(self, *args):
        """Summary of instance method.

        Description of instance method.
        Can consist of multiple lines.


        Parameters:
        -----------
        args* : list
            A list of arguments.

        """

```

[^1]:
    Krause, F. & Lindemann, O. (2014). Expyriment: A Python library for cognitive and neuroscientific experiments. _Behavior Research Methods, 46(2)_, 416-428. [https://doi.org/10.3758/s13428-013-0390-6](https://doi.org/10.3758/s13428-013-0390-6)
[^2]:
    Mathôt, S., Schreij, D., & Theeuwes, J. (2012). OpenSesame: An  open-source, graphical experiment builder for the social sciences. *Behavior Research Methods*, *44*(2), 314-324. [https://doi.org/10.3758/s13428-011-0168-7](https://doi.org/10.3758/s13428-011-0168-7)
