# Project Guide

This project is a demonstration of a Markdown document used to test a RAG chunking system. The main goal is to have enough text inside one section to make the section larger than the maximum allowed chunk size. We want to verify that our chunker can recognize headings, understand their hierarchy, and later split large sections using meaningful subheadings instead of cutting the document randomly.

This paragraph adds more information about the project. A Markdown chunker should preserve the relationship between a heading and the content that belongs to it. When a heading appears, everything following it belongs to that heading until another heading at the same or higher level appears.

## Installation

The installation section explains how a user can prepare the project environment. First, create the required environment and install the dependencies. The dependencies may include Python packages, development tools, testing libraries, and other utilities required by the application.

### Requirements

The project requires Python 3.10 or a newer version. It also requires a package manager capable of installing the dependencies defined by the project configuration. Before starting the installation process, make sure that the environment has enough disk space and that the required commands are available from the terminal.

### Dependencies

The project uses several dependencies. These dependencies are installed before the application is executed. A dependency can provide functionality such as parsing Markdown files, calculating text similarity, creating embeddings, validating data models, or communicating with a language model.

## Setup

After installing the dependencies, configure the project. The configuration step may include preparing directories, checking input files, creating an index directory, and selecting the maximum chunk size.

The setup process should be reproducible. This means that another developer should be able to follow the same instructions and obtain a working environment without manually modifying the source code.

# Usage

The usage section is intentionally very long so that we can test what happens when a Markdown section becomes larger than 2000 characters.

The RAG system starts by reading documents from the input directory. Each document is analyzed according to its type. Python files are handled using an AST-based chunking strategy, while Markdown and text files are handled according to their heading structure.

The Markdown strategy begins by reading the complete document and determining the starting character position of every line. These positions are important because the final source information must contain character indexes rather than only line numbers.

After calculating the line positions, the chunker examines every line and determines whether it represents a Markdown heading. An ATX heading begins with one or more hash characters followed by a space. The number of hash characters determines the heading level. For example, one hash represents a level-one heading, two hashes represent a level-two heading, and three hashes represent a level-three heading.

Once headings have been identified, the chunker determines the boundaries of every section. A section begins at its own heading and ends when another heading with the same or a higher priority appears. A lower-level heading belongs to the current section and therefore does not immediately terminate the parent section.

This hierarchy is important for our chunking strategy. Consider a level-one heading followed by several level-two headings. The level-one section includes all of those level-two sections until another level-one heading appears. Similarly, a level-two section can contain level-three sections until another level-two or level-one heading appears.

The purpose of this approach is to preserve the logical structure of the documentation. If we were to split the document every fixed number of characters, we could easily separate a heading from the explanation that belongs to it. Logical splitting should instead prefer Markdown structure whenever possible.

The retrieval system will later use these chunks to search for information related to a question. Therefore, keeping meaningful pieces of information together can improve retrieval quality. A chunk containing a heading and its explanation is generally more useful than a chunk containing an arbitrary portion of a sentence.

This section continues with additional explanatory text to make sure that its total size is larger than the configured maximum chunk size. The text itself is not particularly important. What matters for this test is that the chunker recognizes that the Usage section is too large and then looks for its child headings as possible logical boundaries.

The chunker should not immediately create a random 2000-character slice. Instead, it should first inspect the structure of the Markdown document. If the large section contains useful subheadings, those subheadings can provide natural places where the section can be divided.

For example, a large Usage section may contain a Basic Usage subsection, an Advanced Usage subsection, and a Configuration subsection. Each subsection can potentially become its own chunk. If one subsection is still too large, the chunker can continue looking at headings below it.

The important idea is that the chunking process should respect the hierarchy of the document. The heading level tells us whether a heading belongs inside the current section or whether it terminates that section.

### Basic Usage

The basic usage subsection explains the simplest way to run the application. A user can start the program from the command line and provide a query. The system then loads the previously created index and searches for relevant chunks.

### Advanced Usage

The advanced usage subsection describes more complicated operations. Users may search an entire dataset of questions, configure the number of retrieved results, and save the results to a specified output directory.

### Configuration

The configuration subsection contains information about configurable parameters. One important parameter is the maximum chunk size. The default value required by the project is 2000 characters, and retrieved sources must never exceed that limit.

### Troubleshooting

If the application does not behave as expected, first check that the input files exist and that the project dependencies have been installed. Also verify that the generated index is available before attempting a search operation.

## More Help

Additional documentation can be added here. This section exists to provide another heading after the large Usage section so that the chunker has a clear ending boundary for the Usage section.