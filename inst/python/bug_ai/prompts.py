import json
import config
import re

def ANNOTATE_SRC_CODE(src_code):
    return f'''
The following SOURCE CODE is in R Programming language.
I need to create unit test cases for the below R code
Identify key values and edge values that each of the parameters must take for each line of the code for exhaustive unit test cases.
Then use those values to generate exhaustive unit test case for thr R code.

SOURCE CODE:
```
{src_code}
```
Perform the mentioned tasks on the source code above and give output like the examples below.
Do not repeat the examples as output.


EXAMPLE INPUT:
```
calculate_average <- function(numbers) {{
  total <- 0
  for (num in numbers) {{
    total <- total + num
  }}
  average <- total / length(numbers)
  return(average)
}}
```

EXAMPLE OUTPUT:
```
{{
    "programming_language": "R",
    "elements": [{{
        "function": "calculate_average <- function(numbers)",
        "unit_test": "_NEWLINE_# Unit tests_NEWLINE_test_that(_QUOTE_ calculate_average handles empty list _QUOTE_, {{_NEWLINE_  expect_error(calculate_average(numeric(0)), _QUOTE_division by zero_QUOTE_)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles a single positive number_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(5)), 5)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles multiple positive numbers_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(1, 2, 3, 4, 5)), 3)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles multiple negative numbers_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(-1, -2, -3, -4, -5)), -3)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles mixed positive and negative numbers_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(-10, 20, -30, 40)), 5)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles a list of zeros_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(0, 0, 0, 0)), 0)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles decimal numbers_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(1.5, 2.5, 3.5)), 2.5)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles large numbers_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(1e6, 2e6, 3e6)), 2e6)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles a single negative number_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(-42)), -42)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles a list with one zero_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(0)), 0)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles a list with equal positive and negative numbers_QUOTE_, {{_NEWLINE_  expect_equal(calculate_average(c(-2, 2, -3, 3)), 0)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles invalid input_QUOTE_, {{_NEWLINE_  expect_error(calculate_average(c(_QUOTE_a_QUOTE_, _QUOTE_b_QUOTE_, _QUOTE_c_QUOTE_)), _QUOTE_non-numeric argument to binary operator_QUOTE_)_NEWLINE_}})_NEWLINE__NEWLINE_test_that(_QUOTE_calculate_average handles a large list_QUOTE_, {{_NEWLINE_  large_list <- rep(1, 10^6)_NEWLINE_  expect_equal(calculate_average(large_list), 1)
}})
",
    }}]
}}
```

- The unit test cases must be exhaustive for the function.
- Make sure there are no syntax errors in the code.
- Do not repeat the example.

IMPORTANT: Output MUST be valid JSON. Escape \" with _QUOTE_, \' with _SQUOTE_ and \n with _NEWLINE_.

'''

def _pick_longest(parts):
    max_len = -1
    longest = None
    for part in parts:
        if len(part) > max_len:
            longest = part
            max_len = len(part)
    return longest

def _clean_text(text):
    BAD_TEXTS = ['```json', '```']
    for BAD in BAD_TEXTS:
        if BAD in text:
            parts = text.split(BAD)
            text = _pick_longest(parts)
    return text

def parse_response(response):
    response = _clean_text(response)
    response = re.sub(r'(?<!\\)\\n', '\\\\n', response)
    return json.loads(response)

def dummy_response():
    if not config.is_dry_run:
        return None

    return '''
```json
{{
    "programming_language": "Python",
    "elements": [{{
        "line_of_code": "def calculate_average(numbers):",
        "FATAL": "",
        "WARNING": "The function lacks a docstring or comments explaining its purpose, inputs, and error handling."
    }},
    {{
        "line_of_code": "total += num",
        "FATAL": "If num is non-numeric (e.g., a string or None), this line raises a TypeError.",
        "WARNING": ""
    }},
    {{
        "line_of_code": "average = total / len(numbers)",
        "FATAL": "If num is non-numeric (e.g., a string or None), this line raises a TypeError.",
        "WARNING": "If len(numbers) == 0, this line raises a ZeroDivisionError."
    }},
    
    ]
}}
```
'''
