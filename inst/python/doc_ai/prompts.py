import json
import config

def ANNOTATE_SRC_CODE(src_code):
    return f'''
The following source code contains R code.
Comment the element definitions (classes and functions) of this source code with documentation, using ROxygen format.
The documentation should be very detailed.
After adding the documentation add detailed comment line on top of each line of code describing what it does and why.

SOURCE CODE:
```
{src_code}
```

# EXAMPLE R INPUT:
```
moving_average <- function(x, window_size = 3) {{
  
  assertthat::assert_that(is.numeric(x), msg = 'x should be numeric')

  if (!is.numeric(window_size) || window_size <= 0 || window_size != floor(window_size)) {{
    stop()
  }}

  n <- length(x)
  result <- numeric(n)
  
  for (i in 1:n) {{
    start <- max(1, i - window_size + 1)
    result[i] <- mean(x[start:i], na.rm = TRUE)
  }}
  
  return(result)
}}

```
EXAMPLE R OUTPUT:

```json
{{
    "programming_language": "R",
    "overall_comment": "# Calculate Averages.",
    "documentation": [{{
        "line_of_code": "moving_average <- function(x, window_size = 3)",
        "comment": " #_SQUOTE_ Calculate the Moving Average _NEWLINE_  #_SQUOTE_ _NEWLINE_  #_SQUOTE_ This function calculates the moving average of a numeric vector. It takes a window size parameter to determine how many previous values to include in the average calculation. _NEWLINE_  #_SQUOTE_ _NEWLINE_  #_SQUOTE_ @param x A numeric vector for which the moving average will be calculated. _NEWLINE_  #_SQUOTE_ @param window_size A positive integer specifying the number of elements to include in the moving average window. Default is 3. _NEWLINE_  #_SQUOTE_ @importFrom assertthat assert_that _NEWLINE_  #_SQUOTE_ _NEWLINE_  #_SQUOTE_ @return A numeric vector of the same length as `x`, containing the moving average values. _NEWLINE_  #_SQUOTE_"
    }}], 
    comments: [{{
        "line_of_code": "assertthat::assert_that(is.numeric(x), msg = 'x should be numeric')",
        "comment": "# Ensure that `x` is a numeric vector. If not, throw an error message _QUOTE_ x should be numeric _QUOTE_."
    }}, {{
        "line_of_code": "if (!is.numeric(window_size) || window_size <= 0 || window_size != floor(window_size))",
        "comment": "# Validate `window_size`: it must be numeric, positive, and an integer. Halt execution if invalid."
    }}, {{
        "line_of_code": "n <- length(x)",
        "comment": "# Get the length of the input vector `x`."
    }}
    ]
}}
```




IMPORTANT:
- Make sure that comments have correct indentation.
- Output MUST be valid JSON. Escape \" with _QUOTE_, \' with _SQUOTE_ and \n with _NEWLINE_.
- The documentation should be in ROxygen style.
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

    return json.loads(response)

def dummy_response():
    if not config.is_dry_run:
        return None

    return '''
```json
{{
    "overall_comment": "_QUOTE__QUOTE__QUOTE_Read and write JSON files._QUOTE__QUOTE__QUOTE_",
    "elements": [{{
        "definition": "def read_from_json_file(path_to_json, encoding='utf-8'):",
        "comment": "    _QUOTE__QUOTE__QUOTE_Read JSON data from a file. _NEWLINE_ Args: _NEWLINE_ path_to_json (str): The path to the JSON file. _NEWLINE_ encoding (str): The encoding of the file. Default is 'utf-8'. _NEWLINE_ Returns: _NEWLINE_ dict: The JSON data read from the file. _NEWLINE_ _QUOTE__QUOTE__QUOTE_"
    }}
    ]
}}
```
'''
