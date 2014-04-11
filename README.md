sublime-jad
===========

Simple Sublime plugin to decompile (JAD) or disassemble (javap) java classes 

Supported commands: 
 - `java_jad`: Call JAD to decompile .class file. Optional boolean argument to open results in new tab: `new_view`
 - `java_javap`: Call javap to disassemble .class file
 - `java_jad_undo`: undo and reset of view flags


Configuration options:

 - `java_jad_path` - Path to JAD executable. Default value for osx and linux: ~/jad/jad, for windows: jad.exe
 - `java_javap_path` - Path to javap executable. Default value for osx and linux: javap, for windows: javap.exe
 - `java_jad_default_command` - Command to execut on .class file load. Default value: `java_jad`. 
 
Key Bindings:
 - No key bindings by default

Example:
 
    { "keys": ["super+w", "d"], "command": "java_jad" },
    { "keys": ["super+w", "p"], "command": "java_javap" , "args" : {"new_view" : 1 }}



![Commands ](https://raw.github.com/vcharnahrebel/Main/master/img/sublime-jad-commands.png)
