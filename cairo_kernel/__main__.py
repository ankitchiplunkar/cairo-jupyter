from ipykernel.kernelapp import IPKernelApp
from .kernel import CairoKernel

IPKernelApp.launch_instance(kernel_class=CairoKernel)