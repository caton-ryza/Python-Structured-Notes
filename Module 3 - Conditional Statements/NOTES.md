
# Python Conditional Statements

## Introduction

Conditional statements are used in Python to make decisions based on whether a specific condition is true or false.

They allow a program to execute different blocks of code depending on the situation. Conditional statements are important because they help programs respond to user input, compare values, and perform different actions.

Python has three main conditional statements:

1. `if` statement
2. `if-else` statement
3. `if-elif-else` statement

---

# 1. If Statement

## Overview

The `if` statement executes a block of code only when a given condition is true.

If the condition is false, the code inside the `if` block is skipped.

## Syntax

```python
if condition:
    # code to execute if condition is true
```

## Example

```python
age = 18

if age >= 18:
    print("You are an adult.")
```

**Output:**
```text
You are an adult.
```

**Explanation:**

The program checks whether the value of `age` is greater than or equal to 18.

Since the condition is true, the message is displayed.

**Purpose:** Used when a program needs to perform an action only when a specific condition is met.

---

# 2. If-Else Statement

## Overview

The `if-else` statement allows a program to choose between two possible actions.

The `if` block executes when the condition is true, while the `else` block executes when the condition is false.

## Syntax

```python
if condition:
    # code if condition is true
else:
    # code if condition is false
```

## Example

```python
number = 7

if number % 2 == 0:
    print("Even number")
else:
    print("Odd number")
```

**Output:**
```text
Odd number
```

**Explanation:**

The program checks whether the number is divisible by 2.

- `%` is the modulo operator, which returns the remainder.
- If the remainder is 0, the number is even.
- Otherwise, the number is odd.

Since 7 is not divisible by 2 without a remainder, the program displays "Odd number."

**Purpose:** Used when a program needs to choose between two different outcomes.

---

# 3. If-Elif-Else Statement

## Overview

The `if-elif-else` statement is used when a program needs to check multiple conditions.

- `if` checks the first condition.
- `elif` checks another condition if the previous one was false.
- `else` executes when none of the conditions are true.

Python checks the conditions from top to bottom and executes the first matching block.

## Syntax

```python
if condition1:
    # code if condition1 is true
elif condition2:
    # code if condition2 is true
else:
    # code if all conditions are false
```

## Example

```python
grade = 85

if grade >= 90:
    print("Excellent")
elif grade >= 80:
    print("Very Good")
elif grade >= 75:
    print("Passed")
else:
    print("Failed")
```

**Output:**
```text
Very Good
```

**Explanation:**

The program checks the student's grade against several conditions.

- If the grade is 90 or higher, it displays "Excellent."
- If the first condition is false but the grade is 80 or higher, it displays "Very Good."
- If the grade is 75 or higher, it displays "Passed."
- If none of the conditions are met, it displays "Failed."

Since the grade is 85, the second condition is true.

**Purpose:** Used when a program needs to choose from multiple possible outcomes.

---

# 4. Nested If Statements

## Overview

A nested `if` statement is an `if` statement placed inside another `if` statement.

It allows a program to check an additional condition only after an earlier condition has been satisfied.

## Example

```python
age = 20
has_id = True

if age >= 18:
    if has_id:
        print("Entry allowed.")
    else:
        print("Please present your ID.")
else:
    print("Entry not allowed.")
```

**Output:**
```text
Entry allowed.
```

**Explanation:**

The program first checks whether the person is at least 18 years old.

If the condition is true, it checks whether the person has an ID.

Since both conditions are satisfied, the program displays "Entry allowed."

**Purpose:** Useful when a decision depends on more than one condition.

---

# 5. Comparison and Logical Operators

Conditional statements commonly use comparison and logical operators to evaluate conditions.

## A. Comparison Operators

Comparison operators are used to compare two values. They return either `True` or `False`.

| Operator | Meaning | Example |
|---|---|---|
| `==` | Equal to | `5 == 5` |
| `!=` | Not equal to | `5 != 3` |
| `>` | Greater than | `8 > 4` |
| `<` | Less than | `3 < 7` |
| `>=` | Greater than or equal to | `5 >= 5` |
| `<=` | Less than or equal to | `4 <= 6` |

## B. Logical Operators

Logical operators are used to combine or reverse conditions.

| Operator | Meaning |
|---|---|
| `and` | True when both conditions are true. |
| `or` | True when at least one condition is true. |
| `not` | Reverses the result of a condition. |

## Example

```python
age = 19
has_id = True

if age >= 18 and has_id:
    print("Access granted.")
else:
    print("Access denied.")
```

**Output:**
```text
Access granted.
```

**Explanation:**

The `and` operator requires both conditions to be true.

Since the age is at least 18 and `has_id` is true, the program displays "Access granted."

---

# 6. Practical Applications of Conditional Statements

Conditional statements are used in many types of programs.

| Application | How It Uses Conditional Statements |
|---|---|
| Login Systems | Checks whether entered information is correct. |
| Grading Systems | Determines grades based on scores. |
| Games | Checks whether a player wins or loses. |
| Alarm Applications | Checks whether the current time matches a scheduled alarm. |
| Shopping Applications | Checks prices, discounts, and payment conditions. |

---

# 7. Advantages and Disadvantages

## Advantages

- Allows programs to make decisions.
- Makes applications more interactive.
- Helps validate user input.
- Supports different outcomes based on conditions.
- Makes program behavior more flexible.

## Disadvantages

- Too many conditions can make code difficult to understand.
- Incorrect logical expressions may produce unexpected results.
- Deeply nested conditions can make programs harder to maintain.

---

# Conclusion

Conditional statements are an essential part of Python programming because they allow programs to make decisions and respond to different situations.

By using `if`, `if-else`, `if-elif-else`, and nested `if` statements, programmers can control how their applications behave depending on specific conditions.

Understanding conditional statements helps in developing programs that are more interactive, logical, and responsive.
