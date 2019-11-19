# MQL5 Language Pack for Sublime Text 3

This plugin contains all features you need to code with the MetaQuotes Language 5 with Sublime Text 3.

These features are:
* Code completion - available for all Mql5 functions that are listed at https://www.mql5.com/en/docs/function_indices
* Syntax highlighting - the syntax highlighting is based on the C++ syntax that is shipped with ST3 and is still work in progress
* Code compiling - with the short cut `ctrl + alt + m` you can compile your mq5 files and get feedback about the compile result. This feature is inspired by the MQL4 Compiler plugin for ST3.

## Requirements

To use the compile feature the MetaEditor has to be installed on your Windows machine.

## Manual Install

- `cd <Packages directory>`   (e.g. `~\Sublime Text 3\Data\Packages`)
- `git clone https://github.com/tombout/SublimeMql5LanguagePack.git Mql5LanguagePack`

## Package Settings

The settings for this plugin are available in ST3 at `Preferences -> Package Settings -> Mql5 Language Pack`. The plugin needs to know the path to the MetaEditor executable. Also the path to the Mql5 Include files must be set in the preferences. This is needed because I wanted to be able to have my source code outside the Mql5 directory.

The default settings are:
`
{
    "metaeditor_file": "C:/Program Files/MetaTrader 5/metaeditor64.exe",
    "mql5_home" : "%APPDATA%/MetaQuotes/Terminal/D0E8209F77C8CF37AD8BF550E51FF075/MQL5"
}
`