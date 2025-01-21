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

  # Construct the Python command
  python_script <- system.file("python", "doc_ai.py", package = "arcaneR")
  args <- c(input_file_or_dir, "--out-dir", output_dir)

  # Call the Python script
  result <- system2("python", c(python_script, args), stdout = TRUE, stderr = TRUE)

  # Handle errors
  if (any(grepl("Error", result, ignore.case = TRUE))) {
    stop(paste("Error in calling doc_ai:", paste(result, collapse = "\n")))
  }

  # Return the path to the documented file
  output_file <- file.path(output_dir, basename(input_file))
  if (!file.exists(output_file)) {
    stop("Output file was not created.")
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

  # Construct the Python command
  python_script <- system.file("python", "bug_ai.py", package = "arcaneR")
  args <- c(input_file_or_dir, "--out-dir", output_dir)

  # Call the Python script
  result <- system2("python", c(python_script, args), stdout = TRUE, stderr = TRUE)

  # Return the path to the documented file
  output_file <- file.path(output_dir, basename(input_file))
  if (!file.exists(output_file)) {
    stop("Output file was not created.")
  }

  return(output_file)
}
