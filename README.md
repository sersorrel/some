# some

More than less, but less than more.

some is a pager… sometimes. If the input is less than one screen long,
some will print it directly to the terminal; otherwise, it will use
whatever pager you have configured to display the input.

some currently only supports input from stdin, and will not open files
passed as arguments. If you want to page a file, most shells support the
following syntax:

```sh
some < file_to_page
```
