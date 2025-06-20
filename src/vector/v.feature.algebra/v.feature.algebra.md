---
name: v.feature.algebra
description: A vector calculator program
---

# A vector calculator program

## DESCRIPTION

*v.feature.algebra* is a vector calculator program inspired by
r.mapcalc.

## NOTES

It's much more complicated to deal with vector maps than with raster
maps. Particularly, there are several levels on which we might want to
deal with a vector map. For this reason the design of v.feature.algebra
is that of a skeleton with plugins: A parser will interpret statements
and call the appropriate functions it finds in dynamically loaded
plugins.

The syntax should be able to deal with four different types: - numbers -
points - point lists - maps

Numeric expressions should do what everybody would expect. There are
some dozens of built in functions from the math library. Points and
point lists are meant in the mathematical sense: A point is a set of two
or three numbers, representing the coordinate. All points have three
components, but the third, if missing has the value of 0.0/0.0 (NaN). An
expression will yield a 3D result if all arguments a 3D. There is a set
of basic built in operations like dot and cross product. Point lists are
meant for polygons, lines, areas, etc. Points and point lists have no
categories or attributes. And finally, of course, v.feature.algebra
deals with map expressions.

For numbers, the infix operators do the obvious. For other types, the
parser will translate them to function calls with predefined names. Some
samples are set and can be replaced by something useful.

The plugins are designed to be as simple as possible. There is one
example which actually doesn't do anything but shows how it can be
called. Such a plugin needs three global functions: One which can be
called to find out the name the user must type to use the function, one
which returns a string denoting the return type and the type and number
of arguments, and finally the function itself.

There are two more types which are somewhat special: One is type
\`argument' which can be any of the basic types. The parser will accept
anything to be the argument to a function call, but the mechanism to
actually call that function will check if the types match the prototype.
The second special type \`any' is sort of a backdoor: If something new
comes up, it can be treated as type any, and it will be responsibility
of the plugin to verify that it's the correct type. One case where the
any-type can be useful is for SQL statement-pieces or other constructs
when dealing with attributes, which can be literally of "any" type.

There is one problem with this approach within v.feature.algebra, which
is calling a function with a variable list of arguments. This is a bit
complicated, and before thinking of easy solutions, I need to recommend
reading the code. Just before calling it, v.feature.algebra has a
pointer to that functions and a linked list of structures which hold the
argument types and values. It would be nice to be able to construct such
a call argument by argument, but there is no portable way to do so:
First assembly would be needed, and second, the way a stack frame is
built for a particular compiler/architecture can vary. The solution is
to maintain a list of typedef'd prototypes and call them in a switch.
This means, if someone needs a new function and writes a plugin, either
he finds a typedef which matches this prototype, or he needs to add the
typedef and a case in the switch.

It makes only limited sense to mix arguments of different types: three
at the power of map-A doesn't seem to be useful. So, the basic strategy
is accept expressions only of the same type, while mixing types is
always possible within the arguments to a function call.

There is a file listing some example expressions. I hope that it is what
one could expect. Adding a few plugins should allow for very complex
expressions and operations.

## EXAMPLES

This is an empty statement, which is legal

```text
;
```

Some built in constants:

```text
12;
e;
pi;
pnt_o;
pnt_i;
pnt_j;
pnt_k;
rivers;
```

The last one isn't really a constant, as it depends on what if found at
startup, but it behaves just the like.

```text
a;
```

This gives an error. "a", which is (not yet) defined, is handled as a
string. There is no operation associated, so this gives a parse error.

Next some simple assignments. Also here, the name of the variable is
initially not more than a string, but after performing the assignment,
they take the type of the expressionL:

```text
num = 10.3;
pnt = (0,0);
map = rivers;
any = mkstring (hallo);
```

The last is only a backdoor for cases when exceptional things are
needed. The function mkstring is a sample implementation of type ANY.
For now, only one word could be passed, but when flex is being used a
quoted string might contain just anything.

Next, I overwrite these variables. This is somewhat tricky. If you say
"map = rivers", what should happen? In theory, we should actually
duplicate this map, which could imply gigabytes on disk. This is not
done, but if the map is changed, it must not change the former \`value'.
I hope it's doing now, what everybody would expect (including to free
eventually the allocated memory).

```text
num = 3.1;
pnt = (1,1);
map = cities;
any = mkstring (hello);
```

The pure numeric operations aren't new, beside that I'm trying to catch
illegal operations:

```text
sqrt(e);
num = cos (pi/4);
num = -num + 3 * num - sqrt (num^2);
3.3 + 4.4;
2.2 - 1.1;
5 * 7;
21 / 0;
21 / 2;
-21 / 7;
-6.6 ^ 1.2;
6.6 ^ 1.2;
12.5 % 3.6;
2 * (3.1 + 0.9);
```

Next are points. Note that 2D and 3D are dealt with identically; in case
of 2D, the z-value is 0.0/0.0 (NaN, "Not a Number"). This should be
pretty portable. Generally, if at least one point is 2D, the result of a
point operation will be 2D even if 3D points are involved too, ignoring
the third dimension. I've defined some infix operations a bit
arbitrarily. Of course, this could be changed. The double () in case of
a single function argument are surely ugly, but not avoidable.

```text
origin2d = (0,0);
p1 = (1,1);
p2 = p1;
p2 = v_copy (p1);
v_add ((1,0), (0,1));
(1,0) + (0,1);
v_sub ((1,1), (0,1));
(1,1) - (0,1);
v_abs ((-2, -1));
v_neg ((2, 1));
-(2,1);
v_mul ((2,4), 3.3);
(2,4) * 3.3;
3.3 * (2,4);
v_div ((6.6, 13.2), 3.3);
(6.6, 13.2) / 3.3;
v_unit ((12, 8));
v_cross ((1,2), (4,5));
v_cross ((1,2,3), (4,5,6));
(1,2,3) ^ (4,5,6);
v_val ((3,3));
v_dot ((1,2), (3,4));
(1,2) % (3,4);
v_dot ((1,2,3), (4,5,6));
(1,2,3) % (4,5,6);
v_area ((1,2,3), (4,5,6));
v_eq ((1,2), (1, 2));
v_eq ((1,2), (1.0001, 2.0001));
epsilon = (1e-3, 1e-3);
v_eq_epsilon ((1,2), (1.0001, 2.0001), epsilon);
v_isortho ((0,1), (1,0));
v_ispara ((0, 1), (0, -1));
v_isacute ((0, 1), (0, 0.5));
3 * (pnt + (2,2));
```

This is planned, but doesn't work yet:

```sh
         line = ((1,1), (2,1));
         triangle = (line, (1.5, 2));
```

And finally the map operations, which also aren't new, beside some
internal details (freeing memory, not duplicating, etc.). I think that
there is no map-operation which makes sense if it is not assigned to a
variable. So all map expressions need to follow a variable and an equal
sign. The very first expression, hence, will give an error:

```text
rivers + cities;
map = rivers;
map;
map = rivers + cities;
map = testmap (rivers);
map = test2map (rivers, cities);
map = dltest (rivers, cities);
```

## TODO

\- The lexical scanner. At this point, there is a very simple and
limited scanner. My plan was to provide 4 methods of input: + from the
command line + from stdin, interactively, using GNU readline and history

+ from stdin by IO redirection like in "script | v.feature.algebra" +
from a file, like in "v.feature.algebra -i statementfile" Of course,
this should be done with Flex, with the input selection as needed for
all methods, as well as support for Bison to indicate the position of a
parse error. - There should be several built in commands allowing to: +
include a file with statements + document the meaning of a variable or
function + attaching documentation to a variable or function + saving
certain things in a readable script like documentation or constant
values. + a command to terminate the program (right now, only with
Ctrl-D) - There is not yet any support for loops and conditionals. These
do not seem to be of much use with maps, but can prove powerful on
points and point lists. - There are certain operations which need to be
performed always, like opening a map. For now, they need to be done in
the plugin, but should definitively move to v.feature.algebra. - Point
lists are not working yet, though much of the basic infrastructure is
already done. - There seems to be a bug in memory management which can
cause the program to crash. Probably there are many more than that.

## SEE ALSO

*[r.mapcalc](https://grass.osgeo.org/grass-stable/manuals/r.mapcalc.html)*

## AUTHOR

Christoph Simon \<ciccio at kiosknet com.br\>
