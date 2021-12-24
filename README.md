# Resa - a strategic (py)game
Resa is swedish and means _journey_ or _to travel_.

This project tries to bring classic strategic games to life in a new and different form. My idea is strongly influenced by the _Anno_ series and _Age of Empires_ and combines the different ways of playing. It should be platform-independent and completely freely available.

![Resa](https://bitbyteopen.org/wp-content/uploads/2021/12/Bildschirmfoto-2021-12-24-um-16.11.56.png)

> **Disclaimer**
> 
> The game does not claim to run at extremely high FPS and  resolution. Personally, my goal is that it runs smoothly on a RaspberryPi. Of course, other programming languages are better suited for game development, but I like python and the possibility of C extensions. It combines two of my favorites in development, even if my C is extremely rusty.
> 
> I am happy about every player, tester, pull request or creative contribution and discussions about possible improvements, but not about the programming language that is used.

# Table of Contents

1. [How to install and run Resa](#How-to-install-and-run-Resa)
   - [Install](#Install)
   - [Run the game](#Run-the-game)
2. [How to contribute](#How-to-contribute)
3. [Credits](#Credits)
   - [Music](#Music)
   - [Sounds](#Sounds)
   - [Graphics](#Graphics)
4. [Documentation](#Documentation)
5. [License](#License)

# How to install and run Resa
Resa is based on `python3` with `pygame2`. I am currently using `python 3.10` for developing pre-releases. For non-pre-releases, I will store the python version in the release notes. Compatibility down to `python 3.6` will be tested for playable releases.

### Install
1. Make sure that you have installed the python version specified in the release, as well as pygame2 
2. Download from [Resa Releases](https://github.com/Kanasaru/resa/releases) the release of your choice
3. Unzip the archive

### Run the game
1. Switch to the directory in the terminal
2. Run `python3 main.py`

# How to contribute
Resa is intended as an open source project and therefore lives from people who contribute to making the game better. So support is welcome.

**_Everyone_** can play the current (pre-)release and report bugs or suggestions for improvement. To do so, please open an [issuse](https://github.com/Kanasaru/resa/issues) and provide some detailed information.

**_Developer_** can use the branch `develop` for pull requests and [issuse](https://github.com/Kanasaru/resa/issues) or [discussions](https://github.com/Kanasaru/resa/discussions) for everything else.

**_Designers_** are always very welcome as I have absolutely no idea about music production or graphic design. The game needs a little more structure to create meaningful sprites or a uniform concept for graphics. But if you want to design graphics, sounds or music for resa, please use the [discussions](https://github.com/Kanasaru/resa/discussions). 

# Credits

### Music
- _In Dreams_ by [Scott Buckley](https://www.scottbuckley.com.au), promoted by [chosic.com](https://www.chosic.com/free-music/all/) under [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- _Forest Walk_ by [Alexander Nakarada](https://www.serpentsoundstudios.com), promoted by [chosic.com](https://www.chosic.com/free-music/all/) under [Attribution 4.0 International (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/)
- _Illusory Realm_ by [Darren Curtis](https://www.darrencurtismusic.com/), promoted by [chosic.com](https://www.chosic.com/free-music/all/) under [Attribution 3.0 Unported (CC BY 3.0)](https://creativecommons.org/licenses/by/3.0/)

### Sounds
- _screenshot.wav_ orignal _camera.wav_ by [alejandra0908](https://freesound.org/people/alejandra0908/sounds/364499/) published under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)

### Graphics
- isometric 2D tiles by [Screaming Brain Studios](http://www.screamingbrainstudios.com), published on [https://itch.io](https://itch.io) under under [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/)
- trees by [Bleed](https://opengameart.org/users/bleed), published on [OpenGameArt.org](https://opengameart.org/content/tree-collection-v26-bleeds-game-art) under [Attribution 3.0 Unported (CC BY 3.0)](https://creativecommons.org/licenses/by/3.0/)

# Documentation
A good open source project, but also a game in general, benefits a lot from complete documentation. The current development status does not yet allow efficient documentation, but I don't want to lose any time and have to catch up on everything later.

On [my website](https://bitbyteopen.org) I write about the development process. Everything else, at least that's how I initially determined it, goes into the [documentation](resa/docs/index.md). Simple markdown files are used for this.

`doc/HowTos`: The HowTo's can be used to provide instructions for the development or the game itself.

`doc/GameRef`: The game reference is used to describe the game itself. The objects and the game dynamics, controls and processes are to be described. 

`doc/CodeRef`: The source code reference serves to document the individual modules with their classes, methods, functions and relationships. In addition, examples should be listed.

Maybe I will move some parts to the wiki later or use it for other purposes or continue to ignore it.

# License
Resa is published under the `GNU General Public License V3` and can be used under its conditions. The project contains many graphics, sounds and pieces of music that have been published under CC licenses. All works used are listed under [Credits](#Credits) with the respective license and linked accordingly.