![Noto](images/noto.png)

This repository is intended to continue the development of the Blob emojis, originally invented in 2013, which have been replaced by different round designs more similar to other vendors, in Android Oreo from 2017.

Please note that I did not create most of the emojis; you can find an overview of the changes compared to the original state in `MODIFIED.md`

Most information on this fork will be included in the [Wiki](https://github.com/C1710/blobmoji/wiki). There you'll find more detailed build instructions and other helpful information on how to use this font and much more.

_[Emojipedia®](https://emojipedia.org) is a registered trademark of Emojipedia Pty Ltd_  
_Microsoft, Windows are trademarks of the Microsoft group of companies._  
_Noto is a trademark of Google Inc._

## Using the font
See https://github.com/C1710/blobmoji/wiki/Installation-and-Usage

## Building
Starting with Emoji 13, the build scripts used by Noto Emoji are not (directly) used anymore.  
Instead the font is built using a [new build toolset](https://github.com/C1710/emoji_builder), which works on top of these scripts and handles rendering and preprocessing the images as well as a completeness validation.

Instructions on how to build the font can be found in its repository.

Once you have it running, you can build it using the following command (you'll need to replace `emoji_builder` by the executable you use, e.g. `emoji_builder.exe` and maybe including the path):
```
emoji_builder --flags ./third_party/region-flags/svg blobmoji -w -a ./emoji_aliases.txt --ttx-tmpl ./NotoColorEmoji.tmpl.ttx.tmpl --palette ./Blobmoji.gpl --default_font "Comic Neue"
```
- `--flags`: Use the directory conaining the flags
- `-w` add a wave-effect to the flags
- `-a` use an alias file
- `--ttx-tmpl` Use the template for the font metadata
- `--palette` normalize the colors to a specific color palette in the GIMP format (which is a derivation of the color palette present in the [2014 _Material Design_](https://material.io/archive/guidelines/style/color.html#color-color-palette))
- `--default_font` Because the graphics program I currently use (Affinity Designer) outputs font specifications in a format that `resvg`/`emoji_builder` has issues with, the font is explicitly specified here (note that if the font is correctly recognized, this one is not used. So as of now it is _not_ used to use a font for _all_ emojis)

The build script I use myself is included. Please be aware that this is made to be used on Windows and requires `emoji_builder` to be installed and included in PATH, as well as an adjacent directory containing the EmojiCompat scripts and unicode tables.

## Docker Build
Alternatively, you can also build the font within Docker through the provided Dockerfile.
Just run `docker build . -t blobmoji && docker run --rm -it -v "$PWD/output:/output" blobmoji`. The resulting font will reside in the 'output' folder in your current working directory (Note that the volume assignment `-v "$PWD/output:/output"` might not work correctly on Windows).


## License

From Noto Emoji:
 > Emoji fonts (under the fonts subdirectory) are under the
[SIL Open Font License, version 1.1](fonts/LICENSE).<br/>
Tools and most image resources are under the [Apache license, version 2.0](./LICENSE).
Flag images under third_party/region-flags are in the public domain or
otherwise exempt from copyright ([more info](third_party/region-flags/LICENSE)).

This repository is licensed under these same terms as Noto Emoji.  

*In compliance with the [APACHE-2.0](https://opensource.org/licenses/Apache-2.0) license: I declare that this version of the program contains my modifications, which can be seen through the usual "git" mechanism.*  


## Contributing

As there is not much going on here, there are as of now no complicated rules for contribution.  
You can simply start pull requests, issues and discussions. I'll try to respond as soon as possible. 

The only requirement is that you allow to publish new assets under the same license.  
Feel free to add yourself to `CONTRIBUTORS_Blob` when creating a PR :)

_Please try to use the discussion feature for artistic topics, like the style of the emojis. Issues are better suited for real issues, like not being able to use the font or really **missing** characters, etc._

> ## Disclaimers
> I am **neither** affiliated nor in _any_ relationship to the original creators of the Noto Color Emoji font or to Emojipedia or anything or anyone else.
>
> > Android™ is a registered trademark or trademark of Google Inc in the United States and/or other countries.\
> > Unicode is a registered trademark of Unicode, Inc. in the United States and other countries.\
> > Emojipedia® is a registered trademark of Emojipedia Pty Ltd\
> > Microsoft, Windows are trademarks of the Microsoft group of companies.\
> > Noto is a trademark of Google Inc.
