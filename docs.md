# Normal Brainfuck commands

| Instruction | Effect|
|-------------|---------------|
| > | Pointer right |
| < | Pointer left |
| + | Increment value |
| - | Decrement value |
| . | Output ascii |
| , | Input single ascii charachter |
| [ | Jump past the matching ] if the cell at the pointer is 0 |
| ] | Jump back to the matching [ if the cell at the pointer is nonzero |

# New commands in YABFD
| Instruction | Effect |
|-------------|--------|
| **Realms** |
| @ | Open portal to realm refrenced by current cell |
| \| | Puts the current realms ID into the current cell |
| _ | Runs the realm-specific function
| **If/If-Else** |
| { | opening bracket for if statment see [below](#if-block) about format (it is a little weird)
| } | close a if statment
| ( | opening parenthesis for Else block
| ) | closing parenthesis for Else block
| **Pointers** |
| * | save current location to pointer |
| % | copy current cell value to pointer |
| $ | write either link or value to current cell |
| ^ | unlink cell pointer |


# If block
After a If starting instruction `{`<br>
you need to have another symbol to define the condition
valid conditions are
| Symbol | Condition |
|--------|-----------|
| 0 | current cell value is =0
| @ | pointer is in the same Realm ID as defined by cell |
| * | cell is pointer to another cell |
| = | cell to the left is equal to this cell |
| < | cell to the left is less then this cell |
| > | cell to the left is greater then this cell |

# ~~Notable~~ Cursed Features
The If/If-Else block which is more than one character opening<br>
Pointers redirect all actions taken on them to where they point to<br>
Whenever jumping realms you will always be at cell 0 regardless of where you were<br>
The \$ command doing different things based on the pointer value<br>
The pointer starts with a value of 0<br>
Pointer Notation is $\<realm>:\<cell> so a pointer to realm 1 cell 6 would be written as 1:6<br>
Cells when unlinked copy the value of the target cell<br>
When unlinking cells they copy the value from their linked cell before unlinking<br>
Limited sized realms (TODO: allow overriding of `>` and `<` commands like done with `,` and `.`)<br>