from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

from frappe_smart_inventory import __version__ as app_version

setup(
    name="frappe_smart_inventory",
    version=app_version,
    description="Smart Inventory Quality & Batch Traceability Suite for ERPNext",
    author="Antx",
    author_email="dev@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
