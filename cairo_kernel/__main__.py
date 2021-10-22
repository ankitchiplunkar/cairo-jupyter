from ipykernel.kernelapp import IPKernelApp
from . import CairoKernel

IPKernelApp.launch_instance(kernel_class=CairoKernel)