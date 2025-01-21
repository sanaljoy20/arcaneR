#' Document R Files using doc_ai
#'
#' This function documents an R file using the `doc_ai` Python tool.
#'
#' @param output_dir Directory to save the documented R file.
#' @param input_file_or_dir path to input_file or dir
#'
#' @return Path to the documented R file.
#' @export
document_r <- function(input_file_or_dir, output_dir) {
  # Validate inputs
  if (!file.exists(input_file_or_dir) && !dir.exists(input_file_or_dir)) {
    stop("Input file does not exist.")
  }
  if (!dir.exists(output_dir)) {
    stop("Output directory does not exist.")
  }

  if(Sys.getenv("OPENAI_API_KEY") == "") {
    stop("OPENAI_API_KEY should be present in the env.")
  }

  if(dir.exists(input_file_or_dir)) {
    r_files <- list.files(path = input_file_or_dir, pattern = "\\.R$", full.names = TRUE)
  } else {
    r_files <- input_file_or_dir
  }

  output_file <- c()
  for(f in r_files) {
    # Construct the Python command
    python_script <- system.file("python", "doc_ai", package = "arcaneR")
    args <- c(f, "--out-dir", output_dir)

    # Call the Python script
    cli::cli_alert_info(paste0("ARCANE >> Adding documentation for ", f))
    result <- system2("python", c(python_script, args), stdout = TRUE, stderr = TRUE)

    # Handle errors
    if (any(grepl("Error", result, ignore.case = TRUE))) {
      output_file <- c(output_file, paste("Error in calling doc_ai:", paste(result, collapse = "\n")))
      next
    }

    # Return the path to the documented file
    ofile <- file.path(output_dir, basename(f))
    if (!file.exists(ofile)) {
      output_file <- c(output_file, "Output file was not created.")
      next
    }
    output_file <- c(output_file, ofile)
  }

  return(output_file)
}


#' Create Unit tests for R Files using bug_ai
#'
#' This function documents an R file using the `bug_ai` Python tool.
#'
#' @param output_dir Directory to save the documented R file.
#' @param input_file_or_dir path to input_file or dir
#'
#' @return Path to the documented R file.
#' @export
unit_r <- function(input_file_or_dir, output_dir) {
  # Validate inputs
  if (!file.exists(input_file_or_dir) && !dir.exists(input_file_or_dir)) {
    stop("Input file does not exist.")
  }
  if (!dir.exists(output_dir)) {
    stop("Output directory does not exist.")
  }

  if(Sys.getenv("OPENAI_API_KEY") == "") {
    stop("OPENAI_API_KEY should be present in the env.")
  }

  if(dir.exists(input_file_or_dir)) {
    r_files <- list.files(path = input_file_or_dir, pattern = "\\.R$", full.names = TRUE)
  } else {
    r_files <- input_file_or_dir
  }

  output_file <- c()
  for(f in r_files) {
    # Construct the Python command
    python_script <- system.file("python", "bug_ai", package = "arcaneR")
    args <- c(f, "--out-dir", output_dir)

    # Call the Python script
    cli::cli_alert_info(paste0("ARCANE >> Creating unit test cases for ", f))
    result <- system2("python", c(python_script, args), stdout = TRUE, stderr = TRUE)

    # Return the path to the documented file
    ofile <- file.path(output_dir, basename(f))
    if (!file.exists(ofile)) {
      output_file <- c(output_file, "Output file was not created.")
      next
    }
    output_file <- c(output_file, ofile)
  }


  return(output_file)
}
