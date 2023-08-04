from pathlib import Path
from time import sleep

here = Path(__file__).parent
expected_output = "hello world"

try:
    sleep(5)
    output = list(here.glob('*.out'))
    print(list(here.glob('*')))
    assert len(output) > 0, "No output file found"
    assert len(output) == 1, "More than one output file found"
    
    # read output
    content = output[0].read_text()
    assert content.strip() == expected_output, f"Output does not match expected output: {content}"

except AssertionError as e:
    print(e)
    exit(1)
