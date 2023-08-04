from pathlib import Path
from time import sleep

here = Path(__file__).parent
expected_output = "Hello World, from inside the container!"

try:
    sleep(5)
    output = list(here.glob('*.out'))
    assert len(output) > 0, "No output file found"
    assert len(output) == 1, "More than one output file found"
    
    # read output
    content = output[0].read_text()
    assert content.strip() == expected_output, f"Output does not match expected output: \n{content}"

    print("Passed")
    exit(0)

except AssertionError as e:
    print(e)
    exit(1)
