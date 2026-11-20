
# Python Match-Case Statements

## Introduction

The `match-case` statement is a control flow structure introduced in Python 3.10. It allows a program to compare a value against multiple possible patterns and execute the code associated with the matching pattern.

It is useful when a program needs to handle several possible choices or situations. It can also make code easier to read compared to using many `if-elif-else` statements.

The `match-case` statement is also known as structural pattern matching.

---

# 1. Understanding Match-Case

## Syntax

```python
match variable:
    case value1:
        # code if value matches value1
    case value2:
        # code if value matches value2
    case _:
        # code if no other case matches
```

### Explanation

- `match` specifies the value that the program will check.
- `case` defines a possible pattern to compare against.
- Each case contains instructions that execute when a matching pattern is found.
- `_` is a wildcard pattern that matches anything. It is commonly used as the default case.

Python checks the cases in order and executes the first matching case.

## Example

```python
day = 2

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case _:
        print("Invalid day")
```

**Output:**
```text
Tuesday
```

**Explanation:**

The program checks the value of `day`. Since its value is 2, the second case matches and displays "Tuesday."

---

# 2. Practical Match-Case Examples

## Example 1: Simple Calculator

A match-case statement can be used to select which mathematical operation a calculator should perform.

```python
operator = "+"

num1 = 10
num2 = 5

match operator:
    case "+":
        print(num1 + num2)
    case "-":
        print(num1 - num2)
    case "*":
        print(num1 * num2)
    case "/":
        print(num1 / num2)
    case _:
        print("Invalid operator")
```

**Output:**
```text
15
```

**Explanation:**

The program checks the value of `operator` to determine which mathematical operation to perform.

- `"+"` performs addition.
- `"-"` performs subtraction.
- `"*"` performs multiplication.
- `"/"` performs division.
- `_` handles operators that do not match any of the listed cases.

Since the operator is `+`, the program adds 10 and 5.

**Purpose:** Useful for programs that need to select between multiple operations.

## Example 2: Menu Selection

Match-case can be used to handle choices in a menu system.

```python
choice = 2

match choice:
    case 1:
        print("View Profile")
    case 2:
        print("Open Settings")
    case 3:
        print("Log Out")
    case _:
        print("Invalid choice")
```

**Output:**
```text
Open Settings
```

**Explanation:**

The program checks the user's selected menu option.

- `case 1` displays the profile option.
- `case 2` displays the settings option.
- `case 3` displays the logout option.
- `case _` handles invalid selections.

Since the selected choice is 2, the program displays "Open Settings."

**Purpose:** Useful for applications with menus and navigation options.

## Example 3: Checking Traffic Light Signals

Match-case can also be used to determine actions based on different conditions or signals.

```python
light = "yellow"

match light:
    case "red":
        print("Stop")
    case "yellow":
        print("Prepare to stop")
    case "green":
        print("Go")
    case _:
        print("Invalid traffic light")
```

**Output:**
```text
Prepare to stop
```

**Explanation:**

The program checks the value of `light` and displays the corresponding instruction.

- `"red"` displays "Stop."
- `"yellow"` displays "Prepare to stop."
- `"green"` displays "Go."
- `_` handles unrecognized values.

Since the light is yellow, the program displays "Prepare to stop."

**Purpose:** Useful when a program needs to respond to different predefined values.

---

# 3. Using Multiple Values in One Case

A match-case statement can match multiple possible values in a single case by using the `|` operator.

## Example

```python
day = "Saturday"

match day:
    case "Saturday" | "Sunday":
        print("Weekend")
    case "Monday" | "Tuesday" | "Wednesday" | "Thursday" | "Friday":
        print("Weekday")
    case _:
        print("Invalid day")
```

**Output:**
```text
Weekend
```

**Explanation:**

The `|` operator allows a single case to match more than one value.

In this example, both Saturday and Sunday belong to the weekend case. The program displays "Weekend" because the value of `day` is Saturday.

---

# 4. Using Conditions with Match-Case

Match-case supports additional conditions through the `if` keyword, which is called a guard.

A guard adds another condition that must be true before the case can execute.

## Example

```python
number = 15

match number:
    case n if n > 0:
        print("Positive number")
    case n if n < 0:
        print("Negative number")
    case _:
        print("Zero")
```

**Output:**
```text
Positive number
```

**Explanation:**

- `case n if n > 0` matches a value and checks whether it is greater than zero.
- `case n if n < 0` checks whether it is less than zero.
- `case _` handles the remaining value.

Since 15 is greater than zero, the program displays "Positive number."

---

# 5. Match-Case vs. If-Elif-Else

Both match-case and if-elif-else can be used to make decisions in Python. However, they have different uses.

| Feature | If-Elif-Else | Match-Case |
|---|---|---|
| Main Purpose | Checks conditions | Matches values and patterns |
| Syntax | Uses `if`, `elif`, and `else` | Uses `match` and `case` |
| Multiple Choices | Supports multiple conditions | Supports multiple patterns |
| Complex Patterns | Usually requires additional conditions | Supports structural pattern matching |
| Python Version | Available in older Python versions | Introduced in Python 3.10 |

### When to Use Each

- Use `if-elif-else` when checking ranges, comparisons, or general conditions.
- Use `match-case` when comparing a value against several specific patterns or choices.

---

# 6. Advantages and Disadvantages

## Advantages

- Makes multiple-choice logic easier to organize.
- Improves code readability when checking many possible values.
- Supports multiple patterns in one case.
- Includes a wildcard case for handling unmatched values.
- Can work with more advanced structural patterns.

## Disadvantages

- Requires Python 3.10 or newer.
- May be unnecessary for simple conditions.
- Can become complicated when using advanced patterns.
- Is not always the best replacement for `if-elif-else`.

---

# 7. Practical Applications of Match-Case

Match-case statements are useful in different types of programs.

| Application | How It Uses Match-Case |
|---|---|
| Calculator | Selects mathematical operations. |
| Menu Systems | Handles user selections. |
| Games | Checks player actions or game states. |
| Applications | Handles navigation options. |
| Information Systems | Categorizes data based on matching values. |

---

# Conclusion

The `match-case` statement is a useful feature in Python that allows programs to compare values against different patterns and execute the corresponding instructions.

It makes multiple-choice decision structures easier to organize and understand. By using `match`, `case`, wildcard patterns, and guards, programmers can create applications that respond to different values and situations.

Understanding match-case statements helps programmers write cleaner and more organized code, especially when handling multiple possible choices.
