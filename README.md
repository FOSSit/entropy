# Entropy

See the informational entropy of a file (assuming the encoded symbols are bytes or bits)
This doesn't necessarily give the best possible compression, as for certain data, it is possible
to identify bit sequences as symbols such that it minimises the entropy.

Here we assume that a byte is the only symbol encoded and output the entropy which
can reflect accurately the compression ratios possible for byte level compression algorithms


```
python3 entropy.py source.txt
In the README.md file, you should include information about how to install, configure, and use your command-line tool. Here's what you can include:

Title and Description: Provide a clear and concise title for your project. Describe what the project does and its purpose.

Installation: Explain how users can install your command-line tool. Typically, you'll instruct users to install it using pip:

markdown
Copy code
## Installation

You can install the entropy calculator using pip:

```bash
pip install .
Copy code
Usage: Provide examples of how to use your command-line tool, including different options and arguments.

markdown
Copy code
## Usage

After installing, you can use the entropy calculator from the command line:

```bash
entropy-calculator byte file1 file2 file3 ...
or

bash
Copy code
entropy-calculator bit file1 file2 file3 ...
This command will calculate byte-level or bit-level entropy for the specified files.

Copy code
Contributing: If you welcome contributions to your project, provide guidelines for how users can contribute, such as reporting bugs, submitting feature requests, or contributing code.

markdown
Copy code
## Contributing

Contributions are welcome! If you encounter any issues or have suggestions for improvements, please open an issue on the GitHub repository. If you'd like to contribute code, please fork the repository and submit a pull request.
License: Include information about the license under which your project is distributed.

markdown
Copy code
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
Acknowledgments: Optionally, you can acknowledge any individuals or projects that helped or inspired you during the development of your project.

markdown
Copy code
## Acknowledgments

- Thanks to the contributors of the numpy library for providing efficient array operations.
Ensure that the README.md file is well-formatted, easy to read, and provides all the necessary information for users to understand and use your command-line tool.
```