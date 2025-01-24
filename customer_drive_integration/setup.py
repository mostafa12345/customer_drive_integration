from setuptools import setup, find_packages

setup(
    name="customer_drive_integration",
    version="0.0.1",
    description="Customer Drive Integration App",
    author="Your Name",
    author_email="your_email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "create-folders-for-existing-customers=customer_drive_integration.commands:create_folders_for_existing_customers",
        ],
    },
)

