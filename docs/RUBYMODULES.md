# Creating Rubymodules

### Introduction

You can create ruby modules by adding your scripts to the ruby_modules folder. There they get automatically loaded as a command. The command will hold the name of the file! 

The communication between ruby and beastbot happens with piping. But you don't have to dive into how beastbot interprets your data. The "beastbot" gem will handle that


First you will have to install the gem. You can install the beastbot gem by typing:

```
gem install beastbot
```

### Lets code!

The gem is very tiny and has just 3 functions for now. 

If your script needs to have arguments you can pass them to ruby and catch them with

```
Beastbot::Interpret::get_arguments
```

This works the same as piping. Only if no argument is given it will return **nil**.

To send info to irc use:

For sending to the channel where command is executed

```
Beastbot::Talk::send_to_channel
```

For sending to the user who invoked the command

```
Beastbot::Talk::send_to_user
```

