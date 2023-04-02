# Test page with the code

Some kind of text. Add links <https://habr.com/> and [Habr](https://habr.com/).

## Subtitle

```python
x = input()
```

```python
y = input()
```

There's a comment here.

<details>
<summary>Summary</summary>

````md
```python
a = int(input())
k = 0
for i in range(1, a):
    if a % i == 0:
        print(i, end=" ")
        k += 1
print(a)
if k == 1:
    print("Prime")
else:
    print("No")
```
````

**Bold text.**

</details>

Text.

```
a = list("Example")
print(a)
for i in range(len(a)):
    if a[i] == "a":
        a[i] = "o"
print("".join(a))
```

Code:

    a = list("Example")
    print(a)
    for i in range(len(a)):
        if a[i] == "a":
            a[i] = "o"
    print("".join(a))

More code:

    a = list("Example")
    print(a)
    for i in range(len(a)):
        if a[i] == "a":
            a[i] = "o"
    print("".join(a))
