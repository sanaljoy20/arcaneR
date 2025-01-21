# arcaneR

arcaneR (Audit for Reliable Coding and Adherence to Norms Engine in R) is an R package that uses OpenAI's ChatGPT to generate documentation and unit test cases for R scripts.

## Features

- **Documentation**: Generate detailed documentation for any R script.
- **Unit Tests**: Create unit test cases automatically.

## Installation

Install arcaneR from GitHub:

```R
# Install devtools if not already installed
if (!requireNamespace("devtools", quietly = TRUE)) {
  install.packages("devtools")
}

devtools::install_github("<your-github-username>/arcaneR")
```

## Usage

### `document_r(input_file, output_dir)`
Generates documentation for the given R script.

#### Example:
```R
arcaneR::document_r("scripts/my_analysis.R", "outputs/")
```

### `unit_r(input_file, output_dir)`
Creates unit test cases for the given R script.

#### Example:
```R
arcaneR::unit_r("scripts/my_analysis.R", "outputs/")
```

### API Key
Set the OpenAI API key before using arcaneR:

```R
Sys.setenv(OPENAI_API_KEY = "your-api-key")
```
