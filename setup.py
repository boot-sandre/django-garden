from setuptools import setup

setup(
    name="DjangoGarden",
    version="0.3.1",
    include_package_data=True,
    packages=["apps.account", "apps.base",
              "garden.cms_user", "gardens.cms", "garden.cms_ninja", "garden.api_garden"],
    zip_safe=False,
)
