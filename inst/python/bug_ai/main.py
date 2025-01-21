import os

from cornsnake import util_file, util_wait, util_print, util_dir
import json
import prompts
import service_chat

def percent(num, denom, ndigits = 0):
    if denom == 0:
        return format(0, f'.{ndigits}f')
    return str(round((num * 100.0) / denom, ndigits)) + '%'

def debug_directory(path_to_src_dir, options):
    files = util_dir.find_files(path_to_src_dir)
    files_processed = 0
    files_skipped = 0
    for file in files:
        if options.exclude and os.path.basename(file) in options.exclude:
            util_print.print_custom(f"Skippping file {file}")
            files_skipped += 1
            continue
        debug_file(file, options)
        files_processed += 1
        util_wait.wait_seconds(1)
    util_print.print_result(f"Processed {files_processed} files - skipped {files_skipped} files.")

def _write_new_code(result, file_name, out_dir):
    jfile_name = os.path.splitext(file_name)[0] + ".json"
    jout_file_path = os.path.join(out_dir, jfile_name)
    # util_print.print_section(f"Saving test code to {jout_file_path}")
    # 
    # with open(jout_file_path, "w") as json_file:
    #     json.dump(result, json_file, indent=4)

    elements = result['elements']
    r_test_code = ""
    for e in elements:
        r_test_code = r_test_code + e['unit_test'] + "\n\n\n"

    r_test_code = _unquote(r_test_code)

    rfile_name = "test-" + os.path.splitext(file_name)[0] + ".R"
    rout_file_path = os.path.join(out_dir, rfile_name)
    util_print.print_section(f"Saving test code to {rout_file_path}")
    util_file.write_text_to_file(r_test_code, rout_file_path)

def _unquote(text):
    return text.replace("_QUOTE_", '"').replace("_SQUOTE_", "'").replace("_NEWLINE_", "\n").replace("_QUOTE", '"')

def debug_file(path_to_src_file, options):
    util_print.print_section(f"Reading code from {[path_to_src_file]}")
    code = util_file.read_text_from_file(path_to_src_file)
    response = service_chat.send_prompt(prompts.ANNOTATE_SRC_CODE(code), dummy_response="")
    comments = prompts.parse_response(response)

    if options.out_dir is None:
        util_print.print_custom(comments)
    else:
        util_dir.ensure_dir_exists(options.out_dir)
        _write_new_code(comments, os.path.basename(path_to_src_file), options.out_dir)

 
