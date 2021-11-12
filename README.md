cairo_kernel
===========

test 
``cairo_kernel`` is a simple Jupyter kernel for Cairo a smart contract programing language for STARKs. 

Installation
------------
1. Install virtualenv

    ```
    virtualenv -p python3.8 venv
    source venv/bin/activate
    ```

2. Clone the repo:

    ```
    git clone https://github.com/ankitchiplunkar/cairo-jupyter.git
    ```

3. To install ``cairo_kernel`` from local:

    ```
    pip install -e .
    python -m cairo_kernel.install
    ```

Using the Kernel
---------------------

[Cairo example](https://github.com/ankitchiplunkar/cairo-jupyter/blob/master/Cairo%20example.ipynb) is a working example of the notebook.


**Notebook**: The *New* menu in the notebook should show an option for an Cairo notebook.

**Console frontends**: To use it with the console frontends, add ``--kernel cairo`` to
their command line arguments.
