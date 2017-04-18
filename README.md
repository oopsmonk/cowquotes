# cowquotes
cowquotes is inspired by [cowsay](https://en.wikipedia.org/wiki/Cowsay) and [fortune](https://en.wikipedia.org/wiki/Fortune_\(Unix\))  

## cowquotes.py  

Get online quotes and show in the terminal.  

Requirement: 
`sudo -H pip install requests`  

Optional: 
`sudo apt install cowsay`  

Usage:  

1. Put in `~/.bashrc`  

```
$ echo "export COWSPATH='/path/to/cows/'" >> ~/.bashrc
$ echo "/path/to/cowquotes.py -f python" >> ~/.bashrc
```

2. Run in command line  

```
$ export COWSPATH="/path/to/cows/"
$ ./cowquotes.py -f worm
 ________________________________________________
/   Teach self-denial and make its practice      \
| pleasure, and you can create for the world a   |
| destiny more sublime that ever issued from the |
| brain of the wildest dreamer.                  |
|                                                |
\ << Sir Walter Scott >> from Forbes             /
 ------------------------------------------------
        \
         \
             -oo
              |"
              |
            --'

$ ./cowquotes.py -f ./cows/witch1.cow
 _________________________________________________
/ I am of the opinion that my life belongs to the \
| community, and as long as I live it is my       |
| privilege to do for it whatever I can.          |
|                                                 |
\ << Bernard Shaw >> from Forismatic              /
 -------------------------------------------------
       \           ___
        \         `'-.`'-.
                      )   `\
                     /      \   ^V^
                  __/________\__
        ^V^      '--/}}}}}}"}}--'
                   {{{{{{  aa\__
                   }}}}} ,___ __}
                  {{{{{\  \_//
                   }}}}//'--u
             _     .--'`U\
        ::::| \   (   _,\\\
        ::::|  |===\  \\=\))=======D
        ::::|_/     `> \\
                    /__//
                    Y\_\\_

$ ./cowquotes.py -f python
 _______________________________________________
/ Creativity comes from trust. Trust your       \
| instincts. And never hope more than you work. |
|                                               |
\ << Rita Mae Brown >> from Forismatic          /
 -----------------------------------------------
    \
     \      ---_ ......._-_--.
      \    (|\ /      / /| \  \
          /  /     .'  -=-'   `.
         /  /    .'             )
       _/  /   .'        _.)   /
      / o   o        _.-' /  .'
      \          _.-'    / .'*|
       \______.-'//    .'.' \*|
        \|  \ | //   .'.' _ |*|
         `   \|//  .'.'_ _ _|*|
          .  .// .'.' | _ _ \*|
          \`-|\_/ /    \ _ _ \*\
           `/'\__/      \ _ _ \*\
          /^|            \ _ _ \*
         '  `             \ _ _ \      ASH (+VK)
                           \_


$
```

3. Loop all cow files:  
`for i in $(./cowquotes.py -l); do ./cowquotes.py -f $i -m "$i"; done`  

## cowFactory.py  

Create a cow file from image. For help: `./cowFactory.py -h`  

Requirement: 
`sudo -H pip install pillow`  

Usage: 

```
$ ./cowFactory.py -r 5 -i -a raspberrypi -s 30 raspberry-pi-logo2.png > raspberry_logo.cow  
```

