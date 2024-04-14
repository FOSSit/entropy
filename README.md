Install Your CLI Application:
Open a terminal and navigate to the directory containing your setup.py file. Then, run the following command to install your CLI application:

```bash
cd directory
pip install .
```
This command tells pip to install the current directory (.) as a Python package, using the setup.py file.

Test Your CLI Application:
After installation, users can run your script from the command line using the entropy-calculator command. Test your CLI application to ensure it works as expected:

```bash
python entropy.py bit <file1> [<file2> ...]
python entropy.py byte <file1> [<file2> ...]
```