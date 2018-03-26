# Reuters parser

Small script for parsing all available news entries of http://reuters.com

## Prerequirements

Install all python modules of `requirements.txt`.

## Receiving summary

Before downloading all news entries let's first fetch a small summary of all available news entries by using `fetch_reuters.py`:

```
python fetch_reuters.py --output_dir=/my/output/path
```

Within the directory provided by `output_dir` a summary of all news will be saved in the form of pkl files. The files are saved in a new subdirectory `output_TIMESTAMP` with `TIMESTAMP` representing the current time of the first call. There is one pkl file for each day.

## Generating datasets

Next we want to generate the datasets out of this pkl files. Therefor the script `reuters_parser.py` can be used. 

```
python reuters_parser.py --input_dir=/my/output/path/output_TIMESTAMP --output_dir=/my/dataset/output/dir
```

One can add additional parameters of the information that should be extracted: `-author`, `-title`, `-text`. 
Furthermore it is possible to define the output types: `-json`, `-csv`.

## Adapt to other pages

It is very simple to adapt this to other pages having archives. Just replace to URLs in `fetch_reuters.py`.