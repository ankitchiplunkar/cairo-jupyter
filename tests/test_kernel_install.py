import pytest
try:
    from jupyter_client.kernelspec import find_kernel_specs
except ImportError:
    try:
        from IPython.kernel.kernelspec import find_kernel_specs
    except ImportError:
        print("Please install either Jupyter to IPython before continuing")

def test_cairo_kernelspec():
    print(find_kernel_specs()['cairo'])
