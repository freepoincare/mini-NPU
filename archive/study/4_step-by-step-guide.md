Absolutely — I cleaned up the formatting, fixed the Markdown syntax, and structured it as a proper `README.md`-style document.

# Mini NPU Simulator — Step-by-Step Development Guide

## 1. Project Goal

The goal is to create a Python console application that can:

* Accept two 3×3 filters and one 3×3 pattern from the user.
* Calculate MAC scores between the pattern and each filter.
* Determine whether the pattern is **Cross**, **X**, or **UNDECIDED**.
* Load larger test cases from `data.json`.
* Validate the JSON data.
* Normalize different label formats such as `+` and `x`.
* Compare the calculated result with the expected result.
* Measure MAC execution time for 3×3, 5×5, 13×13, and 25×25.
* Print a final PASS/FAIL report.
* Explain the implementation and performance in `README.md`.

---

## 2. Recommended Project Structure

Keep the project simple:

```text
mini-npu/
│
├── main.py
├── data.json
└── README.md
```

You only need these three files for the basic assignment.

### `main.py`

Contains the Python implementation.

### `data.json`

Contains the filters and test patterns supplied by the assignment.

### `README.md`

Contains:

* How to run the program
* How MAC works
* Label normalization
* Epsilon comparison
* Performance results
* Failure analysis
* Time complexity

---

# 3. Understand MAC First

This is the most important concept in the assignment.

Suppose we have:

### Pattern

```text
0 1 0
1 1 1
0 1 0
```

### Cross Filter

```text
0 1 0
1 1 1
0 1 0
```

Multiply corresponding elements:

```text
0×0   1×1   0×0
1×1   1×1   1×1
0×0   1×1   0×0
```

Then add everything:

```text
0 + 1 + 0
1 + 1 + 1
0 + 1 + 0
```

```text
= 5
```

Therefore:

```text
MAC(pattern, filter) = 5
```

The Python implementation is simply:

```python
score = 0

for i in range(n):
    for j in range(n):
        score += pattern[i][j] * filter_matrix[i][j]
```

This is the heart of the entire project.

---

# 4. Why Is This Related to an NPU?

An NPU is designed to perform enormous numbers of mathematical operations efficiently.

A simplified view is:

```text
Input
  ↓
Matrix / Tensor
  ↓
Multiply
  ↓
Accumulate
  ↓
Result
```

Your simulator does:

```text
Pattern × Filter
       ↓
      MAC
       ↓
     Score
```

A real NPU performs this kind of operation many millions or billions of times, often in parallel.

Your project deliberately uses normal Python loops so that you can understand the underlying computation.

---

# 5. Step 1 — Create the MAC Function

Start with the simplest function:

```python
def mac(pattern, filter_matrix):
    n = len(pattern)
    score = 0.0

    for i in range(n):
        for j in range(n):
            score += pattern[i][j] * filter_matrix[i][j]

    return score
```

### What happens here?

If:

```python
pattern = [
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
]
```

then:

```python
mac(pattern, pattern)
```

returns:

```text
5.0
```

---

# 6. Step 2 — Validate Matrix Size

You need to make sure that the pattern and filter have the same dimensions.

Create:

```python
def validate_matrix(matrix, n):
    if len(matrix) != n:
        return False

    for row in matrix:
        if len(row) != n:
            return False

    return True
```

For example:

```python
matrix = [
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
]

print(validate_matrix(matrix, 3))
```

Result:

```text
True
```

But:

```python
matrix = [
    [1, 0, 1],
    [0, 1],
]
```

should return:

```text
False
```

This is important because the assignment explicitly says that a size mismatch must not crash the entire program.

---

# 7. Step 3 — Implement 3×3 User Input

The user needs to enter matrices one row at a time.

For example:

```text
0 1 0
1 1 1
0 1 0
```

A useful function is:

```python
def input_matrix(n, name):
    while True:
        print(f"{name} ({n}x{n})")

        matrix = []

        try:
            for i in range(n):
                values = input(f"Row {i + 1}: ").split()

                if len(values) != n:
                    raise ValueError

                row = [float(value) for value in values]
                matrix.append(row)

            return matrix

        except ValueError:
            print(
                f"입력 형식 오류: 각 줄에 {n}개의 숫자를 "
                "공백으로 구분해 입력하세요."
            )
```

The important part is:

```python
.split()
```

For:

```text
1 0 1
```

you get:

```python
["1", "0", "1"]
```

Then:

```python
float(value)
```

converts them into numbers.

---

# 8. Step 4 — Create the Label Normalization Function

This is one of the most important requirements.

The JSON may use:

```text
+
x
cross
```

but your program should internally use only:

```text
Cross
X
```

Create one function responsible for this:

```python
def normalize_label(label):
    label = str(label).strip().lower()

    if label in ["+", "cross"]:
        return "Cross"

    if label in ["x"]:
        return "X"

    return None
```

Now:

```python
normalize_label("+")
```

returns:

```text
Cross
```

And:

```python
normalize_label("cross")
```

also returns:

```text
Cross
```

while:

```python
normalize_label("x")
```

returns:

```text
X
```

### Why is this necessary?

Without normalization, your program might compare:

```text
+
```

with:

```text
Cross
```

and incorrectly decide:

```text
FAIL
```

even though they mean exactly the same thing.

Therefore, normalize before comparison.

---

# 9. Step 5 — Understand the JSON Structure

Your `data.json` is expected to contain something conceptually like:

```json
{
  "filters": {
    "size_5": {
      "cross": [
        [0, 1, 0, 1, 0]
      ],
      "x": [
        [1, 0, 1, 0, 1]
      ]
    }
  },
  "patterns": {
    "size_5_1": {
      "input": [
        [0, 1, 0, 1, 0]
      ],
      "expected": "+"
    }
  }
}
```

The exact data should follow the provided assignment file.

Load it using only Python's standard library:

```python
import json

with open("data.json", "r", encoding="utf-8") as file:
    data = json.load(file)
```

No NumPy is required.

---

# 10. Step 6 — Extract N From the Pattern Key

The pattern key looks like:

```text
size_5_1
size_13_1
size_25_3
```

The important part is the `N`.

You can do:

```python
def extract_size(key):
    parts = key.split("_")

    if len(parts) < 2:
        return None

    try:
        return int(parts[1])
    except ValueError:
        return None
```

For:

```python
extract_size("size_13_1")
```

you get:

```text
13
```

Then you can select:

```python
filters["size_13"]
```

---

# 11. Step 7 — Load the Filters

Create a function such as:

```python
def load_filters(data):
    filters = {}

    for size_key, filter_data in data["filters"].items():
        normalized = {}

        for label, matrix in filter_data.items():
            standard_label = normalize_label(label)

            if standard_label is not None:
                normalized[standard_label] = matrix

        filters[size_key] = normalized

    return filters
```

Now instead of worrying about whether the JSON uses:

```text
cross
```

or:

```text
+
```

your program internally works with:

```python
{
    "Cross": ...,
    "X": ...
}
```

This makes the rest of the program much easier.

---

# 12. Step 8 — Validate JSON Cases

For every pattern:

```text
size_5_1
size_5_2
size_13_1
...
```

you should:

1. Extract `N`.
2. Find `size_N` filters.
3. Load the pattern.
4. Check the pattern size.
5. Check Cross filter size.
6. Check X filter size.
7. If something is wrong → mark the case as `FAIL`.
8. Otherwise → perform MAC.

Conceptually:

```text
size_13_1
    ↓
Extract N = 13
    ↓
Find filters["size_13"]
    ↓
Load pattern
    ↓
Validate sizes
    ↓
MAC Cross
    ↓
MAC X
    ↓
Compare scores
    ↓
Cross / X / UNDECIDED
    ↓
Compare with expected
    ↓
PASS / FAIL
```

---

# 13. Step 9 — Implement Epsilon Comparison

This is another important part of the assignment.

Floating-point numbers can have tiny differences.

For example, mathematically:

```text
0.9 = 0.9
```

but internally Python might have values such as:

```text
0.9000000000000000
0.8999999999999999
```

Therefore, don't simply do:

```python
score_a == score_b
```

Instead:

```python
EPSILON = 1e-9
```

Then:

```python
if abs(score_a - score_b) < EPSILON:
    # tie
```

Create:

```python
def decide(score_cross, score_x):
    if abs(score_cross - score_x) < EPSILON:
        return "UNDECIDED"

    if score_cross > score_x:
        return "Cross"

    return "X"
```

This gives you:

```text
Cross > X    → Cross
X > Cross    → X
Almost equal → UNDECIDED
```

---

# 14. Step 10 — Calculate PASS / FAIL

Once you have:

```python
result = decide(cross_score, x_score)
```

normalize the expected label:

```python
expected = normalize_label(case["expected"])
```

Then:

```python
if result == expected:
    status = "PASS"
else:
    status = "FAIL"
```

For example:

```text
Cross score: 5.0
X score:     1.0

Result:   Cross
Expected: Cross

PASS
```

But:

```text
Cross score: 0.9
X score:     0.9

Result:   UNDECIDED
Expected: X

FAIL
```

This is exactly the kind of situation the assignment wants you to analyze.

---

# 15. Step 11 — Measure MAC Performance

Use Python's standard `time` module:

```python
import time
```

You should measure only the MAC function, not:

* `input()`
* `print()`
* JSON loading
* File reading

Use:

```python
start = time.perf_counter()

mac(pattern, filter_matrix)

end = time.perf_counter()

elapsed = end - start
```

Convert seconds to milliseconds:

```python
elapsed_ms = elapsed * 1000
```

---

# 16. Step 12 — Repeat the Measurement 10 Times

The assignment requires at least 10 repetitions.

Create:

```python
def benchmark(pattern, filter_matrix, repeat=10):
    times = []

    for _ in range(repeat):
        start = time.perf_counter()

        mac(pattern, filter_matrix)

        end = time.perf_counter()

        times.append((end - start) * 1000)

    average = sum(times) / len(times)

    return average
```

Then:

```python
average = benchmark(pattern, filter_matrix)
```

You can print:

```text
Average: 0.012 ms
```

---

# 17. Step 13 — Performance Test Sizes

You need to test:

* 3×3
* 5×5
* 13×13
* 25×25

The number of MAC operations is:

```text
N × N = N²
```

Therefore:

| Size  | MAC Operations |
| ----- | -------------: |
| 3×3   |              9 |
| 5×5   |             25 |
| 13×13 |            169 |
| 25×25 |            625 |

You can calculate it in Python:

```python
operation_count = n * n
```

---

# 18. Step 14 — Why Is the Complexity O(N²)?

Your MAC function has:

```python
for i in range(n):
    for j in range(n):
```

The outer loop runs:

```text
N
```

times.

The inner loop also runs:

```text
N
```

times for every outer iteration.

Therefore:

```text
N × N = N²
```

operations.

So the time complexity is:

```text
O(N²)
```

For example:

```text
3×3    → 9
5×5    → 25
13×13  → 169
25×25  → 625
```

Notice that increasing `N` has a quadratic effect.

---

# 19. Step 15 — Build Mode 1

Your program should start with:

```text
=== Mini NPU Simulator ===

[모드 선택]

1. 사용자 입력 (3x3)
2. data.json 분석

선택:
```

If the user chooses:

```text
1
```

the flow should be:

```text
Select Mode 1
    ↓
Input Filter A
    ↓
Input Filter B
    ↓
Input Pattern
    ↓
Calculate A MAC
    ↓
Calculate B MAC
    ↓
Decide A/B/UNDECIDED
    ↓
Measure 3×3 performance
    ↓
Print result
```

---

# 20. Step 16 — Build Mode 2

If the user chooses:

```text
2
```

the flow should be:

```text
Load data.json
    ↓
Validate JSON
    ↓
Load filters
    ↓
Normalize filter labels
    ↓
Read each pattern
    ↓
Extract N
    ↓
Find size_N filters
    ↓
Validate dimensions
    ↓
Normalize expected label
    ↓
MAC Cross
    ↓
MAC X
    ↓
Decide result
    ↓
PASS / FAIL
    ↓
Performance test
    ↓
Final summary
```

---

# 21. Step 17 — Keep Failed Cases Instead of Crashing

This requirement is important.

### Bad implementation

```python
if wrong_size:
    raise Exception("Invalid size")
```

That could terminate the entire application.

### Better implementation

```python
failures.append({
    "case": case_id,
    "reason": "Pattern size does not match filter size"
})
```

Then continue processing the next case.

For example:

```text
size_5_1  → PASS
size_5_2  → PASS
size_13_1 → FAIL
size_13_2 → PASS
size_25_1 → PASS
```

The program should continue all the way to the end.

---

# 22. Step 18 — Track the Final Statistics

Maintain:

```python
total = 0
passed = 0
failed = 0
failures = []
```

For each test:

```python
total += 1
```

If successful:

```python
passed += 1
```

Otherwise:

```python
failed += 1
failures.append(...)
```

At the end:

```text
#---------------------------------------
# [4] 결과 요약
#---------------------------------------

총 테스트: 8개
통과: 7개
실패: 1개

실패 케이스:

- size_13_1: 동점(UNDECIDED) 처리 규칙에 따라 FAIL
```

---

# 23. Recommended Functions

I strongly recommend organizing `main.py` into functions rather than putting everything inside one huge `main()`.

A good structure is:

```python
import json
import time

EPSILON = 1e-9
REPEAT = 10


def normalize_label(label):
    ...


def validate_matrix(matrix, n):
    ...


def input_matrix(n, name):
    ...


def mac(pattern, filter_matrix):
    ...


def decide(score_cross, score_x):
    ...


def extract_size(key):
    ...


def benchmark(pattern, filter_matrix, repeat=10):
    ...


def load_json(filename):
    ...


def run_user_mode():
    ...


def run_json_mode():
    ...


def run_performance_analysis():
    ...


def main():
    ...


if __name__ == "__main__":
    main()
```

This structure is much easier to explain in your README and much easier to debug.

---

# 24. Recommended `main()` Flow

Your final `main()` can conceptually look like this:

```python
def main():
    print("=== Mini NPU Simulator ===")

    print()
    print("[모드 선택]")
    print("1. 사용자 입력 (3x3)")
    print("2. data.json 분석")

    choice = input("선택: ").strip()

    if choice == "1":
        run_user_mode()

    elif choice == "2":
        run_json_mode()

    else:
        print("잘못된 선택입니다.")
```

---

# 25. Important Design Decision: Don't Mix Responsibilities

Try to keep each function responsible for one thing.

For example:

### `mac()`

Only calculates MAC.

```text
Pattern + Filter
       ↓
     Score
```

### `decide()`

Only compares scores.

```text
Cross score + X score
          ↓
Cross / X / UNDECIDED
```

### `normalize_label()`

Only converts labels.

```text
+      → Cross
cross  → Cross
x      → X
```

### `benchmark()`

Only measures execution time.

This separation makes debugging much easier.

---

# 26. A Good Error-Handling Strategy

You have three major categories of possible failures.

## A. Data / Schema Problem

Example:

```text
size_13_1
```

contains a 12×12 pattern.

Report:

```text
FAIL
Reason: Pattern size mismatch
```

## B. Logic Problem

Example:

```text
Cross score = 10
X score     = 4
```

but your program outputs:

```text
X
```

This suggests your decision logic is wrong.

## C. Numerical Comparison Problem

Example:

```text
Cross = 0.9000000000000000
X     = 0.8999999999999999
```

The raw values are technically different, but the difference is tiny.

With:

```python
EPSILON = 1e-9
```

you treat them as a tie:

```text
UNDECIDED
```

This is a numerical comparison policy, not necessarily a MAC calculation bug.

This distinction is important for your README.

---

# 27. One Important Point About the Assignment Example

There is a subtle thing you should be careful about.

The assignment sometimes describes filters using labels such as:

```text
Cross
X
```

but the actual JSON may use:

```text
cross
x
```

and expected labels may use:

```text
+
x
```

Therefore, do not scatter label conversion throughout your code.

Avoid doing things like:

```python
if label == "+":
    ...
elif label == "cross":
    ...
elif label == "x":
    ...
```

in many different places.

Instead, always use:

```python
normalize_label(label)
```

This gives you one source of truth.

---

# 28. Another Important Point: Don't Hard-Code the Matrix Size

Avoid:

```python
for i in range(3):
    for j in range(3):
```

inside `mac()`.

Instead:

```python
n = len(pattern)

for i in range(n):
    for j in range(n):
```

Then the exact same function works for:

* 3×3
* 5×5
* 13×13
* 25×25

This is one of the main ideas of the assignment.

---

# 29. How to Test Mode 1

First test the simplest possible case.

### Cross filter

```text
0 1 0
1 1 1
0 1 0
```

### X filter

```text
1 0 1
0 1 0
1 0 1
```

### Cross pattern

```text
0 1 0
1 1 1
0 1 0
```

Expected:

```text
Cross score = 5
X score     = 1
Result      = Cross
```

Then test the X pattern:

```text
1 0 1
0 1 0
1 0 1
```

Expected:

```text
Cross score = 1
X score     = 5
Result      = X
```

If these two cases work, your basic MAC logic is probably correct.

---

# 30. Test Input Validation

You should deliberately enter bad data.

For example:

```text
0 1
1 1 1
0 1 0
```

The program should not crash.

It should say something like:

```text
입력 형식 오류: 각 줄에 3개의 숫자를 공백으로 구분해 입력하세요.
```

Also test:

```text
0 1 abc
```

This should also cause a friendly error.

---

# 31. Test Epsilon

Create a test such as:

```python
score_a = 0.9000000000000000
score_b = 0.8999999999999999
```

Then:

```python
abs(score_a - score_b)
```

is much smaller than:

```text
1e-9
```

so:

```python
decide(score_a, score_b)
```

should return:

```text
UNDECIDED
```

This is useful to demonstrate that your epsilon policy actually works.

---

# 32. Test JSON Failure Handling

You should deliberately test a malformed case.

For example, imagine:

```text
Filter: 13×13
Pattern: 12×12
```

Your program should output something like:

```text
size_13_4: FAIL
Reason: pattern size 12 does not match filter size 13
```

and then continue:

```text
size_13_5: PASS
```

The important requirement is:

> One bad case must not terminate the entire JSON analysis.

---

# 33. Performance Analysis

Your performance table should look approximately like:

| Size  | Average Time (ms) | Operation Count |
| ----- | ----------------: | --------------: |
| 3×3   |             0.010 |               9 |
| 5×5   |             0.030 |              25 |
| 13×13 |             0.180 |             169 |
| 25×25 |             0.680 |             625 |

**Do not copy these exact times into your README.**

Those numbers depend on:

* CPU
* Python version
* Operating system
* Background processes
* Measurement overhead

Use the numbers produced by your own computer.

The operation count, however, is deterministic:

```text
3×3    = 9
5×5    = 25
13×13  = 169
25×25  = 625
```

---

# 34. What You Should Explain About Performance

Your README should explain something like:

> The MAC operation uses two nested loops. The outer loop runs N times and the inner loop runs N times for each outer iteration. Therefore, the total number of multiplication and accumulation operations is N², which means the time complexity is O(N²).
>
> For example, a 3×3 matrix requires 9 MAC operations, while a 25×25 matrix requires 625 operations. Therefore, increasing the matrix dimension from 3 to 25 increases the number of operations by approximately 69.4 times.
>
> The measured execution time should generally increase as N increases, although the exact timing ratio may not exactly match the operation ratio because of Python interpreter overhead, system load, and timer resolution.

That would be a good explanation.

---

# 35. README Structure I Recommend

Your `README.md` can have these sections:

```markdown
# Mini NPU Simulator

## 1. 프로젝트 소개

## 2. 실행 환경

## 3. 실행 방법

## 4. 프로그램 구조

## 5. MAC 연산 구현

## 6. 라벨 정규화

## 7. Epsilon 기반 비교

## 8. JSON 데이터 처리

## 9. 성능 측정

## 10. 결과 리포트

## 11. 실패 원인 분석

## 12. 시간 복잡도 분석

## 13. 배운 점
```

---

# 36. README — Implementation Summary

You should explain the three important implementation decisions.

### MAC

MAC is implemented using two nested loops without NumPy.

For every position `(i, j)`, the pattern value and filter value are multiplied and added to the accumulated score.

### Label Normalization

Input labels are normalized to two internal labels: `Cross` and `X`.

For example, `+` and `cross` are converted to `Cross`, while `x` is converted to `X`.

This prevents differences in JSON label format from causing incorrect PASS/FAIL results.

### Epsilon

Floating-point calculations can produce very small numerical differences.

Therefore, scores are considered tied when their absolute difference is smaller than `1e-9`.

---

# 37. README — Failure Analysis

Your report should distinguish the causes.

A good structure is:

## 실패 원인 분석

실패 케이스는 크게 데이터/스키마 문제, 로직 문제, 수치 비교 문제로 분류할 수 있다.

### 1. 데이터/스키마 문제

패턴 키에서 추출한 N과 실제 패턴 크기가 일치하지 않는 경우가 발생할 수 있다. 이런 경우 MAC 연산을 수행하지 않고 해당 케이스만 FAIL 처리하도록 구현했다.

### 2. 로직 문제

필터 선택이나 MAC 계산 과정에서 잘못된 필터를 사용하면 정상적인 데이터에서도 잘못된 Cross/X 판정이 발생할 수 있다.

### 3. 수치 비교 문제

부동소수점 계산에서는 동일한 값을 계산하더라도 아주 작은 차이가 발생할 수 있다. 따라서 단순한 `==` 비교 대신 epsilon 기반 비교를 사용했다.

Then discuss your actual failed cases.

---

# 38. If You Have Zero FAIL Cases

The assignment explicitly says you should explain why.

You can write:

### 실패 케이스가 없는 경우

최종 테스트에서 FAIL이 0개인 경우에도 단순히 "모든 테스트가 성공했다"고만 기록하지 않았다.

먼저 JSON의 filter와 pattern 크기를 검증하여 올바른 크기의 데이터만 MAC 연산에 사용했다.

또한 JSON에서 사용되는 `+`, `cross`, `x` 등의 표현을 내부적으로 `Cross`와 `X`로 정규화하여 라벨 표현 차이로 인한 잘못된 비교를 방지했다.

마지막으로 부동소수점 값은 정확한 `==` 비교를 사용하지 않고 `1e-9`의 epsilon을 적용했다.

따라서 계산 결과의 아주 작은 부동소수점 오차 때문에 정상적인 결과가 FAIL로 처리되는 문제를 방지했다.

이러한 데이터 검증, 라벨 정규화, epsilon 비교 정책을 적용했기 때문에 최종 테스트에서 FAIL이 0개가 되었다.

**Of course, adjust this to what actually happened in your run.**

---

# 39. Suggested Development Order

Don't try to write everything at once.

I recommend this exact order:

### Phase 1 — Basic MAC

Implement:

```text
mac()
```

Test with the 3×3 Cross/X examples.

### Phase 2 — Decision

Implement:

```text
decide()
EPSILON
```

Test:

* Cross > X
* X > Cross
* Almost equal

### Phase 3 — User Input

Implement:

```text
input_matrix()
run_user_mode()
```

Test invalid input.

### Phase 4 — JSON

Implement:

```text
load_json()
extract_size()
normalize_label()
validate_matrix()
```

Then process one JSON case.

### Phase 5 — All JSON Cases

Add:

* PASS
* FAIL
* Failure list
* Summary

### Phase 6 — Benchmark

Implement:

```text
benchmark()
run_performance_analysis()
```

Test:

```text
3
5
13
25
```

### Phase 7 — README

Only after your program works, record:

* How to run
* Implementation
* Test results
* Failures
* Performance
* O(N²)
* Lessons learned

This order will save you a lot of debugging time.

---

# 40. Final Architecture

When you're finished, think of your application like this:

```text
                 Mini NPU Simulator
                        │
         ┌──────────────┴──────────────┐
         │                             │
    User Mode                       JSON Mode
       3×3                      5×5 / 13×13 / 25×25
         │                             │
   Input Matrix                   Load JSON
         │                             │
         └──────────────┬──────────────┘
                        │
                 Matrix Validation
                        │
                 Label Normalization
                        │
                ┌───────┴───────┐
                │               │
           Cross Filter       X Filter
                │               │
                └───────┬───────┘
                        │
                      MAC()
                        │
              ┌─────────┴─────────┐
              │                   │
         Cross Score           X Score
              │                   │
              └─────────┬─────────┘
                        │
                     decide()
                        │
            ┌───────────┼───────────┐
            │           │           │
          Cross         X       UNDECIDED
            │           │           │
            └───────────┼───────────┘
                        │
                   PASS / FAIL
                        │
                Performance Test
                        │
                3² / 5² / 13² / 25²
                        │
                     O(N²)
                        │
                   Final Report
```

---

# 41. What the Instructor Is Really Testing

Although the project looks like a matrix-programming exercise, there are actually five concepts being evaluated.

## ① Can you implement MAC yourself?

You should understand:

```text
multiply → accumulate
```

rather than simply using a library.

## ② Can you handle real-world data?

`data.json` may not always use exactly the representation your code expects.

That's why:

* Normalization
* Schema validation
* Size validation

matter.

## ③ Can you handle numerical issues?

You need to understand why:

```python
a == b
```

isn't always appropriate for floating-point calculations.

Hence:

```python
abs(a - b) < EPSILON
```

## ④ Can you measure performance correctly?

You should measure:

```text
MAC only
```

rather than accidentally measuring:

```text
input + print + JSON loading + MAC
```

## ⑤ Can you diagnose failures?

A good submission shouldn't just say:

```text
FAIL
```

It should say why:

```text
Data/schema issue
Logic issue
Numerical comparison issue
```

That diagnostic thinking is probably one of the most important learning objectives of the project.

---

# 42. Your Minimum Completion Checklist

Before submitting, check every item below.

## Project Files

* [ ] `main.py` exists
* [ ] `data.json` is in the expected location
* [ ] `README.md` exists
* [ ] Python 3.8+ works

## User Mode

* [ ] 3×3 user mode works
* [ ] Filter A can be entered
* [ ] Filter B can be entered
* [ ] Pattern can be entered
* [ ] Invalid row length is handled
* [ ] Invalid number input is handled

## MAC

* [ ] MAC uses nested loops
* [ ] NumPy is **NOT** used
* [ ] MAC works for arbitrary N×N matrices

## Label Normalization

* [ ] Cross label normalization works
* [ ] X label normalization works
* [ ] `+` becomes `Cross`
* [ ] `x` becomes `X`

## Epsilon

* [ ] Epsilon is implemented
* [ ] Tie produces `UNDECIDED`

## JSON

* [ ] `data.json` loads correctly
* [ ] `size_N` is extracted from pattern key
* [ ] Correct filter size is selected
* [ ] Pattern/filter dimensions are validated
* [ ] Invalid JSON cases don't crash the program

## PASS / FAIL Reporting

* [ ] PASS/FAIL is printed
* [ ] Total count is printed
* [ ] Pass count is printed
* [ ] Fail count is printed
* [ ] Failed case list is printed

## Performance

* [ ] 3×3 performance measured
* [ ] 5×5 performance measured
* [ ] 13×13 performance measured
* [ ] 25×25 performance measured
* [ ] At least 10 repetitions are used
* [ ] Average time is printed
* [ ] N² operation count is printed

## README

* [ ] README explains MAC
* [ ] README explains normalization
* [ ] README explains epsilon
* [ ] README explains failures
* [ ] README explains O(N²)
* [ ] README contains actual performance results

---

# My Recommended Next Step

Don't start by writing the entire `main.py`.

Build it incrementally:

```text
1. mac()
      ↓
2. decide()
      ↓
3. normalize_label()
      ↓
4. input_matrix()
      ↓
5. user mode
      ↓
6. JSON loading
      ↓
7. JSON validation
      ↓
8. PASS/FAIL reporting
      ↓
9. benchmark
      ↓
10. README
```

If you follow that order, the project becomes much less intimidating.

At its core, it is just:

```text
matrix input
     ↓
    MAC
     ↓
comparison
     ↓
validation
     ↓
benchmarking
     ↓
reporting
```

That is the main idea behind the Mini NPU Simulator.

You can copy everything inside the writing block directly into a file named **`README.md`**. I also corrected the broken Markdown/code formatting from the original, including escaped underscores, Python indentation, code fences, tables, headings, and `if __name__ == "__main__":`.
