cairo_kernel
===========

``cairo_kernel`` is a simple Jupyter kernel for Cairo a smart contract programing language for STARKs. 

[Kanban](https://ankitchiplunkar.notion.site/Cairo-kernel-starkware-py-5f64ee70cfde4578969c430bf1a14531)

Installation
------------
1. Install virtualenv

    ```
    virtualenv -p python3.8 venv
    source venv/bin/activate
    ```

2. To install ``cairo_kernel``:

    ```
    pip install cairo-kernel
    ```

Using the Kernel
---------------------

[Cairo example](https://github.com/ankitchiplunkar/cairo-jupyter/blob/master/notebooks/Cairo%20example.ipynb) is a working example of the notebook.


**Notebook**: The *New* menu in the notebook should show an option for an Cairo notebook.

**Console frontends**: To use it with the console frontends, add ``--kernel cairo`` to
their command line arguments.

Running the kernel on notebook
--------------------------------

1. Start the notebook

    ```
    jupyter notebook
    ```

2. Start cairo kernel via UI

![cairo_jupyter_gif](https://user-images.githubusercontent.com/5904910/146619802-6ee1bb5d-243a-4e0d-9ab2-064e101f5bcd.gif)



Development
-------------------------------

1. Clone & enter the repo. 

```
    git clone https://github.com/ankitchiplunkar/cairo-jupyter.git
```

2. Install required libraries. 

```
    pip install -r requirements.txt
```

3. Install the cairo-jupyter library locally:
```
    pip install -e .
    python -m cairo_kernel.install
```

